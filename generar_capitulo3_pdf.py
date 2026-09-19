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
            self.drawString(54, A4[1] - 36, "LA GUERRA DE LA HERENCIA • NOVELA DE CIENCIA FICCIÓN")
            self.drawRightString(A4[0] - 54, A4[1] - 36, "ACTO I: LA SEMILLA Y EL TEJIDO SILENCIOSO")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, A4[1] - 42, A4[0] - 54, A4[1] - 42)
        
        # Pie de página
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 45, A4[0] - 54, 45)
        
        self.drawString(54, 32, "Capítulo 3: La Sala Dos (El Mensaje del Avatar)")
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
        spaceAfter=4
    )
    content = []
    for line in paragraphs_text:
        formatted = re.sub(r'\*(.*?)\*', r'<i>\1</i>', line)
        content.append(Paragraph(formatted, q_style))
        
    t = Table([[content]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('LINELEFT', (0,0), (-1,-1), 3.5, colors.HexColor("#0284C7")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
    ]))
    return t

def generate_chapter3_pdf(md_path, output_filename):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    super_title_style = ParagraphStyle(
        'BookSuperTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#0284C7"),
        alignment=1,
        spaceAfter=4
    )
    
    title_style = ParagraphStyle(
        'ChapterTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#0F172A"),
        alignment=1,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'ChapterSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor("#475569"),
        alignment=1,
        spaceAfter=14
    )
    
    scene_h2_style = ParagraphStyle(
        'SceneH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=14,
        spaceAfter=3,
        keepWithNext=True
    )
    
    scene_meta_style = ParagraphStyle(
        'SceneMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=8,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'NovelBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.8,
        leading=14.5,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=7.5,
        alignment=4 # Justificado
    )
    
    dialogue_style = ParagraphStyle(
        'NovelDialogue',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.8,
        leading=14.5,
        textColor=colors.HexColor("#0F172A"),
        leftIndent=10,
        spaceAfter=6,
        alignment=4
    )
    
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    story = []
    
    # Encabezado editorial del Capítulo 3
    story.append(Paragraph("LA GUERRA DE LA HERENCIA • LIBRO I", super_title_style))
    story.append(Paragraph("Capítulo 3: La Sala Dos", title_style))
    story.append(Paragraph("Nueva York: La convocatoria secreta y la caída de la máscara", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=14))
    
    i = 0
    in_quote = False
    quote_buffer = []
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Saltar título principal de markdown (ya añadido arriba)
        if line.startswith("# Capítulo 3:"):
            i += 1
            continue
            
        # Detectar fin de bloque de cita
        if in_quote and (not line.startswith(">") or line == ""):
            story.append(create_quote_box(quote_buffer, styles))
            story.append(Spacer(1, 6))
            in_quote = False
            quote_buffer = []
            
        if not line:
            i += 1
            continue
            
        # Separador horizontal
        if line == "---":
            story.append(Spacer(1, 4))
            story.append(HRFlowable(width="60%", thickness=0.5, color=colors.HexColor("#E2E8F0"), spaceBefore=6, spaceAfter=8))
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
        
        # Diálogos
        if line.startswith("—") or line.startswith("- "):
            story.append(Paragraph(formatted_line, dialogue_style))
        else:
            story.append(Paragraph(formatted_line, body_style))
            
        i += 1
        
    # Si quedó alguna cita abierta al final
    if in_quote and quote_buffer:
        story.append(create_quote_box(quote_buffer, styles))
        story.append(Spacer(1, 6))
        
    doc.build(story, canvasmaker=BookCanvas)
    print(f"PDF generado con éxito: {output_filename}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    md_file = os.path.join(base_dir, "novela", "capitulos", "capitulo_3.md")
    out_file1 = os.path.join(base_dir, "novela", "Capitulo_3_La_Sala_Dos.pdf")
    out_file2 = os.path.join(base_dir, "Capitulo_3_La_Sala_Dos.pdf")
    
    generate_chapter3_pdf(md_file, out_file1)
    shutil.copyfile(out_file1, out_file2)
    print(f"Copia creada en la raíz: {out_file2}")
