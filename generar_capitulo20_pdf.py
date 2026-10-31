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
        
        self.drawString(54, 32, "Capítulo 20: El Salmo de la Falsa Victoria")
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
        alignment=4
    )
    story_cell = []
    for p in paragraphs_text:
        story_cell.append(Paragraph(p, q_style))
        story_cell.append(Spacer(1, 3))
    if story_cell:
        story_cell.pop()

    t = Table([[story_cell]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#94A3B8")),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    return t

def generate_chapter20_pdf(input_md_path, output_filename):
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
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=14
    )
    
    h3_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'ChapterBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.2,
        textColor=colors.HexColor("#334155"),
        spaceAfter=7,
        alignment=4
    )

    meta_style = ParagraphStyle(
        'MetaText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#475569"),
        spaceAfter=3
    )

    story = []
    lines = content.split('\n')
    
    in_quote = False
    quote_lines = []

    for line in lines:
        stripped = line.strip()
        
        # Título del capítulo
        if stripped.startswith('# '):
            title_text = stripped[2:].replace("«", '"').replace("»", '"')
            story.append(Paragraph(title_text, title_style))
            story.append(Spacer(1, 4))
            continue
            
        # Subsecciones / Escenas
        if stripped.startswith('### '):
            if in_quote:
                story.append(create_quote_box(quote_lines, styles))
                story.append(Spacer(1, 6))
                in_quote = False
                quote_lines = []
            sec_title = stripped[4:].replace("«", '"').replace("»", '"')
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

        # Metadatos del encabezado
        if any(marker in stripped for marker in ['Fase', 'Fecha', 'Puntos de Vista', 'Ubicación']):
            story.append(Paragraph(clean_line, meta_style))
            story.append(Spacer(1, 1.5))
            continue

        story.append(Paragraph(clean_line, body_style))

    if in_quote:
        story.append(create_quote_box(quote_lines, styles))
        story.append(Spacer(1, 6))

    doc.build(story, canvasmaker=BookCanvas)
    print(f"PDF generado exitosamente: {output_filename}")

if __name__ == "__main__":
    md_file = os.path.join("novela", "capitulos", "capitulo_20.md")
    pdf_out = "Capitulo_20_El_Salmo_de_la_Falsa_Victoria.pdf"
    generate_chapter20_pdf(md_file, pdf_out)

    dest_novela = os.path.join("novela", pdf_out)
    shutil.copyfile(pdf_out, dest_novela)
    print(f"Copia sincronizada en: {dest_novela}")
