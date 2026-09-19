import os
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
            self.drawRightString(A4[0] - 54, A4[1] - 36, "ACTO I: EL DESTELLO ATÓMICO")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, A4[1] - 42, A4[0] - 54, A4[1] - 42)
        
        # Pie de página
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 45, A4[0] - 54, 45)
        
        self.drawString(54, 32, "Capítulo 1: El Amanecer de Alamogordo (Trinity, 16 de julio de 1945)")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(A4[0] - 54, 32, page_str)
        self.restoreState()

def create_quote_box(quote_text, author_text, styles, width=A4[0] - 108):
    q_style = ParagraphStyle(
        'QuoteText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14.5,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=4
    )
    a_style = ParagraphStyle(
        'QuoteAuthor',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#64748B"),
        alignment=2 # Derecha
    )
    content = [
        Paragraph(f"«{quote_text}»", q_style),
        Paragraph(f"— {author_text}", a_style)
    ]
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

def generate_chapter_pdf(output_filename):
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
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=12,
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
    
    story = []
    
    # Cabecera de Portada del Capítulo
    story.append(Paragraph("LA GUERRA DE LA HERENCIA • LIBRO I", super_title_style))
    story.append(Paragraph("Capítulo 1: El Amanecer de Alamogordo", title_style))
    story.append(Paragraph("Trinity: El día en que la Tierra encendió la cerilla del cosmos", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=12))
    
    # -------------------------------------------------------------
    # ESCENA I
    # -------------------------------------------------------------
    story.append(Paragraph("I. La Torre bajo la Tormenta", scene_h2_style))
    story.append(Paragraph("02:35 AM — 16 de julio de 1945 • Paraje de Jornada del Muerto, Desierto de Alamogordo, Nuevo México", scene_meta_style))
    
    story.append(Paragraph(
        "El viento del desierto arrastraba un hedor espeso a creosota mojada y ozono quemado.",
        body_style
    ))
    story.append(Paragraph(
        "En lo alto de la torre de acero de treinta metros, la estructura gemía bajo las ráfagas de una tormenta que nadie había previsto en los partes meteorológicos. El doctor David Miller se sujetó con una mano enguantada a la barandilla de hierro empapada, mientras con la otra sostenía una linterna militar cuyo haz temblaba sobre el vientre de la bestia.",
        body_style
    ))
    story.append(Paragraph(
        "Frente a él reposaba «El Artefacto» (<i>The Gadget</i>).",
        body_style
    ))
    story.append(Paragraph(
        "No parecía el artefacto más caro y letal jamás concebido por la inteligencia humana; parecía un gigantesco erizo de hierro forjado, una esfera negra y bulbosa de la que brotaban decenas de cables coaxiales que se retorcían como tripas negras hacia los detonadores de choque pentolita. En su corazón, una diminuta masa de plutonio-239 del tamaño de una naranja esperaba en equilibrio crítico.",
        body_style
    ))
    story.append(Paragraph(
        "Un relámpago desgarró las nubes bajas, tiñendo el desierto de un azul eléctrico espectral.",
        body_style
    ))
    story.append(Paragraph(
        "—¡Cuidado con ese cable de retorno, Miller! —gritó George Kistiakowsky desde la trampilla de madera, con la voz quebrada por el cansancio y el estruendo del trueno—. Si un rayo impacta en la antena de pararrayos y salta a la caja de disparo, nos evaporaremos antes de que el general Groves termine su café en el campamento base.",
        dialogue_style
    ))
    story.append(Paragraph(
        "Miller tragó saliva. La lluvia le resbalaba por el cuello de la camisa militar, helada. Tenía veintiséis años, un doctorado en física teórica por Princeton y las manos engrasadas con la pasta de sellado de los explosivos de implosión. Había dedicado los últimos dos años de su vida, encerrado en el cañón de Los Álamos, a resolver las ecuaciones diferenciales de cómo comprimir una masa subcrítica de manera perfectamente simétrica hacia su centro. Ahora que la máquina estaba allí, colgada en el vacío sobre un colchón de tela de saco, un terror infantil le atenazaba la garganta.",
        body_style
    ))
    story.append(Paragraph(
        "Abajo, al pie de la torre, los faros de un Dodge militar cortaron la cortina de agua. De la portezuela del copiloto descendió una figura alta, encorvada, envuelta en una gabardina demasiado ancha y coronada por un sombrero de fieltro gris que la lluvia doblaba sobre sus ojos.",
        body_style
    ))
    story.append(Paragraph(
        "Robert Oppenheimer.",
        body_style
    ))
    story.append(Paragraph(
        "El director científico del Proyecto Manhattan levantó la vista hacia la plataforma. Su rostro, consumido por las noches en vela y el consumo incesante de cigarrillos Chesterfield, parecía una calavera esculpida en tiza húmeda. Apenas pesaba cuarenta y cinco kilos. A su lado, con paso firme y pesado de mastín de intendencia, el general Leslie Groves pisoteaba los charcos con las botas de cuero crujiendo de furia.",
        body_style
    ))
    story.append(Paragraph(
        "—¡Oppenheimer! —rugió la voz de Groves a través del megáfono de mano—. ¡El presidente Truman está en Potsdam sentado a la mesa frente a Churchill y Stalin! ¡Necesita saber hoy si tenemos un arma o si le hemos regalado dos mil millones de dólares del contribuyente a un puñado de profesores lunáticos! ¡Ese artefacto tiene que arder antes del amanecer!",
        dialogue_style
    ))
    story.append(Paragraph(
        "Oppenheimer no respondió con la voz militar que Groves esperaba. Simplemente miró hacia el este, donde las nubes negras borraban las estrellas sobre las montañas de Oscuro.",
        body_style
    ))
    story.append(Paragraph(
        "—La naturaleza tiene su propio reloj, general —dijo Oppenheimer con una calma que sonaba a despedida fúnebre—. Si detonamos bajo este aguacero, la lluvia radiactiva caerá sobre nuestros propios búnkeres y liquidará a cada ser vivo en cincuenta millas a la redonda. Esperaremos a las cinco. Si el cielo se abre, partiremos el átomo. Si no, desarmaremos la torre con nuestras propias manos.",
        dialogue_style
    ))
    story.append(Paragraph(
        "Miller ajustó el último terminal de alta impedancia con un destornillador de baquelita. Al rozar el metal frío de la cápsula, sintió una vibración ilusoria, como si el núcleo de plutonio tuviera pulso propio.",
        body_style
    ))
    story.append(Paragraph(
        "Estaban a tres horas de encender un sol en la corteza de la Tierra.",
        body_style
    ))
    
    # -------------------------------------------------------------
    # ESCENA II
    # -------------------------------------------------------------
    story.append(Spacer(1, 4))
    story.append(Paragraph("II. El Humo de la Duda en el Búnker S-10.000", scene_h2_style))
    story.append(Paragraph("04:20 AM — Búnker de Mando a 9 kilómetros al sur del Punto Cero", scene_meta_style))
    
    story.append(Paragraph(
        "A diez mil yardas al sur del Punto Cero —unos nueve kilómetros de distancia—, el búnker de control S-10.000 olía a sudor rancio, café recalentado en latas de conserva y humo denso de tabaco Lucky Strike. Las paredes de hormigón armado y tablones de madera de pino estaban reforzadas con toneladas de tierra del desierto para resistir un cataclismo teórico.",
        body_style
    ))
    story.append(Paragraph(
        "En una esquina, sentado sobre una caja de municiones vacía, el doctor Samuel Allison sostenía el micrófono del sistema de megafonía con los nudillos blancos. En la mesa central, varios físicos se amontonaban alrededor de un tablero donde alguien había garabateado una lista de números con tiza blanca.",
        body_style
    ))
    story.append(Paragraph(
        "—Doscientos dólares a que la onda expansiva incendia el nitrógeno de la atmósfera y el fuego no se detiene hasta hervir el océano Atlántico —dijo una voz arrastrada con marcado acento italiano.",
        dialogue_style
    ))
    story.append(Paragraph(
        "Miller se volvió, secándose los cristales de las gafas con el faldón de la camisa. Quien hablaba era Enrico Fermi. El premio Nobel barajaba un mazo de hojas de papel cuadriculado con una sonrisa burlona que no lograba disimular el temblor de sus párpados.",
        body_style
    ))
    story.append(Paragraph(
        "—¡Cierre la boca, Fermi! —estalló el general Groves desde el umbral, arrojando su impermeable empapado contra una banqueta—. ¡Hay oficiales jóvenes escuchando! ¡Bethe ya demostró hace seis meses que la temperatura de ignición del nitrógeno es matemáticamente inalcanzable!",
        dialogue_style
    ))
    story.append(Paragraph(
        "—Las matemáticas son hermosas sobre una pizarra limpia en Los Álamos, general —replicó Fermi sin inmutarse, encogiéndose de hombros—. Pero jamás hemos sometido la corteza terrestre a sesenta millones de grados kelvin. Nadie ha estado allí para preguntarle al nitrógeno qué opina.",
        dialogue_style
    ))
    story.append(Paragraph(
        "Miller se apartó de la mesa y se acercó a la rendija de observación blindada, donde Oppenheimer permanecía de pie, fumando en silencio con los brazos cruzados.",
        body_style
    ))
    story.append(Paragraph(
        "—Doctor Oppenheimer —susurró Miller, temiendo romper el trance del director—. He verificado los cables de disparo tres veces. Los condensadores están cargados a cinco mil voltios. Si Allison presiona el conmutador, la detonación ocurrirá en una millonésima de segundo.",
        dialogue_style
    ))
    story.append(Paragraph(
        "Oppenheimer expulsó una columna de humo gris que chocó contra el cristal blindado.",
        body_style
    ))
    story.append(Paragraph(
        "—¿Sabe qué me preguntó mi esposa Kitty antes de subir al tren en Lamy, David? —dijo Oppenheimer sin apartar la mirada de la oscuridad exterior—. Me preguntó si debíamos rezar para que funcione o para que sea un completo fracaso.",
        dialogue_style
    ))
    story.append(Paragraph(
        "Miller guardó silencio. Aquella pregunta llevaba días martilleándole las sienes.",
        body_style
    ))
    story.append(Paragraph(
        "—Nuestros muchachos están muriendo a miles en el Pacífico, señor —dijo Miller con voz vacilante, tratando de aferrarse a la justificación oficial que todos repetían como un mantra en los barracones—. Okinawa fue una carnicería. Si este artefacto funciona... la invasión de la isla principal japonesa nunca tendrá que ocurrir. Se salvarán un millón de vidas. La guerra terminará este mismo verano.",
        dialogue_style
    ))
    story.append(Paragraph(
        "Oppenheimer ladeó la cabeza. Sus ojos azules, hundidos en cuencas oscuras, se clavaron en los de su joven pupilo con una lucidez devastadora.",
        body_style
    ))
    story.append(Paragraph(
        "—La guerra terminará, Miller. En eso tiene usted razón. Los japoneses capitularán ante el horror absoluto. Pero este artefacto no se apagará cuando firme la rendición el emperador Hirohito. Lo que estamos a punto de hacer aquí no es construir un arma militar más grande; estamos cambiando la escala física de la civilización. A partir de esta mañana, la humanidad sabrá que posee la llave para encender su propio funeral cósmico. Cualquier tirano, cualquier miedo futuro, se medirá en megatones.",
        dialogue_style
    ))
    story.append(Paragraph(
        "Oppenheimer arrojó la colilla al suelo de tierra y la aplastó con la punta de la bota gastada.",
        body_style
    ))
    story.append(Paragraph(
        "—Dios nos perdone si tenemos éxito.",
        dialogue_style
    ))
    story.append(Paragraph(
        "Un sargento del cuerpo de transmisiones entró corriendo, jadeante, con un papel amarillo en la mano.",
        body_style
    ))
    story.append(Paragraph(
        "—¡Señores! ¡El capitán Stone acaba de recibir el parte de la estación meteorológica! El frente de tormenta se desplaza hacia el norte. El viento en superficie ha caído a cuatro millas por hora. Tenemos luz verde. Repito: ¡luz verde para las cinco y media!",
        dialogue_style
    ))
    story.append(Paragraph(
        "Groves miró su reloj de bolsillo de oro y asintió secamente hacia Allison.",
        body_style
    ))
    story.append(Paragraph(
        "—Que empiece la cuenta atrás.",
        dialogue_style
    ))
    
    # -------------------------------------------------------------
    # ESCENA III
    # -------------------------------------------------------------
    story.append(Spacer(1, 4))
    story.append(Paragraph("III. El Sol de Medianoche", scene_h2_style))
    story.append(Paragraph("05:29:45 AM — Trinchera de Observación, 9 km al sur del Punto Cero", scene_meta_style))
    
    story.append(Paragraph(
        "Afuera, en las zanjas abiertas en la tierra a nueve kilómetros de la torre, los hombres se tumbaron boca abajo en el barro, con los pies apuntando hacia el Punto Cero y las cabezas pegadas al suelo. Miller sostenía un trozo de vidrio oscuro de soldador número diez apretado contra las cuencas de los ojos, sintiendo las pulsaciones de su corazón retumbar en el esternón como un tambor de guerra.",
        body_style
    ))
    story.append(Paragraph(
        "La voz de Allison, transmitida por los altavoces de campaña fijados a los postes de madera, arañaba la atmósfera con cadencia hipnótica:",
        body_style
    ))
    story.append(Paragraph(
        "—<i>Menos sesenta segundos... Cincuenta segundos... Cuarenta...</i>",
        dialogue_style
    ))
    story.append(Paragraph(
        "El silencio que siguió entre los números era sepulcral. El viento se había extinguido por completo. El desierto contenía la respiración bajo una bóveda de nubes desgarradas que comenzaban a teñirse de un gris ceniciento por el este.",
        body_style
    ))
    story.append(Paragraph(
        "—<i>Diez... nueve... ocho... siete... seis... cinco... cuatro... tres... dos... uno...</i>",
        dialogue_style
    ))
    story.append(Paragraph(
        "A las <b>05:29:45</b>, el universo se quebró.",
        body_style
    ))
    story.append(Paragraph(
        "No hubo sonido al principio. La velocidad de la luz no espera a la acústica de los hombres.",
        body_style
    ))
    story.append(Paragraph(
        "A través del cristal blindado de soldador, un destello instantáneo, monstruoso y absoluto devoró la oscuridad. No era una luz dorada ni el fogonazo rojizo de los explosivos convencionales: era un blanco púrpura de una pureza sobrenatural, una incandescencia tan violenta que Miller vio, con nitidez quirúrgica, el esqueleto completo de sus propios dedos proyectado a través de sus párpados apretados.",
        body_style
    ))
    story.append(Paragraph(
        "La noche dejó de existir. Por una fracción de segundo, las crestas de las montañas de Oscuro, a más de veinte millas de distancia, quedaron iluminadas con un detalle más deslumbrante que bajo el mediodía de agosto.",
        body_style
    ))
    story.append(Paragraph(
        "—¡Dios todopoderoso! —gritó alguien en la trinchera contigua, cubriéndose el rostro con ambos brazos.",
        dialogue_style
    ))
    story.append(Paragraph(
        "A los pocos segundos, una ola de calor abrasador barrió las zanjas. No era aire caliente arrastrado por el viento; era radiación térmica pura que golpeó la nuca y las orejas de los hombres como la puerta abierta de una acería industrial a pleno rendimiento, secando instantáneamente el barro de sus uniformes.",
        body_style
    ))
    story.append(Paragraph(
        "Y entonces, cuarenta segundos después del relámpago, llegó el trueno.",
        body_style
    ))
    story.append(Paragraph(
        "La onda de choque no sonó como una explosión: sonó como si la corteza sólida del planeta se hubiera desgarrado de polo a polo. Un bramido telúrico, sordo y colosal que golpeó el pecho de Miller como un puñetazo físico, levantando nubes de arena ardiente y derribando cajas de madera en los terraplenes. El rugido rebotó en los cañones y quebradas del desierto, multiplicándose en un eco infinito que parecía no terminar jamás.",
        body_style
    ))
    story.append(Paragraph(
        "Miller se puso en pie, tambaleándose, y apartó el vidrio protector.",
        body_style
    ))
    story.append(Paragraph(
        "En el lugar exacto donde había estado la torre de acero de treinta metros, ya no quedaba nada. La estructura se había evaporado; la arena del desierto se había fundido en una costra verde, lisa y translúcida de vidrio radiactivo: <i>trinitita</i>.",
        body_style
    ))
    story.append(Paragraph(
        "Sobre el cráter humeante, una colosal columna de fuego y escombros de tres kilómetros de ancho ascendía a velocidades supersónicas hacia el cielo. El hongo atómico se hinchó con colores imposibles: un núcleo naranja brillante envuelto en un velo de gas ionizado de color púrpura y verde esmeralda que perforó las nubes y alcanzó la estratosfera a doce mil metros de altura.",
        body_style
    ))
    story.append(Paragraph(
        "A su lado, Oppenheimer miraba la columna con las manos metidas en los bolsillos de la gabardina. Su boca estaba inmóvil, pero Miller pudo leer en el movimiento de sus labios secos las palabras milenarias del texto sánscrito que el físico repetía en su mente:",
        body_style
    ))
    
    quote_bhagavad = create_quote_box(
        "Si el resplandor de mil soles estallara al unísono en el cielo, sería como el esplendor del Poderoso... Ahora me he convertido en la Muerte, el destructor de mundos.",
        "Bhagavad Gita (XI, 32) — Meditación de J. Robert Oppenheimer",
        styles
    )
    story.append(Spacer(1, 2))
    story.append(quote_bhagavad)
    story.append(Spacer(1, 4))
    
    story.append(Paragraph(
        "A unos metros, el director de la prueba, Kenneth Bainbridge, se volvió hacia Oppenheimer, le puso una mano pesada sobre el hombro y murmuró con voz ronca:",
        body_style
    ))
    story.append(Paragraph(
        "—Robert... a partir de ahora, todos somos unos auténticos hijos de puta.",
        dialogue_style
    ))
    story.append(Paragraph(
        "Los soldados comenzaron a gritar, saltando y abrazándose en el barro, embriagados por el alivio de haber sobrevivido y por la certeza de que la Segunda Guerra Mundial estaba sentenciada. Groves ya redactaba febrilmente el telegrama cifrado para el presidente Truman en Alemania.",
        body_style
    ))
    story.append(Paragraph(
        "Nadie en aquel desierto miraba más allá de las nubes.",
        body_style
    ))
    story.append(Paragraph(
        "Nadie imaginaba que la verdadera detonación no se había quedado en la arena de Nuevo México.",
        body_style
    ))
    
    # -------------------------------------------------------------
    # ESCENA IV
    # -------------------------------------------------------------
    story.append(Spacer(1, 4))
    story.append(Paragraph("IV. El Despertar en la Nube de Oort", scene_h2_style))
    story.append(Paragraph("05:30:00 AM — En los confines silenciosos del Sistema Solar", scene_meta_style))
    
    story.append(Paragraph(
        "La atmósfera de la Tierra retuvo la onda expansiva del aire y las cenizas de la arena triturada. Pero las leyes de la física electromagnética no conocen fronteras planetarias.",
        body_style
    ))
    story.append(Paragraph(
        "En el instante exacto de la fisión, el núcleo de plutonio liberó un pulso invisible de radiación de alta energía y firmas isotópicas artificiales que perforó la ionosfera terrestre y se expandió hacia la negrura del vacío a trescientos mil kilómetros por segundo:<br/>"
        "• A las <b>05:29:47 AM</b>, la onda barrió el regolito gris y silencioso de la Luna.<br/>"
        "• A las <b>05:44 AM</b>, cruzó el cielo desierto de Marte.<br/>"
        "• A las <b>06:15 AM</b>, atravesó la inmensidad tormentosa de Júpiter.<br/>"
        "• A las <b>07:05 AM</b>, acarició los anillos de hielo de Saturno.<br/>"
        "• A las <b>09:42 AM</b>, rebasó la órbita de Neptuno y se internó en el frío perpetuo del Cinturón de Kuiper.",
        body_style
    ))
    story.append(Paragraph(
        "Y horas más tarde, tras devorar miles de millones de kilómetros por el desierto cósmico, aquel suspiro nacido en Alamogordo alcanzó la última frontera de nuestro sistema planetario: la <b>Nube de Oort</b>.",
        body_style
    ))
    story.append(Paragraph(
        "Allí, a casi un año luz de distancia, el Sol no es más que una aguja de luz lejana, un punto brillante e indiferente suspendido entre millones de estrellas inmóviles. Allí no hay estaciones, ni atmósfera, ni amaneceres. Solo reina un océano inconmensurable de hielo y silencio: una llanura insondable donde vagan miles de millones de cometas errantes, bloques ciclópeos de metano, amoníaco y agua petrificada a doscientos setenta grados bajo cero. Un reino donde nada había cambiado desde el nacimiento de los planetas.",
        body_style
    ))
    story.append(Paragraph(
        "Y sin embargo, una de aquellas rocas no era enteramente natural.",
        body_style
    ))
    story.append(Paragraph(
        "Incrustada en el corazón de un cometa colosal de quince kilómetros de diámetro, descansaba una presencia que no pertenecía a la geología del sistema solar. Era una estructura ciclópea de varios cientos de metros de longitud, un fuselaje de curvas complejas y elegantes forjado en una aleación desconocida, sin costuras, remaches ni soldaduras. Su superficie poseía la textura del grafito pulido y la capacidad milagrosa de absorber cualquier haz de luz que incidiera sobre ella, fundiéndose por completo con la negrura del vacío.",
        body_style
    ))
    story.append(Paragraph(
        "Llevaba medio millón de años durmiendo bajo una costra de escarcha cósmica. Durante eones, su temperatura interna había sido exactamente la misma que la del vacío interestelar: inerte, muda, fría como la piedra.",
        body_style
    ))
    story.append(Paragraph(
        "Entonces, la onda invisible nacida en Alamogordo cruzó la distancia.",
        body_style
    ))
    story.append(Paragraph(
        "No hubo sonido ni viento en el vacío, pero una alteración electromagnética antinatural, un pulso nítido cargado con la firma de núcleos atómicos divididos por el ingenio humano, acarició los sensores pasivos enterrados en la piel de la nave dormida.",
        body_style
    ))
    story.append(Paragraph(
        "El coloso reaccionó.",
        body_style
    ))
    story.append(Paragraph(
        "Fue un despertar lento, de una solemnidad sobrecogedora. Bajo la costra de hielo negro, una red de filamentos luminosos, tenues como venas de zafiro líquido, comenzó a pulsar a lo largo de las hendiduras geométricas del fuselaje. El hielo que la aprisionaba desde hacía quinientos mil años crujió con una serie de fracturas limpias y silenciosas, desprendiendo nubes de esquirlas cristalinas que flotaron a la deriva en la microgravedad de la roca.",
        body_style
    ))
    story.append(Paragraph(
        "En la proa de la nave nodriza, una sección del blindaje se deslizó hacia adentro sin fricción ni chasquidos mecánicos. De sus entrañas protegidas emergió con lentitud majestuosa una segunda embarcación: una nave estilizada, delgada como un estilete de obsidiana, con líneas puras y afiladas que parecían recortar el fondo estrellado a su paso. No expulsaba fuego ni humo de combustión; al desprenderse de la matriz madre, una leve distorsión en el espacio curvó fugazmente la luz de las constelaciones tras su popa. La pequeña nave aguja enderezó su rumbo con precisión matemática, enfiló su proa hacia el minúsculo destello dorado del Sol en la lejanía y comenzó a deslizarse hacia el interior del sistema planetario, iniciando un largo y paciente viaje solitario.",
        body_style
    ))
    story.append(Paragraph(
        "Pero en aquel rincón helado del cosmos no había un solo espectador durmiente.",
        body_style
    ))
    story.append(Paragraph(
        "A menos de dos millones de kilómetros de allí, en otro cometa que flotaba en la misma penumbra, aguardaba otra presencia.",
        body_style
    ))
    story.append(Paragraph(
        "Era una silueta oscura, de geometría angulosa y agresiva, agazapada en una grieta profunda del hielo como un depredador camuflado en la nieve. Llevaba exactamente el mismo medio millón de años allí, sepultada en el frío absoluto, observando a la primera máquina sin tocarla, sin emitir jamás una sola señal de radio. Había permanecido inmóvil durante eras con la paciencia infinita de quien sabe con certeza matemática que la presa terminará por moverse.",
        body_style
    ))
    story.append(Paragraph(
        "En el instante exacto en que la nave aguja se separó del cometa nodriza y su leve distorsión rasgó el vacío, la segunda criatura mecánica abrió sus ojos en la oscuridad.",
        body_style
    ))
    story.append(Paragraph(
        "En su superficie no hubo filamentos azules ni destellos de belleza. Con una frialdad implacable, la nave cazadora retrajo sus anclajes de roca helada. Su fuselaje oscuro se desacopló de la pared del cometa mediante un impulso mudo de gas invisible. Giró sobre su eje con una precisión geométrica letal y se colocó en la misma trayectoria del viajero, acelerando a una distancia calculada, fundiéndose en la negrura tras él como una sombra adherida a su espalda.",
        body_style
    ))
    story.append(Paragraph(
        "Ningún telescopio en la Tierra vio nada.",
        body_style
    ))
    story.append(Paragraph(
        "Nadie en el desierto de Alamogordo, mientras brindaban con café caliente y celebraban el fin inminente de la guerra bajo el humo del hongo atómico, podía sospechar que allá afuera, en el patio trasero del sistema solar, dos voluntades ancestrales acababan de ponerse en marcha.",
        body_style
    ))
    story.append(Paragraph(
        "Una viajaba hacia el hogar de los seres humanos con un propósito desconocido.<br/>"
        "Y la otra la seguía paso a paso en la sombra, armada con el silencio del cazador.",
        body_style
    ))
    
    doc.build(story, canvasmaker=BookCanvas)
    print(f"Capítulo 1 actualizado y generado con éxito en PDF: {output_filename}")

if __name__ == "__main__":
    root_pdf = os.path.abspath("Capitulo_1_El_Amanecer_de_Alamogordo.pdf")
    novela_pdf = os.path.abspath(os.path.join("novela", "Capitulo_1_El_Amanecer_de_Alamogordo.pdf"))
    
    generate_chapter_pdf(root_pdf)
    shutil.copy2(root_pdf, novela_pdf)
    print(f"Copia sincronizada en: {novela_pdf}")
