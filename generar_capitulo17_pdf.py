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
            self.drawRightString(A4[0] - 54, A4[1] - 36, "ACTO II: LA CAÍDA DEL ESCUDO Y EL GRAN CAOS")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, A4[1] - 42, A4[0] - 54, A4[1] - 42)
        
        # Pie de página
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 45, A4[0] - 54, 45)
        
        self.drawString(54, 32, "Capítulo 17: El Páramo de Mediodía")
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
        alignment=0
    )
    elements = []
    for p in paragraphs_text:
        elements.append(Paragraph(p, q_style))
        elements.append(Spacer(1, 4))
    if elements:
        elements.pop()

    t = Table([[elements]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('LINELEFT', (0, 0), (-1, -1), 2.5, colors.HexColor("#3B82F6")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t

def generate_chapter17_pdf(input_md, output_filename):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    act_subtitle_style = ParagraphStyle(
        'ActSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor("#64748B"),
        alignment=0,
        spaceAfter=4
    )

    title_style = ParagraphStyle(
        'ChapterTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        alignment=0,
        spaceAfter=12
    )

    h3_style = ParagraphStyle(
        'SceneHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#475569")
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.5,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=7,
        alignment=4  # Justificado
    )

    with open(input_md, 'r', encoding='utf-8') as f:
        md_text = f.read()

    lines = md_text.split('\n')
    story = []

    story.append(Paragraph("ACTO II: LA CAÍDA DEL ESCUDO Y EL GRAN CAOS", act_subtitle_style))
    story.append(Spacer(1, 2))

    in_quote = False
    quote_lines = []

    for line in lines:
        stripped = line.strip()

        # Título principal
        if stripped.startswith('# '):
            raw_title = stripped[2:].strip()
            # Limpiar posibles prefijos
            raw_title = re.sub(r'^CAPÍTULO\s+\d+:\s*', 'Capítulo 17: ', raw_title, flags=re.IGNORECASE)
            # Reemplazar comillas tipográficas
            raw_title = raw_title.replace("«", '"').replace("»", '"').replace("—", "-")
            story.append(Paragraph(raw_title, title_style))
            story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
            continue

        # Subtítulo de escena o sección
        if stripped.startswith('### '):
            if in_quote:
                story.append(create_quote_box(quote_lines, styles))
                story.append(Spacer(1, 6))
                in_quote = False
                quote_lines = []
            sub = stripped[4:].strip().replace("«", '"').replace("»", '"').replace("—", "-")
            sub = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', sub)
            story.append(Paragraph(sub, h3_style))
            continue

        # Citas en bloque
        if stripped.startswith('> '):
            in_quote = True
            q_text = stripped[2:].strip().replace("«", '"').replace("»", '"').replace("—", "-")
            q_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', q_text)
            q_text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', q_text)
            quote_lines.append(q_text)
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
        if any(marker in stripped for marker in ['Fase 4', 'Cuenta atrás', 'Puntos de Vista', 'Ubicación', 'T+229']):
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
    md_file = os.path.join("novela", "capitulos", "capitulo_17.md")
    pdf_out = "Capitulo_17_El_Paramo_de_Mediodia.pdf"
    generate_chapter17_pdf(md_file, pdf_out)

    dest_novela = os.path.join("novela", pdf_out)
    shutil.copyfile(pdf_out, dest_novela)
    print(f"Copia sincronizada en: {dest_novela}")
