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
USABLE_WIDTH = PAGE_WIDTH - 108  # 487.27 pt (54 pt margins)

class ReportCanvas(canvas.Canvas):
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
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#0284C7"))
        
        # Encabezado (páginas > 1)
        if self._pageNumber > 1:
            self.drawString(54, PAGE_HEIGHT - 36, "LA CANCIÓN DEL SILENCIO • INFORME DE RECAPITULACIÓN Y AUDITORÍA")
            self.setFont("Helvetica", 7.5)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(PAGE_WIDTH - 54, PAGE_HEIGHT - 36, "EVALUACIÓN DE COHERENCIA EDITORIAL")
            self.setStrokeColor(colors.HexColor("#0284C7"))
            self.setLineWidth(0.75)
            self.line(54, PAGE_HEIGHT - 40, PAGE_WIDTH - 54, PAGE_HEIGHT - 40)
        
        # Pie de página
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 45, PAGE_WIDTH - 54, 45)
        
        self.setFont("Helvetica", 7.8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "Códice Editorial y Control de Continuidad • Capítulos 1 al 7")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(PAGE_WIDTH - 54, 32, page_str)
        self.restoreState()

def create_alert_box(title, text_paragraphs, styles, border_color="#D97706", bg_color="#FFFBEB", width=USABLE_WIDTH):
    t_style = ParagraphStyle(
        'AlertTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=colors.HexColor("#92400E"),
        spaceAfter=4
    )
    b_style = ParagraphStyle(
        'AlertBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.5,
        textColor=colors.HexColor("#78350F"),
        spaceAfter=3
    )
    content = [Paragraph(f"<b>{title}</b>", t_style)]
    for p in text_paragraphs:
        content.append(Paragraph(p, b_style))
    t = Table([[content]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_color)),
        ('LINELEFT', (0,0), (-1,-1), 3.5, colors.HexColor(border_color)),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    return t

