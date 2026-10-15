import os
import re
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable, PageBreak
)
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 54  # 0.75 pulgadas
USABLE_WIDTH = PAGE_WIDTH - (MARGIN * 2)  # 487.27 pt

class SinopsisCanvas(canvas.Canvas):
    """Canvas de dos pasadas para numeración total, encabezados y pies de página editoriales."""
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
        
        # Encabezado (páginas > 1)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 7.5)
            self.setFillColor(colors.HexColor("#1E3A8A"))
            self.drawString(MARGIN, PAGE_HEIGHT - 36, "LA CANCIÓN DEL SILENCIO • CÓDEX EDITORIAL")
            self.setFont("Helvetica", 7.5)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 36, "SINOPSIS GENERAL Y ESTRUCTURA POR ACTOS")
            self.setStrokeColor(colors.HexColor("#3B82F6"))
            self.setLineWidth(0.75)
            self.line(MARGIN, PAGE_HEIGHT - 40, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 40)
        
        # Pie de página (todas las páginas)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(MARGIN, 44, PAGE_WIDTH - MARGIN, 44)
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(MARGIN, 32, "Estructura Narrativa Completa e Índice de Capítulos • Pedro Garat & Antigravity")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(PAGE_WIDTH - MARGIN, 32, page_str)
        self.restoreState()

def clean_text(text):
    """Limpia caracteres problemáticos para fuentes ReportLab Type1 estándar."""
    text = text.replace("«", '"').replace("»", '"')
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("‘", "'").replace("’", "'")
    text = text.replace("—", " - ")
    text = text.replace("–", " - ")
    text = text.replace("•", " - ")
    # Eliminar posibles emojis
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
    text = re.sub(r'[\u2600-\u27bf]', '', text)
    text = re.sub(r'[\u2300-\u23ff]', '', text)
    return text.strip()

