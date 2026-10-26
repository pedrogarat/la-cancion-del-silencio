import os
import re
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfgen import canvas

class BookCanvas(canvas.Canvas):
    """Canvas de dos pasadas para calcular la numeración total de páginas y añadir encabezados y pies de página editoriales."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Encabezado (páginas > 1)
        if self._pageNumber > 1:
            self.drawString(54, A4[1] - 36, "LA CANCIÓN DEL SILENCIO • NOVELA DE CIENCIA FICCIÓN")
            self.drawRightString(A4[0] - 54, A4[1] - 36, "ACTO III: LA FALSA VICTORIA Y LA CACERÍA SILENCIOSA")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, A4[1] - 42, A4[0] - 54, A4[1] - 42)
        
        # Pie de página
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 45, A4[0] - 54, 45)
        
        self.drawString(54, 32, "Capítulo 22: La Máscara de los Héroes y el Reencuentro del Hogar")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(A4[0] - 54, 32, page_str)
        self.restoreState()

def create_quote_box(paragraphs_text, styles, width=A4[0] - 108):
    q_style = ParagraphStyle(
        'QuoteText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.2,
        leading=13.5,
        textColor=colors.HexColor("#1E293B"),
    )
    flowables = [Paragraph(p, q_style) for p in paragraphs_text]
    t = Table([[flowables]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LINELEFT', (0,0), (0,0), 3.5, colors.HexColor("#0284C7")),
    ]))
    return t

def create_code_box(code_lines, styles, width=A4[0] - 108):
    c_style = ParagraphStyle(
        'CodeText',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#0F172A"),
    )
    formatted = "<br/>".join(code_lines)
    flowables = [Paragraph(formatted, c_style)]
    t = Table([[flowables]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#E2E8F0")),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LINELEFT', (0,0), (0,0), 3.5, colors.HexColor("#475569")),
    ]))
    return t

def generate_chapter22_pdf(input_md_path, output_filename):
    if not os.path.exists(input_md_path):
        print(f"Error: No se encuentra el archivo {input_md_path}")
        return

    with open(input_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'ChapterTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=12,
        alignment=0
    )

    h3_style = ParagraphStyle(
        'SectionH3',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=colors.HexColor("#0284C7"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=14.5,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=6,
        alignment=4 # Justificado
    )

    story = []
    lines = content.split('\n')
    
    in_quote = False
    quote_lines = []

    in_code = False
    code_lines = []

    for line in lines:
        stripped = line.strip()

        # Bloques de código preformateado (como notas manuscritas)
        if stripped.startswith('```'):
            if not in_code:
                in_code = True
                code_lines = []
            else:
                in_code = False
                story.append(create_code_box(code_lines, styles))
                story.append(Spacer(1, 6))
                code_lines = []
            continue

        if in_code:
            code_lines.append(stripped)
            continue

        # Título principal del capítulo
        if stripped.startswith('# '):
            if in_quote:
                story.append(create_quote_box(quote_lines, styles))
                story.append(Spacer(1, 6))
                in_quote = False
                quote_lines = []
            title_text = stripped.lstrip('# ').strip()
            title_text = title_text.replace("«", '"').replace("»", '"').replace("—", " - ")
            story.append(Paragraph(title_text, title_style))
            story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284C7"), spaceBefore=2, spaceAfter=14))
            continue

        # Subtítulos de sección (###)
        if stripped.startswith('### '):
            if in_quote:
                story.append(create_quote_box(quote_lines, styles))
                story.append(Spacer(1, 6))
                in_quote = False
                quote_lines = []
            sec_title = stripped.lstrip('# ').strip()
            sec_title = sec_title.replace("«", '"').replace("»", '"').replace("—", " - ")
            story.append(Spacer(1, 4))
            story.append(Paragraph(sec_title, h3_style))
            continue
            
        # Citas y epígrafes
        if stripped.startswith('>'):
            in_quote = True
            raw_quote = stripped.lstrip('> ').replace("«", '"').replace("»", '"')
            raw_quote = raw_quote.replace("—", " - ")
            raw_quote = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', raw_quote)
            raw_quote = re.sub(r'\*(.*?)\*', r'<i>\1</i>', raw_quote)
            quote_lines.append(raw_quote)
            continue
        elif in_quote:
            story.append(create_quote_box(quote_lines, styles))
            story.append(Spacer(1, 6))
            in_quote = False
            quote_lines = []

        # Separadores horizontales
        if stripped.startswith('---'):
            story.append(Spacer(1, 4))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceBefore=4, spaceAfter=8))
            continue

        # Líneas vacías
        if not stripped:
            continue

        # Formato de texto y diálogos
        clean_line = stripped.replace("«", '"').replace("»", '"')
        clean_line = clean_line.replace("—", " - ")
        clean_line = clean_line.replace("–", " - ")
        clean_line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', clean_line)
        clean_line = re.sub(r'\*(.*?)\*', r'<i>\1</i>', clean_line)

        story.append(Paragraph(clean_line, body_style))

    if in_quote:
        story.append(create_quote_box(quote_lines, styles))
        story.append(Spacer(1, 6))

    if in_code:
        story.append(create_code_box(code_lines, styles))
        story.append(Spacer(1, 6))

    doc.build(story, canvasmaker=BookCanvas)
    print(f"PDF generado exitosamente: {output_filename}")

if __name__ == "__main__":
    md_file = os.path.join("novela", "capitulos", "capitulo_22.md")
    pdf_out = "Capitulo_22_La_Mascara_de_los_Heroes_y_el_Reencuentro_del_Hogar.pdf"
    generate_chapter22_pdf(md_file, pdf_out)

    dest_novela = os.path.join("novela", pdf_out)
    shutil.copyfile(pdf_out, dest_novela)
    print(f"Copia sincronizada en: {dest_novela}")
