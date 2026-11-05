import os
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable, PageBreak
)
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 36  # ~0.5 pulgadas
USABLE_WIDTH = PAGE_WIDTH - (MARGIN * 2)

class TitulosCanvas(canvas.Canvas):
    """Canvas de dos pasadas para numeración total, encabezados y pies de página."""
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
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        self.saveState()
        
        # Encabezado (páginas > 1)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 7.5)
            self.setFillColor(colors.HexColor("#0F172A"))
            self.drawString(MARGIN, PAGE_HEIGHT - 24, "LA CANCIÓN DEL SILENCIO • PROPUESTA DE TÍTULOS CORTOS")
            self.setFont("Helvetica", 7.5)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 24, "ACTOS, CAPÍTULOS Y APARTADOS (MÁX. 3 PALABRAS)")
            self.setStrokeColor(colors.HexColor("#0284C7"))
            self.setLineWidth(0.75)
            self.line(MARGIN, PAGE_HEIGHT - 28, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 28)
        
        # Pie de página
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(MARGIN, 28, PAGE_WIDTH - MARGIN, 28)
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(MARGIN, 18, "Auditoría de Nomenclatura Editorial • Criterio de Concisión (1-3 Palabras) • Pedro Garat & Antigravity")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(PAGE_WIDTH - MARGIN, 18, page_str)
        self.restoreState()

def clean(t):
    if not t: return ""
    return str(t).replace("«", '"').replace("»", '"').replace("—", "-").replace("–", "-")

