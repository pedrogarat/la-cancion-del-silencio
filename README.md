# Proyecto de Novela Interactiva

Este espacio de trabajo contiene el lector web oficial y la infraestructura de desarrollo para tu nueva novela interactiva, con diseño adaptativo, control de temas visuales, reproductor de audiolibro y ambiente sonoro.

---

## 🚀 Estructura de la Novela

El contenido narrativo se organiza y redacta de forma modular dentro de la carpeta `novela/`:

- **`novela/meta.json`**: Configuración central del título, subtítulo, autor y metadatos por capítulo (POV, ubicación, actos).
- **`novela/genesis.md`**: Premisa, temática y guía de estilo.
- **`novela/personajes.md`**: Perfiles del elenco principal (se muestra en el Códex del lector).
- **`novela/biografias.md`**: Biografías detalladas.
- **`novela/escaleta.md`**: Arco narrativo estructurado en 3 Actos.
- **`novela/notas_cientificas.md`**: Fuente técnica y enciclopedia de conceptos científicos para la redacción.
- **`novela/capitulos/`**: Archivos de texto en Markdown (`capitulo_1.md`, `capitulo_2.md`, etc.) y sus desgloses técnicos (`capitulo_1_desglose.md`).

---

## 🛠️ Compilación Automática del Lector

Cada vez que agregues un nuevo capítulo o modifiques `meta.json`, ejecuta en tu terminal:

```bash
node build-novel-data.js
```

Esto compilará la novela y actualizará `chapters-data.js` para que se refleje inmediatamente en `index.html`.

---

## 🔗 Vincular a tu nuevo Repositorio de GitHub

Este proyecto ha sido desvinculado del repositorio anterior. Para conectar tu nuevo repositorio en GitHub:

1. Crea un nuevo repositorio en [GitHub](https://github.com/new) (puede ser público o privado).
2. Ejecuta los siguientes comandos en la terminal de este proyecto:

```bash
git add .
git commit -m "Estructura inicial de la nueva novela"
git remote add origin https://github.com/TU_USUARIO/TU_NUEVO_REPOSITORIO.git
git branch -M main
git push -u origin main
```
