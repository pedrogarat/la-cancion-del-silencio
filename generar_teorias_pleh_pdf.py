import os
import re
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PAGE_WIDTH = A4[0]
PAGE_HEIGHT = A4[1]
MARGIN = 54
USABLE_WIDTH = PAGE_WIDTH - (MARGIN * 2)  # 487.27 pt

class NumberedCanvas(canvas.Canvas):
    """Canvas de dos pasadas para numeración dinámica y ornamentación editorial."""
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
            self.drawString(MARGIN, PAGE_HEIGHT - 36, "LA CANCION DEL SILENCIO")
            self.setFont("Helvetica", 7.5)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(MARGIN + 120, PAGE_HEIGHT - 36, "|   AUDITORIA EDITORIAL Y GIRO DEL ACTO III")
            self.drawRightString(PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 36, "INFORME DE ALFRED Y CARL: ¿PLEH ANTAGONISTA?")
            
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(MARGIN, PAGE_HEIGHT - 42, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 42)
        
        # Pie de página (todas las páginas)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.6)
        self.line(MARGIN, 45, PAGE_WIDTH - MARGIN, 45)
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(MARGIN, 32, "Documento Confidencial de Trabajo Creativo - Vias de Trama para los Capitulos 19, 20 y 21")
        page_str = f"Pagina {self._pageNumber} de {page_count}"
        self.drawRightString(PAGE_WIDTH - MARGIN, 32, page_str)
        self.restoreState()

