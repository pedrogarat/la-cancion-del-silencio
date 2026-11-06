# Registro de Avance de la Novela: "La Canción del Silencio"

> **Dirección Creativa:** Pedro Garat  
> **Estado:** Novela Completa (Capítulos 1 al 25 concluidos) — Edición Oficial para Imprenta Compilada  

---

## 📊 Estado Actual
- **Novela Completa y Cerrada:** Los 25 capítulos que componen la obra se encuentran íntegramente redactados, revisados y validados técnica y literariamente:
  * **Acto I: La Semilla** (Capítulos 1 a 3)
  * **Acto II: El Colapso** (Capítulos 4 a 18)
  * **Acto III: El Silencio** (Capítulos 19 a 25)
- **Master Unificado:** [la_cancion_del_silencio_completa.md](file:///g:/OneDrive/ANTIGRAVITY/NOVELA_3/novela/la_cancion_del_silencio_completa.md) (120.488 palabras, 732.069 caracteres) con jerarquía Markdown estricta (`# Actos`, `## Capítulos`, `### Apartados`, `#### Subapartados`).
- **Módulo de Maquetación Editorial Física ([generar_edicion_imprenta.py](file:///g:/OneDrive/ANTIGRAVITY/NOVELA_3/generar_edicion_imprenta.py)):**
  * Formato: 150 mm × 210 mm (corte de novela europea).
  * Márgenes simétricos opuestos: Lomo 22 mm, Corte 15 mm, Cabeza 15 mm, Pie 22 mm. Caja de texto: 113 × 173 mm.
  * Tipografía: Garamond regular 11/13.5 pt, justificada con partición automática de sílabas léxicas en español (`pyphen` es_ES) y sangría de primera línea de 5 mm.
  * Separatas de Acto: Comienzo forzado en página impar (derecha), texto centrado vertical y horizontalmente a 24 pt versalitas, con reverso (página par) completamente en blanco, sin encabezados ni folios.
  * Capítulos: Apertura en página impar (recto), drop superior de 40 mm, título 18 pt negrita, separación de 15 mm antes del texto, primer párrafo sin sangría.
  * Apartados: Flujo continuo con `keepWithNext = True` contra títulos viudos/huérfanos.
  * Folios y Encabezados Vivos: Canvas de 2 pasadas (`PrintCanvas`). Folios a 9.5 pt en margen exterior inferior; encabezados vivos alternados (título de obra en páginas pares, título de capítulo en impares).
- **PDF de Edición para Imprenta Generado:**
  * [La_Cancion_del_Silencio_Edicion_Imprenta_150x210.pdf](file:///g:/OneDrive/ANTIGRAVITY/NOVELA_3/La_Cancion_del_Silencio_Edicion_Imprenta_150x210.pdf) (y réplica en `novela/`).
  * Extensión exacta: **388 páginas** (múltiplo de 4 para pliegos de imprenta: $97 \times 4$).
  * Cumplimiento estricto del 100% de aperturas de capítulo y separatas en páginas impares.
- **Web Interactiva y Sistema Anti-Caché:**
  * Actualizada y compilada con `node build-novel-data.js` para servir los 25 capítulos en GitHub Pages.
- **Bitácora y Memoria Continua de Sesiones:**
  * Supervisada por el agente **Capitán Memo** en [historial.md](file:///g:/OneDrive/ANTIGRAVITY/NOVELA_3/historial/historial.md).
