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
        
        self.drawString(54, 32, "Capítulo 8: La Gran Mentira")
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

def generate_chapter8_pdf(input_md, output_filename):
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

    story = []

    with open(input_md, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    story.append(Paragraph("ACTO II: LA CAÍDA DEL ESCUDO Y EL GRAN CAOS", act_subtitle_style))
    story.append(Paragraph("Capítulo 8: La Gran Mentira", title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=4, spaceAfter=14))

    in_quote = False
    quote_buffer = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Ignorar título h1 original
        if line.startswith("# "):
            i += 1
            continue
            
        if line == "":
            if in_quote and quote_buffer:
                story.append(create_quote_box(quote_buffer, styles))
                story.append(Spacer(1, 6))
                quote_buffer = []
                in_quote = False
            i += 1
            continue
            
        # Separador horizontal
        if line == "---":
            if in_quote and quote_buffer:
                story.append(create_quote_box(quote_buffer, styles))
                quote_buffer = []
                in_quote = False
            story.append(Spacer(1, 6))
            story.append(HRFlowable(width="40%", thickness=0.5, color=colors.HexColor("#94A3B8"), spaceBefore=4, spaceAfter=8, hAlign='CENTER'))
            i += 1
            continue

        if line == "***":
            story.append(Spacer(1, 4))
            story.append(HRFlowable(width="20%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceBefore=4, spaceAfter=8, hAlign='CENTER'))
            i += 1
            continue
            
        # Encabezado de Escena (### 📍 ...)
        if line.startswith("### 📍"):
            scene_title = line.replace("### 📍", "").strip()
            meta_lines = []
            j = i + 1
            while j < len(lines):
                next_l = lines[j].strip()
                if next_l.startswith("*") and next_l.endswith("*"):
                    clean_m = next_l.strip("*").strip()
                    meta_lines.append(clean_m)
                    j += 1
                elif next_l == "":
                    j += 1
                else:
                    break
            i = j
            story.append(Spacer(1, 6))
            story.append(Paragraph(scene_title, scene_h2_style))
            if meta_lines:
                combined_meta = " • ".join(meta_lines)
                story.append(Paragraph(combined_meta, scene_meta_style))
            continue
            
        # Encabezado h4 (#### 1. ...)
        if line.startswith("#### "):
            sub_title = line.replace("#### ", "").strip()
            story.append(Spacer(1, 4))
            story.append(Paragraph(sub_title, scene_h2_style))
            i += 1
            continue

        # Bloque de cita (> ...)
        if line.startswith(">"):
            in_quote = True
            clean_q = line.lstrip(">").strip()
            if clean_q:
                quote_buffer.append(clean_q)
            i += 1
            continue
            
        # Convertir negritas y cursivas básicas a HTML
        formatted_line = line
        formatted_line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', formatted_line)
        formatted_line = re.sub(r'\*(.*?)\*', r'<i>\1</i>', formatted_line)
        
        # Diálogos o viñetas
        if line.startswith("—") or line.startswith("- "):
            story.append(Paragraph(formatted_line, dialogue_style))
        else:
            story.append(Paragraph(formatted_line, body_style))
            
        i += 1
        
    if in_quote and quote_buffer:
        story.append(create_quote_box(quote_buffer, styles))
        story.append(Spacer(1, 6))
        
    doc.build(story, canvasmaker=BookCanvas)
    print(f"PDF generado con éxito: {output_filename}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    md_file = os.path.join(base_dir, "novela", "capitulos", "capitulo_8.md")
    
    out_file1 = os.path.join(base_dir, "novela", "Capitulo_8_La_Gran_Mentira.pdf")
    out_file2 = os.path.join(base_dir, "Capitulo_8_La_Gran_Mentira.pdf")
    
    generate_chapter8_pdf(md_file, out_file1)
    shutil.copyfile(out_file1, out_file2)
    print(f"Copia creada en la raíz: {out_file2}")