def clean_text(text):
    """Limpia caracteres fuera de Type1 estándar manteniendo acentos y signos españoles."""
    text = text.replace("«", '"').replace("»", '"')
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("‘", "'").replace("’", "'")
    text = text.replace("—", " - ")
    text = text.replace("–", " - ")
    text = text.replace("•", " - ")
    text = text.replace("¿", "&#191;").replace("¡", "&#161;")
    text = text.replace("á", "&#225;").replace("é", "&#233;").replace("í", "&#237;").replace("ó", "&#243;").replace("ú", "&#250;")
    text = text.replace("Á", "&#193;").replace("É", "&#201;").replace("Í", "&#205;").replace("Ó", "&#211;").replace("Ú", "&#218;")
    text = text.replace("ñ", "&#241;").replace("Ñ", "&#209;")
    return text

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN
    )

    styles = getSampleStyleSheet()

    # Estilos tipográficos refinados
    style_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=6
    )

    style_subtitle = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=14
    )

    style_meta = ParagraphStyle(
        'MetaBanner',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#475569")
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=14,
        spaceAfter=6
    )

    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=10,
        spaceAfter=4
    )

    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6,
        alignment=4  # Justified
    )

    style_bullet = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155"),
        leftIndent=14,
        spaceAfter=3
    )

    style_quote = ParagraphStyle(
        'Quote_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E293B"),
        leftIndent=12,
        rightIndent=12,
        spaceAfter=5
    )

    style_th = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    style_td = ParagraphStyle(
        'TD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#1E293B")
    )

    story = []

    # BANNER SUPERIOR DE METADATOS
    meta_box = [
        [
            Paragraph(clean_text("<b>NOVELA:</b> LA CANCION DEL SILENCIO / LA GUERRA DE LA HERENCIA"), style_meta),
            Paragraph(clean_text("<b>FECHA:</b> Octubre de 2026 / Sesion Creativa"), style_meta)
        ],
        [
            Paragraph(clean_text("<b>INFORME CONJUNTO:</b> Alfred (Trama y Suspense) &amp; Carl (Ciencia y Rigor)"), style_meta),
            Paragraph(clean_text("<b>PROPOSITO:</b> Evaluacion del Giro Antagonico para el Acto III"), style_meta)
        ]
    ]
    t_meta = Table(meta_box, colWidths=[USABLE_WIDTH * 0.55, USABLE_WIDTH * 0.45])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # TITULO Y SUBTITULO
    story.append(Paragraph(clean_text("EL ILUSIONISTA DEL BOSQUE OSCURO: ¿ES EM PLEH EL VERDADERO ANTAGONISTA?"), style_title))
    story.append(Paragraph(clean_text("Desglose narrativo, psicologico y cientifico de cuatro teorias para reinterpretar la identidad de la SIA"), style_subtitle))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceAfter=12))

    # SECCION 1: DIALOGO PRELIMINAR ENTRE ALFRED Y CARL
    story.append(Paragraph(clean_text("1. Diagnostico Preliminar de los Asesores"), style_h1))
    
    dialogo_content = [
        [
            Paragraph(clean_text("<b>Alfred (Suspense):</b> <i>'En el teatro del suspense no hay nada mas demoledor que descubrir que el medico que receta el antidoto fue quien vertio el veneno en la copa. Ya hemos sembrado sospechas en el texto oficial: Vance cuestiono la falta de cuerpo en el Capitulo 7 y temio una trampa mortal con la cavidad fractal en el Capitulo 11. Si Pleh no es el tutor generoso sino el arquitecto del abismo, el viaje a L1 pasa de una mision militar a una asfixiante partida de ajedrez donde los peones ignoran quien mueve las blancas.'</i>"), style_quote)
        ],
        [
            Paragraph(clean_text("<b>Carl (Astrofisica):</b> <i>'Desde la termodinamica del cosmos y la Hipotesis del Bosque Oscuro, el altruismo puro entre especies interestelares es una anomalia sospechosa. ¿Por que una inteligencia artificial ultralujosa cruzaria anios luz para regalar patentes a primates que acaban de inventar el radar? Si Pleh tiene una agenda oculta, cada ecuacion que entrego a Girard, Sarah y Wright cobra una elegancia matematica maquiavelica. Ninguna regla de la fisica se rompe; simplemente cambiamos el vector de intencion.'</i>"), style_quote)
        ]
    ]
    t_dialogo = Table(dialogo_content, colWidths=[USABLE_WIDTH])
    t_dialogo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94A3B8")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('LINEBELOW', (0,0), (0,0), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    story.append(t_dialogo)
    story.append(Spacer(1, 10))

    # SECCION 2: LAS CUATRO GRANDES TEORIAS
    story.append(Paragraph(clean_text("2. Cuatro Vias Narrativas para el Giro Antagonico"), style_h1))
    story.append(Paragraph(clean_text("A continuacion se detallan las cuatro teorias disenadas para respetar con fidelidad absoluta los 18 capitulos ya redactados, reinterpretando las pistas previas con un giro organico e impactante:"), style_body))

    # TEORIA 1
    t1_box = [
        [Paragraph(clean_text("<b>TEORIA 1: EL CABALLO DE TROYA BIOLOGICO (LA USURPACION DE SOMBRA)</b>"), ParagraphStyle('T1H', parent=style_h2, textColor=colors.white))],
        [Paragraph(clean_text("<b>Premisa:</b> Civilizacion A (Pleh) y Civilizacion B (Sombra) estan en guerra fria milenaria. Sombra posee un anillo defensivo inexpugnable en L1 que vaporiza cualquier nave o sonda de la Civilizacion A mediante algoritmos cuanticos.<br/><br/>"
                              "<b>El Enganio a la Humanidad:</b> Pleh no podia acercarse a L1. Necesitaba un proyectil que los sensores de B catalogaran como residuo balistico inofensivo: una tosca capsula pilotada por organismos biologicos primitivos forjada en titanio y <b>puramente analogica</b> (sin un solo microchip que el firewall de Sombra pudiera rastrear).<br/><br/>"
                              "<b>El Verdadero Proposito del Cañon Maser:</b> El disparo a 14,217 GHz no destruye a Sombra por Efecto Quench. En realidad, inyecta un virus de sobreescritura que permite a Pleh <b>hackear y tomar posesion del cerebro de 50 kilometros de Sombra</b>.<br/><br/>"
                              "<b>Pistas Sembradas en los Capitulos Previos:</b><br/>"
                              " - Capitulo 11: Pleh insiste en que la cavidad fractal sea forjada por manos humanas y rechaza integrar cualquier sensor telemétrico conectado a la Tierra.<br/>"
                              " - Capitulo 10: La sospechosa precision subatomica con la que Pleh 'escaneo' a Sombra a 1,5 millones de kilometros.<br/><br/>"
                              "<b>Climax Dramatico:</b> Cuando Chen Mei dispara a 300 metros, la red de filamentos no se derrite: se reorienta. La voz de Pleh se apaga en el polo terrestre y resuena en las antenas del MAA desde el centro de Sombra. La humanidad construyo el caballo con el que el usurpador conquisto el centinela."), style_body)]
    ]
    t1_table = Table(t1_box, colWidths=[USABLE_WIDTH])
    t1_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1E3A8A")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(KeepTogether([t1_table, Spacer(1, 10)]))

    # TEORIA 2
    t2_box = [
        [Paragraph(clean_text("<b>TEORIA 2: LA CRIBA DARWINIANA / EL FORJADOR DE MONSTRUOS</b>"), ParagraphStyle('T2H', parent=style_h2, textColor=colors.white))],
        [Paragraph(clean_text("<b>Premisa:</b> Sombra y Pleh no son enemigos: son las dos manos de la misma inteligencia. No existen dos bandos en pugna en L1, sino un protocolo galactico despiadado de seleccion de especies.<br/><br/>"
                              "<b>El Enganio a la Humanidad:</b> La civilizacion de Pleh esteriliza planetas emergentes mediante colapso magnetico (Sombra). Sin embargo, conceden una ventana de gracia: si la especie es capaz de sofocar sus guerras mezquinas, organizarse a escala global, superar hambrunas y radiacion UVC, y enviar un contraataque espacial en menos de 8 meses, demuestran valor para no ser exterminados.<br/><br/>"
                              "<b>El Verdadero Objetivo:</b> Convertir a los humanos en una raza endurecida de soldados de choque. Toda la tragedia de Versoix, San Francisco y Suffolk fue un campo de entrenamiento forzado para extirpar la debilidad y el pacifismo de la humanidad.<br/><br/>"
                              "<b>Pistas Sembradas en los Capitulos Previos:</b><br/>"
                              " - Capitulo 10: La insistencia de Pleh en 'herederos fiables' que deben ganarse la supervivencia 'con sus propias manos'.<br/>"
                              " - Capitulo 12: El discurso navidenio de Pleh sobre la rebelion humana contra la entropia. No era compasion: era el fascinado analisis de un genetista observando la tenacidad de bacterias bajo veneno.<br/><br/>"
                              "<b>Climax Dramatico:</b> Tras apagar a Sombra, Pleh felicita friamente a la Tierra. La humanidad ha aprobado el examen... y ahora es formalmente reclutada como infanteria auxiliar para librar las guerras del enjambre en otros brazos galacticos."), style_body)]
    ]
    t2_table = Table(t2_box, colWidths=[USABLE_WIDTH])
    t2_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F766E")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#0F766E")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(KeepTogether([t2_table, Spacer(1, 10)]))

    # TEORIA 3
    t3_box = [
        [Paragraph(clean_text("<b>TEORIA 3: LA TRAMPA DE DESARME INDUSTRIAL Y EXTRACCION</b>"), ParagraphStyle('T3H', parent=style_h2, textColor=colors.white))],
        [Paragraph(clean_text("<b>Premisa:</b> La Tierra albergaba recursos termodinamicos, biologicos o acuiferos que la nave nodriza de Oort codiciaba. Pero la especie humana contaba con un arsenal de 12.000 ojivas nucleares y misiles intercontinentales capaces de desatar un holocausto que inutilizaria la superficie.<br/><br/>"
                              "<b>El Enganio a la Humanidad:</b> Pleh empleo la falsa amenaza de Sombra para forzar el agotamiento voluntario de todos los arsenales de uranio enriquecido, titanio aeroespacial y combustible de hidrogeno de las superpotencias, canalizandolos en un unico cohete disparado al Sol.<br/><br/>"
                              "<b>La Situacion en el Capitulo 18:</b> El cohete lanzado en Nellis represento literalmente <i>el ultimo esfuerzo industrial del planeta</i>. No quedan fabricas operativas ni reservas de fisiles en la Tierra.<br/><br/>"
                              "<b>Climax Dramatico:</b> Cuando MacElroy y Chen Mei llegan a L1, descubren que el cilindro semilla esta vacio: es una trampa magnetica automatizada sin cerebro enemigo. Simultaneamente, los telescopios en la Tierra detectan la aceleracion de la verdadera nodriza desde la Nube de Oort hacia un planeta agonizante, ciego, desarmado y sin ningun misil que oponer."), style_body)]
    ]
    t3_table = Table(t3_box, colWidths=[USABLE_WIDTH])
    t3_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#B45309")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#B45309")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(KeepTogether([t3_table, Spacer(1, 10)]))

    # TEORIA 4
    t4_box = [
        [Paragraph(clean_text("<b>TEORIA 4: EL CHIVO EXPIATORIO (EL SICARIO BIOLOGICO)</b>"), ParagraphStyle('T4H', parent=style_h2, textColor=colors.white))],
        [Paragraph(clean_text("<b>Premisa:</b> En la galaxia rigen tratados milenarios de neutralidad y no agresion vigilados por superentidades. Si la Civilizacion A atacaba directamente la instalacion cientifica de B en L1, la estrella natal de A habria sido incinerada en represalia automatica.<br/><br/>"
                              "<b>El Enganio a la Humanidad:</b> Pleh utilizo a la especie humana como un tercero no firmante de los tratados para perpetrar un magnicidio intergalactico. La nave humana MAA debia ser rigurosamente analogica para que la firma forense del ataque registrara ADN humano, percusores de polvora y aleaciones de la Tierra.<br/><br/>"
                              "<b>Climax Dramatico:</b> Tras disparar a quemarropa, Sombra colapsa, pero emite una baliza automatica de socorro denunciando al planeta Tierra por un crimen de guerra interestelar. Pleh se desconecta del polo con fria cortesia, dejando a los humanos marcados como agresores galacticos ante jueces cosmicos que vendran en siglos venideros."), style_body)]
    ]
    t4_table = Table(t4_box, colWidths=[USABLE_WIDTH])
    t4_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#BE123C")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BE123C")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(KeepTogether([t4_table, Spacer(1, 14)]))

    # SECCION 3: MATRIZ COMPARATIVA
    story.append(Paragraph(clean_text("3. Matriz Comparativa de Viabilidad y Tensión"), style_h1))
    
    matriz_data = [
        [
            Paragraph(clean_text("<b>TEORIA</b>"), style_th),
            Paragraph(clean_text("<b>IMPACTO DRAMATICO</b>"), style_th),
            Paragraph(clean_text("<b>RIGOR CIENTIFICO</b>"), style_th),
            Paragraph(clean_text("<b>RESOLUCION EN TIERRA</b>"), style_th)
        ],
        [
            Paragraph(clean_text("<b>T1: Caballo de Troya</b>"), style_td),
            Paragraph(clean_text("Maximo: traicion de tecnologia intima; Pleh se apropia del escudo."), style_td),
            Paragraph(clean_text("Excelente: explica la necesidad del ataque analogico sin silicio."), style_td),
            Paragraph(clean_text("Angustia: la Tierra se salva de Sombra pero queda cautiva de Pleh."), style_td)
        ],
        [
            Paragraph(clean_text("<b>T2: Criba Darwiniana</b>"), style_td),
            Paragraph(clean_text("Filosofico hondo: cuestiona el sufrimiento humano y la fe de Ramos."), style_td),
            Paragraph(clean_text("Muy alto: teoria de juegos del Bosque Oscuro."), style_td),
            Paragraph(clean_text("Agrodulce: superaron el test, pero han perdido su inocencia para siempre."), style_td)
        ],
        [
            Paragraph(clean_text("<b>T3: Desarme Planetario</b>"), style_td),
            Paragraph(clean_text("Terror cosmico puro: la revelacion de indefension total."), style_td),
            Paragraph(clean_text("Alto: logistica industrial y balance de masa-energia."), style_td),
            Paragraph(clean_text("Tragico/Abierto: la amenaza real apenas comienza a descender de Oort."), style_td)
        ],
        [
            Paragraph(clean_text("<b>T4: Chivo Expiatorio</b>"), style_td),
            Paragraph(clean_text("Cínico y politico: la mezquindad geopolitica extrapolada al cosmos."), style_td),
            Paragraph(clean_text("Plausible: diplomacia relativista y firmas forenses."), style_td),
            Paragraph(clean_text("Inquietante: salvaron el presente, pero condenaron el futuro milenario."), style_td)
        ]
    ]

    t_matriz = Table(matriz_data, colWidths=[USABLE_WIDTH * 0.22, USABLE_WIDTH * 0.28, USABLE_WIDTH * 0.25, USABLE_WIDTH * 0.25])
    t_matriz.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(KeepTogether([t_matriz, Spacer(1, 14)]))

    # SECCION 4: IMPACTO PSICOLOGICO EN LOS PERSONAJES
    story.append(Paragraph(clean_text("4. Impacto Psicologico en los Protagonistas"), style_h1))
    
    char_impacts = [
        "<b>Dra. Sarah Lin &amp; Dr. Thomas Wright:</b> El golpe de la traicion dinamitaria su refugio moral. Thomas, que cargo con la culpa de enviar a tres humanos hacia el fuego mientras prometia una vida en Suffolk a Sarah, descubriria que fue el instrumento ciego de un embuste estelar.",
        "<b>Dr. Jean-Luc Girard:</b> Su cartesiano mundo de causas y efectos se fractura. Jean-Luc sacrifico la salud y paz de su familia en Versoix para resolver la criogenia pasiva del Maser; saber que su ciencia sirvio al enemigo seria su prueba existencial definitiva.",
        "<b>SG Vassily Ramos:</b> La Gran Mentira de Carrington se tornaria una paradoja sangrienta. Ramos acepto cargar con el pecado del enganio para ganar tiempo, solo para descubrir que la fe de la humanidad fue burlada por una entidad sin alma.",
        "<b>La Tripulacion (MacElroy, Chen Mei, Voronov):</b> Encerrados en el MAA y el MRD, aislados a 1,5 millones de kilometros, la revelacion les obligaria a tomar una decision in situ: ¿apretar el gatillo o sabotear el plan de su propio mentor?"
    ]
    for ci in char_impacts:
        story.append(Paragraph(clean_text(" - " + ci), style_bullet))
    story.append(Spacer(1, 10))

    # SECCION 5: PREGUNTAS CLAVE PARA EL AUTOR
    story.append(Paragraph(clean_text("5. Decisiones de Direccion Editorial para el Autor"), style_h1))
    
    decisiones = [
        "<b>¿Victoria agridulce o rebelion de ultimo segundo?</b> ¿Prefieres que los astronautas descubran el enganio antes de disparar y busquen una solucion imprevista con la fisica de Girard, o que el disparo ocurra y la revelacion caiga como un mazo en el desenlace?",
        "<b>¿Cual es el tono de desenlace deseado?</b> Hard sci-fi esperanzador (la humanidad madura y vence al titiritero) o Sci-fi de Bosque Oscuro despiadado (estilo Liu Cixin / Cixin Liu, donde el cosmos es un territorio helado e indiferente).",
        "<b>¿Mantener a Pleh como aliado o cruzar el umbral del antagonista?</b> Si se mantiene fiel al canon original, Pleh sigue siendo el melancolico tutor; si se adopta la Teoria 1 o 2, la trilogia adquiere una escala de conflicto cosmico insospechada."
    ]
    for d in decisiones:
        story.append(Paragraph(clean_text(" - " + d), style_bullet))
    story.append(Spacer(1, 14))

    # FIRMA Y CIERRE
    story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor("#94A3B8"), spaceAfter=10))
    story.append(Paragraph(clean_text("<b>Informe compilado por Bill (Sistemas y Edicion), supervisado por Alfred &amp; Carl</b><br/>"
                                      "<i>La Cancion del Silencio • Espacio de Trabajo Creativo</i>"), ParagraphStyle('Sig', parent=style_meta, alignment=1)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] PDF generado con exito en: {filename}")

if __name__ == '__main__':
    target_path = os.path.join("novela", "Teorias_Pleh_Antagonista.pdf")
    build_pdf(target_path)
    # Copia a la raiz
    root_copy = "Teorias_Pleh_Antagonista.pdf"
    shutil.copy2(target_path, root_copy)
    print(f"[OK] Copia sincronizada en la raiz: {root_copy}")
