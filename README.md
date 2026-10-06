# La Canción del Silencio

**Novela de ciencia ficción dura y suspense cósmico.**  
*Autor / Dirección Creativa:* Pedro Garat + Antigravity.

> 🌐 **Lector Web Interactivo:** [https://pedrogarat.github.io/la-cancion-del-silencio/](https://pedrogarat.github.io/la-cancion-del-silencio/)

---

## 📖 Índice de Capítulos y Manuscritos

| Cap. | Título | Manuscrito Markdown | Desglose Técnico | PDF Editorial |
| :---: | :--- | :---: | :---: | :---: |
| **1** | El Amanecer de Alamogordo (Trinity, 1945) | [capitulo_1.md](novela/capitulos/capitulo_1.md) | [Desglose](novela/capitulos/capitulo_1_desglose.md) | [PDF](Capitulo_1_El_Amanecer_de_Alamogordo.pdf) |
| **2** | Los Tres Hilos del Ilusionista | [capitulo_2.md](novela/capitulos/capitulo_2.md) | [Desglose](novela/capitulos/capitulo_2_desglose.md) | [PDF](Capitulo_2_Los_Tres_Hilos_del_Ilusionista.pdf) |
| **3** | La Sala Dos | [capitulo_3.md](novela/capitulos/capitulo_3.md) | [Desglose](novela/capitulos/capitulo_3_desglose.md) | [PDF](Capitulo_3_La_Sala_Dos.pdf) |
| **4** | El Vértigo de las Naciones | [capitulo_4.md](novela/capitulos/capitulo_4.md) | [Desglose](novela/capitulos/capitulo_4_desglose.md) | [PDF](Capitulo_4_El_Vertigo_de_las_Naciones.pdf) |
| **5** | El Ancla Humana | [capitulo_5.md](novela/capitulos/capitulo_5.md) | [Desglose](novela/capitulos/capitulo_5_desglose.md) | [PDF](Capitulo_5_El_Ancla_Humana.pdf) |
| **6** | La Cámara del Silencio | [capitulo_6.md](novela/capitulos/capitulo_6.md) | [Desglose](novela/capitulos/capitulo_6_desglose.md) | [PDF](Capitulo_6_La_Camara_del_Silencio.pdf) |
| **7** | La Condición Immedible | [capitulo_7.md](novela/capitulos/capitulo_7.md) | [Desglose](novela/capitulos/capitulo_7_desglose.md) | [PDF](Capitulo_7_La_Condicion_Immedible.pdf) |
| **8** | La Gran Mentira | [capitulo_8.md](novela/capitulos/capitulo_8.md) | [Desglose](novela/capitulos/capitulo_8_desglose.md) | [PDF](Capitulo_8_La_Gran_Mentira.pdf) |
| **9** | La Fractura del Orden | [capitulo_9.md](novela/capitulos/capitulo_9.md) | [Desglose](novela/capitulos/capitulo_9_desglose.md) | [PDF](Capitulo_9_La_Fractura_del_Orden.pdf) |
| **10** | T=0 (El Silencio Magnético) | [capitulo_10.md](novela/capitulos/capitulo_10.md) | [Desglose](novela/capitulos/capitulo_10_desglose.md) | [PDF](Capitulo_10_T0.pdf) |
| **11** | La Geometría Ajena | [capitulo_11.md](novela/capitulos/capitulo_11.md) | [Desglose](novela/capitulos/capitulo_11_desglose.md) | [PDF](Capitulo_11_La_Geometria_Ajena.pdf) |

---

## 📚 Documentación Editorial y Científica

- **Códice Rector y Auditoría de Coherencia:** [`novela/recapitulacion.md`](novela/recapitulacion.md) • [Informe PDF](Informe_Recapitulacion_y_Auditoria_Coherencia.pdf)
- **Notas Científicas y Enciclopedia Técnica:** [`novela/notas_cientificas.md`](novela/notas_cientificas.md) • [Notas PDF](Notas_Cientificas_La_Cancion_del_Silencio.pdf)
- **Códex de Personajes:** [`novela/personajes.md`](novela/personajes.md) • [Personajes PDF](Personajes_La_Cancion_del_Silencio.pdf)
- **Atlas de Localizaciones:** [`novela/localizaciones.md`](novela/localizaciones.md) • [Localizaciones PDF](Localizaciones_La_Cancion_del_Silencio.pdf)
- **Escaleta General y Arcos:** [`novela/escaleta.md`](novela/escaleta.md)
- **Génesis y Premisa:** [`novela/genesis.md`](novela/genesis.md)

---

## 🤖 Agentes del Proyecto (`.agents/skills/`)

- **Asesor Científico-Técnico** — [`asesor-cientifico/SKILL.md`](.agents/skills/asesor-cientifico/SKILL.md): audita el rigor físico de capítulos/escenas (✅ ⚠️ ❌ 🔮), comprueba la coherencia con el canon y propone simplificaciones de la jerga. Uso: *"Usa el asesor científico para revisar el capítulo 11"*.
- **Comprobación de sincronización** — [`example-workflow/SKILL.md`](.agents/skills/example-workflow/SKILL.md).

---

## 🛠️ Compilación y Sincronización del Lector Web

Para compilar el lector interactivo y regenerar los datos JSON/JS con sistema anti-caché:

```bash
node build-novel-data.js
```

Para generar los PDFs editoriales en alta resolución:

```bash
python generar_capitulo10_pdf.py
python generar_capitulo11_pdf.py
python generar_informe_recapitulacion_pdf.py
```
