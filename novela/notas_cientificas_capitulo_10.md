# 🔬 Notas Científicas y Guía Técnica: Capítulo 10
## *T +24 a 72 Horas: Colapso Tecnológico Orbital y Lluvia de Chatarra Espacial*

Este documento establece las bases físicas, astrodinámicas y aeroespaciales para narrar con absoluto rigor (*hard sci-fi*) la destrucción de los satélites terrestres, el fallo de los planes de contingencia y la precipitación de fragmentos orbitales sobre la Tierra durante la Fase 2 del colapso magnetosférico ($T+24$ a $72$ horas).

---

## 🛰️ 1. Física de la Destrucción de Microchips en Órbita

Al anularse el campo geomagnético en $T = 0$, los **Cinturones de Radiación de Van Allen** (que atrapaban protones y electrones de alta energía) se disipan en el viento solar. La magnetopausa desaparece. El espacio orbital queda expuesto al flujo directo y sin filtrar de **Partículas Energéticas Solares (SEP)** y **Rayos Cósmicos Galácticos (GCR)**.

### A. Mecanismos Físicos de Fallo en Semiconductores
Los satélites comerciales y civiles (e incluso satélites militares con blindaje parcial) no están diseñados para operar en un entorno interplanetario puro sin magnetosfera protectora:

1. **SEE (Single Event Effects - Efectos de Evento Único):**
   * **SEU (Single Event Upset):** Un protón pesado o ion pesado atraviesa una celda de memoria de silicio, depositando carga por ionización lineal ($LET$). Esto invierte bits en las computadoras de a bordo (OBC).
     * *Efecto operativo:* Corrupción de los relojes atómicos de cuarzo y cesio, alteración de las tablas de efemérides y bucles de reinicio infinito (*watchdog resets*).
   * **SEL (Single Event Latchup):** Un ion energético activa la estructura parásita de tiristor (p-n-p-n) inherente a los circuitos CMOS. Se genera un cortocircuito interno directo entre la alimentación ($V_{DD}$) y tierra ($GND$).
     * *Efecto operativo:* La corriente se dispara súbitamente; si no hay interruptores rápidos de sobrecorriente (*current-limiters*), la pista de silicio se funde térmicamente en microsegundos.
   * **SEGR (Single Event Gate Rupture):** Perforación irreversible del óxido de puerta en transistores MOSFET de potencia por ruptura dieléctrica.
     * *Efecto operativo:* Inutilización de los reguladores de potencia, de los controladores de actuadores de los paneles solares y de las electroválvulas de los motores de combustible.

2. **Carga Profunda en Dieléctricos y Descargas Electrostáticas (Deep Dielectric ESD):**
   * Los electrones relativistas ("electrones asesinos", > 2 MeV) penetran el chasis de aluminio del satélite y se acumulan en aislantes internos (placas de circuitos impresos, aisladores de cables coaxiales).
   * El potencial electrostático supera la rigidez dieléctrica del material ($> 10^7\text{ V/m}$), generando arcos voltaicos espontáneos que queman buses de datos (CAN bus, SpaceWire, MIL-STD-1553).

---

## 🌍 2. Astrodinámica por Regímenes: ¿Por qué LEO Cae y GEO No?

Es fundamental mantener la precisión de la mecánica celeste: **los satélites en órbitas altas no caen inmediatamente a la Tierra.**

```
+-------------------------------------------------------------------------------+
| GEO (35.786 km) & MEO (GPS, 20.200 km)                                        |
| -> Fricción atmosférica = 0.                                                  |
| -> Mueren electrónicamente, pero PERMANECEN en órbita miles de años (Zombies).|
+-------------------------------------------------------------------------------+
                                      |
+-------------------------------------------------------------------------------+
| LEO (Órbita Baja Terrestre: 200 - 1.000 km)                                    |
| -> Constelaciones masivas (Starlink, OneWeb), satélites espía, ISS, Tiangong.  |
| -> Fricción atmosférica violenta + Pérdida de control de actitud (ADCS).      |
| -> DECAIMIENTO ORBITAL ACELERADO Y REENTRADA EN 24 A 72 HORAS.                |
+-------------------------------------------------------------------------------+
```