def build_pdf(filename="Propuesta_Titulos_Cortos.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN
    )

    base = getSampleStyleSheet()

    # Estilos
    title_style = ParagraphStyle(
        'MainTitle',
        parent=base['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=2
    )

    sub_style = ParagraphStyle(
        'Subtitle',
        parent=base['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#0284C7"),
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=base['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body',
        parent=base['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#334155")
    )

    th_style = ParagraphStyle(
        'TH',
        parent=base['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white
    )

    td_elem = ParagraphStyle(
        'TDElem',
        parent=base['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor("#1E3A8A")
    )

    td_old = ParagraphStyle(
        'TDOld',
        parent=base['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor("#475569")
    )

    td_new = ParagraphStyle(
        'TDNew',
        parent=base['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#047857")
    )

    td_note = ParagraphStyle(
        'TDNote',
        parent=base['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=6.8,
        leading=8.5,
        textColor=colors.HexColor("#64748B")
    )

    story = []

    # Portadilla
    story.append(Paragraph("LA CANCIÓN DEL SILENCIO", title_style))
    story.append(Paragraph("PROPUESTA EDITORIAL DE NOMENCLATURA CONCISA (1 A 3 PALABRAS)", sub_style))

    # Caja de metadatos y justificación
    just_text = (
        "<b>Directriz del Autor:</b> Sustituir los títulos extensos y descriptivos de actos, capítulos y apartados "
        "por fórmulas sumamente concisas: preferiblemente <b>una palabra clave</b>, y como máximo <b>tres palabras</b>. "
        "Esta propuesta aporta un tono literario moderno, seco, cinematográfico y de alto impacto dramático, "
        "eliminando la sobreexplicación y potenciando el suspense."
    )
    t_just = Table([[Paragraph(just_text, body_style)]], colWidths=[USABLE_WIDTH])
    t_just.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_just)
    story.append(Spacer(1, 10))

    # =========================================================================
    # TABLA 1: ACTOS Y BLOQUES
    # =========================================================================
    story.append(Paragraph("1. ESTRUCTURA GLOBAL: ACTOS Y BLOQUES TEMÁTICOS", h1_style))
    
    actos_data = [
        [
            Paragraph("Nivel", th_style),
            Paragraph("Nombre Actual (Extenso)", th_style),
            Paragraph("Propuesta Concisa (1-2 Palabras)", th_style),
            Paragraph("Concepto / Resonancia", th_style)
        ],
        [
            Paragraph("<b>ACTO I</b>", td_elem),
            Paragraph("ACTO I: La Semilla y el Tejido Silencioso", td_old),
            Paragraph("<b>LA SEMILLA</b>", td_new),
            Paragraph("Génesis atómica y siembra tecnológica de Pleh.", td_note)
        ],
        [
            Paragraph("<b>ACTO II</b>", td_elem),
            Paragraph("ACTO II: La Caída del Escudo y el Gran Caos", td_old),
            Paragraph("<b>EL COLAPSO</b>", td_new),
            Paragraph("Muerte de la magnetosfera y caída de la civilización.", td_note)
        ],
        [
            Paragraph("Bloque II-A", td_elem),
            Paragraph("Movilización Encubierta y La Gran Mentira", td_old),
            Paragraph("<b>LA MENTIRA</b>", td_new),
            Paragraph("Decreto Alfa Cero y engaño global de Carrington.", td_note)
        ],
        [
            Paragraph("Bloque II-B", td_elem),
            Paragraph("Silencio Magnético y Toque de Alba", td_old),
            Paragraph("<b>LA OSCURIDAD</b>", td_new),
            Paragraph("El apagón, la lluvia de satélites y vida nocturna.", td_note)
        ],
        [
            Paragraph("Bloque II-C", td_elem),
            Paragraph("La Tierra Herida y el Despegue en Nellis", td_old),
            Paragraph("<b>EL ÉXODO</b>", td_new),
            Paragraph("Asedio climático, hambre, tsunami y partida del cohete.", td_note)
        ],
        [
            Paragraph("<b>ACTO III</b>", td_elem),
            Paragraph("ACTO III: La Falsa Victoria y la Canción del Silencio", td_old),
            Paragraph("<b>EL SILENCIO</b>", td_new),
            Paragraph("El duelo en L1, el engaño del granjero y la liberación.", td_note)
        ],
        [
            Paragraph("Bloque III-A", td_elem),
            Paragraph("En el Abismo Solar y la Victoria en L1", td_old),
            Paragraph("<b>EL DUELO</b>", td_new),
            Paragraph("Incursión ciega por el Muro de Lorentz y Quench.", td_note)
        ],
        [
            Paragraph("Bloque III-B", td_elem),
            Paragraph("La Máscara de los Héroes y la Verdad en el Desván", td_old),
            Paragraph("<b>LA AGUJA</b>", td_new),
            Paragraph("Retorno, coartada y revelación de la cinta en Suffolk.", td_note)
        ],
        [
            Paragraph("Bloque III-C", td_elem),
            Paragraph("La Conjuración y la Batalla Final", td_old),
            Paragraph("<b>EL ARPONAZO</b>", td_new),
            Paragraph("Pacto en Ginebra y caída del statite sobre el polo.", td_note)
        ]
    ]

    t_actos = Table(actos_data, colWidths=[65, 175, 125, 155])
    t_actos.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")])
    ]))
    story.append(t_actos)
    story.append(Spacer(1, 12))

    # =========================================================================
    # TABLA 2: LOS 25 CAPÍTULOS
    # =========================================================================
    story.append(Paragraph("2. TABLA COMPARATIVA DE LOS 25 CAPÍTULOS", h1_style))

    capitulos_data = [
        [
            Paragraph("Cap.", th_style),
            Paragraph("Título Actual (Extenso)", th_style),
            Paragraph("Propuesta Concisa (1-3 palabras)", th_style),
            Paragraph("Palabra Clave / Foco", th_style)
        ],
        [Paragraph("1", td_elem), Paragraph("El Amanecer de Alamogordo", td_old), Paragraph("<b>Alamogordo</b>", td_new), Paragraph("Detonación atómica Trinity.", td_note)],
        [Paragraph("2", td_elem), Paragraph("Los Tres Hilos del Ilusionista", td_old), Paragraph("<b>Tres Hilos</b>", td_new), Paragraph("CERN, MIT y ESA.", td_note)],
        [Paragraph("3", td_elem), Paragraph("La Sala Dos", td_old), Paragraph("<b>Sala Dos</b>", td_new), Paragraph("Convocatoria y revelación de Pleh.", td_note)],
        [Paragraph("4", td_elem), Paragraph("El Vértigo de las Naciones", td_old), Paragraph("<b>Alfa Cero</b>", td_new), Paragraph("Decreto secreto de la ONU.", td_note)],
        [Paragraph("5", td_elem), Paragraph("El Ancla Humana", td_old), Paragraph("<b>El Ancla</b>", td_new), Paragraph("Despedidas de las familias.", td_note)],
        [Paragraph("6", td_elem), Paragraph("La Cámara del Silencio", td_old), Paragraph("<b>El Consejo</b>", td_new), Paragraph("Sesión con los 15 embajadores.", td_note)],
        [Paragraph("7", td_elem), Paragraph("La Condición Inmedible", td_old), Paragraph("<b>Inmedible</b>", td_new), Paragraph("El factor ético y humano.", td_note)],
        [Paragraph("8", td_elem), Paragraph("La Gran Mentira", td_old), Paragraph("<b>Carrington</b>", td_new), Paragraph("Coartada cósmica oficial.", td_note)],
        [Paragraph("9", td_elem), Paragraph("La Fractura del Orden", td_old), Paragraph("<b>La Fractura</b>", td_new), Paragraph("Pánico civil y resistencia íntima.", td_note)],
        [Paragraph("10", td_elem), Paragraph("T=0 (El Silencio Magnético)", td_old), Paragraph("<b>T=0</b>", td_new), Paragraph("Colapso del campo magnético.", td_note)],
        [Paragraph("11", td_elem), Paragraph("La Geometría Ajena", td_old), Paragraph("<b>Geometría Ajena</b>", td_new), Paragraph("La cavidad fractal imposible.", td_note)],
        [Paragraph("12", td_elem), Paragraph("La Tregua de las Velas", td_old), Paragraph("<b>Nochebuena</b>", td_new), Paragraph("La vela de cera en el búnker.", td_note)],
        [Paragraph("13", td_elem), Paragraph("El Toque de Alba", td_old), Paragraph("<b>Toque de Alba</b>", td_new), Paragraph("Vida nocturna y huida del sol.", td_note)],
        [Paragraph("14", td_elem), Paragraph("El Pan y la Pólvora", td_old), Paragraph("<b>Hambre y Fuego</b>", td_new), Paragraph("Trigo calcinado y megasismo.", td_note)],
        [Paragraph("15", td_elem), Paragraph("El Vientre de la Bahía", td_old), Paragraph("<b>Market Street</b>", td_new), Paragraph("Tsunami y refugio subterráneo.", td_note)],
        [Paragraph("16", td_elem), Paragraph("El Umbral de Ceniza", td_old), Paragraph("<b>Ceniza</b>", td_new), Paragraph("Asedio y ceguera en Versoix.", td_note)],
        [Paragraph("17", td_elem), Paragraph("El Páramo de Mediodía", td_old), Paragraph("<b>El Páramo</b>", td_new), Paragraph("Incursión solar a 45 °C en Suffolk.", td_note)],
        [Paragraph("18", td_elem), Paragraph("La Rampa del Juicio Final", td_old), Paragraph("<b>La Rampa</b>", td_new), Paragraph("Despegue nuclear hacia L1.", td_note)],
        [Paragraph("19", td_elem), Paragraph("La Travesía a Ciegas y el Velo de Sombra", td_old), Paragraph("<b>Muro de Lorentz</b>", td_new), Paragraph("Penetración ciega en la malla.", td_note)],
        [Paragraph("20", td_elem), Paragraph("El Salmo de la Falsa Victoria", td_old), Paragraph("<b>Falsa Victoria</b>", td_new), Paragraph("Quench en L1 y martirio fingido.", td_note)],
        [Paragraph("21", td_elem), Paragraph("El Despertar del Azul", td_old), Paragraph("<b>Cielo Azul</b>", td_new), Paragraph("Regeneración de la capa de ozono.", td_note)],
        [Paragraph("22", td_elem), Paragraph("La Máscara de los Héroes y el Reencuentro del Hogar", td_old), Paragraph("<b>El Hogar</b>", td_new), Paragraph("Paz aparente y cinta en el relicario.", td_note)],
        [Paragraph("23", td_elem), Paragraph("La Aguja en el Desván", td_old), Paragraph("<b>El Desván</b>", td_new), Paragraph("Voz de Sombra y plan contra el pastor.", td_note)],
        [Paragraph("24", td_elem), Paragraph("La Conjuración del Silencio", td_old), Paragraph("<b>El Pacto</b>", td_new), Paragraph("Conspiración analógica en Ginebra.", td_note)],
        [Paragraph("25", td_elem), Paragraph("La Canción del Silencio", td_old), Paragraph("<b>La Canción</b>", td_new), Paragraph("Caída del Avatar y libertad cósmica.", td_note)]
    ]

    t_caps = Table(capitulos_data, colWidths=[28, 195, 125, 172])
    t_caps.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284C7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")])
    ]))
    story.append(t_caps)
    story.append(Spacer(1, 14))

    # =========================================================================
    # TABLA 3: PROPUESTA DE APARTADOS / ESCENAS (CAPÍTULO A CAPÍTULO)
    # =========================================================================
    story.append(Paragraph("3. DESGLOSE COMPLETO DE APARTADOS (1 AL 25)", h1_style))

    # Lista estructurada de apartados
    # formato: (cap_num, cap_nom_prop, [(sec_num, sec_old, sec_new)])
    apartados_master = [
        (1, "Alamogordo", [
            ("I", "La Torre bajo la Tormenta", "La Torre"),
            ("II", "El Humo de la Duda en el Búnker S-10.000", "El Búnker"),
            ("III", "El Sol de Medianoche", "El Destello"),
            ("IV", "El Despertar en la Nube de Oort", "Oort")
        ]),
        (2, "Tres Hilos", [
            ("I", "El Espectro Sucio de Ginebra", "Ginebra"),
            ("II", "El Fuego en la Botella de Boston", "Boston"),
            ("III", "El Fantasma de Darmstadt", "Darmstadt"),
            ("IV", "El Tejido de la Confianza", "El Señuelo")
        ]),
        (3, "Sala Dos", [
            ("I", "La Huella del Ermitaño", "La Espera"),
            ("II", "El Auditorio Silencioso", "Penumbra"),
            ("III", "El Rostro en la Pantalla y el Elogio Humano", "El Rostro"),
            ("IV", "La Caída del Velo y la Gran Pregunta", "La Entidad"),
            ("V", "La Amenaza Desconocida y el Vector L1", "Vector L1"),
            ("VI", "La Sentencia Silenciosa y el Vértigo de la Extinción", "Ocho Meses"),
            ("VII", "El Origen Revelado: 1945, Luz y el Avatar", "El Statite"),
            ("VIII", "La Respuesta de la Tierra", "El Arpón")
        ]),
        (4, "Alfa Cero", [
            ("I", "Del Hotel Millennium al East River", "East River"),
            ("II", "La Incredulidad del Secretario General", "Ramos"),
            ("III", "La Reunión de Crisis y la Verificación", "Confirmación"),
            ("IV", "El Mandato Extraordinario", "Alfa Cero")
        ]),
        (5, "El Ancla", [
            ("I", "El Almuerzo del Silencio", "Último Almuerzo"),
            ("II", "Las Voces al Otro Lado del Hilo", "Despedidas"),
            ("III", "El Retorno al Búnker", "La Puerta")
        ]),
        (6, "El Consejo", [
            ("I", "El Tablero de las Quince Voces", "Las Quince Voces"),
            ("II", "La Apertura del Abismo", "El Abismo"),
            ("III", "El Cronómetro de la Extinción", "El Cronómetro"),
            ("IV", "El Muro de Lorentz y el Desafío Analógico", "Muro de Lorentz")
        ]),
        (7, "Inmedible", [
            ("I", "La Burbuja de Cristal", "Culpa"),
            ("II", "La Herida Racional", "Girard"),
            ("III", "Las Variables Ocultas", "La Tripulación")
        ]),
        (8, "Carrington", [
            ("I", "La Transgresión del Relojero", "La Advertencia"),
            ("II", "El Falso Evento Carrington", "Cadena Mundial"),
            ("III", "El Peso de la Corona", "Soledad"),
            ("IV", "El Eco de las Familias", "El Éxodo"),
            ("V", "La Fractura y el Consuelo", "El Beso"),
            ("VI", "El Preludio del Caos", "Fe y Razón")
        ]),
        (9, "La Fractura", [
            ("I", "El Bastión de Versoix", "Versoix"),
            ("II", "La Ruta hacia el Este", "La Fuga"),
            ("III", "La Batalla de Market Street", "Market Street"),
            ("IV", "El Pulso de la Costumbre", "Normalidad")
        ]),
        (10, "T=0", [
            ("I", "La Cuenta de los Cinco Segundos", "Cuenta Atrás"),
            ("II", "La Bóveda Esmeralda y el Primer Freno", "Cielo Verde"),
            ("III", "El Enigma de la Noche y la Rueda Orbital", "La Órbita"),
            ("IV", "La Asimetría Austral y el Escudo Inadvertido", "Asimetría"),
            ("V", "La Noche de los Bólidos y el Asedio de Nellis", "Lluvia de Fuego"),
            ("VI", "El Silencio del Vacío y el Velo Rasgado", "La Máscara"),
            ("VII", "Epílogo: La Falsa Tregua y la Noche Esmeralda", "Noche Esmeralda")
        ]),
        (11, "Geometría Ajena", [
            ("I", "El Muro de la Longitud de Onda", "La Antena"),
            ("II", "En la Penumbra del Refugio", "La Promesa"),
            ("III", "El Diseño Imposible y la Sospecha", "Cavidad Fractal"),
            ("IV", "El Vértigo de la Fe", "Validación"),
            ("V", "El Pacto del Metal", "Los Hornos")
        ]),
        (12, "Nochebuena", [
            ("I", "El Chocolate y la Promesa de Suffolk", "Chocolate"),
            ("II", "La Silla Vacía de Versoix", "Noche de Paz"),
            ("III", "Dos Luces en la Noche: Market Street y Suffolk", "Dos Hogares"),
            ("IV", "El Brindis de los Tres en Nellis", "El Brindis"),
            ("V", "La Mesa de B-4: El Amor frente a la Máquina", "La Cena"),
            ("VI", "El Teletipo de la Medianoche", "El Teletipo")
        ]),
        (13, "Toque de Alba", [
            ("I", "La Nochevieja Muda y el Beso en la Azotea", "Año Nuevo"),
            ("II", "El Toque de Alba", "Inversión Circadiana"),
            ("III", "El Invierno Extraño en Europa", "Pájaros Ciegos"),
            ("IV", "En el Vientre del Monstruo", "Horno H-1"),
            ("V", "La Grieta y el Veredicto", "La Soldadura")
        ]),
        (14, "Hambre y Fuego", [
            ("I", "Los Campos Negros", "Campos Negros"),
            ("II", "El Ajedrez Invisible", "Ciberguerra"),
            ("III", "El Crujido de la Tierra", "El Terremoto"),
            ("IV", "La Ruptura del Manto", "Fractura"),
            ("V", "La Herida Abierta y la Muralla de Agua", "El Tsunami")
        ]),
        (15, "Market Street", [
            ("I", "El Semisótano Fracturado", "El Derrumbe"),
            ("II", "La Sirena del Puerto y el Instinto de Huida", "La Sirena"),
            ("III", "La Ola en Market Street", "La Ola"),
            ("IV", "La Noche en el Andén Seco", "El Andén"),
            ("V", "La Carrera contra la Luz", "Carrera al Alba"),
            ("VI", "El Refugio de Hormigón", "A Salvo")
        ]),
        (16, "Ceniza", [
            ("I", "El Páramo de Versoix", "El Lago"),
            ("II", "Los Golpes en la Noche", "Refugiados"),
            ("III", "La Falsa Calma y la Quiebra Moral", "El Miedo"),
            ("IV", "El Acero y la Ceniza", "El Disparo"),
            ("V", "La Herida y el Silencio de Versoix", "La Cicatriz"),
            ("VI", "La Promesa de Jean-Luc", "Helio Líquido")
        ]),
        (17, "El Páramo", [
            ("I", "La Medida del Hambre", "Hambre"),
            ("II", "El Acecho de los Ciegos", "El Mastín"),
            ("III", "El Teorema del Sol", "El Blindaje"),
            ("IV", "La Forja del Capullo", "El Traje"),
            ("V", "La Travesía del Fuego Blanco", "Fuego Blanco"),
            ("VI", "El Santuario de Hojalata y el Percance", "El Almacén"),
            ("VII", "La Carrera contra la Sombra", "La Emboscada"),
            ("VIII", "El Sabor de la Promesa", "El Melocotón")
        ]),
        (18, "La Rampa", [
            ("I", "Las Luces de la Madrugada", "La Torre"),
            ("II", "El Relicario de la Tierra Viva", "El Relicario"),
            ("III", "La Pasarela de la Esperanza", "La Pasarela"),
            ("IV", "La Sala de la Vigilia", "La Despedida"),
            ("V", "El Trueno Nuclear", "El Despegue"),
            ("VI", "La Soledad del Vigía", "Rumbo a L1")
        ]),
        (19, "Muro de Lorentz", [
            ("I", "El Abismo Silencioso", "El Abismo"),
            ("II", "La Voz Sin Retardo", "La Voz"),
            ("III", "El Umbral de los Doce Mil Kilómetros", "El Umbral"),
            ("IV", "El Pacto en la Esclusa", "La Esclusa"),
            ("V", "El Despertar del Titanio", "El MAA"),
            ("VI", "El Muro de Lorentz y el Gran Silencio", "Muro de Lorentz")
        ]),
        (20, "Falsa Victoria", [
            ("I", "La Espera del Grafito", "Cuarenta Minutos"),
            ("II", "La Vigilia Bajo el Desierto", "Consolas Mudas"),
            ("III", "El Rayo Blanco", "Quench"),
            ("IV", "El Fantasma de Titanio", "El Rescate"),
            ("V", "El Abrazo del Vacío y la Voz del Salvador", "Regreso"),
            ("VI", "La Custodia del Relicario (La Falsa Victoria)", "La Arcilla")
        ]),
        (21, "Cielo Azul", [
            ("I", "La Noche de las Estrellas Huérfanas", "Estrellas"),
            ("II", "El Éxodo de las Trincheras", "Las Calles"),
            ("III", "El Pulso de la Lluvia", "La Lluvia")
        ]),
        (22, "El Hogar", [
            ("I", "El Deshielo de las Máquinas", "Desmovilización"),
            ("II", "El Vientre que Vuelve a Respirar", "San Francisco"),
            ("III", "El Silencio del Lago Lemán", "Versoix"),
            ("IV", "El Retorno a Suffolk", "Suffolk"),
            ("V", "La Paz Frente a la Chimenea", "La Chimenea"),
            ("VI", "El Secreto del Relicario", "La Cinta")
        ]),
        (23, "El Desván", [
            ("I", "El Templo de Madera y Cobre", "El Desván"),
            ("II", "La Frecuencia del Abismo y la Voz de Sombra", "La Frecuencia"),
            ("III", "El Testamento Demoledor", "El Granjero"),
            ("IV", "El Veredicto Metalúrgico", "El Microscopio"),
            ("V", "La Conjuración de Ginebra", "Ginebra")
        ]),
        (24, "El Pacto", [
            ("I", "El Festín de los Ciegos", "La Asamblea"),
            ("II", "La Lluvia en el Parque Ariana", "El Pacto"),
            ("III", "El Altar de las Válvulas", "Válvulas"),
            ("IV", "El Caballo de Troya Burocrático y la Mirada de Pleh", "Cuarenta y Dos Kilos"),
            ("V", "La Víspera del Disparo", "La Víspera")
        ]),
        (25, "La Canción", [
            ("I", "El Vuelo en la Sombra", "La Flecha Negra"),
            ("II", "El Abismo y el Alma", "El Alma"),
            ("III", "El Quiebre de la Vela", "La Vela"),
            ("IV", "El Meteoro de la Libertad", "El Meteoro"),
            ("V", "La Canción del Silencio", "El Silencio"),
            ("Post-Scríptum", "La Semilla en la Sombra", "Kernel A-01")
        ])
    ]

    sec_rows = [
        [
            Paragraph("Cap.", th_style),
            Paragraph("Sec.", th_style),
            Paragraph("Nombre Actual del Apartado (Extenso)", th_style),
            Paragraph("Propuesta Concisa (1-3 palabras)", th_style)
        ]
    ]

    for cnum, cprop, secs in apartados_master:
        for snum, sold, snew in secs:
            sec_rows.append([
                Paragraph(f"<b>{cnum}</b>", td_elem),
                Paragraph(str(snum), td_note),
                Paragraph(clean(sold), td_old),
                Paragraph(f"<b>{clean(snew)}</b>", td_new)
            ])

    t_secs = Table(sec_rows, colWidths=[24, 28, 280, 188])
    t_secs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")])
    ]))
    story.append(t_secs)

    doc.build(story, canvasmaker=TitulosCanvas)
    print(f"PDF generado: {filename}")

if __name__ == "__main__":
    out_name = "Propuesta_Titulos_Cortos_La_Cancion_del_Silencio.pdf"
    build_pdf(out_name)
    
    # Copias de cortesía
    destinos = [
        "novela/Propuesta_Titulos_Cortos_La_Cancion_del_Silencio.pdf",
        "PROPUESTA_TITULOS_CORTOS.pdf",
        "novela/PROPUESTA_TITULOS_CORTOS.pdf"
    ]
    for d in destinos:
        shutil.copyfile(out_name, d)
        print(f"Copiado a: {d}")

