# Manual del Director y Método Creativo (Co-escritura con Antigravity AI)

Este espacio de trabajo integra un flujo de trabajo para escribir novelas interactivas en pareja con Antigravity AI.

---

## 🧭 Flujo de Trabajo Creativo

### 1. Configuración de Metadatos (`novela/meta.json`)
Define el título, subtítulo, autor y metadatos de los capítulos (POV, ubicación, acto al que pertenecen).

### 2. Definición del Universo y Personajes
- **`novela/genesis.md`**: Define la premisa, el género y las reglas del mundo.
- **`novela/personajes.md`**: Perfiles visuales, psicológicos y relaciones del elenco.
- **`novela/biografias.md`**: Biografías detalladas accesibles desde el Códex del lector web.
- **`novela/escaleta.md`**: Arco narrativo estructurado en 3 Actos.
- **`novela/notas_cientificas.md`**: Referencia de verosimilitud y notas científicas/técnicas.

### 3. Redacción de Capítulos (`novela/capitulos/`)
- Guarda cada capítulo como `capitulo_N.md`.
- Guarda el desglose técnico como `capitulo_N_desglose.md` para alimentar la ficha de coherencia en el lector web.

### 4. Compilación del Lector Web
Cada vez que agregues o modifiques un capítulo, ejecuta:
```bash
node build-novel-data.js
```
Esto regenerará `chapters-data.js` al instante.

---

## 🔄 Sincronización con tu Repositorio de GitHub

Para conectar este proyecto con tu nuevo repositorio en GitHub:

```bash
git add .
git commit -m "Estructura inicial de la nueva novela"
git remote add origin https://github.com/TU_USUARIO/TU_NUEVO_REPOSITORIO.git
git branch -M main
git push -u origin main
```