### A. El "Hinchamiento Termosférico" (*Atmospheric Swell / Drag Spike*)
* La radiación ionizante no filtrada (rayos X solares, UV extremo y viento solar) golpea de lleno la **termosfera** (85 - 600 km).
* La absorción directa de energía calienta la alta atmósfera de $1.000\text{ K}$ a más de $2.500\text{ K}$, expandiendo los gases hacia arriba.
* **Resultado:** La densidad del gas neutro a 300-500 km se multiplica por un factor de **10 a 50**. La atmósfera "muerde" a los satélites con una fuerza de arrastre aerodinámico ($F_D$) descomunal:
  $$F_D = \frac{1}{2} \rho v^2 C_d A$$
  *(donde $\rho$ es la densidad atmosférica, $v \approx 7.8\text{ km/s}$ es la velocidad orbital, $C_d$ es el coeficiente de arrastre $\approx 2.2$, y $A$ es el área de sección transversal).*

### B. Fallo Crítico del Sistema de Control de Actitud (ADCS)
* En LEO, casi todos los satélites emplean **magnetorquers** (bobinas electromagnéticas) para descargar el momento angular acumulado por las ruedas de reacción, interactuando con el campo magnético terrestre.
* **El efecto en T = 0:** Al suprimirse el campo geomagnético, **los magnetorquers dejan de funcionar instantáneamente**.
* Las ruedas de reacción se saturan de momento en pocas órbitas (12-24 horas). Al saturarse, el satélite entra en **rotación caótica incontrolada (*tumbling*)**.
* Los paneles solares dejan de orientarse al filo de avance y se colocan de plano contra el flujo de gas. El área frontal ($A$) se multiplica por 5 o 10. El satélite actúa como un paracaídas roto, precipitando su desorbitado de meses a horas.

---

## 📋 3. El Plan de Contingencia Internacional y sus Puntos de Fractura

Ante la advertencia oficial decretada tras la comparecencia de Ramos (Cap. 8), las agencias espaciales (NASA, ESA, Roscosmos, CNSA, JAXA) y operadores comerciales activaron el **Protocolo Internacional de Desorbitado Controlado y Pasivación**.

### A. En qué consistía el plan
1. **Desorbitado Dirigido a Punto Nemo:** En satélites pesados y estaciones con motores activos, ejecutar un encendido retrógrado ($\Delta v \approx 100\text{ - }250\text{ m/s}$) para fijar el perigeo a $< 50\text{ km}$ sobre el **Polo Oceánico de Inaccesibilidad (Punto Nemo, Pacífico Sur)**, lejos de costas y rutas marítimas.
2. **Elevación a Órbita Cementerio:** En satélites GEO/MEO, gastar el combustible residual para subirlos $300\text{ km}$ por encima del cinturón geoestacionario.
3. **Pasivación de Sistemas:** Agotar las baterías y purgar los tanques de presurización y propelente para evitar que las cargas residuales causen explosiones espontáneas.

### B. Por qué colapsó el plan (Puntos de fallo técnico)
1. **Pérdida de Telemetría y Cadenas de Comando (TT&C):** El bombardeo de SEUs en las estaciones de tierra y en los transpondedores satelitales corrompió los paquetes de telecomando. Miles de órdenes de frenado nunca llegaron o se ejecutaron desincronizadas.
2. **Ignición Asimétrica o Atascamiento de Válvulas:** Transistores que sufrieron *Latchup* (SEL) dejaron abiertas o cerradas las válvulas de combustible a medio encendido. En vez de frenar hacia el Pacífico, el empuje asimétrico desvió la trayectoria de reentrada hacia corredores continentales densamente poblados (Europa, Asia Oriental, Norteamérica).
3. **Explosiones en Cadena por Fragmentación:** Baterías de litio no pasivadas sufrieron cortocircuitos por arcos térmicos, estallando en órbita a 400 km y generando miles de fragmentos de metralla a $8\text{ km/s}$, acelerando la caída de satélites vecinos mediante un **Síndrome de Kessler localizado a baja cota**.

