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
        
        self.drawString(54, 32, "Capítulo 11: La Geometría Ajena")
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
    story_cell = []
    for p in paragraphs_text:
        formatted_p = p
        formatted_p = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', formatted_p)
        formatted_p = re.sub(r'\*(.*?)\*', r'<i>\1</i>', formatted_p)
        story_cell.append(Paragraph(formatted_p, q_style))
        story_cell.append(Spacer(1, 3))
    if story_cell:
        story_cell.pop()
    
    t = Table([[story_cell]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('LINEBEFORE', (0, 0), (0, -1), 2.5, colors.HexColor("#3B82F6")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    return t

def generate_chapter11_pdf(input_md, output_filename):
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
        spaceAfter=4,
        alignment=0
    )

    act_subtitle_style = ParagraphStyle(
        'ActSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#2563EB"),
        spaceAfter=12,
        textTransform='uppercase'
    )

    scene_h2_style = ParagraphStyle(
        'SceneH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=14,
        spaceAfter=2,
        keepWithNext=True
    )

    scene_meta_style = ParagraphStyle(
        'SceneMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=8,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'NovelBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.6,
        leading=14.2,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=6,
        alignment=4
    )

    dialogue_style = ParagraphStyle(
        'NovelDialogue',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.6,
        leading=14.2,
        textColor=colors.HexColor("#0F172A"),
        leftIndent=12,
        firstLineIndent=-12,
        spaceAfter=5,
        alignment=4
    )

    with open(input_md, 'r', encoding='utf-8') as f:
        md_text = f.read()

    lines = md_text.split('\n')
    story = []

    story.append(Paragraph("LA CANCIÓN DEL SILENCIO • ACTO II", act_subtitle_style))
    story.append(Paragraph("Capítulo 11: La Geometría Ajena", title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E2E8F0"), spaceBefore=4, spaceAfter=14))

    quote_buffer = []
    in_quote = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith('# Capítulo 11'):
            continue

        if stripped.startswith('>'):
            in_quote = True
            quote_text = re.sub(r'^>\s*', '', stripped)
            quote_buffer.append(quote_text)
            continue
        else:
            if in_quote:
                story.append(create_quote_box(quote_buffer, styles))
                story.append(Spacer(1, 6))
                quote_buffer = []
                in_quote = False

        if not stripped:
            continue

        if stripped.startswith('### '):
            clean_title = stripped.replace('### ', '').strip()
            story.append(Spacer(1, 8))
            story.append(Paragraph(clean_title, scene_h2_style))
            continue

        if stripped.startswith('**') and stripped.endswith('**') and len(stripped) < 120 and ('UTC' in stripped or 'Subsuelo' in stripped or 'Nivel' in stripped or 'Faltan' in stripped or 'Sala' in stripped or 'Galería' in stripped or 'La Caída' in stripped or 'El Pacto' in stripped):
            clean_meta = stripped.replace('**', '').strip()
            story.append(Paragraph(f"<b>{clean_meta}</b>", scene_meta_style))
            continue

        if stripped.startswith('*') and stripped.endswith('*') and len(stripped) < 140 and ('Faltan' in stripped or 'Cuenta' in stripped):
            clean_meta = stripped.replace('*', '').strip()
            story.append(Paragraph(f"<i>{clean_meta}</i>", scene_meta_style))
            continue

        if stripped == '***' or stripped == '---':
            story.append(Spacer(1, 6))
            story.append(HRFlowable(width="30%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceBefore=4, spaceAfter=8, hAlign='CENTER'))
            continue

        formatted_line = stripped
        formatted_line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', formatted_line)
        formatted_line = re.sub(r'\*(.*?)\*', r'<i>\1</i>', formatted_line)

        if formatted_line.startswith('—') or formatted_line.startswith('&mdash;') or formatted_line.startswith('-'):
            story.append(Paragraph(formatted_line, dialogue_style))
        else:
            story.append(Paragraph(formatted_line, body_style))

    if in_quote:
        story.append(create_quote_box(quote_buffer, styles))
        story.append(Spacer(1, 6))

    doc.build(story, canvasmaker=BookCanvas)
    print(f"PDF generado con éxito: {output_filename}")

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, "novela", "capitulos", "capitulo_11.md")
    output_path = os.path.join(base_dir, "novela", "Capitulo_11_La_Geometria_Ajena.pdf")
    generate_chapter11_pdf(input_path, output_path)

    # Copia en la raíz del proyecto para visibilidad directa
    root_output_path = os.path.join(base_dir, "Capitulo_11_La_Geometria_Ajena.pdf")
    shutil.copyfile(output_path, root_output_path)
    print(f"Copia creada en la raíz: {root_output_path}")
