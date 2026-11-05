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

CHAPTER_METADATA = {
    1: {"titulo": "Capítulo 1: Alamogordo", "acto": "ACTO I: LA SEMILLA", "new_pdf": "Capitulo_1_Alamogordo.pdf", "legacy_pdf": "Capitulo_1_El_Amanecer_de_Alamogordo.pdf"},
    2: {"titulo": "Capítulo 2: Tres Hilos", "acto": "ACTO I: LA SEMILLA", "new_pdf": "Capitulo_2_Tres_Hilos.pdf", "legacy_pdf": "Capitulo_2_Los_Tres_Hilos_del_Ilusionista.pdf"},
    3: {"titulo": "Capítulo 3: Sala Dos", "acto": "ACTO I: LA SEMILLA", "new_pdf": "Capitulo_3_Sala_Dos.pdf", "legacy_pdf": "Capitulo_3_La_Sala_Dos.pdf"},
    4: {"titulo": "Capítulo 4: Alfa Cero", "acto": "ACTO II: EL COLAPSO", "new_pdf": "Capitulo_4_Alfa_Cero.pdf", "legacy_pdf": "Capitulo_4_El_Vertigo_de_las_Naciones.pdf"},
    5: {"titulo": "Capítulo 5: El Adiós", "acto": "ACTO II: EL COLAPSO", "new_pdf": "Capitulo_5_El_Adios.pdf", "legacy_pdf": "Capitulo_5_El_Ancla_Humana.pdf"},
    6: {"titulo": "Capítulo 6: El Consejo", "acto": "ACTO II: EL COLAPSO", "new_pdf": "Capitulo_6_El_Consejo.pdf", "legacy_pdf": "Capitulo_6_La_Camara_del_Silencio.pdf"},
    7: {"titulo": "Capítulo 7: El Secreto", "acto": "ACTO II: EL COLAPSO", "new_pdf": "Capitulo_7_El_Secreto.pdf", "legacy_pdf": "Capitulo_7_La_Condicion_Immedible.pdf"},
    8: {"titulo": "Capítulo 8: Carrington", "acto": "ACTO II: EL COLAPSO", "new_pdf": "Capitulo_8_Carrington.pdf", "legacy_pdf": "Capitulo_8_La_Gran_Mentira.pdf"},
    9: {"titulo": "Capítulo 9: La Fractura", "acto": "ACTO II: EL COLAPSO", "new_pdf": "Capitulo_9_La_Fractura.pdf", "legacy_pdf": "Capitulo_9_La_Fractura_del_Orden.pdf"},
    10: {"titulo": "Capítulo 10: T=0", "acto": "ACTO II: EL COLAPSO", "new_pdf": "Capitulo_10_T0.pdf", "legacy_pdf": "Capitulo_10_T0.pdf"},
    11: {"titulo": "Capítulo 11: Geometría Ajena", "acto": "ACTO II: EL COLAPSO", "new_pdf": "Capitulo_11_Geometria_Ajena.pdf", "legacy_pdf": "Capitulo_11_La_Geometria_Ajena.pdf"},
    12: {"titulo": "Capítulo 12: Nochebuena", "acto": "ACTO II: EL COLAPSO", "new_pdf": "Capitulo_12_Nochebuena.pdf", "legacy_pdf": "Capitulo_12_La_Tregua_de_las_Velas.pdf"},
    13: {"titulo": "Capítulo 13: Toque de Alba", "acto": "ACTO II: EL COLAPSO", "new_pdf": "Capitulo_13_Toque_de_Alba.pdf", "legacy_pdf": "Capitulo_13_El_Toque_de_Alba.pdf"},
    14: {"titulo": "Capítulo 14: Hambre y Fuego", "acto": "ACTO II: EL COLAPSO", "new_pdf": "Capitulo_14_Hambre_y_Fuego.pdf", "legacy_pdf": "Capitulo_14_El_Pan_y_la_Polvora.pdf"},
    15: {"titulo": "Capítulo 15: Market Street", "acto": "ACTO II: EL COLAPSO", "new_pdf": "Capitulo_15_Market_Street.pdf", "legacy_pdf": "Capitulo_15_El_Vientre_de_la_Bahia.pdf"},
    16: {"titulo": "Capítulo 16: Ceniza", "acto": "ACTO II: EL COLAPSO", "new_pdf": "Capitulo_16_Ceniza.pdf", "legacy_pdf": "Capitulo_16_El_Umbral_de_Ceniza.pdf"},
    17: {"titulo": "Capítulo 17: El Páramo", "acto": "ACTO II: EL COLAPSO", "new_pdf": "Capitulo_17_El_Paramo.pdf", "legacy_pdf": "Capitulo_17_El_Paramo_de_Mediodia.pdf"},
    18: {"titulo": "Capítulo 18: La Rampa", "acto": "ACTO II: EL COLAPSO", "new_pdf": "Capitulo_18_La_Rampa.pdf", "legacy_pdf": "Capitulo_18_La_Rampa_del_Juicio_Final.pdf"},
    19: {"titulo": "Capítulo 19: Muro de Lorentz", "acto": "ACTO III: EL SILENCIO", "new_pdf": "Capitulo_19_Muro_de_Lorentz.pdf", "legacy_pdf": "Capitulo_19_La_Travesia_a_Ciegas_y_el_Velo_de_Sombra.pdf"},
    20: {"titulo": "Capítulo 20: Falsa Victoria", "acto": "ACTO III: EL SILENCIO", "new_pdf": "Capitulo_20_Falsa_Victoria.pdf", "legacy_pdf": "Capitulo_20_El_Salmo_de_la_Falsa_Victoria.pdf"},
    21: {"titulo": "Capítulo 21: Cielo Azul", "acto": "ACTO III: EL SILENCIO", "new_pdf": "Capitulo_21_Cielo_Azul.pdf", "legacy_pdf": "Capitulo_21_El_Despertar_del_Azul.pdf"},
    22: {"titulo": "Capítulo 22: El Hogar", "acto": "ACTO III: EL SILENCIO", "new_pdf": "Capitulo_22_El_Hogar.pdf", "legacy_pdf": "Capitulo_22_La_Mascara_de_los_Heroes_y_el_Reencuentro_del_Hogar.pdf"},
    23: {"titulo": "Capítulo 23: El Desván", "acto": "ACTO III: EL SILENCIO", "new_pdf": "Capitulo_23_El_Desvan.pdf", "legacy_pdf": "Capitulo_23_La_Aguja_en_el_Desvan.pdf"},
    24: {"titulo": "Capítulo 24: El Pacto", "acto": "ACTO III: EL SILENCIO", "new_pdf": "Capitulo_24_El_Pacto.pdf", "legacy_pdf": "Capitulo_24_La_Conjuracion_del_Silencio.pdf"},
    25: {"titulo": "Capítulo 25: La Canción", "acto": "ACTO III: EL SILENCIO", "new_pdf": "Capitulo_25_La_Cancion.pdf", "legacy_pdf": "Capitulo_25_La_Cancion_del_Silencio.pdf"}
}