---

## 💥 4. Balística de Reentrada: Qué se Quema y Qué Sobrevive al Impacto

A altitudes entre **80 y 60 km**, el satélite entra en régimen hipersónico libre ($Mach\text{ }20\text{ a }25$). El aire se comprime adiabáticamente formando una onda de choque de plasma a más de **$1.800^\circ\text{C}$ a $2.500^\circ\text{C}$**.

```
+---------------------------------------------------------------------------------+
| ALTITUD: 85 - 65 km (Zona de Disrupción Térmica y Aerodinámica)                 |
|                                                                                 |
| [SE VAPORIZAN AL 100%]:                                                         |
| - Paneles solares de silicio y marcos de aluminio.                              |
| - Estructura primaria y revestimientos de fibra de carbono.                    |
| - Antenas parabólicas y cableado de cobre.                                      |
|                                                                                 |
| [SOBREVIVEN Y LLEGAN AL SUELO (20% a 40% de la masa total)]:                    |
| - Esferas de titanio (Tanques de combustible de hidracina / helio).             |
| - Rotores de acero macizo / tungsteno (Ruedas de reacción).                     |
| - Toberas y cámaras de empuje de Inconel / Niobio.                              |
| - Espejos primarios de berilio (satélites de reconocimiento militar).           |
+---------------------------------------------------------------------------------+
```

### A. Amenazas Específicas de Impacto Terrestre
1. **Bombas Cinéticas de Titanio:**
   * Las esferas de titanio (utilizadas para almacenar propelente o helio presurizante a $300\text{ bar}$) tienen un punto de fusión de **$1.668^\circ\text{C}$** y una geometría aerodinámica hiperestable.
   * Llegan al suelo a velocidades terminales de **$300\text{ a }700\text{ km/h}$**. Una esfera de $80\text{ kg}$ a esa velocidad posee una energía cinética equivalente a varios proyectiles de artillería pesada, capaz de perforar cinco forjados de hormigón armado.
2. **Toxicidad Química de la Hidracina ($N_2H_4$):**
   * Muchos satélites no lograron purgar sus tanques. La hidracina líquida dentro del tanque de titanio no llega a hervir si el tanque permanece sellado durante la reentrada rápida.
   * Al estrellarse contra el suelo, el tanque fractura y libera un aerosol de hidracina pura: vapor hipergólico altamente corrosivo, letal por inhalación a concentraciones de apenas $50\text{ ppm}$, que genera edema pulmonar, quemaduras químicas y muerte masiva en cientos de metros a la redonda.
3. **Riesgo Radiológico (Fuentes RTG):**
   * Aunque la mayoría de satélites LEO son solares, satélites militares rusos antiguos o cargas de espacio profundo en órbitas elípticas cuentan con cápsulas de óxido de plutonio ($Pu\text{-}238$) o generadores termoeléctricos. Su dispersión en aerosol provocaría un evento similar al del *Kosmos 954* en Canadá (1978).

---

## 🚀 5. Interceptación Cinética con Baterías Defensivas (ASAT / ABM)

No se puede derribar un satélite con defensas antiaéreas convencionales (Patriot PAC-3 o S-400 no alcanzan órbitas espaciales; su techo de servicio es de $30\text{ - }35\text{ km}$). La intercepción requiere sistemas balísticos exoatmosféricos.

### A. Sistemas de Armas Involucrados
1. **EE.UU. / OTAN:**
   * **RIM-161 Standard Missile 3 (SM-3 Block IA/IB/IIA):** Desplegados en destructores *Aegis* (cruceros clase Ticonderoga y destructores Arleigh Burke) y emplazamientos terrestres *Aegis Ashore* (Redzikowo en Polonia, Deveselu en Rumanía).
     * *Ojiva:* Vehículo de Muerte Cinética (**KW - Kinetic Warhead**) que choca a velocidad combinada de impacto de **$9\text{ a }11\text{ km/s}$** (*Hit-to-Kill*, sin explosivos).
     * *Precedente histórico real:* Operación *Burnt Frost* (febrero de 2008), donde un SM-3 derribó el satélite espía averiado *USA-193* a $247\text{ km}$ para pulverizar su tanque de hidracina de 450 kg.
   * **THAAD (Terminal High Altitude Area Defense):** Capacidad de intercepción en la frontera endo-exoatmosférica (hasta $150\text{ km}$).