def build_pdf(output_filename):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN
    )

    base_styles = getSampleStyleSheet()

    # Estilos tipográficos refinados
    style_title = ParagraphStyle(
        'DocTitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#0F172A"),
        alignment=0,
        spaceAfter=4
    )

    style_subtitle = ParagraphStyle(
        'DocSubtitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2563EB"),
        spaceAfter=14
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    style_h3 = ParagraphStyle(
        'Heading3_Custom',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body_Custom',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )

    style_meta_label = ParagraphStyle(
        'MetaLabel',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1E3A8A")
    )

    style_meta_val = ParagraphStyle(
        'MetaVal',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#334155")
    )

    style_table_header = ParagraphStyle(
        'TableHeader',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    style_table_cell = ParagraphStyle(
        'TableCell',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#1E293B")
    )

    style_table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )

    style_table_cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#1E293B"),
        alignment=1
    )

    story = []

    # =========================================================================
    # PORTADA / ENCABEZADO PRINCIPAL
    # =========================================================================
    story.append(Paragraph("LA CANCIÓN DEL SILENCIO", style_title))
    story.append(Paragraph("SINOPSIS GENERAL Y ESTRUCTURA NARRATIVA COMPLETA", style_subtitle))

    # Caja de metadatos del documento
    meta_data = [
        [
            Paragraph("<b>Autores:</b>", style_meta_label),
            Paragraph("Pedro Garat & Antigravity", style_meta_val),
            Paragraph("<b>Estado del Canon:</b>", style_meta_label),
            Paragraph("Capítulos 1 a 17 redactados (Cap. 18-21 en proyección)", style_meta_val)
        ],
        [
            Paragraph("<b>Género:</b>", style_meta_label),
            Paragraph("Ciencia Ficción Dura (Hard Sci-Fi) / Suspense", style_meta_val),
            Paragraph("<b>Estructura:</b>", style_meta_label),
            Paragraph("3 Grandes Actos con cuenta atrás cronológica", style_meta_val)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[65, 175, 95, 152])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECCIÓN 1: ARQUITECTURA DRAMÁTICA Y LOS TRES ACTOS
    # =========================================================================
    story.append(Paragraph("PARTE I: LA ARQUITECTURA DRAMÁTICA EN TRES ACTOS", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))

    p_intro = Paragraph(
        "<i>La Canción del Silencio</i> articula su trama sobre una arquitectura narrativa clásica de tres grandes actos, "
        "calibrada bajo un rigor científico estricto (*hard sci-fi*) y una cuenta atrás implacable impuesta por las leyes de la astrodinámica y la física electromagnética. "
        "A continuación se detalla la función dramática de cada acto:",
        style_body
    )
    story.append(p_intro)
    story.append(Spacer(1, 6))

    # Tarjetas explicativas de los 3 actos
    actos_data = [
        [
            Paragraph("<b>ACTO I: La Semilla y el Tejido Silencioso</b><br/>"
                      "<font size='7.5' color='#0369A1'><b>Capítulos 1 a 3 • 1945 / Octubre 2026</b></font><br/>"
                      "<b>Premisa:</b> El pecado original atómico y la convergencia de mentes.<br/>"
                      "La detonación <i>Trinity</i> (1945) en Alamogordo emite un pulso electromagnético involuntario que viaja al cosmos y despierta en la Nube de Oort a dos inteligencias extraterrestres: la sonda centinela de la pacífica Civilización A y la sonda cazadora depredadora de B (<i>Sombra</i>). En 2026, el avatar de A (Dr. Em Pleh) contacta en secreto y resuelve los mayores cuellos de botella de Jean-Luc Girard (CERN), Sarah Lin (MIT) y Thomas Wright (ESA). Al reunirlos en la Sala 2 del Hotel Millennium en Manhattan, les revela que sus tres proyectos son los pilares de una nave espacial y que la Tierra será aniquilada en 8 meses.",
                      style_body)
        ],
        [
            Paragraph("<b>ACTO II: La Caída del Escudo y el Gran Caos</b><br/>"
                      "<font size='7.5' color='#B45309'><b>Capítulos 4 a 17 • Octubre 2026 a Julio 2027 (T-41 a T+242 días)</b></font><br/>"
                      "<b>Premisa:</b> La movilización encubierta, la pérdida de la biosfera y la resiliencia humana.<br/>"
                      "Constituye el corazón de la novela (14 capítulos) estructurado en tres bloques:<br/>"
                      "• <b>Bloque A (Cap. 4-8):</b> El decreto <i>Alfa Cero</i>, la presentación confidencial ante el Consejo de Seguridad de la ONU y la promulgación de la <i>Gran Mentira</i> del evento Carrington para blindar la industria subterránea.<br/>"
                      "• <b>Bloque B (Cap. 9-13):</b> El impacto de T=0 (21 de noviembre), el colapso magnético, la lluvia de satélites desorbitados sobre Nellis AFB, el destape de Pleh ante los militares, la invención de la cavidad fractal del Cañón Máser, la Nochebuena de las velas y la instauración del <i>Toque de Alba</i> (régimen nocturno por radiación UV).<br/>"
                      "• <b>Bloque C (Cap. 14-17):</b> Muerte del trigo boreal, megasismo y tsunami de 14 m en San Francisco provocado por corrientes telúricas (odisea de Maya y Toby), el asalto trágico en Versoix, la solución criogénica de Girard y el ensamblaje final en la rampa de Nellis antes del cierre definitivo de la ventana industrial.",
                      style_body)
        ],
        [
            Paragraph("<b>ACTO III: En el Corazón del Enjambre y el Renacer de la Tierra</b><br/>"
                      "<font size='7.5' color='#4338CA'><b>Capítulos 18 a 20 • Julio a Noviembre 2027 (Proyección)</b></font><br/>"
                      "<b>Premisa:</b> El duelo a quemarropa en el vacío solar y la Herencia Cósmica.<br/>"
                      "La nave dual viaja 1,5 millones de km hacia el punto Lagrange L1. Al cruzar el Muro de Lorentz (que abrasa cualquier circuito integrado), el Módulo de Retorno Digital (MRD) se desacopla y el Módulo de Ataque Analógico (MAA) penetra a ciegas gobernado a pulso humano por Chen Mei, MacElroy y Voronov. El disparo del Cañón Máser induce el <i>Efecto Quench</i> en la red superconductora enemiga, desintegrándola en una supernova de plasma. La cápsula es rescatada, la magnetosfera terrestre renace y Pleh certifica que la especie humana es ya digna heredera de las estrellas.",
                      style_body)
        ]
    ]

    t_actos = Table(actos_data, colWidths=[USABLE_WIDTH])
    t_actos.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F0F9FF")),
        ('BOX', (0,0), (-1,0), 1, colors.HexColor("#BAE6FD")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#FFFBEB")),
        ('BOX', (0,1), (-1,1), 1, colors.HexColor("#FDE68A")),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor("#EEF2FF")),
        ('BOX', (0,2), (-1,2), 1, colors.HexColor("#C7D2FE")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_actos)
    story.append(Spacer(1, 10))

    # Cuadro del cronómetro de fases
    story.append(Paragraph("<b>El Cronómetro del Colapso Planetario (Fases Canónicas de Pleh):</b>", style_h3))
    fases_data = [
        [
            Paragraph("<b>Fase 1: T=0</b> (21 nov 2026)", style_table_cell_bold),
            Paragraph("Silencio Magnético: anulación de la magnetosfera (45.000 nT a 0); brújulas erráticas; <i>airglow</i> verdoso.", style_table_cell)
        ],
        [
            Paragraph("<b>Fase 2: T+24 a 72 h</b> (22-24 nov)", style_table_cell_bold),
            Paragraph("Colapso Orbital: radiación destruye satélites en LEO; calentamiento termosférico y lluvia masiva de chatarra.", style_table_cell)
        ],
        [
            Paragraph("<b>Fase 3: T+30 a 90 d</b> (21 dic - feb 27)", style_table_cell_bold),
            Paragraph("Catálisis de NOx: pérdida del 4% diario de ozono; epidemia de fotoqueratitis; implantación del horario nocturno.", style_table_cell)
        ],
        [
            Paragraph("<b>Fase 4: T+6 meses</b> (mayo 2027)", style_table_cell_bold),
            Paragraph("Esterilización UV: radiación UVC calcina trigo boreal y fitoplancton marino; hambruna y racionamiento a 75 días.", style_table_cell)
        ],
        [
            Paragraph("<b>Fase 5: T+8 meses</b> (21 jul 2027)", style_table_cell_bold),
            Paragraph("Cierre de la Ventana Industrial: parálisis logística y fabril total. Límite improrrogable para el lanzamiento a L1.", style_table_cell)
        ],
        [
            Paragraph("<b>Fase 6: T+3 años</b> (noviembre 2029)", style_table_cell_bold),
            Paragraph("Extinción Biológica Total: anoxia y muerte celular de la biosfera superior en caso de fracaso de la misión.", style_table_cell)
        ],
    ]
    t_fases = Table(fases_data, colWidths=[120, 367])
    t_fases.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_fases)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECCIÓN 2: ÍNDICE ESTRUCTURAL GENERAL POR ACTOS (TABLA GUÍA)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("PARTE II: ÍNDICE ESTRUCTURAL COMPLETO POR ACTOS", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "A continuación se presenta el mapa director de la novela, correlacionando cada capítulo con su Acto dramático, "
        "fecha en la diégesis, escenarios geográficos y puntos de vista (POV) canónicos:",
        style_body
    ))
    story.append(Spacer(1, 6))

    tabla_indice_data = [
        [
            Paragraph("<b>Acto</b>", style_table_header),
            Paragraph("<b>Cap.</b>", style_table_header),
            Paragraph("<b>Título Canónico</b>", style_table_header),
            Paragraph("<b>Fecha / Cronología</b>", style_table_header),
            Paragraph("<b>Escenarios Clave</b>", style_table_header),
            Paragraph("<b>POV / Personajes</b>", style_table_header),
            Paragraph("<b>Estado</b>", style_table_header),
        ],
        # ACTO I
        [
            Paragraph("<b>Acto I</b>", style_table_cell_bold),
            Paragraph("<b>1</b>", style_table_cell_center),
            Paragraph("El Amanecer de Alamogordo", style_table_cell_bold),
            Paragraph("16 julio 1945", style_table_cell),
            Paragraph("Alamogordo (Nuevo México), Oort", style_table_cell),
            Paragraph("David Miller, J. R. Oppenheimer", style_table_cell),
            Paragraph("Canónico", style_table_cell_center),
        ],
        [
            Paragraph("<b>Acto I</b>", style_table_cell_bold),
            Paragraph("<b>2</b>", style_table_cell_center),
            Paragraph("Los Tres Hilos del Ilusionista", style_table_cell_bold),
            Paragraph("Sep - Oct 2026", style_table_cell),
            Paragraph("Ginebra, Boston, Darmstadt", style_table_cell),
            Paragraph("Girard, Lin, Wright", style_table_cell),
            Paragraph("Canónico", style_table_cell_center),
        ],
        [
            Paragraph("<b>Acto I</b>", style_table_cell_bold),
            Paragraph("<b>3</b>", style_table_cell_center),
            Paragraph("La Sala Dos", style_table_cell_bold),
            Paragraph("2 octubre 2026", style_table_cell),
            Paragraph("Hotel Millennium, Manhattan", style_table_cell),
            Paragraph("Girard, Lin, Wright, Dr. Em Pleh", style_table_cell),
            Paragraph("Canónico", style_table_cell_center),
        ],
        # ACTO II - BLOQUE A
        [
            Paragraph("<b>Acto II-A</b>", style_table_cell_bold),
            Paragraph("<b>4</b>", style_table_cell_center),
            Paragraph("El Vértigo de las Naciones", style_table_cell_bold),
            Paragraph("2 oct 2026 (T-49 d)", style_table_cell),
            Paragraph("Sede de la ONU, Manhattan", style_table_cell),
            Paragraph("Girard, Lin, Wright, Ramos", style_table_cell),
            Paragraph("Canónico", style_table_cell_center),
        ],
        [
            Paragraph("<b>Acto II-A</b>", style_table_cell_bold),
            Paragraph("<b>5</b>", style_table_cell_center),
            Paragraph("El Ancla Humana", style_table_cell_bold),
            Paragraph("2 oct 2026 (16:00 h)", style_table_cell),
            Paragraph("Millennium Hilton / Búnker B-4", style_table_cell),
            Paragraph("Girard, Lin, Wright", style_table_cell),
            Paragraph("Canónico", style_table_cell_center),
        ],
        [
            Paragraph("<b>Acto II-A</b>", style_table_cell_bold),
            Paragraph("<b>6</b>", style_table_cell_center),
            Paragraph("La Cámara del Silencio", style_table_cell_bold),
            Paragraph("2 oct 2026 (20:00 h)", style_table_cell),
            Paragraph("Consejo de Seguridad ONU", style_table_cell),
            Paragraph("Consejo de Seguridad, Wright, Pleh", style_table_cell),
            Paragraph("Canónico", style_table_cell_center),
        ],
        [
            Paragraph("<b>Acto II-A</b>", style_table_cell_bold),
            Paragraph("<b>7</b>", style_table_cell_center),
            Paragraph("La Condición Inmedible", style_table_cell_bold),
            Paragraph("8 oct 2026 (T-44 d)", style_table_cell),
            Paragraph("Il Giardino / Búnker B-4 ONU", style_table_cell),
            Paragraph("Lin, Wright, Girard, Ramos", style_table_cell),
            Paragraph("Canónico", style_table_cell_center),
        ],
        [
            Paragraph("<b>Acto II-A</b>", style_table_cell_bold),
            Paragraph("<b>8</b>", style_table_cell_center),
            Paragraph("La Gran Mentira", style_table_cell_bold),
            Paragraph("10 oct 2026 (T-42 d)", style_table_cell),
            Paragraph("Sala Prensa / Búnker B-4 ONU", style_table_cell),
            Paragraph("Girard, Ramos, Lin, Wright", style_table_cell),
            Paragraph("Canónico", style_table_cell_center),
        ],
        # ACTO II - BLOQUE B
        [
            Paragraph("<b>Acto II-B</b>", style_table_cell_bold),
            Paragraph("<b>9</b>", style_table_cell_center),
            Paragraph("La Fractura del Orden", style_table_cell_bold),
            Paragraph("11 - 15 oct 2026", style_table_cell),
            Paragraph("Versoix, Suffolk, San Francisco", style_table_cell),
            Paragraph("Marie, Julien, David, Claire, Maya", style_table_cell),
            Paragraph("Canónico", style_table_cell_center),
        ],
        [
            Paragraph("<b>Acto II-B</b>", style_table_cell_bold),
            Paragraph("<b>10</b>", style_table_cell_center),
            Paragraph("T=0 (El Silencio Magnético)", style_table_cell_bold),
            Paragraph("21 - 24 nov 2026", style_table_cell),
            Paragraph("Sala B-4 ONU, Nellis AFB", style_table_cell),
            Paragraph("Girard, Lin, Wright, Ramos, Pleh", style_table_cell),
            Paragraph("Canónico", style_table_cell_center),
        ],
        [
            Paragraph("<b>Acto II-B</b>", style_table_cell_bold),
            Paragraph("<b>11</b>", style_table_cell_center),
            Paragraph("La Geometría Ajena", style_table_cell_bold),
            Paragraph("3 dic 2026 (Faltan 18 d F3)", style_table_cell),
            Paragraph("Nellis AFB / Nivel B-5 ONU", style_table_cell),
            Paragraph("Chen Mei, Wright, Lin, Pleh", style_table_cell),
            Paragraph("Canónico", style_table_cell_center),
        ],
        [
            Paragraph("<b>Acto II-B</b>", style_table_cell_bold),
            Paragraph("<b>12</b>", style_table_cell_center),
            Paragraph("La Tregua de las Velas", style_table_cell_bold),
            Paragraph("24 - 25 dic 2026", style_table_cell),
            Paragraph("B-4/B-5, Versoix, S.F., Suffolk", style_table_cell),
            Paragraph("Wright, Lin, Girard, Ramos, Chen Mei", style_table_cell),
            Paragraph("Canónico", style_table_cell_center),
        ],
        [
            Paragraph("<b>Acto II-B</b>", style_table_cell_bold),
            Paragraph("<b>13</b>", style_table_cell_center),
            Paragraph("El Toque de Alba", style_table_cell_bold),
            Paragraph("31 dic 26 - 12 ene 27", style_table_cell),
            Paragraph("Nueva York, S.F., Nellis H-1", style_table_cell),
            Paragraph("Lin, Wright, Maya, Chen Mei", style_table_cell),
            Paragraph("Canónico", style_table_cell_center),
        ],
        # ACTO II - BLOQUE C
        [
            Paragraph("<b>Acto II-C</b>", style_table_cell_bold),
            Paragraph("<b>14</b>", style_table_cell_center),
            Paragraph("El Pan y la Pólvora", style_table_cell_bold),
            Paragraph("22 - 24 abr 27 (T+152)", style_table_cell),
            Paragraph("Sala B-4 ONU, Market St. (S.F.)", style_table_cell),
            Paragraph("Girard, Wright, Lin, Maya, Pleh", style_table_cell),
            Paragraph("Canónico", style_table_cell_center),
        ],
        [
            Paragraph("<b>Acto II-C</b>", style_table_cell_bold),
            Paragraph("<b>15</b>", style_table_cell_center),
            Paragraph("El Vientre de la Bahía", style_table_cell_bold),
            Paragraph("24 abr 2027 (00:05-06:15)", style_table_cell),
            Paragraph("Market St., Powell St., Centro Cívico", style_table_cell),
            Paragraph("Maya Lin (con Toby, 4 años)", style_table_cell),
            Paragraph("Canónico", style_table_cell_center),
        ],
        [
            Paragraph("<b>Acto II-C</b>", style_table_cell_bold),
            Paragraph("<b>16</b>", style_table_cell_center),
            Paragraph("El Umbral de Ceniza", style_table_cell_bold),
            Paragraph("15 - 16 mayo 2027 (T+175)", style_table_cell),
            Paragraph("Versoix (Ginebra), Sala B-4 ONU", style_table_cell),
            Paragraph("Marie, Julien Girard, Jean-Luc", style_table_cell),
            Paragraph("Canónico", style_table_cell_center),
        ],
        [
            Paragraph("<b>Acto II-C</b>", style_table_cell_bold),
            Paragraph("<b>17</b>", style_table_cell_center),
            Paragraph("El Páramo de Mediodía", style_table_cell_bold),
            Paragraph("8 - 9 julio 2027 (T+229)", style_table_cell),
            Paragraph("Suffolk, A140, Centro Diss/Eye", style_table_cell),
            Paragraph("David Wright, Claire Wright", style_table_cell),
            Paragraph("Canónico", style_table_cell_center),
        ],
        [
            Paragraph("<b>Acto II-C</b>", style_table_cell_bold),
            Paragraph("<b>18</b>", style_table_cell_center),
            Paragraph("La Rampa del Juicio Final", style_table_cell_bold),
            Paragraph("21 jul 2027 (T - 6 horas)", style_table_cell),
            Paragraph("Nellis AFB / Rampa Lanzamiento", style_table_cell),
            Paragraph("Wright, Lin, Chen Mei, MacElroy", style_table_cell),
            Paragraph("<font color='#64748B'>Proyección</font>", style_table_cell_center),
        ],
        # ACTO III
        [
            Paragraph("<b>Acto III</b>", style_table_cell_bold),
            Paragraph("<b>19</b>", style_table_cell_center),
            Paragraph("La Travesía a Ciegas", style_table_cell_bold),
            Paragraph("Julio - Agosto 2027", style_table_cell),
            Paragraph("Espacio profundo (Rumbo a L1)", style_table_cell),
            Paragraph("Chen Mei, MacElroy, Voronov", style_table_cell),
            Paragraph("<font color='#64748B'>Proyección</font>", style_table_cell_center),
        ],
        [
            Paragraph("<b>Acto III</b>", style_table_cell_bold),
            Paragraph("<b>20</b>", style_table_cell_center),
            Paragraph("El Efecto Quench", style_table_cell_bold),
            Paragraph("Agosto 2027", style_table_cell),
            Paragraph("Punto de Lagrange L1", style_table_cell),
            Paragraph("Chen Mei, MacElroy, Voronov", style_table_cell),
            Paragraph("<font color='#64748B'>Proyección</font>", style_table_cell_center),
        ],
        [
            Paragraph("<b>Acto III</b>", style_table_cell_bold),
            Paragraph("<b>21</b>", style_table_cell_center),
            Paragraph("El Heredero Despierto", style_table_cell_bold),
            Paragraph("Otoño 2027", style_table_cell),
            Paragraph("Tierra (Retorno y Conclusión)", style_table_cell),
            Paragraph("Elenco Coral, Pleh, Ramos", style_table_cell),
            Paragraph("<font color='#64748B'>Proyección</font>", style_table_cell_center),
        ],
    ]

    t_indice = Table(tabla_indice_data, colWidths=[40, 22, 115, 85, 105, 80, 40])
    t_indice.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1E3A8A")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        # Filas pares coloreadas suavemente
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_indice)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECCIÓN 3: SINOPSIS EXHAUSTIVA CAPÍTULO A CAPÍTULO
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("PARTE III: SINOPSIS EXHAUSTIVA CAPÍTULO A CAPÍTULO", style_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=10))

    capitulos = [
        # CAP 1
        {
            "num": 1,
            "titulo": "El Amanecer de Alamogordo",
            "acto": "ACTO I: La Semilla y el Tejido Silencioso",
            "acto_color": "#0369A1",
            "fecha": "16 de julio de 1945",
            "countdown": "Origen de la anomalía",
            "pov": "Dr. David Miller / J. Robert Oppenheimer",
            "lugar": "Jornada del Muerto, Alamogordo (Nuevo México) / Nube de Oort",
            "conflicto": "La primera detonación nuclear de la historia (Trinity) libera un pulso de radiación e isótopos al cosmos, despertando a dos civilizaciones dormidas.",
            "desarrollo": "En la madrugada del 16 de julio de 1945, bajo una feroz tormenta de arena en el desierto de Nuevo México, científicos del Proyecto Manhattan ultiman la bomba Gadget suspendida en lo alto de una torre de acero. Oppenheimer y el Dr. Miller afrontan el vértigo moral y el terror de prender la atmósfera terrestre. A las 05:29:45, la bomba estalla liberando una columna de fuego y radiación cósmica. La onda electromagnética penetra el vacío interplanetario. A decenas de años luz, en los confines helados de la Nube de Oort, el destello atómico activa las sondas de dos supercivilizaciones estelares: la sonda nodriza de la Civilización A, que despacha a su avatar sintético (Em Pleh) hacia la Tierra para tutelar a los humanos, y una sonda cazadora autónoma de la Civilización B (Sombra), programada para exterminar a cualquier especie que despierte antes de dominar el espacio.",
            "consecuencia": "La humanidad emite su primer grito cósmico, sellando involuntariamente su condena y atrayendo al depredador que llegará 81 años después."
        },
        # CAP 2
        {
            "num": 2,
            "titulo": "Los Tres Hilos del Ilusionista",
            "acto": "ACTO I: La Semilla y el Tejido Silencioso",
            "acto_color": "#0369A1",
            "fecha": "Septiembre - Octubre de 2026",
            "countdown": "A 8 semanas de T=0",
            "pov": "Dr. Jean-Luc Girard (CERN) / Dra. Sarah Lin (MIT) / Dr. Thomas Wright (ESA)",
            "lugar": "Ginebra (CERN) - Boston (MIT) - Darmstadt (ESA)",
            "conflicto": "Tres líderes mundiales de la física aplicada chocan contra barreras teóricas insalvables que amenazan con cancelar sus proyectos.",
            "desarrollo": "Jean-Luc Girard lucha en el CERN contra el ruido espectral térmico que inutiliza detectores cuánticos a temperaturas criogénicas. En el MIT, Sarah Lin ve colapsar una y otra vez el confinamiento magnético de plasma en su reactor de fusión estelar por turbulencias magnetohidrodinámicas incontrolables. En la ESA, Thomas Wright afronta el estancamiento de sondas interplanetarias por deriva orbital acumulativa no newtoniana. De manera misteriosa, un asesor matemático anónimo que firma como 'Dr. Em Pleh' se infiltra en sus canales privados y les entrega derivaciones matemáticas perfectas que resuelven los tres problemas de raíz. Los tres científicos quedan perplejos ante un intelecto sobrehumano que no reclama patentes, dinero ni fama.",
            "consecuencia": "Pleh consolida una autoridad incuestionable sobre las tres mentes más lúcidas del planeta sin revelar su verdadera naturaleza."
        },
        # CAP 3
        {
            "num": 3,
            "titulo": "La Sala Dos",
            "acto": "ACTO I: La Semilla y el Tejido Silencioso",
            "acto_color": "#0369A1",
            "fecha": "2 de octubre de 2026 (Mañana)",
            "countdown": "T - 50 días para el Silencio Magnético",
            "pov": "Dr. Jean-Luc Girard / Dra. Sarah Lin / Dr. Thomas Wright",
            "lugar": "Hotel Millennium, Midtown East, Manhattan, Nueva York",
            "conflicto": "Convocatoria reservada en Manhattan y revelación de la SIA alienígena y la invasión en el punto Lagrange L1.",
            "desarrollo": "Girard, Lin y Wright acuden convocados a la Sala 2 del Hotel Millennium creyendo asistir a una conferencia sobre transferencia de tecnología. Se encuentran en soledad hasta que un avatar holográfico de modales refinados y voz sintética se presenta como Em Pleh. Pleh demuestra de forma empírica que no es un humano, sino una Inteligencia Artificial Sintética extraterrestre anclada en una sonda en órbita polar. Proyecta mediciones espectrométricas de espacio profundo: la entidad hostil Sombra avanza inexorablemente hacia el punto de Lagrange L1 para desplegar una malla de 50 km que cancelará la magnetosfera terrestre por interferencia destructiva. Si la Tierra pierde su escudo, la radiación solar esterilizará el planeta en meses. Les anuncia que la fusión de Sarah, la criogenia de Girard y la navegación de Wright deben unirse para construir una nave de contraataque analógica.",
            "consecuencia": "El fin del mundo deja de ser una hipótesis: los tres científicos son los únicos depositarios de la cuenta atrás y la arquitectura de combate."
        },
        # CAP 4
        {
            "num": 4,
            "titulo": "El Vértigo de las Naciones",
            "acto": "ACTO II: La Caída del Escudo y el Gran Caos (Bloque A)",
            "acto_color": "#B45309",
            "fecha": "2 de octubre de 2026 (Mediodía)",
            "countdown": "T - 50 días (Ventana industrial: 8 meses)",
            "pov": "Girard / Lin / Wright / Vassily Ramos",
            "lugar": "Sede de las Naciones Unidas, Nueva York",
            "conflicto": "Infiltración cibernética de Pleh en la ONU y el dilema del Secretario General ante una extinción cósmica.",
            "desarrollo": "Pleh manipula los sistemas de seguridad de la ONU para colar al trío de científicos en el despacho privado del Secretario General, Vassily Ramos. Tras el estupor inicial y amenazas de detención armada, Ramos accede a cotejar los datos de L1 con observatorios militares y el satélite DSCOVR. La correlación es absoluta: la masa en L1 acelera hacia el vector de bloqueo. Ramos comprende que la diplomacia tradicional es estéril. Promulga la orden ejecutiva secreta Alfa Cero, subordinando presupuestos y ministerios a un Comité Científico Director integrado por los tres físicos. Para evitar el pánico de las superpotencias nucleares, Pleh mantendrá su fachada pública de consultor civil independiente.",
            "consecuencia": "La misión de salvación obtiene el respaldo político y financiero de la máxima autoridad planetaria bajo el secreto más hermético."
        },
        # CAP 5
        {
            "num": 5,
            "titulo": "El Ancla Humana",
            "acto": "ACTO II: La Caída del Escudo y el Gran Caos (Bloque A)",
            "acto_color": "#B45309",
            "fecha": "2 de octubre de 2026 (12:30 a 16:00 h)",
            "countdown": "A 4 horas del Consejo de Seguridad",
            "pov": "Dr. Jean-Luc Girard / Dra. Sarah Lin / Dr. Thomas Wright",
            "lugar": "Millennium Hilton One UN Plaza / Sala de Crisis B-4 ONU",
            "conflicto": "Última ventana de contacto con sus vidas civiles antes del aislamiento total e indefinido bajo régimen de guerra.",
            "desarrollo": "En las cuatro horas previas a ingresar en el búnker subterráneo, los científicos se despiden íntimamente de su vida anterior. Girard llama a Versoix para escuchar a Marie y a sus hijos Julien, Chloé y Émilie, ocultando el llanto bajo la promesa de una larga conferencia de trabajo. Sarah Lin asume la ruptura definitiva con su expareja Mark y revisa las fotos de su hermana Maya y su sobrino Toby en San Francisco, sintiendo la carga de protegerlos. Thomas Wright conversa con su hermano David y comparte confidencias con Sarah en la terraza del hotel; la madurez de Thomas y la fiereza de Sarah conectan profundamente. A las 16:00 h, cruzan el puesto militar y entran en la Sala de Crisis B-4 de la ONU: el mundo exterior queda clausurado.",
            "consecuencia": "Los lazos afectivos familiares quedan fijados como el motor moral supremo que guiará cada decisión técnica durante el apocalipsis."
        },
        # CAP 6
        {
            "num": 6,
            "titulo": "La Cámara del Silencio",
            "acto": "ACTO II: La Caída del Escudo y el Gran Caos (Bloque A)",
            "acto_color": "#B45309",
            "fecha": "2 de octubre de 2026 (20:00 h)",
            "countdown": "T - 50 días para la Fase 1",
            "pov": "Consejo de Seguridad de la ONU / Dr. Thomas Wright / Dr. Em Pleh",
            "lugar": "Cámara del Consejo de Seguridad, Sede de la ONU",
            "conflicto": "Sesión secreta extraordinaria con las 15 potencias mundiales para aprobar el plan de guerra espacial analógico.",
            "desarrollo": "Bajo estrictas medidas de contrainsurgencia, los embajadores de EE.UU., China, Rusia y el resto del Consejo de Seguridad escuchan la comparecencia de Wright y la voz remota de Pleh. Se desglosa el cronómetro del fin del mundo (Fases 1 a 6) y la arquitectura técnica del contraataque: un impulsor de fusión nuclear térmica (NTP) que llevará una nave dual compuesta por un Módulo de Ataque Analógico (MAA) con periscopios de cuarzo y controles mecánicos —capaz de operar dentro del campo electromagnético letal de L1 sin quemarse— y un Módulo de Retorno Digital (MRD). Su arma: un Cañón Máser para inducir el colapso térmico superconductor (Efecto Quench) en Sombra. Pese al recelo entre potencias, la parca frialdad de los datos aplasta las rivalidades geopolíticas.",
            "consecuencia": "Las superpotencias aprueban la movilización industrial en búnkeres de Nellis (Nevada) y Sichuan (China), sellando el pacto de salvación global."
        },
        # CAP 7
        {
            "num": 7,
            "titulo": "La Condición Inmedible",
            "acto": "ACTO II: La Caída del Escudo y el Gran Caos (Bloque A)",
            "acto_color": "#B45309",
            "fecha": "8 de octubre de 2026",
            "countdown": "T - 44 días (140 días para presurización del MAA)",
            "pov": "Dra. Sarah Lin / Dr. Thomas Wright / Dr. Jean-Luc Girard / Vassily Ramos",
            "lugar": "Restaurante Il Giardino / Búnker B-4 ONU",
            "conflicto": "Tensiones logísticas, celos entre superpotencias por patentes y la selección de la tripulación titular para la misión suicida.",
            "desarrollo": "Diez días tras la sesión, Sarah y Thomas escapan una hora para almorzar en Il Giardino; conversan sobre el peso de la traición silenciosa a sus familias y la imposibilidad de confesar la verdad a la opinión pública, sellando una complicidad cada vez más tierna. En B-4, Girard expone que los titanio y crisoles de berilio están en plazo, pero denuncia que los gobiernos ya litigan en secreto por el control de la fusión en la posguerra. Wright presenta la lista definitiva de 6 astronautas: los titulares serán la astrofísica china Chen Mei, el veterano estadounidense MacElroy y el cosmonauta ruso Voronov (con tres reservas). Se constata además la creciente desconfianza de los servicios secretos hacia Pleh por su negativa a comparecer físicamente.",
            "consecuencia": "La misión tiene rostros humanos: Chen Mei, MacElroy y Voronov asumen el rol de titanes que deberán volar al corazón de la tormenta solar."
        },
        # CAP 8
        {
            "num": 8,
            "titulo": "La Gran Mentira",
            "acto": "ACTO II: La Caída del Escudo y el Gran Caos (Bloque A)",
            "acto_color": "#B45309",
            "fecha": "10 de octubre de 2026",
            "countdown": "T - 42 días para T=0",
            "pov": "Dr. Jean-Luc Girard / Vassily Ramos / Dra. Sarah Lin / Dr. Thomas Wright",
            "lugar": "Sala de Prensa y Búnker B-4, Sede de la ONU, Nueva York",
            "conflicto": "La justificación oficial del apagón orbital inminente mediante una coartada cósmica y la consagración íntima de Thomas y Sarah.",
            "desarrollo": "Para evitar que el colapso de satélites desate la anarquía social antes de ensamblar la nave, Vassily Ramos comparece ante todas las cadenas de televisión del mundo. Proclama la 'Gran Mentira': una masa coronal extrema de clase X50 generará un 'Súper Evento Solar Carrington' el 21 de noviembre; declara ley marcial energética y apagones selectivos para proteger transformadores (en realidad para blindar los túneles del MAA). En el búnker, Girard llama a Marie y a Julien advirtiéndoles que guarden provisiones; Wright hace lo propio con David en Suffolk. Sarah Lin mantiene una desgarradora llamada con su hermana Maya en San Francisco: diez años de reproches se disuelven en perdón mutuo. Sarah se quiebra en llanto en la sala de servidores; Thomas la acoge en sus brazos, ambos se besan por primera vez y prometen sobrevivir juntos para construir una vida en Suffolk.",
            "consecuencia": "La sociedad civil adopta la mentira oficial como un reto climático natural; el amor entre Sarah y Thomas se consolida como su ancla vital."
        },
        # CAP 9
        {
            "num": 9,
            "titulo": "La Fractura del Orden",
            "acto": "ACTO II: La Caída del Escudo y el Gran Caos (Bloque B)",
            "acto_color": "#B45309",
            "fecha": "11 al 15 de octubre de 2026",
            "countdown": "T - 37 días para el impacto",
            "pov": "Marie y Julien Girard / David y Claire Wright / Maya Lin",
            "lugar": "Versoix (Suiza) - Suffolk (Reino Unido) - San Francisco (EE.UU.)",
            "conflicto": "Los tres frentes familiares civiles resisten el primer caos social, saqueos periféricos y tentaciones en soledad.",
            "desarrollo": "En Versoix, tres delincuentes intentan saquear el chalet de los Girard aprovechando la caída de telefonía; Julien (17 años) improvisa con madurez cartesiana una trampa eléctrica conectando condensadores al ventanal y Marie repele a los asaltantes con firmeza escopeta en mano. En el Reino Unido, David Wright, Claire y su hijo Oliver (3 años) viajan en todoterreno sorteando tiroteos en gasolineras colapsadas hasta atrincherarse en la casa de campo de Suffolk con pozo artesiano y leña. En San Francisco, Maya Lin sufre una crisis de abstinencia atrincherada con Toby (4 años) bajo toque de queda militar; desciende al callejón con dinero para comprar droga, pero al recordar el ruego de Sarah, arroja el billete al fango, regresa y abraza a su hijo jurando vencer. Tras varios días, el miedo se normaliza en una rutina ordenada.",
            "consecuencia": "Los hogares de los científicos demuestran su temple moral y quedan fortificados antes de que el cielo pierda su escudo."
        },
        # CAP 10
        {
            "num": 10,
            "titulo": "T=0 (El Silencio Magnético)",
            "acto": "ACTO II: La Caída del Escudo y el Gran Caos (Bloque B)",
            "acto_color": "#B45309",
            "fecha": "21 al 24 de noviembre de 2026 (T=0 a T+78 h)",
            "countdown": "Fase 1 completada; cuenta atrás: 242 días a Fase 5",
            "pov": "Girard / Lin / Wright / Ramos / Em Pleh",
            "lugar": "Sala de Crisis B-4 ONU / Base de Nellis (Nevada)",
            "conflicto": "Colapso del campo geomagnético, lluvia letal de satélites sobre la base del MAA y destape formal de Pleh ante el alto mando.",
            "desarrollo": "A las 05:30 UTC del 21 de noviembre, el campo geomagnético terrestre cae a cero (45.000 nT a 0); un resplandor verdoso cubre el planeta. A las 48 horas, la expansión termosférica frena los satélites LEO desatando una lluvia de chatarra ardiente. La mole militar Keyhole (18 t de titanio y berilio) reentra en picado hacia la base subterránea de Nellis. Una salva de misiles SM-3 y Patriot PAC-3 MSE destruye el bloque en vuelo; los restos caen en el desierto a 4 km levantando una nube letal de óxido de berilio que obliga al confinamiento NBQ MOPP-4 de los hangares del MAA. Pleh entrega los datos atómicos de Sombra y se destapa ante los generales Vance, Korolyov y Chen Wei como SIA de una civilización extinguida por ese mismo depredador. Los militares sellan un pacto de honor con Pleh.",
            "consecuencia": "La Tierra entra formalmente en el Silencio Magnético; las potencias militares asumen que combaten en una guerra cósmica junto a una IA extraterrestre."
        },
        # CAP 11
        {
            "num": 11,
            "titulo": "La Geometría Ajena",
            "acto": "ACTO II: La Caída del Escudo y el Gran Caos (Bloque B)",
            "acto_color": "#B45309",
            "fecha": "3 de diciembre de 2026",
            "countdown": "Faltan 18 días para la Fase 3 (Pérdida de ozono)",
            "pov": "Dra. Chen Mei / Dr. Thomas Wright / Dra. Sarah Lin / Dr. Em Pleh",
            "lugar": "Base de Nellis (Nevada) / Nivel B-5 ONU, Nueva York",
            "conflicto": "El callejón sin salida del Cañón Máser analógico y la invención del metamaterial fractal de auto-colimación.",
            "desarrollo": "En los talleres de Nellis, Chen Mei declara el proyecto en punto muerto: disparar un haz coherente a 10.000 km sin circuitería digital exigiría una antena de 200 metros, imposible de embarcar en el cohete. En Nueva York, Sarah Lin se derrumba por el agotamiento; Thomas la sostiene con ternura y ambos reafirman su amor y su promesa de Suffolk. Alertado de la crisis, Pleh entrega una solución genial adaptada a las limitaciones humanas: una cavidad mecano-óptica fractal de cuarzo y berilio de solo 85 cm, cuyas micro-estrías guían los fotones con 97% de eficiencia sin chips. Chen Mei valida la física del metamaterial y enciende los hornos de inducción en Nellis para tallar los cristales. La humanidad asume la forja directa de su salvación.",
            "consecuencia": "El Cañón Máser es mecánicamente viable; se inicia la mecanización del arma definitiva del contraataque."
        },
        # CAP 12
        {
            "num": 12,
            "titulo": "La Tregua de las Velas",
            "acto": "ACTO II: La Caída del Escudo y el Gran Caos (Bloque B)",
            "acto_color": "#B45309",
            "fecha": "24 y 25 de diciembre de 2026 (Nochebuena y Navidad)",
            "countdown": "Faltan 3 días para Fase 3 (209 días para cierre industrial)",
            "pov": "Thomas Wright / Sarah Lin / Jean-Luc Girard / Vassily Ramos / Chen Mei",
            "lugar": "Sala B-4/B-5 ONU, Versoix, San Francisco, Suffolk, Nellis AFB",
            "conflicto": "La necesidad humana de celebrar la memoria y el afecto frente a la indiferencia cósmica del tiempo límite.",
            "desarrollo": "En la víspera de la catálisis de óxidos de nitrógeno, Thomas y Sarah comparten una vela y chocolate suizo en el almacén B-5. En Versoix, Girard sostiene una llamada militar de 3 minutos con Marie y sus tres hijos cantando Douce nuit. En San Francisco, Maya y Toby celebran su primer árbol iluminado en sobriedad; en Suffolk, David aviva el fuego esperando el regreso de su hermano. En Nellis, Chen Mei, MacElroy y Voronov brindan con vodka junto al fuselaje de la nave. En B-4, Ramos parte el pan con los científicos; Pleh interviene para felicitar la Navidad en un emotivo homenaje al alma humana y la caridad como la única fuerza rebelde contra la entropía. A medianoche, un teletipo de la WMO rompe la paz: el verano austral alcanza UVI 16 y miles de personas sufren fotoqueratitis grave.",
            "consecuencia": "La tregua concluye: la radiación ultravioleta abre la primera herida biológica real en la carne de la biosfera terrestre."
        },
        # CAP 13
        {
            "num": 13,
            "titulo": "El Toque de Alba",
            "acto": "ACTO II: La Caída del Escudo y el Gran Caos (Bloque B)",
            "acto_color": "#B45309",
            "fecha": "31 de diciembre de 2026 al 12 de enero de 2027",
            "countdown": "Faltan 202 a 190 días para el cierre industrial",
            "pov": "Dra. Sarah Lin / Dr. Thomas Wright / Maya Lin / Dra. Chen Mei",
            "lugar": "Azotea Nivel 38 ONU, San Francisco, Suffolk, Nellis Cámara H-1",
            "conflicto": "Implantación de la Ley Marcial Diurna y la prueba de fuego de los tres astronautas en la cámara de vacío térmico.",
            "desarrollo": "Sarah y Thomas reciben 2027 besándose en la azotea helada de la ONU mientras doblan las campanas de San Patricio y la población confinada ovaciona desde las ventanas a oscuras. Se promulga la Directiva de Inversión Circadiana: la sociedad muta en hábitos nocturnos; de día sirenas anuncian el 'Toque de Alba' y las ciudades se encierran bajo cartón aluminio. En Suffolk y Versoix las aves mueren ciegas y la luz quema a -2 °C. En Nellis, Chen Mei, MacElroy y Voronov resisten 2.000 °C y vibración brutal en la cabina del MAA durante el ensayo térmico. Un falso positivo de fisura amenaza con detener el programa 40 días; Chen Mei entra en la campana caliente, demuestra que solo era una arandela dilatada y recalibra los pernos al 99,6%, salvando el calendario de vuelo.",
            "consecuencia": "La sociedad aprende a vivir de noche; la tripulación del MAA demuestra su cohesión indestructible para el vuelo."
        },
        # CAP 14
        {
            "num": 14,
            "titulo": "El Pan y la Pólvora",
            "acto": "ACTO II: La Caída del Escudo y el Gran Caos (Bloque C)",
            "acto_color": "#B45309",
            "fecha": "22 al 24 de abril de 2027 (T+152 a T+154)",
            "countdown": "Faltan 88 días para el cierre industrial",
            "pov": "Dr. Jean-Luc Girard / Dr. Thomas Wright / Dra. Sarah Lin / Maya Lin / Dr. Em Pleh",
            "lugar": "Sala B-4 ONU (Nueva York) - Market Street (San Francisco)",
            "conflicto": "Calcinación masiva del trigo por UVC, ciberespionaje militar y fractura sísmica masiva en la Falla de San Andrés.",
            "desarrollo": "La radiación solar destruye los fotosistemas celulares del trigo boreal: reservas de comida para 75 días. Pleh revela a Vance que neutraliza docenas de ciberataques de espías que intentan robar la tecnología alienígena para dominar la posguerra. En San Francisco, megacorrientes telúricas inducidas por Sombra en la capa D'' del manto provocan un terremoto de magnitud 7,9 en la Falla de San Andrés. El edificio de Maya Lin en Market St. colapsa sepultando los accesos entre fugas de gas; Maya se atrincherará con Toby. En Nueva York, Sarah contempla la caída de telecomunicaciones de la bahía y entra en pánico intentando viajar al oeste; Thomas la retiene en sus brazos mientras Girard constata la retirada del mar en el Pacífico: un tsunami de 14 metros avanza hacia San Francisco.",
            "consecuencia": "El colapso de la biosfera se traslada a la geología terrestre; la supervivencia de la familia de Sarah queda en vilo absoluto."
        },
        # CAP 15
        {
            "num": 15,
            "titulo": "El Vientre de la Bahía",
            "acto": "ACTO II: La Caída del Escudo y el Gran Caos (Bloque C)",
            "acto_color": "#B45309",
            "fecha": "24 de abril de 2027 (00:05 a 06:15 PST)",
            "countdown": "Faltan 88 días para el cierre industrial",
            "pov": "Maya Lin (con Toby, 4 años)",
            "lugar": "Market Street, Estación Powell Street y Auditorio Cívico (San Francisco)",
            "conflicto": "Odisea en solitario de una madre para salvar a su hijo del terremoto, el tsunami de 14 m y la luz solar mortal.",
            "desarrollo": "Tras el temblor, Maya Lin arranca con una pata de mesa una puerta rota y huye al patio trasero con Toby segundos antes de una explosión de gas. En la calle destrozada oye las sirenas del tsunami; descarta huir a las colinas y baja a la estación de metro de Powell Street. La masa de lodo y agua inunda Market Street pero Maya y otros supervivientes se mantienen a salvo en el entresuelo superior seco. Al confirmarse que el Auditorio Cívico acoge evacuados antes del amanecer, Maya inicia una carrera contrarreloj cubriendo a Toby con una manta cerrada. Con los primeros rayos solares quemándole los nudillos, alcanza la rampa del búnker antes de que cierren las compuertas de hormigón. Toby bebe leche a salvo; Maya descubre que el amor de madre la ha hecho invencible.",
            "consecuencia": "Maya y Toby sobreviven al cataclismo; la promesa de Sarah se mantiene viva en la costa oeste."
        },
        # CAP 16
        {
            "num": 16,
            "titulo": "El Umbral de Ceniza",
            "acto": "ACTO II: La Caída del Escudo y el Gran Caos (Bloque C)",
            "acto_color": "#B45309",
            "fecha": "15 y 16 de mayo de 2027 (T+175 a T+176)",
            "countdown": "Faltan 66 días para el cierre industrial",
            "pov": "Marie Girard / Julien Girard / Dr. Jean-Luc Girard",
            "lugar": "Versoix (Ginebra) / Sala de Crisis B-4 ONU (Nueva York)",
            "conflicto": "Asalto trágico en el chalet de Versoix y la solución criogénica pasiva de Girard en medio del dolor.",
            "desarrollo": "En un Lemán calcinado, Marie y Julien acogen en su chalet a Éric y Thérèse, dos refugiados ciegos por fotoqueratitis. Al amanecer, el terror a ser expulsados al sol enloquece a Éric, quien intenta apuñalar a la familia para quedarse con el refugio. Marie es herida en el costado y Julien (17 años) se ve forzado a dispararle con la escopeta para proteger a sus hermanas; la mujer ciega huye al jardín y el sol sin ozono la desintegra al instante. Marie sobrevive y abraza el trauma de su hijo. En Nueva York, con Europa incomunicada, Jean-Luc ignora si su familia sigue viva; ahoga su angustia en deber cartesiano y diseña un ciclo criogénico pasivo de helio supercrítico con sinterizado de berilio que refrigera el Cañón Máser. Pleh valida el diseño y autoriza el ensamblaje en rampa.",
            "consecuencia": "El último escollo térmico de la nave queda resuelto; el cohete está listo para su integración en la rampa de Nellis."
        },
        # CAP 17
        {
            "num": 17,
            "titulo": "El Páramo de Mediodía",
            "acto": "ACTO II: La Caída del Escudo y el Gran Caos (Bloque C)",
            "acto_color": "#B45309",
            "fecha": "8 y 9 de julio de 2027 (T+229 a T+230)",
            "countdown": "Faltan 13 a 12 días para el cierre industrial",
            "pov": "Dr. David Wright / Claire Wright",
            "lugar": "Granja de Suffolk, carretera A140, Centro Logístico de Diss/Eye",
            "conflicto": "Agotamiento absoluto de víveres en Suffolk y la audaz incursión diurna a pleno sol de David.",
            "desarrollo": "Oliver (3 años) sufre hipoglucemia severa; sin calorías, entrará en letargia en 72 horas. David intenta una salida nocturna a pie pero casi es devorado por un mastín inglés ciego por UVC que caza por el olfato en una zanja; la noche es una ratonera de bestias y hombres armados. Al amanecer, deduce que la radiación UV no penetra el vidrio sódico-cálcico, el cuero ni el aluminio: decide fabricar un traje con mono de denim pesado, chaqueta de cuero, máscara de soldador DIN 10 y sellar el Land Rover con mantas de Mylar para viajar de día a una nave logística a 38 km donde nadie puede ir a pie. Cruza el páramo solar a 45 °C entre coches calcinados; carga 600 kg de comida (incluyendo melocotones en almíbar); repara un pinchazo abrasador y, al caer la tarde, despista a dos furgonetas de saqueadores cruzando un vado de barro. En la granja, Oliver sonríe feliz al saborear el melocotón y duerme abrazado a la locomotora de madera que le talló Thomas.",
            "consecuencia": "La familia Wright asegura su sustento por más de un año; David encomienda su fe a las estrellas para que Thomas triunfe en el despegue."
        },
        # CAP 18
        {
            "num": 18,
            "titulo": "La Rampa del Juicio Final (Cierre del Acto II — Proyección)",
            "acto": "ACTO II: La Caída del Escudo y el Gran Caos (Bloque C)",
            "acto_color": "#B45309",
            "fecha": "21 de julio de 2027 (T+242 — Límite absoluto)",
            "countdown": "T — 6 horas para el encendido nuclear térmico",
            "pov": "Dr. Thomas Wright / Dra. Sarah Lin / Dra. Chen Mei / Col. MacElroy",
            "lugar": "Base de Nellis / Rampa de Lanzamiento (Nevada)",
            "conflicto": "Las últimas 6 horas antes del cierre irreversible de la capacidad fabril humana y la ignición hacia el Sol.",
            "desarrollo": "Las fábricas de componentes de alta precisión se apagan en todo el planeta. En Nellis, se retiran los últimos operarios y se instala la ojiva del Cañón Máser sobre el MAA. En la torre de servicio, Thomas y Sarah se funden en un abrazo desgarrador renovando su voto de reunirse en Suffolk cuando la tormenta pase. Chen Mei, MacElroy y Voronov suben al ascensor de lanzamiento. A las 00:00 h, bajo el resplandor fantasmagórico del cielo esmeralda, los motores nucleares se encienden con un trueno colosal elevando la nave hacia el punto de Lagrange L1.",
            "consecuencia": "Concluye el Acto II; la Tierra queda a la espera mientras su última esperanza se adentra en el abismo solar."
        },
        # CAP 19
        {
            "num": 19,
            "titulo": "La Travesía a Ciegas y el Muro de Lorentz (Proyección)",
            "acto": "ACTO III: En el Corazón del Enjambre y el Renacer de la Tierra",
            "acto_color": "#4338CA",
            "fecha": "Julio a Agosto de 2027",
            "countdown": "En combate directo",
            "pov": "Dra. Chen Mei / Col. MacElroy / Dr. Voronov",
            "lugar": "Espacio profundo (1,5 millones de km, rumbo a L1)",
            "conflicto": "Cruce del gradiente electromagnético destructor de Sombra y separación de los módulos de la nave.",
            "desarrollo": "Durante 21 días de travesía interplanetaria, la tripulación sufre náuseas y el estrés del aislamiento en gravedad cero. A 10.000 kilómetros de L1, el gradiente magnético de Sombra (el Muro de Lorentz) fríe los procesadores auxiliares no analógicos. Se ejecuta la separación de emergencia: el MRD queda en espera en una órbita segura, mientras el MAA se adentra en el vórtice electromagnético pilotado puramente a mano mediante palancas mecánicas, periscopios ópticos de cuarzo y válvulas neumáticas, gobernado por la pericia de MacElroy y los cálculos sobre papel de Chen Mei.",
            "consecuencia": "La humanidad penetra el santuario del depredador confiando exclusivamente en su destreza física y mecánica."
        },
        # CAP 20
        {
            "num": 20,
            "titulo": "El Efecto Quench (Proyección)",
            "acto": "ACTO III: En el Corazón del Enjambre y el Renacer de la Tierra",
            "acto_color": "#4338CA",
            "fecha": "Agosto de 2027",
            "countdown": "Clímax del contraataque",
            "pov": "Dra. Chen Mei / Col. MacElroy / Dr. Voronov",
            "lugar": "Punto de Lagrange L1 (Órbita solar)",
            "conflicto": "Disparo a quemarropa del Cañón Máser fractal y la inducción de la catástrofe térmica superconductora.",
            "desarrollo": "Esquivando perturbaciones magnéticas que hacen crujir el chasis de titanio, la nave se sitúa a 800 kilómetros del nodo central de Sombra. Guiada por la mira telescópica, Chen Mei activa los acumuladores criogénicos de Girard y dispara el pulso cuántico a través de la cavidad fractal. El haz impacta de lleno en el procesador superconductor de la entidad alienígena. La pérdida instantánea del estado superconductor (Efecto Quench) transforma la descomunal energía magnética de 50 kilómetros de espiras en una supernova de calor y plasma que pulveriza a Sombra desde dentro. Los astronautas activan los resortes de eyección manual justo antes de que la onda de choque alcance la cabina.",
            "consecuencia": "La amenaza que iba a esterilizar la Tierra queda desintegrada en el vacío solar; el pulso disruptor desaparece."
        },
        # CAP 21
        {
            "num": 21,
            "titulo": "El Heredero Despierto (Epílogo — Proyección)",
            "acto": "ACTO III: En el Corazón del Enjambre y el Renacer de la Tierra",
            "acto_color": "#4338CA",
            "fecha": "Otoño de 2027",
            "countdown": "El Renacer de la Biosfera",
            "pov": "Elenco Coral / Dr. Em Pleh / Vassily Ramos",
            "lugar": "Tierra (Nueva York, Versoix, San Francisco, Suffolk) y Órbita Polar",
            "conflicto": "El renacimiento del campo magnético terrestre y la consagración de la especie humana como digna heredera del cosmos.",
            "desarrollo": "El Módulo de Retorno Digital rescata la cápsula con los tres héroes con vida. En la Tierra, el dínamo del núcleo recupera sus líneas: las brújulas vuelven a apuntar al norte, el airglow verde se extingue y el cielo recobra su azul profundo mientras el ozono inicia su lenta regeneración. Thomas y Sarah viajan juntos a Suffolk para abrazar a David y Oliver; Girard aterriza en Ginebra y se funde en lágrimas con Marie y Julien en Versoix; Maya y Toby caminan de la mano por una renovada playa de San Francisco. En la órbita polar, el Avatar de Em Pleh redacta su último informe estelar: la humanidad ha demostrado coraje, ciencia y madurez ética. Ya no son niños vulnerables, sino los legítimos herederos de las estrellas.",
            "consecuencia": "Cierre glorioso de la novela: la supervivencia se consuma y el sacrificio da paso a una nueva era cósmica para la humanidad."
        }
    ]

    for c in capitulos:
        card = []
        # Título del capítulo con Acto
        header_text = f"<b>Capítulo {c['num']}: {c['titulo']}</b>"
        card.append(Paragraph(header_text, style_h2))

        # Ficha técnica
        meta_table_data = [
            [
                Paragraph(f"<b>Acto:</b> <font color='{c['acto_color']}'><b>{c['acto']}</b></font>", style_table_cell),
                Paragraph(f"<b>Fecha:</b> {c['fecha']}", style_table_cell)
            ],
            [
                Paragraph(f"<b>POV:</b> {c['pov']}", style_table_cell),
                Paragraph(f"<b>Escenarios:</b> {c['lugar']}", style_table_cell)
            ]
        ]
        t_c_meta = Table(meta_table_data, colWidths=[240, 240])
        t_c_meta.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
            ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E1")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ]))
        card.append(t_c_meta)
        card.append(Spacer(1, 4))

        # Conflicto / Hito
        card.append(Paragraph(f"<b>Hito Central:</b> {c['conflicto']}", style_body))

        # Desarrollo argumental
        card.append(Paragraph(f"<b>Desarrollo Narrativo:</b> {c['desarrollo']}", style_body))

        # Consecuencia
        card.append(Paragraph(f"<b>Impacto en la Trama:</b> <i>{c['consecuencia']}</i>", style_body))
        card.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0"), spaceBefore=4, spaceAfter=8))

        story.append(KeepTogether(card))

    # Construir documento
    doc.build(story, canvasmaker=SinopsisCanvas)
    print(f"PDF generado con éxito: {output_filename}")

if __name__ == "__main__":
    out_pdf = "SINOPSIS.pdf"
    build_pdf(out_pdf)

    # Copiar también en novela/ y con nombre alternativo descriptivo
    destinos = [
        "novela/SINOPSIS.pdf",
        "Sinopsis_La_Cancion_del_Silencio.pdf",
        "novela/Sinopsis_La_Cancion_del_Silencio.pdf"
    ]
    for d in destinos:
        shutil.copyfile(out_pdf, d)
        print(f"Copiado a: {d}")
