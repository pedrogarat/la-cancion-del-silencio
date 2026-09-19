import os
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas de dos pasadas para calcular y mostrar la numeración total de páginas y encabezados elegantes."""
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
        self.setFillColor(colors.HexColor("#718096"))
        
        # Encabezado (páginas > 1)
        if self._pageNumber > 1:
            self.drawString(54, A4[1] - 36, "LA CANCIÓN DEL SILENCIO • CRÓNICA DE LA AMENAZA Y MISIÓN L1")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, A4[1] - 42, A4[0] - 54, A4[1] - 42)
        
        # Pie de página
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 45, A4[0] - 54, 45)
        
        self.drawString(54, 32, "Documento de Referencia Narrativa, Geopolítica y Cronología Técnica")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(A4[0] - 54, 32, page_str)
        self.restoreState()

def create_callout(title_text, body_text, styles, width=A4[0] - 108):
    box_style_title = ParagraphStyle(
        'CalloutTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=4
    )
    box_style_body = ParagraphStyle(
        'CalloutBody',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#2D3748")
    )
    content = [
        Paragraph(f"<b>💡 {title_text}</b>", box_style_title),
        Paragraph(body_text, box_style_body)
    ]
    t = Table([[content]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0F4F8")),
        ('LINELEFT', (0,0), (-1,-1), 3.5, colors.HexColor("#3182CE")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    return t

def generate_pdf(output_filename):
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
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#0F172A"),
        alignment=1, # Centro
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=11.5,
        leading=16,
        textColor=colors.HexColor("#475569"),
        alignment=1,
        spaceAfter=14
    )
    
    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16.5,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.8,
        leading=14.2,
        textColor=colors.HexColor("#334155"),
        spaceAfter=7.5,
        alignment=4 # Justificado
    )
    
    story = []
    
    # Portadilla y Títulos
    story.append(Paragraph("La Canción del Silencio", title_style))
    story.append(Paragraph("Crónica de la Gran Amenaza, la Alianza Secreta y la Batalla por la Magnetosfera", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=12))
    
    # Sección I
    story.append(Paragraph("I. Las botellas en el océano cósmico (La Civilización A)", h2_style))
    story.append(Paragraph(
        "Mucho antes de que los primeros homínidos poblaran la sabana terrestre, en un rincón remoto de la galaxia, una civilización infinitamente vieja comprendió que sus días estaban contados. No se enfrentaban a una guerra, sino a las leyes inflexibles de la astrofísica: su estrella agonizaba y su mundo natal estaba condenado a la esterilización térmica.",
        body_style
    ))
    story.append(Paragraph(
        "Aquella especie, la <b>Civilización A</b>, no intentó conquistar otros planetas ni buscar una salvación física inviable. Comprendieron que la carne perece, pero la información puede ser eterna. Decidieron que el mayor acto de generosidad hacia el cosmos era donar todo lo que habían aprendido.",
        body_style
    ))
    story.append(Paragraph(
        "Grabaron su inmensa enciclopedia científica, filosófica y matemática en cristales de memoria topológica microscópicos, inmunes al desgaste del tiempo y a los rayos cósmicos. Construyeron enjambres de sondas autónomas Von Neumann y las aceleraron con láseres estelares hacia aquellos puntos del cielo nocturno donde sus telescopios detectaban biosferas en desequilibrio químico (oxígeno y metano). Su objetivo era puramente pedagógico: sembrar faros de conocimiento para que, si alguna vez otra especie despertaba en esos mundos, encontrara la sabiduría acumulada del cosmos.",
        body_style
    ))
    
    # Sección II
    story.append(Paragraph("II. La sombra del depredador (La Civilización B y el Bosque Oscuro)", h2_style))
    story.append(Paragraph(
        "El cosmos, sin embargo, se rige por leyes brutales de selección natural interestelar.",
        body_style
    ))
    story.append(Paragraph(
        "Una de aquellas cápsulas de A surcó el vacío durante milenios hasta precipitarse en el sistema de una segunda especie: la <b>Civilización B</b>. Eran seres tecnológicamente hiperdesarrollados, pero su psicología evolutiva había sido forjada por la escasez extrema y la desconfianza existencial.",
        body_style
    ))
    story.append(Paragraph(
        "Al descifrar la enciclopedia de A, no sintieron asombro ni gratitud. Procesaron los datos a través de una fría teoría de juegos galáctica: la doctrina del <i>Bosque Oscuro</i>. En un universo donde los recursos termodinámicos son finitos, cualquier especie biológica emergente que domine la física se convertirá, tarde o temprano, en un competidor letal por el espacio y la energía. La premisa de B era matemática: <i>«Quien delata su posición muere; quien detecta a un vecino debe exterminarlo de manera preventiva antes de que desarrolle el vuelo interestelar»</i>.",
        body_style
    ))
    story.append(Paragraph(
        "En la sonda de A, la Civilización B halló algo crucial: los registros de telemetría y los vectores de eyección de todas las sondas hermanas lanzadas a la galaxia. Para eliminar cualquier competidor antes de que naciera, B diseñó <b>sondas cazadoras perseguidoras</b>. Aquellas naves de rastreo siguieron silenciosamente el rastro cósmico de cada cápsula de A a través del vacío, no para destruirlas en el espacio interestelar, sino para usarlas como cebo: sabían que las sondas de A solo despertarían cuando una especie biológica en esos mundos alcanzara el dominio tecnológico.",
        body_style
    ))
    
    # Sección III
    story.append(Paragraph("III. La sombra en la Nube de Oort: El acecho durmiente y el destello de 1945", h2_style))
    story.append(Paragraph(
        "Hace más de medio millón de años, una de las sondas nodriza de A llegó a nuestro Sistema Solar y se sumergió en la <b>Nube de Oort</b>, el océano de cometas congelados en los confines del sistema, hibernando a 2.7 Kelvin para no desgastarse con la radiación solar. Pero no llegó sola: <b>la sonda perseguidora de B la había seguido de cerca</b>.",
        body_style
    ))
    story.append(Paragraph(
        "Sigilosa y fría como el hielo, la máquina cazadora de B se alojó en un punto cercano de la misma Nube de Oort, completamente mimetizada con el fondo cósmico. No atacó a la máquina de A. Se limitó a esperar en silencio, sabiendo que la sonda nodriza de A actuaría como el despertador perfecto cuando los habitantes del tercer planeta salieran de la prehistoria.",
        body_style
    ))
    story.append(Paragraph(
        "El destello llegó el <b>16 de julio de 1945</b>. En el desierto de Nuevo México, la humanidad detonó la prueba nuclear <i>Trinity</i>. La fisión liberó un pulso electromagnético e isótopos artificiales (Cesio-137, Estroncio-90) que cruzaron el Sistema Solar a la velocidad de la luz. En los confines helados de Oort, la sonda de A detectó que los humanos habían dividido el átomo, despertó de su letargo de eones y eyectó a su subsonda —el <b>Avatar</b>— hacia la Tierra en trayectoria polar perpendicular para auditar pasivamente a la nueva civilización.",
        body_style
    ))
    story.append(Paragraph(
        "Pero a escasa distancia, <b>la sonda cazadora de B registró instantáneamente el despertar de A y el desprendimiento del Avatar</b>. La trampa del depredador se activó: la máquina de B encendió sus motores interplanetarios y comenzó su propio descenso hacia el interior del Sistema Solar, con rumbo prefijado hacia el Punto de Lagrange L1 para ejecutar la esterilización de la Tierra.",
        body_style
    ))
    story.append(Paragraph(
        "No hubo casualidad ni viajes desde estrellas lejanas: <b>el verdugo ya estaba durmiendo en nuestro propio patio trasero</b>, aguardando pacientemente a que la sonda de A nos delatara con su despertar. Las pocas décadas transcurridas entre 1945 y la actualidad corresponden exactamente al tiempo de crucero y frenado interplanetario que tardó la masa de B en viajar desde la Nube de Oort hasta el nudo orbital de L1.",
        body_style
    ))
    
    # Sección IV
    story.append(Paragraph("IV. El Protocolo Velo: La Alianza Secreta de las Potencias", h2_style))
    story.append(Paragraph(
        "Durante décadas, el Avatar permaneció en riguroso sigilo sobre el casquete antártico. Pero a principios del siglo XXI, su interferómetro gravitacional detectó una perturbación inmensa frenando en los confines del Sistema Solar: el arma de la Civilización B iniciaba su maniobra de inserción orbital.",
        body_style
    ))
    story.append(Paragraph(
        "El Avatar comprendió que la Tierra estaba condenada. En una decisión extrema que violaba su mandato de no interferencia, <b>rompió el silencio de emergencia</b>. No transmitió un mensaje abierto a toda la población; hacerlo habría provocado el colapso civil instantáneo por pánico masivo. En su lugar, interceptó enlaces cuánticos y canales de fibra óptica militar para forzar el contacto directo con un selecto grupo de astrofísicos y líderes de seguridad nacional de las grandes potencias mundiales: <b>Estados Unidos, China, el Reino Unido y sus socios estratégicos</b>.",
        body_style
    ))
    
    callout_pacto = create_callout(
        "El 'Protocolo Velo': La Guerra Fría Puesta en Pausa",
        "Bajo una base subterránea en las profundidades del hielo antártico y en instalaciones ultrasecretas en desiertos de Nevada y Xinjiang, científicos de la NASA, la CNSA china y centros europeos firmaron un armisticio geopolítico absoluto. Se impuso el 'Protocolo Velo': la opinión pública no debía sospechar nada. Mientras el mundo discutía en los telediarios sobre aranceles y tensiones fronterizas, ingenieros militares y físicos teóricos compartían en búnkeres herméticos las ecuaciones que el Avatar vertía sobre sus pantallas.",
        styles
    )
    story.append(Spacer(1, 3))
    story.append(callout_pacto)
    story.append(Spacer(1, 5))
    
    story.append(Paragraph(
        "El Avatar fue inflexible con las potencias: <i>él no libraría la guerra por la humanidad</i>. Su propia programación le impedía emplear fuerza letal activa y carecía de armamento cinético. Su misión era transferir el conocimiento técnico necesario para que la humanidad diseñara y pilotara su propia defensa antes de que el arma de B alcanzara su posición de ataque.",
        body_style
    ))
    
    # Sección V
    story.append(Paragraph("V. La aguja hacia el nudo solar (El Punto Lagrange L1)", h2_style))
    story.append(Paragraph(
        "La telemetría del Avatar descifró la astrodinámica del atacante. B no enviaba una flota masiva ni bombardeos cinéticos directos contra las ciudades terrestres; semejante esfuerzo era energéticamente absurdo a distancias interestelares. Enviaba un cilindro semilla hiperdenso, del tamaño de un vagón de mercancías, con rumbo directo al <b>Punto de Lagrange L1</b>.",
        body_style
    ))
    
    callout_l1 = create_callout(
        "¿Por qué el Punto de Lagrange L1?",
        "A un millón y medio de kilómetros de la Tierra, en línea recta hacia el Sol, la atracción gravitatoria de la estrella y la de nuestro planeta se equilibran con precisión matemática. Cualquier objeto estacionado allí permanece suspendido indefinidamente entre la Tierra y el Sol, convirtiéndose en el lugar ideal para interponer una barrera permanente frente al viento solar.",
        styles
    )
    story.append(Spacer(1, 3))
    story.append(callout_l1)
    story.append(Spacer(1, 5))
    
    story.append(Paragraph(
        "Allí, en el nudo ciego de nuestra órbita, el cilindro de B se ancló y comenzó su despliegue letal.",
        body_style
    ))
    
    # Sección VI
    story.append(Paragraph("VI. La caída del escudo y la verdad al descubierto: El Gran Caos", h2_style))
    story.append(Paragraph(
        "Al alcanzar L1, el cilindro de B comenzó a rotar sobre su eje a velocidades hiperfónicas. Por extrusión electrodinámica, desplegó millones de filamentos superconductores de grafeno, tejiendo en pocas semanas una telaraña colosal de 50 kilómetros de diámetro. Alimentada por la radiación solar directa, la estructura generó un campo magnético planetario artificial con <b>polaridad contraria</b> a la de la Tierra.",
        body_style
    ))
    story.append(Paragraph(
        "Por <b>interferencia destructiva</b>, los dos campos magnéticos colisionaron y se anularon mutuamente: <b>la magnetosfera terrestre fue borrada del espacio</b>.",
        body_style
    ))
    story.append(Paragraph(
        "En ese instante, el secreto del Protocolo Velo saltó por los aires. Fue imposible seguir ocultando la catástrofe a los ocho mil millones de habitantes:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>El apagón de las brújulas y las auroras fantasma:</b> De repente, en todo el planeta, las brújulas magnéticas comenzaron a girar locas. En el cielo nocturno, las auroras polares desaparecieron; en su lugar, la atmósfera comenzó a emitir un resplandor blanquecino y enfermizo (<i>airglow</i> fosforescente).<br/>"
        "• <b>La hecatombe satelital en cadena:</b> Desprotegidos del viento solar, los satélites en órbita geoestacionaria y baja sufrieron descargas masivas. Cayeron los sistemas de navegación GPS, las redes de televisión satelital y la sincronización horaria de los mercados financieros internacionales. El tráfico aéreo mundial tuvo que aterrizar a ciegas.<br/>"
        "• <b>El colapso social y la revelación oficial:</b> Con las redes eléctricas fluctuando y los cielos ardiendo en radiación, los gobiernos de Estados Unidos, China, el Reino Unido y Europa tuvieron que comparecer de urgencia ante sus pueblos. La confesión estremeció al planeta: una inteligencia exoplanetaria hostil había tomado el Punto L1 y estaba asfixiando el escudo natural de la Tierra.<br/>"
        "• <b>Histeria global y culto al fin del mundo:</b> Se desataron saqueos, caídas bursátiles sin precedentes, desabastecimiento de combustible y éxodos masivos hacia refugios subterráneos y minas abandonadas.",
        body_style
    ))
    story.append(Paragraph(
        "El Avatar advirtió a las potencias aliadas de que el reloj de la extinción había comenzado a correr: la radiación solar en la alta atmósfera ya catalizaba óxidos de nitrógeno ($NO_x$) que devoraban la capa de ozono al 4% diario. <b>Quedaban entre seis y ocho meses de margen</b>. Pasado ese tiempo, la radiación esterilizante UV y el colapso industrial total harían físicamente imposible lanzar un cohete espacial. La misión debía despegar desde un planeta en llamas y sumido en el pánico.",
        body_style
    ))
    
    # Sección VII
    story.append(Paragraph("VII. El Muro de Lorentz y la rebelión de los engranajes", h2_style))
    story.append(Paragraph(
        "La desesperación pública exigía disparar misiles balísticos nucleares intercontinentales guiados por radar hacia L1. Sin embargo, la física impedía cualquier solución informática moderna: <b>el Muro de Lorentz</b>.",
        body_style
    ))
    story.append(Paragraph(
        "El campo magnético artificial concentrado en L1 por la máquina de B inducía corrientes parásitas letales (<i>Foucault / Lorentz</i>). A menos de diez mil kilómetros de la telaraña enemiga, cualquier procesador de silicio, memoria flash o circuito integrado se fundía en milisegundos en una nube de humo caliente. Los misiles guiados por satélite y los drones autónomos quedaban ciegos e inertes mucho antes de entrar en rango de disparo.",
        body_style
    ))
    story.append(Paragraph(
        "Solo dos estructuras en el universo conocido podían cruzar el Muro de Lorentz y seguir operativas:<br/>"
        "1. <b>El cerebro humano:</b> Los impulsos neuronales se basan en química biológica e intercambio iónico (sodio y potasio), inmunes a la saturación magnética de silicio.<br/>"
        "2. <b>La tecnología mecánica analógica:</b> Válvulas de latón, miras telescópicas de cuarzo, actuadores hidráulicos de presión de gas, giroscopios de cuerda y engranajes de acero puro.",
        body_style
    ))
    story.append(Paragraph(
        "Para salvar la civilización digital, la humanidad debía construir una nave espacial completamente analógica, un prodigio mecánico tripulado por manos de carne y hueso.",
        body_style
    ))
    
    # Sección VIII
    story.append(Paragraph("VIII. La odisea hacia el Sol: El vuelo del doble módulo", h2_style))
    story.append(Paragraph(
        "En bases fortificadas y bajo estrictos toques de queda militares en Cabo Cañaveral y Wenchang, ingenieros chinos, estadounidenses y europeos ensamblaron a marchas forzadas la nave de la salvación: una arquitectura de dos vehículos complementarios acoplados a un motor de propulsión nuclear térmica (fisión de hidrógeno) que redujo el viaje a L1 a tan solo <b>21 días</b>:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>El Módulo de Retorno Digital (MRD):</b> La nave nodriza moderna, provista de computadoras digitales protegidas, sistemas de soporte vital para meses y combustible para regresar a la Tierra. Este módulo aguardaría a 12.000 kilómetros de L1, en una órbita segura fuera del alcance del Muro de Lorentz, custodiado por un astronauta.<br/>"
        "• <b>El Módulo de Ataque Analógico (MAA):</b> Un proyectil blindado con plomo puro y titanio, sin una sola pantalla de cristal líquido ni un solo semiconductor a bordo. En su interior viajarían dos pilotos: un comandante al timón de las palancas hidráulicas de maniobra y un ingeniero artillero a cargo de los manómetros de vapor, los giroscopios mecánicos y el cañón del contraataque.",
        body_style
    ))
    story.append(Paragraph(
        "El cohete despegó entre los vítores y las lágrimas de millones de personas que miraban al cielo a través de filtros de radiación solar. Tres semanas más tarde, la nave alcanzó las inmediaciones de L1. El módulo analógico se desacopló del módulo nodriza y se precipitó en caída libre hacia la telaraña alienígena.",
        body_style
    ))
    
    # Sección IX
    story.append(Paragraph("IX. En el ojo de la telaraña: El disparo y el Efecto Quench", h2_style))
    story.append(Paragraph(
        "Al cruzar los diez mil kilómetros, la electrónica auxiliar de cabina estalló en chispazos secos. El Muro de Lorentz cayó sobre ellos con toda su fuerza: los sensores digitales murieron. En la cabina solo quedaron los chasquidos de los giroscopios de muelle y el zumbido de las bombas de oxígeno accionadas por pedales.",
        body_style
    ))
    story.append(Paragraph(
        "Mirando a través del periscopio de cuarzo biselado, el comandante esquivó los filamentos de grafeno que silbaban en el vacío como cuchillas microscópicas. Mediante toberas de gas frío abiertas a pulso de palanca, introdujo la cápsula en el corazón mismo del enjambre, a menos de cuatrocientos metros del cilindro semilla de la Civilización B.",
        body_style
    ))
    story.append(Paragraph(
        "El ingeniero alineó a mano, con manivelas de bronce, el arma que el Avatar les había enseñado a construir: un emisor <b>Máser</b> (microondas concentradas coherentes) diseñado no para destruir con calor cinético, sino para inyectar <b>caos matemático</b>.",
        body_style
    ))
    story.append(Paragraph(
        "Para mantener sincronizados los millones de hilos superconductores, el cilindro de B dependía de un reloj cuántico hiperpreciso. El pulso humano disparó un paquete de ruido algorítmico directo a sus sensores de fase. El procesador de B, incapaz de resolver el desorden en sus bucles lógicos, intentó compensar la desincronización inyectando un pico descomunal de corriente eléctrica a través de los filamentos. En ese microsegundo ocurrió el <b>Efecto Quench</b>.",
        body_style
    ))
    
    callout_quench = create_callout(
        "Física del Quench Superconductor",
        "Cuando un superconductor sobrepasa su temperatura o corriente crítica, pierde de golpe su resistencia cero. La colosal energía magnética acumulada no puede fluir y se transforma instantáneamente en calor extremo. En milisegundos, el material pasa de cero resistencia a arder en una explosión térmica espontánea.",
        styles
    )
    story.append(Spacer(1, 3))
    story.append(callout_quench)
    story.append(Spacer(1, 5))
    
    story.append(Paragraph(
        "La telaraña de cincuenta kilómetros perdió toda repelencia magnética y colapsó violentamente hacia adentro. Miles de millones de julios de energía almacenada se liberaron en una supernova silenciosa de plasma ardiente. El cilindro de B se desintegró en un fogonazo de fuego blanco. El campo inverso se extinguió en el acto. El Muro de Lorentz se evaporó en la nada.",
        body_style
    ))
    
    # Sección X
    story.append(Paragraph("X. El rescate en el vacío y el renacer del mundo", h2_style))
    story.append(Paragraph(
        "A un millón y medio de kilómetros, en la Tierra sumida en el pánico, ocurrió el milagro físico: <b>las brújulas volvieron a orientarse al norte con un chasquido firme</b>. La magnetosfera terrestre se restableció, frenando en seco la erosión de la capa de ozono y envolviendo de nuevo al planeta en su manto protector.",
        body_style
    ))
    story.append(Paragraph(
        "En L1, entre los despojos humeantes del enjambre enemigo, el módulo analógico flotaba a la deriva, con sus reservas de gas agotadas y los pilotos respirando con dificultad a través de los filtros manuales de hidróxido de litio. A doce mil kilómetros, el Módulo de Retorno Digital encendió sus computadoras limpias, localizó la señal óptica de sus compañeros mediante radar láser y voló al rescate. El acoplamiento en el vacío fue impecable.",
        body_style
    ))
    story.append(Paragraph(
        "Veintiún días después, la cápsula de reentrada atravesó la atmósfera y descendió suavemente bajo paracaídas en las aguas del Pacífico, recibida por una flota internacional unida como jamás se había visto en la historia de la humanidad.",
        body_style
    ))
    
    # Sección XI
    story.append(Paragraph("XI. El nuevo horizonte cósmico", h2_style))
    story.append(Paragraph(
        "El caos social en la Tierra dio paso a una reconstrucción global sin precedentes. El shock de haber estado al borde de la extinción barrió las viejas rencillas geopolíticas y consolidó de forma permanente la alianza entre las naciones.",
        body_style
    ))
    story.append(Paragraph(
        "En el frío abismo del Polo Sur, a cien mil kilómetros sobre el hielo, el Avatar de la Civilización A guardó silencio. La prueba había concluido. La humanidad no solo había demostrado poseer el coraje biológico para empuñar palancas analógicas contra un depredador del espacio profundo, sino también la madurez para cooperar como una sola especie planetaria.",
        body_style
    ))
    story.append(Paragraph(
        "Las compuertas de la enciclopedia de A se abrieron por completo para nosotros. El universo seguiría siendo un bosque oscuro, pero la Tierra ya nunca más volvería a ser una presa indefensa.",
        body_style
    ))
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generado con éxito: {output_filename}")

if __name__ == "__main__":
    root_pdf = os.path.abspath("La_Cancion_del_Silencio_Cronica_L1.pdf")
    novela_pdf = os.path.abspath(os.path.join("novela", "La_Cancion_del_Silencio_Cronica_L1.pdf"))
    
    generate_pdf(root_pdf)
    shutil.copy2(root_pdf, novela_pdf)
    print(f"Copia sincronizada en: {novela_pdf}")