def make_canvas_class(act_title, chap_title):
    class DynamicBookCanvas(canvas.Canvas):
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
                self.drawRightString(A4[0] - 54, A4[1] - 36, act_title)
                self.setStrokeColor(colors.HexColor("#CBD5E1"))
                self.setLineWidth(0.5)
                self.line(54, A4[1] - 42, A4[0] - 54, A4[1] - 42)
            
            # Pie de página
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 45, A4[0] - 54, 45)
            
            self.drawString(54, 32, chap_title)
            page_str = f"Página {self._pageNumber} de {page_count}"
            self.drawRightString(A4[0] - 54, 32, page_str)
            self.restoreState()

    return DynamicBookCanvas

def format_markdown_inline(text):
    if not text:
        return ""
    text = text.replace("«", '"').replace("»", '"')
    text = text.replace("—", " - ").replace("–", " - ")
    # Handle bold + italic ***text***
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<b><i>\1</i></b>', text)
    # Handle bold **text**
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Handle italic *text*
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    # Fix any inverted or misnested tags that ReportLab rejects
    text = text.replace("<b><i>", "###BI###")
    text = text.replace("</i></b>", "###/BI###")
    text = text.replace("</b></i>", "###/BI###")
    text = text.replace("###BI###", "<b><i>")
    text = text.replace("###/BI###", "</i></b>")
    return text

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
        ('LINELEFT', (0,0), (0,0), 3.5, colors.HexColor("#4338CA")),
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

def generate_chapter_pdf(chap_num, input_md_path, output_filename):
    if not os.path.exists(input_md_path):
        print(f"Error: No se encuentra {input_md_path}")
        return False

    meta = CHAPTER_METADATA.get(chap_num, {
        "titulo": f"Capítulo {chap_num}",
        "acto": "LA CANCIÓN DEL SILENCIO",
        "new_pdf": f"Capitulo_{chap_num}.pdf",
        "legacy_pdf": f"Capitulo_{chap_num}.pdf"
    })

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
        textColor=colors.HexColor("#4338CA"),
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

        # Bloques de código preformateado
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
            story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#4338CA"), spaceBefore=2, spaceAfter=14))
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
            raw_quote = stripped.lstrip('> ')
            formatted_quote = format_markdown_inline(raw_quote)
            quote_lines.append(formatted_quote)
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
        clean_line = format_markdown_inline(stripped)
        story.append(Paragraph(clean_line, body_style))

    if in_quote:
        story.append(create_quote_box(quote_lines, styles))
        story.append(Spacer(1, 6))

    if in_code:
        story.append(create_code_box(code_lines, styles))
        story.append(Spacer(1, 6))

    canvas_class = make_canvas_class(meta["acto"], meta["titulo"])
    doc.build(story, canvasmaker=canvas_class)
    return True

def compile_all_chapters():
    print("Iniciando compilación integral de los 25 capítulos con nuevos títulos...")
    for chap_num in range(1, 26):
        md_file = os.path.join("novela", "capitulos", f"capitulo_{chap_num}.md")
        meta = CHAPTER_METADATA[chap_num]
        new_pdf_name = meta["new_pdf"]
        legacy_pdf_name = meta["legacy_pdf"]

        # Generar PDF principal con nombre conciso nuevo
        success = generate_chapter_pdf(chap_num, md_file, new_pdf_name)
        if success:
            # Copiar a novela/
            dest_new = os.path.join("novela", new_pdf_name)
            shutil.copyfile(new_pdf_name, dest_new)

            # Si el legacy_pdf es distinto, sincronizarlo también para retrocompatibilidad
            if legacy_pdf_name != new_pdf_name:
                shutil.copyfile(new_pdf_name, legacy_pdf_name)
                dest_legacy = os.path.join("novela", legacy_pdf_name)
                shutil.copyfile(new_pdf_name, dest_legacy)
                print(f"[OK] Cap {chap_num:2d}: {meta['titulo']} -> {new_pdf_name} (+ {legacy_pdf_name})")
            else:
                print(f"[OK] Cap {chap_num:2d}: {meta['titulo']} -> {new_pdf_name}")
        else:
            print(f"[ERROR] Cap {chap_num:2d}: Falló la generación.")

if __name__ == "__main__":
    compile_all_chapters()
