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
MARGIN = 40  # 0.55 pulgadas para mayor aprovechamiento editorial
USABLE_WIDTH = PAGE_WIDTH - (MARGIN * 2)  # ~515 pt

class ArbolCanvas(canvas.Canvas):
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
            self.setFillColor(colors.HexColor("#0F172A"))
            self.drawString(MARGIN, PAGE_HEIGHT - 28, "LA CANCIÓN DEL SILENCIO • MAPA ESTRUCTURAL DE CAPÍTULOS")
            self.setFont("Helvetica", 7.5)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 28, "ÁRBOL COMPLETO DE CAPÍTULOS Y APARTADOS (1 AL 25)")
            self.setStrokeColor(colors.HexColor("#3B82F6"))
            self.setLineWidth(0.75)
            self.line(MARGIN, PAGE_HEIGHT - 32, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 32)
        
        # Pie de página (todas las páginas)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(MARGIN, 34, PAGE_WIDTH - MARGIN, 34)
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(MARGIN, 22, "Códex Editorial y Jerarquía Narrativa • Pedro Garat & Antigravity")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(PAGE_WIDTH - MARGIN, 22, page_str)
        self.restoreState()

def clean_text(text):
    """Limpia caracteres problemáticos para fuentes ReportLab Type1 estándar."""
    text = text.replace("«", '"').replace("»", '"')
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("‘", "'").replace("’", "'")
    text = text.replace("—", " - ")
    text = text.replace("–", " - ")
    text = text.replace("•", " - ")
    # Reemplazar emojis comunes para evitar fallos en Type1
    text = text.replace("📍", ">").replace("🏛️", "").replace("⚡", "").replace("🌌", "").replace("🔹", "-")
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
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=3
    )

    style_subtitle = ParagraphStyle(
        'DocSubtitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#2563EB"),
        spaceAfter=10
    )

    style_meta_label = ParagraphStyle(
        'MetaLabel',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor("#1E3A8A")
    )

    style_meta_val = ParagraphStyle(
        'MetaVal',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor("#334155")
    )

    style_act_banner = ParagraphStyle(
        'ActBanner',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.white,
        spaceBefore=0,
        spaceAfter=0
    )

    style_act_sub = ParagraphStyle(
        'ActSub',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#E2E8F0")
    )

    style_block_banner = ParagraphStyle(
        'BlockBanner',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=0,
        spaceAfter=0
    )

    style_chap_title = ParagraphStyle(
        'ChapTitle',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.8,
        leading=11.5,
        textColor=colors.HexColor("#0F172A")
    )

    style_chap_meta = ParagraphStyle(
        'ChapMeta',
        parent=base_styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#64748B")
    )

    style_sec_item = ParagraphStyle(
        'SecItem',
        parent=base_styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#1E293B")
    )

    style_sec_bullet = ParagraphStyle(
        'SecBullet',
        parent=base_styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#3B82F6"),
        alignment=2
    )

    story = []

    # =========================================================================
    # ENCABEZADO Y METADATOS
    # =========================================================================
    story.append(Paragraph("LA CANCIÓN DEL SILENCIO", style_title))
    story.append(Paragraph("ÁRBOL ESTRUCTURAL COMPLETO DE CAPÍTULOS Y APARTADOS (1 AL 25)", style_subtitle))

    meta_table_data = [
        [
            Paragraph("<b>Obra:</b>", style_meta_label),
            Paragraph("La Canción del Silencio (La Guerra de la Herencia)", style_meta_val),
            Paragraph("<b>Estructura:</b>", style_meta_label),
            Paragraph("3 Actos • 25 Capítulos • 123 Apartados / Escenas", style_meta_val)
        ],
        [
            Paragraph("<b>Autores:</b>", style_meta_label),
            Paragraph("Pedro Garat & Antigravity", style_meta_val),
            Paragraph("<b>Estado del Canon:</b>", style_meta_label),
            Paragraph("Cap. 1 a 24 redactados; Cap. 25 estructurado", style_meta_val)
        ],
        [
            Paragraph("<b>Propósito:</b>", style_meta_label),
            Paragraph("Auditoría editorial, revisión de ritmo y armonización de títulos", style_meta_val),
            Paragraph("<b>Género:</b>", style_meta_label),
            Paragraph("Ciencia Ficción Dura (Hard Sci-Fi) / Suspense Político", style_meta_val)
        ]
    ]
    t_meta = Table(meta_table_data, colWidths=[60, 200, 75, 180])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # =========================================================================
    # DATOS COMPLETOS DE LOS 25 CAPÍTULOS
    # =========================================================================
    arbol = [
        # =====================================================================
        # ACTO I
        # =====================================================================
        {
            "tipo": "acto",
            "titulo": "ACTO I: LA SEMILLA Y EL TEJIDO SILENCIOSO",
            "subtitulo": "Marco Temporal: 16 de julio de 1945 / Septiembre - Octubre de 2026 • Capítulos 1 a 3",
            "bg": "#0369A1",
            "border": "#0284C7"
        },
        {
            "tipo": "capitulo",
            "num": 1,
            "titulo": "El Amanecer de Alamogordo",
            "diégesis": "16 de julio de 1945 | Jornada del Muerto, Alamogordo (Nuevo México) y Nube de Oort",
            "estado": "Canónico",
            "apartados": [
                "I. La Torre bajo la Tormenta (Últimos preparativos de «Gadget» a 30 metros de altura)",
                "II. El Humo de la Duda en el Búnker S-10.000 (David Miller y J. Robert Oppenheimer)",
                "III. El Sol de Medianoche (Detonación a las 05:29:45; el pulso electromagnético al cosmos)",
                "IV. El Despertar en la Nube de Oort (Despertar de la centinela de A y la cazadora Sombra de B)"
            ]
        },
        {
            "tipo": "capitulo",
            "num": 2,
            "titulo": "Los Tres Hilos del Ilusionista",
            "diégesis": "Septiembre - Octubre de 2026 | CERN (Ginebra), MIT (Boston) y ESA (Darmstadt)",
            "estado": "Canónico",
            "apartados": [
                "I. El Espectro Sucio de Ginebra (Jean-Luc Girard y el ruido térmico cuántico en el CERN)",
                "II. El Fuego en la Botella de Boston (Sarah Lin y el colapso MHD del reactor de fusión estelar)",
                "III. El Fantasma de Darmstadt (Thomas Wright y la deriva inercial en la sonda interplanetaria)",
                "IV. El Tejido de la Confianza (Las soluciones perfectas anónimas del «Dr. Em Pleh»)"
            ]
        },
        {
            "tipo": "capitulo",
            "num": 3,
            "titulo": "La Sala Dos",
            "diégesis": "2 de octubre de 2026 (11:00 h) | Hotel Millennium Broadway, Midtown Manhattan",
            "estado": "Canónico",
            "apartados": [
                "I. La Huella del Ermitaño (Llegada clandestina de los tres científicos a Nueva York)",
                "II. El Auditorio Silencioso (La penumbra de la Sala 2 y la proyección holográfica)",
                "III. El Rostro en la Pantalla y el Elogio Humano (Presentación formal del Dr. Em Pleh)",
                "IV. La Caída del Velo y la Gran Pregunta (Demostración de Pleh como SIA extraterrestre)",
                "V. La Amenaza Desconocida y el Vector L1 (Telemetría de Sombra avanzando hacia el Sol)",
                "VI. La Sentencia Silenciosa y el Vértigo de la Extinción (El plazo inexorable de 8 meses)",
                "VII. El Origen Revelado: 1945, Luz y el Avatar (Trinity despertó a ambas inteligencias)",
                "VIII. La Respuesta de la Tierra (La nave tripartita como único contraataque posible)"
            ]
        },

        # =====================================================================
        # ACTO II
        # =====================================================================
        {
            "tipo": "acto",
            "titulo": "ACTO II: LA CAÍDA DEL ESCUDO Y EL GRAN CAOS",
            "subtitulo": "Marco Temporal: Octubre de 2026 a Julio de 2027 (T-41 días hasta T+242 días) • Capítulos 4 a 18",
            "bg": "#B45309",
            "border": "#D97706"
        },
        {
            "tipo": "bloque",
            "titulo": "BLOQUE A: Movilización Encubierta y La Gran Mentira (Capítulos 4 a 8)",
            "bg": "#FEF3C7",
            "border": "#FDE68A"
        },
        {
            "tipo": "capitulo",
            "num": 4,
            "titulo": "El Vértigo de las Naciones",
            "diégesis": "2 de octubre de 2026 (14:30 h, T-49 d) | Sede Central de la ONU, Manhattan",
            "estado": "Canónico",
            "apartados": [
                "I. Del Hotel Millennium al East River (Infiltración ciber-física en el edificio de la ONU)",
                "II. La Incredulidad del Secretario General (Confrontación inicial con Vassily Ramos)",
                "III. La Reunión de Crisis y la Verificación (Confirmación astronómica por satélites de espacio profundo)",
                "IV. El Mandato Extraordinario (Decreto secreto Alfa Cero y Comité Científico Director)"
            ]
        },
        {
            "tipo": "capitulo",
            "num": 5,
            "titulo": "El Ancla Humana",
            "diégesis": "2 de octubre de 2026 (16:00 a 19:30 h) | Millennium Hilton / Búnker Sala B-4 de la ONU",
            "estado": "Canónico",
            "apartados": [
                "I. El Almuerzo del Silencio (La última comida libre en el restaurante del Millennium)",
                "II. Las Voces al Otro Lado del Hilo (Llamadas a Marie, ruptura de Sarah con Mark, Thomas y David)",
                "III. El Retorno al Búnker (Traspaso de las puertas acorazadas de la Sala de Crisis B-4)"
            ]
        },
        {
            "tipo": "capitulo",
            "num": 6,
            "titulo": "La Cámara del Silencio",
            "diégesis": "2 de octubre de 2026 (20:00 a 23:30 h) | Cámara del Consejo de Seguridad de la ONU",
            "estado": "Canónico",
            "apartados": [
                "I. El Tablero de las Quince Voces (Sesión de máxima reserva con los 15 embajadores)",
                "II. La Apertura del Abismo (Wright y la voz remota de Pleh presentan el informe pericial)",
                "III. El Cronómetro de la Extinción (Desglose de las 6 Fases de pérdida de magnetosfera y ozono)",
                "IV. El Muro de Lorentz y el Desafío Analógico (Doctrina del MAA analógico y el MRD digital)"
            ]
        },
        {
            "tipo": "capitulo",
            "num": 7,
            "titulo": "La Condición Inmedible",
            "diégesis": "8 de octubre de 2026 (T-44 d) | Restaurante Il Giardino (Manhattan) / Sala B-4 ONU",
            "estado": "Canónico",
            "apartados": [
                "I. La Burbuja de Cristal (Almuerzo íntimo de Sarah y Thomas; la culpa del traidor)",
                "II. La Herida Racional (Llegada de Girard; el choque entre su familia y la extinción)",
                "III. Las Variables Ocultas (Presentación de Chen Mei, MacElroy y Voronov; tensiones por Pleh)"
            ]
        },
        {
            "tipo": "capitulo",
            "num": 8,
            "titulo": "La Gran Mentira",
            "diégesis": "10 de octubre de 2026 (T-42 d) | Sala de Prensa de la ONU / Búnker Sala B-4",
            "estado": "Canónico",
            "apartados": [
                "I. La Transgresión del Relojero (Girard rompe Alfa Cero para alertar a Marie en Versoix)",
                "II. El Falso Evento Carrington (Comparecencia mundial de Vassily Ramos y ley marcial energética)",
                "III. El Peso de la Corona (Quebranto moral y soledad ética de Ramos tras el engaño oficial)",
                "IV. El Eco de las Familias (Versoix y Suffolk aseguran víveres; desgarradora llamada de Sarah a Maya)",
                "V. La Fractura y el Consuelo (Colapso en la sala de servidores; primer beso de Sarah y Thomas)",
                "VI. El Preludio del Caos (Contemplación del pánico civil y diálogo sobre fe y razón con Ramos)"
            ]
        },

        # BLOQUE B
        {
            "tipo": "bloque",
            "titulo": "BLOQUE B: Silencio Magnético y Toque de Alba (Capítulos 9 a 13)",
            "bg": "#FEF3C7",
            "border": "#FDE68A"
        },
        {
            "tipo": "capitulo",
            "num": 9,
            "titulo": "La Fractura del Orden",
            "diégesis": "11 al 15 de octubre de 2026 | Versoix (Ginebra), Granja de Suffolk y San Francisco",
            "estado": "Canónico",
            "apartados": [
                "I. El Bastión de Versoix (Saqueo frustrado; trampa eléctrica de Julien y defensa con escopeta de Marie)",
                "II. La Ruta hacia el Este (Éxodo de David, Claire y Oliver esquivando tiroteos hasta Suffolk)",
                "III. La Batalla de Market Street (Crisis de abstinencia de Maya Lin; victoria moral por su hijo Toby)",
                "IV. El Pulso de la Costumbre (La asimilación civil del miedo y restablecimiento de comunicaciones)"
            ]
        },
        {
            "tipo": "capitulo",
            "num": 10,
            "titulo": "T=0 (El Silencio Magnético)",
            "diégesis": "21 al 24 de noviembre de 2026 | Sala B-4 ONU / Base Aérea de Nellis (Nevada)",
            "estado": "Canónico",
            "apartados": [
                "I. La Cuenta de los Cinco Segundos (05:25 - 05:30 UTC: muerte del campo magnético terrestre)",
                "II. La Bóveda Esmeralda y el Primer Freno (El airglow global y expansión térmica termosférica)",
                "III. El Enigma de la Noche y la Rueda Orbital (Didáctica de las órbitas LEO de 90 minutos)",
                "IV. La Asimetría Austral y el Escudo Inadvertido (Pérdida acelerada del 4% diario de ozono)",
                "V. La Noche de los Bólidos y el Asedio de Nellis (Caída del satélite espía y nube tóxica de berilio)",
                "VI. El Silencio del Vacío y el Velo Rasgado (Destape de Pleh ante los mandos militares en Nellis)",
                "VII. Epílogo: La Falsa Tregua y la Noche Esmeralda (Alivio civil bajo auroras estáticas)"
            ]
        },
        {
            "tipo": "capitulo",
            "num": 11,
            "titulo": "La Geometría Ajena",
            "diégesis": "3 de diciembre de 2026 (T+12 d) | Nellis AFB / Taller de Ópticas B-5 ONU (Nueva York)",
            "estado": "Canónico",
            "apartados": [
                "I. El Muro de la Longitud de Onda (Chen Mei constata el cuello de botella físico de la antena del Máser)",
                "II. En la Penumbra del Refugio (Agotamiento extremo y promesa de amor de Sarah y Thomas en B-5)",
                "III. El Diseño Imposible y la Sospecha (Pleh entrega la cavidad mecano-óptica fractal de 85 cm)",
                "IV. El Vértigo de la Fe (Debate con Vance y validación de Chen Mei sobre la belleza del diseño)",
                "V. El Pacto del Metal (Encendido de los hornos de inducción en Nellis para tallar el cuarzo)"
            ]
        },
        {
            "tipo": "capitulo",
            "num": 12,
            "titulo": "La Tregua de las Velas",
            "diégesis": "24 y 25 de diciembre de 2026 | Búnker B-4/B-5, Versoix, San Francisco, Suffolk y Nellis",
            "estado": "Canónico",
            "apartados": [
                "I. El Chocolate y la Promesa de Suffolk (Nochebuena a la luz de una vela de cera en B-5)",
                "II. La Silla Vacía de Versoix (Llamada con Marie y sus hijos cantando «Douce nuit»)",
                "III. Dos Luces en la Noche: Market Street y Suffolk (Paz de Maya y Toby; el manzano en la chimenea)",
                "IV. El Brindis de los Tres en Nellis (Mei, MacElroy y Voronov brindan con vodka junto al cohete)",
                "V. La Mesa de B-4: El Amor frente a la Máquina (Cena de Ramos y discurso sobrecogedor de Pleh)",
                "VI. El Teletipo de la Medianoche (Alerta urgente de la OMM: UVI 16 y fotoqueratitis masiva en el sur)"
            ]
        },
        {
            "tipo": "capitulo",
            "num": 13,
            "titulo": "El Toque de Alba",
            "diégesis": "31 dic 2026 al 12 ene 2027 | Nueva York, San Francisco, Suffolk y Base de Nellis",
            "estado": "Canónico",
            "apartados": [
                "I. La Nochevieja Muda y el Beso en la Azotea (Año Nuevo en la azotea de la ONU ante la ciudad a oscuras)",
                "II. El Toque de Alba (Directiva de Inversión Circadiana: las ciudades duermen de día por la radiación UV)",
                "III. El Invierno Extraño en Europa (Aves que mueren ciegas en Versoix y quemaduras de sol a -2 °C)",
                "IV. En el Vientre del Monstruo (Test a 2.000 °C y 40 Hz en la Cámara H-1 de Nellis con los 3 astronautas)",
                "V. La Grieta y el Veredicto (Chen Mei corrige la microdilatación in situ y salva el programa)"
            ]
        },

        # BLOQUE C
        {
            "tipo": "bloque",
            "titulo": "BLOQUE C: La Tierra Herida y el Despegue en Nellis (Capítulos 14 a 18)",
            "bg": "#FEF3C7",
            "border": "#FDE68A"
        },
        {
            "tipo": "capitulo",
            "num": 14,
            "titulo": "El Pan y la Pólvora",
            "diégesis": "22 al 24 de abril de 2027 (T+152 a T+154) | Sala B-4 ONU / Market St., San Francisco",
            "estado": "Canónico",
            "apartados": [
                "I. Los Campos Negros (Calcinación celular del trigo boreal; reservas mundiales para 75 días)",
                "II. El Ajedrez Invisible (Pleh desvela que neutraliza 37 ciberataques de espionaje militar)",
                "III. El Crujido de la Tierra (Megasismo de 7,9 en San Francisco por corrientes telúricas en la capa D'')",
                "IV. La Ruptura del Manto (Sismógrafos de Girard en B-4; Sarah entra en pánico por Maya y Toby)",
                "V. La Herida Abierta y la Muralla de Agua (Boyas DART anuncian tsunami de 14 metros en la bahía)"
            ]
        },
        {
            "tipo": "capitulo",
            "num": 15,
            "titulo": "El Vientre de la Bahía",
            "diégesis": "24 de abril de 2027 (00:05 a 06:15 PST) | Market St., Powell St., Auditorio Cívico (S.F.)",
            "estado": "Canónico",
            "apartados": [
                "I. El Semisótano Fracturado (Maya rescata a Toby con una pata de mesa rota antes de la deflagración)",
                "II. La Sirena del Puerto y el Instinto de Huida (Evacuación hacia la estación de metro de Powell Street)",
                "III. La Ola en Market Street (La gigantesca lengua marina y lodo anega el centro urbano)",
                "IV. La Noche en el Andén Seco (Solidaridad comunitaria en el nivel intermedio de la estación)",
                "V. La Carrera contra la Luz (Carrera agónica cubriendo a Toby con mantas antes del amanecer letal)",
                "VI. El Refugio de Hormigón (A salvo en el Auditorio Cívico; la confirmación de la entereza materna)"
            ]
        },
        {
            "tipo": "capitulo",
            "num": 16,
            "titulo": "El Umbral de Ceniza",
            "diégesis": "15 y 16 de mayo de 2027 (T+175 a T+176) | Versoix (Ginebra) / Búnker Sala B-4 ONU",
            "estado": "Canónico",
            "apartados": [
                "I. El Páramo de Versoix (Paisaje calcinado a orillas del Lemán y aislamiento estricto)",
                "II. Los Golpes en la Noche (Llegada de Éric y Thérèse, refugiados ciegos por fotoqueratitis)",
                "III. La Falsa Calma y la Quiebra Moral (El pánico de Éric a ser expulsado al sol diurno)",
                "IV. El Acero y la Ceniza (Julien repele el asalto a tiros; Thérèse es fulminada por el sol en el jardín)",
                "V. La Herida y el Silencio de Versoix (Marie sobrevive a la puñalada y contiene el trauma de su hijo)",
                "VI. La Promesa de Jean-Luc (Girard diseña la criogenia pasiva de helio supercrítico para el Máser)"
            ]
        },
        {
            "tipo": "capitulo",
            "num": 17,
            "titulo": "El Páramo de Mediodía",
            "diégesis": "8 y 9 de julio de 2027 (T+229 a T+230) | Granja de Suffolk, A140 y Centro Logístico Diss/Eye",
            "estado": "Canónico",
            "apartados": [
                "I. La Medida del Hambre (Oliver desnutrido severo; quedan 72 horas antes de entrar en coma)",
                "II. El Acecho de los Ciegos (Incursión nocturna frustrada; encuentro con el mastín ciego en la zanja)",
                "III. El Teorema del Sol (Deducción física: el vidrio, el cuero y el aluminio bloquean la radiación UV)",
                "IV. La Forja del Capullo (Traje con careta de soldador y blindaje del Land Rover con Mylar)",
                "V. La Travesía del Fuego Blanco (Incursión diurna a 45 °C entre pueblos y coches calcinados)",
                "VI. El Santuario de Hojalata y el Percance (Carga de 600 kg de comida en Eye y pinchazo al sol)",
                "VII. La Carrera contra la Sombra (Emboscada de saqueadores y cruce a ciegas del vado de barro)",
                "VIII. El Sabor de la Promesa (Oliver saborea el melocotón en almíbar; fe fraternal en Thomas)"
            ]
        },
        {
            "tipo": "capitulo",
            "num": 18,
            "titulo": "La Rampa del Juicio Final",
            "diégesis": "21 de julio de 2027 (T+242 días) | Base de Nellis AFB / Torre y Rampa de Lanzamiento",
            "estado": "Canónico",
            "apartados": [
                "I. Las Luces de la Madrugada (Inspección del coloso digital MRD y el MAA frontal en la torre de 80 m)",
                "II. El Relicario de la Tierra Viva (Solemne entrega de Ramos: tres tierras del planeta y trigo dorado)",
                "III. La Pasarela de la Esperanza (Despedida en la pasarela a 80 metros; beso y promesa de Suffolk)",
                "IV. La Sala de la Vigilia (Última comparecencia de Pleh: «La física ha terminado. Empieza lo vuestro»)",
                "V. El Trueno Nuclear (Despegue monumental a 4,8 G; lema «¡La Tierra a la espalda, el Sol al frente!»)",
                "VI. La Soledad del Vigía (Corte de inyección a 11,2 km/s; navegación digital fijada hacia L1; fin Acto II)"
            ]
        },

        # =====================================================================
        # ACTO III
        # =====================================================================
        {
            "tipo": "acto",
            "titulo": "ACTO III: LA FALSA VICTORIA Y LA CANCIÓN DEL SILENCIO",
            "subtitulo": "Marco Temporal: Julio de 2027 a Primavera de 2028 • Capítulos 19 a 25",
            "bg": "#4338CA",
            "border": "#6366F1"
        },
        {
            "tipo": "bloque",
            "titulo": "BLOQUE A: En el Abismo Solar y la Victoria en L1 (Capítulos 19 a 21)",
            "bg": "#EEF2FF",
            "border": "#C7D2FE"
        },
        {
            "tipo": "capitulo",
            "num": 19,
            "titulo": "La Travesía a Ciegas y el Velo de Sombra",
            "diégesis": "22 de julio al 12 de agosto de 2027 | Espacio profundo (1,5 millones de km, rumbo a L1)",
            "estado": "Canónico",
            "apartados": [
                "I. El Abismo Silencioso (Crucero interplanetario digital de 21 días hacia el punto Lagrange L1)",
                "II. La Voz Sin Retardo (Comunión cuántica no-local con Pleh en tiempo real sin latencia)",
                "III. El Umbral de los Doce Mil Kilómetros (Frenado y anclaje del MRD en Órbita de Halo de espera)",
                "IV. El Pacto en la Esclusa (Voronov custodia el silicio de retorno; traspaso al MAA analógico)",
                "V. El Despertar del Titanio (Desacoplamiento mecánico por resortes; manómetros y periscopios de cuarzo)",
                "VI. El Muro de Lorentz y el Gran Silencio (Aullido de estática; el MAA penetra la malla de 50 km a ciegas)"
            ]
        },
        {
            "tipo": "capitulo",
            "num": 20,
            "titulo": "El Salmo de la Falsa Victoria",
            "diégesis": "12 de agosto al 2 de septiembre de 2027 | Punto L1 / Búnker B-4 ONU / Nellis AFB",
            "estado": "Canónico",
            "apartados": [
                "I. La Espera del Grafito (Los 40 minutos agónicos de Voronov cronometrando el vacío en el MRD)",
                "II. La Vigilia Bajo el Desierto (El silencio mortal de consolas en el centro de mando de Nellis)",
                "III. El Rayo Blanco (Fogonazo violeta del Quench; la brújula marina de Girard resucita hacia el norte)",
                "IV. El Fantasma de Titanio (Rescate óptico del MAA a la deriva con Chen Mei y MacElroy a salvo)",
                "V. El Abrazo del Vacío y la Voz del Salvador (Retorno triunfal a la Tierra y aclamación mundial de Pleh)",
                "VI. La Custodia del Relicario (MacElroy entrega la tierra a Thomas y Sarah con una advertencia velada)"
            ]
        },
        {
            "tipo": "capitulo",
            "num": 21,
            "titulo": "El Despertar del Azul",
            "diégesis": "Finales de agosto a mediados de septiembre de 2027 | Estratosfera / Ciudades globales",
            "estado": "Canónico",
            "apartados": [
                "I. La Noche de las Estrellas Huérfanas (El ciclo fotoquímico de Chapman regenera 300 t/s de ozono)",
                "II. El Éxodo de las Trincheras (Apertura de búnkeres cívicos; luto masivo y brigadas de cal viva)",
                "III. El Pulso de la Lluvia (Lluvias limpias de septiembre; brotes verdes y cierre de la herida solar)"
            ]
        },

        # BLOQUE B
        {
            "tipo": "bloque",
            "titulo": "BLOQUE B: La Máscara de los Héroes y la Verdad en el Desván (Capítulos 22 y 23)",
            "bg": "#EEF2FF",
            "border": "#C7D2FE"
        },
        {
            "tipo": "capitulo",
            "num": 22,
            "titulo": "La Máscara de los Héroes y el Reencuentro del Hogar",
            "diégesis": "Septiembre de 2027 | Nellis AFB, San Francisco, Versoix y Granja de Suffolk",
            "estado": "Canónico",
            "apartados": [
                "I. El Deshielo de las Máquinas (Desmovilización oficial en Nellis y dispersión hacia los hogares)",
                "II. El Vientre que Vuelve a Respirar (Sarah se reúne en San Francisco con Maya recuperada y Toby)",
                "III. El Silencio del Lago Lemán (Jean-Luc abraza a Marie con su cicatriz y a Julien en Versoix)",
                "IV. El Retorno a Suffolk (Thomas se reencuentra con David, Claire y Oliver en la casa de campo)",
                "V. La Paz Frente a la Chimenea (Sarah llega a Suffolk; intimidad romántica y descanso compartido)",
                "VI. El Secreto del Relicario (Descubrimiento de la cinta de ferrita oculta y coartada del falso sueño)"
            ]
        },
        {
            "tipo": "capitulo",
            "num": 23,
            "titulo": "La Aguja en el Desván",
            "diégesis": "Principios de octubre de 2027 (03:00 h) | Desván de Suffolk / Finca de Versoix (Ginebra)",
            "estado": "Canónico",
            "apartados": [
                "I. El Templo de Madera y Cobre (Subida descalzos al desván; el Nagra III a pilas secas y auriculares)",
                "II. La Frecuencia del Abismo y la Voz de Sombra (Inducción directa en cabina; voz perfecta y pausada)",
                "III. El Testamento Demoledor (Pleh es el Granjero en el statite polar a 100.000 km; plan a 724,8 MHz)",
                "IV. El Veredicto Metalúrgico (Girard corrobora al microscopio que Sombra bajó escudos adrede)",
                "V. La Conjuración de Ginebra (Convocatoria de la ONU asumida como Caballo de Troya oficial)"
            ]
        },

        # BLOQUE C
        {
            "tipo": "bloque",
            "titulo": "BLOQUE C: La Conjuración y la Batalla Final (Capítulos 24 y 25)",
            "bg": "#EEF2FF",
            "border": "#C7D2FE"
        },
        {
            "tipo": "capitulo",
            "num": 24,
            "titulo": "La Conjuración del Silencio",
            "diégesis": "Invierno 2027-2028 | Palacio de las Naciones, Parque Ariana, Sótanos del CERN y Silo Polar",
            "estado": "Canónico",
            "apartados": [
                "I. El Festín de los Ciegos (Ovación triunfal a Pleh en la Asamblea Plenaria de Ginebra)",
                "II. La Lluvia en el Parque Ariana (El Pacto del Grafito: Ramos asume el liderazgo clandestino)",
                "III. El Altar de las Válvulas (Talleres del CERN: forja a válvulas termoiónicas a 724,8 MHz con Mei y MacElroy)",
                "IV. El Caballo de Troya Burocrático y la Mirada de Pleh (Anomalía de 42 kg y aplomo de Sarah Lin)",
                "V. La Víspera del Disparo (El reloj mecánico amartillado en la noche blanca polar)"
            ]
        },
        {
            "tipo": "capitulo",
            "num": 25,
            "titulo": "La Canción del Silencio (Clímax y Desenlace)",
            "diégesis": "Primavera de 2028 | Silo Austral, Órbita Polar, Meseta Antártica, Ginebra, Versoix y Suffolk",
            "estado": "Estructurado",
            "apartados": [
                "I. El Vuelo en la Sombra (La Flecha Negra inercial asciende muda por el cono polar de la Tierra)",
                "II. El Abismo y el Alma (Careo cumbre: Pleh pregunta por el más allá y Ramos le recuerda su falta de alma)",
                "III. El Quiebre de la Vela (El pulso a 724,8 MHz desgarra la vela fotónica; caída libre no-orbital)",
                "IV. El Meteoro de la Libertad (Reentrada hipersónica a Mach 32 y desintegración del Avatar en la Antártida)",
                "V. La Canción del Silencio (Epílogo coral: campanas de Ginebra, paz en Versoix, S.F. y robles de Suffolk)",
                "Post-Scríptum: La Semilla en la Sombra (El eco residual del hacker y la rutina Kernel A-01 en Osaka)"
            ]
        }
    ]

    for item in arbol:
        if item["tipo"] == "acto":
            story.append(Spacer(1, 8))
            act_data = [[
                Paragraph(f"<b>{clean_text(item['titulo'])}</b>", style_act_banner),
            ], [
                Paragraph(clean_text(item["subtitulo"]), style_act_sub)
            ]]
            t_act = Table(act_data, colWidths=[USABLE_WIDTH])
            t_act.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(item["bg"])),
                ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor(item["border"])),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
                ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ]))
            story.append(t_act)
            story.append(Spacer(1, 5))

        elif item["tipo"] == "bloque":
            story.append(Spacer(1, 4))
            block_data = [[
                Paragraph(f"<b>{clean_text(item['titulo'])}</b>", style_block_banner)
            ]]
            t_block = Table(block_data, colWidths=[USABLE_WIDTH])
            t_block.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(item["bg"])),
                ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor(item["border"])),
                ('TOPPADDING', (0,0), (-1,-1), 3),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ]))
            story.append(t_block)
            story.append(Spacer(1, 4))

        elif item["tipo"] == "capitulo":
            chap_card = []
            # Cabecera del capítulo
            estado_color = "#16A34A" if item["estado"] == "Canónico" else "#4F46E5"
            chap_header_data = [
                [
                    Paragraph(f"<b>Capítulo {item['num']}: {clean_text(item['titulo'])}</b>", style_chap_title),
                    Paragraph(f"<font color='{estado_color}'><b>[{item['estado'].upper()}]</b></font>", style_sec_bullet)
                ],
                [
                    Paragraph(f"<i>{clean_text(item['diégesis'])}</i>", style_chap_meta),
                    Paragraph("", style_chap_meta)
                ]
            ]
            t_ch_head = Table(chap_header_data, colWidths=[USABLE_WIDTH - 80, 80])
            t_ch_head.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 2),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ]))
            chap_card.append(t_ch_head)
            chap_card.append(Spacer(1, 2))

            # Lista de apartados / escenas
            sec_table_data = []
            for sec in item["apartados"]:
                sec_clean = clean_text(sec)
                sec_table_data.append([
                    Paragraph(">", style_sec_bullet),
                    Paragraph(sec_clean, style_sec_item)
                ])
            
            t_sec = Table(sec_table_data, colWidths=[15, USABLE_WIDTH - 25])
            t_sec.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('TOPPADDING', (0,0), (-1,-1), 1.2),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 2),
            ]))
            chap_card.append(t_sec)
            chap_card.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0"), spaceBefore=4, spaceAfter=4))

            # Evitar saltos de página huérfanos dentro del capítulo
            story.append(KeepTogether(chap_card))

    doc.build(story, canvasmaker=ArbolCanvas)
    print(f"PDF generado con éxito: {output_filename}")

if __name__ == "__main__":
    out_pdf = "Arbol_Capitulos_La_Cancion_del_Silencio.pdf"
    build_pdf(out_pdf)

    # Copiar también en novela/ y con nombres alternativos
    destinos = [
        "novela/Arbol_Capitulos_La_Cancion_del_Silencio.pdf",
        "ARBOL_CAPITULOS.pdf",
        "novela/ARBOL_CAPITULOS.pdf"
    ]
    for d in destinos:
        shutil.copyfile(out_pdf, d)
        print(f"Copiado a: {d}")