def generate_report_pdf(output_filename):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    super_title = ParagraphStyle(
        'SuperTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#0284C7"),
        alignment=1,
        spaceAfter=4
    )
    main_title = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0F172A"),
        alignment=1,
        spaceAfter=6
    )
    subtitle = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569"),
        alignment=1,
        spaceAfter=15
    )
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#0369A1"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=6
    )
    bullet_style = ParagraphStyle(
        'ReportBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.8,
        textColor=colors.HexColor("#1E293B"),
        leftIndent=12,
        spaceAfter=4
    )
    tbl_header = ParagraphStyle(
        'TblHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=0
    )
    tbl_cell = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.8,
        textColor=colors.HexColor("#1E293B")
    )
    tbl_cell_bold = ParagraphStyle(
        'TblCellB',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0F172A")
    )

    story = []
    
    # Portadilla
    story.append(Spacer(1, 10))
    story.append(Paragraph("LA CANCIÓN DEL SILENCIO / LA GUERRA DE LA HERENCIA", super_title))
    story.append(Paragraph("Informe de Recapitulación General y Auditoría de Coherencia", main_title))
    story.append(Paragraph("Evaluación exhaustiva de continuidad, voces de personajes y flujo de información (Capítulos 1 al 7)", subtitle))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284C7"), spaceBefore=2, spaceAfter=14))
    
    # 1. Recapitulación Argumental
    story.append(Paragraph("1. Recapitulación Argumental y Cronológica de la Novela", h1_style))
    story.append(Paragraph(
        "La obra desarrolla una trama de <b>hard science fiction</b> donde los descubrimientos de la astrofísica y la ingeniería nuclear "
        "interactúan con la diplomacia internacional y la psicología humana. La línea temporal actual abarca desde el destello de Trinity en 1945 "
        "hasta los preparativos industriales secretos de octubre de 2026.",
        body_style
    ))
    
    # Hitos resumidos
    hitos = [
        ("Capítulo 1: El Amanecer de Alamogordo (16 de julio de 1945)",
         "La detonación atómica <i>Trinity</i> emite un pulso electromagnético que viaja al cosmos. En la Nube de Oort (a 1 año luz), la radiación despierta simultáneamente a la sonda nodriza de la <b>Civilización A</b> (creadora de la SIA protectora) y a la sonda cazadora de la <b>Civilización B</b> (ejecutora del <i>Teorema del Exterminio Preventivo</i>)."),
        ("Capítulo 2: Los Tres Hilos del Ilusionista (Septiembre de 2026)",
         "Ochenta y un años después, tres científicos de élite en crisis investigadora reciben soluciones matemáticas anónimas e impecables firmadas por el Dr. Em Pleh: Girard (CERN, ruido cuántico en CMS), Sarah Lin (MIT, estabilidad MHD en tokamak) y Thomas Wright (ESA, rescate de sonda interplanetaria). Son citados en Manhattan."),
        ("Capítulo 3: La Sala Dos (24 de septiembre de 2026, 10:00 EDT)",
         "Pleh se revela a través de una pantalla como una SIA alienígena en órbita polar (100.000 km). Revela que la máquina de B (<i>Sombra</i>) ha llegado al punto de Lagrange L1 para anular la magnetosfera por interferencia destructiva. Expone la necesidad del contraataque analógico biológico para sortear el Muro de Lorentz."),
        ("Capítulo 4: El Vértigo de las Naciones (24 de septiembre de 2026, mediodía)",
         "Pleh guía a los científicos ante el Secretario General de la ONU, Vassily Ramos. Tras verificar satelitalmente en L1 la firma de radiofrecuencia, Ramos asume la realidad de la crisis, decreta el secreto supremo <b>Alfa Cero</b> y crea el Comité Científico Director."),
        ("Capítulo 5: El Ancla Humana (24 de septiembre de 2026, 13:00 - 16:00 EDT)",
         "Llamadas telefónicas de los científicos bajo el secreto de Estado: Girard con su modélica familia en Ginebra; Sarah asumiendo el distanciamiento irreversible con Mark; Wright añorando la vida sencilla de su hermano y fascinado por el lado humano de Sarah. Ingreso a las 16:00 h en la Sala de Crisis B-4."),
        ("Capítulo 6: La Cámara del Silencio (28 de septiembre de 2026, 19:48 EDT | T - 54 días)",
         "Sesión extraordinaria secreta del Consejo de Seguridad (15 miembros). Pleh comparece como consultor civil y desmonta los recelos militares con datos de satélites rusos y estadounidenses. Expone el <b>Calendario Canónico de Extinción</b> (Fases 1 a 6) y el diseño del doble módulo (MAA/MRD, efecto Quench y cañón Máser)."),
        ("Capítulo 7: La Condición Immedible (8 de octubre de 2026, 13:20 EDT | T - 44 días)",
         "Salto de 10 días. Almuerzo íntimo de Sarah y Thomas en Manhattan (ruptura con Mark, complicidad naciente, culpa del traidor frente a los inocentes). Llegada de Girard conmovido por los planes universitarios de su hijo Julien. Reunión en la Sala B-4 con Ramos: balance industrial favorable, rapiña geopolítica por patentes, selección de los 6 astronautas (MacElroy, Chen Mei, Voronov), desconfianza de los estados mayores hacia el anonimato de Pleh y rumores de movilización exterior.")
    ]
    
    for title, desc in hitos:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", bullet_style))
        
    story.append(Spacer(1, 8))
    
    # 2. Auditoría de Personajes
    story.append(Paragraph("2. Auditoría Psicológica y Coherencia de Personajes", h1_style))
    story.append(Paragraph(
        "Se evaluaron el registro léxico, las motivaciones internas y la consistencia dramática de cada figura clave a lo largo de los siete capítulos:",
        body_style
    ))
    
    personajes_data = [
        [
            Paragraph("Personaje", tbl_header),
            Paragraph("Perfil Canónico", tbl_header),
            Paragraph("Evolución Observada (Caps. 1-7)", tbl_header),
            Paragraph("Diagnóstico", tbl_header)
        ],
        [
            Paragraph("<b>Dr. Em Pleh</b><br/><i>(SIA / Avatar de A)</i>", tbl_cell_bold),
            Paragraph("Riguroso, imperturbable, conciso, melancolía ética hacia lo humano, lenguaje formal sin titubeos.", tbl_cell),
            Paragraph("Se mantiene como una inteligencia aritmética implacable. En Cap. 3 revela la amenaza; en Cap. 4 lidera la diplomacia; en Cap. 6 somete al Consejo de Seguridad con datos fríos. En Cap. 7 actúa como presencia rectora.", tbl_cell),
            Paragraph("<font color='#059669'><b>100% Coherente</b></font><br/>Sin fisuras de registro ni coloquialismos.", tbl_cell)
        ],
        [
            Paragraph("<b>Dra. Sarah Lin</b><br/><i>(MIT - Fusión)</i>", tbl_cell_bold),
            Paragraph("Competitiva, vehemente, directa, volcánica pero con gran resistencia al estrés. Vive por la ciencia.", tbl_cell),
            Paragraph("Pasa de la dureza académica a un proceso de humanización acelerada. En Cap. 5 y 7 asume con tristeza su ruptura con Mark y halla en Thomas su refugio emocional. Muestra culpa por no advertir a sus seres queridos.", tbl_cell),
            Paragraph("<font color='#059669'><b>Muy Coherente</b></font><br/>Evolución orgánica verosímil y profunda.", tbl_cell)
        ],
        [
            Paragraph("<b>Dr. Jean-Luc Girard</b><br/><i>(CERN - Criogenia)</i>", tbl_cell_bold),
            Paragraph("Racionalismo cartesiano puro, escéptico radical, obsesionado con la causalidad. Padre de familia modélico.", tbl_cell),
            Paragraph("Pilar del conflicto moral. Su mente educada para predecir trayectorias se desgarra al fingir ante su hijo Julien, quien planifica su futuro universitario sin saber que la atmósfera colapsará.", tbl_cell),
            Paragraph("<font color='#059669'><b>Sobresaliente</b></font><br/>Mantiene metáforas científicas aun en el dolor.", tbl_cell)
        ],
        [
            Paragraph("<b>Dr. Thomas Wright</b><br/><i>(ESA - Navegación)</i>", tbl_cell_bold),
            Paragraph("Templanza veterana (52 años), pragmatismo operacional, empático, ancla y protector del grupo.", tbl_cell),
            Paragraph("Ejerce de bisagra entre teoría y realidad. En Cap. 6 modera la sesión diplomática; en Cap. 7 lidera la criba de astronautas y protege a Sarah y Girard. Su atracción por Sarah surge de su vulnerabilidad.", tbl_cell),
            Paragraph("<font color='#059669'><b>100% Coherente</b></font><br/>El personaje más sólido y consistente.", tbl_cell)
        ],
        [
            Paragraph("<b>Vassily Ramos</b><br/><i>(Secretario General ONU)</i>", tbl_cell_bold),
            Paragraph("Diplomático prudente y sobrio, transformado en estadista íntegro y custodio ético de toda la especie.", tbl_cell),
            Paragraph("Crecimiento admirable. En Cap. 4 empieza como burócrata cauto; en Cap. 6 preside con solemnidad; en Cap. 7 duerme en un catre del búnker, combate la avaricia de los gobiernos y habla de igual a igual.", tbl_cell),
            Paragraph("<font color='#059669'><b>Excelente</b></font><br/>Líder trágico y de gran talla humana.", tbl_cell)
        ]
    ]
    
    t_pers = Table(personajes_data, colWidths=[80, 125, 185, 97])
    t_pers.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_pers)
    story.append(Spacer(1, 10))
    
    # 3. Flujo de Información
    story.append(Paragraph("3. Auditoría del Flujo de Información (Quién sabe qué)", h1_style))
    story.append(Paragraph(
        "Para evitar filtraciones narrativas de omnisciencia, se verificó el conocimiento exacto de cada estamento:",
        body_style
    ))
    
    info_data = [
        [
            Paragraph("Estamento / Grupo", tbl_header),
            Paragraph("Lo que SABEN", tbl_header),
            Paragraph("Lo que IGNORAN", tbl_header),
            Paragraph("Estado Canónico", tbl_header)
        ],
        [
            Paragraph("<b>Comité Científico</b><br/>(Wright, Sarah, Girard)", tbl_cell_bold),
            Paragraph("Pleh es una SIA alienígena en órbita polar; amenaza de Sombra en L1; cronómetro de Fases 1 a 6; diseño MAA/MRD y efecto Quench.", tbl_cell),
            Paragraph("Ignoran si la psique de los astronautas resistirá el vuelo analógico en L1 y si los gobiernos cooperarán tras la caída de satélites.", tbl_cell),
            Paragraph("<font color='#059669'><b>Impecable</b></font>", tbl_cell)
        ],
        [
            Paragraph("<b>Secretario General</b><br/>(Vassily Ramos)", tbl_cell_bold),
            Paragraph("Amenaza física en L1; plan del doble módulo; que Pleh es una entidad extraterrestre no humana que lo contactó directamente.", tbl_cell),
            Paragraph("Ignora los pormenores de ingeniería profunda de la nave y cómo contener la anarquía civil una vez caiga el secreto en Fase 2.", tbl_cell),
            Paragraph("<font color='#059669'><b>Impecable</b></font>", tbl_cell)
        ],
        [
            Paragraph("<b>Superpotencias</b><br/>(EE.UU., China, Rusia, Consejo Seguridad)", tbl_cell_bold),
            Paragraph("Existe una máquina en L1 desplegando una telaraña superconductora; sus satélites militares confirmaron los datos; necesidad de nave analógica.", tbl_cell),
            Paragraph("<b>IGNORAN que Pleh es una SIA o alienígena.</b> Lo consideran un científico humano clandestino o un hacker de élite. Sospechan que sea un espía rival.", tbl_cell),
            Paragraph("<font color='#059669'><b>Blindado</b></font><br/>Alineado con directriz.", tbl_cell)
        ],
        [
            Paragraph("<b>Opinión Pública</b><br/>(Sociedad civil global)", tbl_cell_bold),
            Paragraph("Comienzan a notar movimientos atípicos de titanio, convoyes y turnos de fábricas; proliferan rumores conspiranoicos de ciberataques bancarios.", tbl_cell),
            Paragraph("Ignoran absolutamente la existencia de Sombra, la anulación del campo magnético y el plazo de gracia biológico.", tbl_cell),
            Paragraph("<font color='#059669'><b>Impecable</b></font>", tbl_cell)
        ]
    ]
    
    t_info = Table(info_data, colWidths=[90, 140, 165, 92])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0369A1")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_info)
    story.append(Spacer(1, 10))
    
    # 4. Puntos de Fricción
    story.append(Paragraph("4. Incoherencias, Desviaciones o Puntos de Fricción Detectados", h1_style))
    story.append(Paragraph(
        "Se señalan tres observaciones técnicas y de continuidad que conviene tener presentes para los próximos capítulos:",
        body_style
    ))
    
    # Alert Box 1
    box1 = create_alert_box(
        "A. Doble archivo de recapitulación en el directorio novela/",
        [
            "En la carpeta <code>novela/</code> conviven dos archivos: <code>recapitulacion.md</code> (14 KB, versión maestra y actualizada con las Reglas 6 y 7) y <code>recapitulación.md</code> (9 KB, con tilde, versión obsoleta).",
            "<b>Riesgo operativo:</b> En sesiones futuras un agente o script podría leer la versión con tilde desactualizada."
        ],
        styles,
        border_color="#D97706",
        bg_color="#FFFBEB"
    )
    story.append(box1)
    story.append(Spacer(1, 6))
    
    # Alert Box 2
    box2 = create_alert_box(
        "B. Lapso temporal de cuatro días entre el Capítulo 5 y el Capítulo 6",
        [
            "Al final del Capítulo 5 (tarde del 24 de septiembre), se menciona que la sesión del Consejo de Seguridad era 'inminente (a cuatro horas)', pero el Capítulo 6 inicia el 28 de septiembre (cuatro días después).",
            "<b>Justificación diegética:</b> Fueron los cuatro días en que el Comité verificó la telemetría de Koronas y Goldstone antes de que Ramos convocara al Consejo. Se recomienda mantener esta coherencia en futuras menciones."
        ],
        styles,
        border_color="#0284C7",
        bg_color="#F0F9FF"
    )
    story.append(box2)
    story.append(Spacer(1, 6))
    
    # Alert Box 3
    box3 = create_alert_box(
        "C. Dosificación del temperamento vehemente de Sarah Lin",
        [
            "En el Capítulo 7 Sarah muestra una gran madurez, empatía y vulnerabilidad íntima. Para evitar que su voz se vuelva excesivamente suave frente a la templanza de Wright, en el Capítulo 8 (cuando comience el trato con militares y astilleros) debe recuperar su habitual mordacidad e intransigencia científica."
        ],
        styles,
        border_color="#059669",
        bg_color="#F0FDF4"
    )
    story.append(box3)
    story.append(Spacer(1, 10))
    
    # 5. Conclusiones
    story.append(Paragraph("5. Conclusiones y Estado del Proyecto", h1_style))
    story.append(Paragraph(
        "• <b>Solidez Global:</b> La novela mantiene un rigor excepcional en ciencia dura (*hard sci-fi*) perfectamente amalgamada con el drama psicológico humano.<br/>"
        "• <b>Ritmo y Tensión:</b> La introducción del <b>Calendario Canónico de Fases</b> en el Capítulo 6 y la sobreimpresión de cuentas atrás en los encabezados (T - 54 días en Cap. 6; T - 44 días en Cap. 7) genera un pulso cinemático que potencia la expectación del lector.<br/>"
        "• <b>Blindaje de Secreto:</b> Queda estrictamente blindado que las superpotencias ignoran el origen extraterrestre/SIA de Pleh, dotando de total credibilidad a la paranoia diplomática de las tres grandes potencias.<br/>"
        "• <b>Camino al Capítulo 8:</b> La estructura está lista para iniciar la fase de ingeniería práctica, el entrenamiento de los 6 astronautas con sistemas manuales y la gestión del inevitable estallido de rumores a medida que se acerque el 21 de noviembre de 2026 (Fase 1: Silencio Magnético).",
        body_style
    ))
    
    doc.build(story, canvasmaker=ReportCanvas)
    print(f"Informe PDF generado con éxito: {output_filename}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_root = os.path.join(base_dir, "Informe_Recapitulacion_y_Auditoria_Coherencia.pdf")
    out_novela = os.path.join(base_dir, "novela", "Informe_Recapitulacion_y_Auditoria_Coherencia.pdf")
    
    generate_report_pdf(out_root)
    shutil.copyfile(out_root, out_novela)
    print(f"Copia sincronizada en: {out_novela}")