2. **Rusia:**
   * **A-235 Nudol (PL-19):** Sistema móvil de misiles antisatélite exoatmosféricos de ascenso directo con ojiva cinética.
   * **S-500 Prometey (55R6M):** Misil 77N6-N diseñado para interceptar blancos espaciales en LEO baja (hasta $200\text{ km}$).
3. **China:**
   * **SC-19 / Dong Neng-3 (DN-3):** Interceptores exoatmosféricos de energía cinética con guiado infrarrojo de doble banda.

### B. La "Ventana de Perigeo Sucio" (Táctica de Derribo de Emergencia)
* Si las defensas disparan contra un satélite a $400\text{ km}$, el choque crea una nube de 10.000 esquirlas que permanecerán en órbita meses, destruyendo otros satélites.
* **El Protocolo de Derribo Terminal:** Las baterías esperan a que el satélite en caída libre descienda al rango de los **$110\text{ a }140\text{ km}$** (la mesopausa). A esa cota:
  1. El impacto cinético fragmenta el satélite en piezas menores a $5\text{ cm}$.
  2. La atmósfera ya tiene suficiente densidad para frenar instantáneamente las esquirlas.
  3. Los fragmentos se desintegran por fricción térmica en minutos, transformando un proyectil macizo mortal en una inofensiva lluvia de meteoros brillantes sin generar basura orbital permanente.

---

## 🖥️ 6. Dinámica Operativa en la Sala de Crisis B-4

Desde el búnker subterráneo de la ONU, la escena ofrece un contraste brutal entre la fría representación gráfica digital y la devastación física en la superficie:

* **El "Mosaico del Enjambre":** La gran pantalla táctica proyecta el catálogo de NORAD / Space-Track con más de 12.000 trazas orbitales:
  * **Verde:** Satélites respondiendo a telemetría.
  * **Ámbar parpadeante:** Telemetría perdida, actitud en rotación descontrolada (*tumbling*), decaimiento acelerado.
  * **Rojo estroboscópico:** Vectores de reentrada balística inminente con los conos de dispersión elípticos (*reentry footprints*) proyectados sobre los mapas de los cinco continentes.
* **Jean-Luc Girard:** Analiza los coeficientes balísticos $\beta = m / (C_d A)$ y el colapso del plasma. Su mente cartesiana sufre al ver cómo las leyes mecánicas que idolatra se convierten en artillería matemática contra las ciudades.
* **Thomas Wright:** Como veterano de operaciones orbitales de la ESA, rastrea con angustia los intentos fallidos de los operadores de Darmstadt y Houston por enviar el "código de pasivación", viendo cómo los satélites se convierten en ataúdes metálicos.
* **Sarah Lin:** Monitorea la interacción entre la onda de choque magnetohidrodinámica de la termosfera y los picos de voltaje inducidos en las subestaciones terrestres que aún quedan en pie.
* **Vassily Ramos:** Sostiene la línea roja directa con los estados mayores en el Pentágono, Moscú y Pekín. Afronta el dilema supremo de priorizar qué interceptores SM-3 o Nudol se autorizan para salvar refinerías o grandes urbes, y qué regiones periféricas quedan expuestas a la caída de restos.
* **Dr. Em Pleh (SIA):** En su pantalla, calcula los impactos con frialdad milimétrica, advirtiendo con voz sosegada pero inexorable cuáles fragmentos representan una amenaza real para las instalaciones subterráneas de Nevada (Nellis) y China (Sichuan), donde se ensambla el Módulo de Ataque Analógico (MAA).
