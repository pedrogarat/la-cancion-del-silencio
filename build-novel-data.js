const fs = require('fs');
const path = require('path');

const projectRoot = __dirname;
const novelaDir = path.join(projectRoot, 'novela');
const capitulosDir = path.join(novelaDir, 'capitulos');
const metaPath = path.join(novelaDir, 'meta.json');

// Cargar configuración de la novela si existe
let metaConfig = {
  title: "NUEVA NOVELA",
  subtitle: "EL COMIENZO DE LA AVENTURA",
  director: "Tu Nombre",
  author: "Tu Nombre",
  coverImage: "cover.png",
  chaptersMeta: []
};

if (fs.existsSync(metaPath)) {
  try {
    metaConfig = JSON.parse(fs.readFileSync(metaPath, 'utf-8'));
  } catch (e) {
    console.error("Error al leer novela/meta.json:", e);
  }
}

// Leer archivos de organización si existen
const personajesText = fs.existsSync(path.join(novelaDir, 'personajes.md')) ? fs.readFileSync(path.join(novelaDir, 'personajes.md'), 'utf-8') : '';
const biografiasText = fs.existsSync(path.join(novelaDir, 'biografias.md')) ? fs.readFileSync(path.join(novelaDir, 'biografias.md'), 'utf-8') : '';
const escaletaText = fs.existsSync(path.join(novelaDir, 'escaleta.md')) ? fs.readFileSync(path.join(novelaDir, 'escaleta.md'), 'utf-8') : '';
const genesisText = fs.existsSync(path.join(novelaDir, 'genesis.md')) ? fs.readFileSync(path.join(novelaDir, 'genesis.md'), 'utf-8') : '';
const notasCientificasText = fs.existsSync(path.join(novelaDir, 'notas_cientificas.md')) ? fs.readFileSync(path.join(novelaDir, 'notas_cientificas.md'), 'utf-8') : '';

const chapters = [];

if (fs.existsSync(capitulosDir)) {
  const files = fs.readdirSync(capitulosDir);
  const chapterFiles = files.filter(f => f.match(/^capitulo_\d+\.md$/i));
  
  // Ordenar por número de capítulo
  chapterFiles.sort((a, b) => {
    const numA = parseInt(a.match(/\d+/)[0], 10);
    const numB = parseInt(b.match(/\d+/)[0], 10);
    return numA - numB;
  });

  chapterFiles.forEach((file) => {
    const num = parseInt(file.match(/\d+/)[0], 10);
    const filePath = path.join(capitulosDir, file);
    const desglosePath = path.join(capitulosDir, `capitulo_${num}_desglose.md`);

    const content = fs.readFileSync(filePath, 'utf-8');
    const desglose = fs.existsSync(desglosePath) ? fs.readFileSync(desglosePath, 'utf-8') : '';

    // Extraer título de la primera línea si existe
    const firstLineMatch = content.match(/^#\s+(.+)$/m);
    const chapterTitle = firstLineMatch ? firstLineMatch[1].trim() : `Capítulo ${num}`;

    // Calcular palabras y páginas
    const plainText = content.replace(/#|\*|`|-|---|/g, '').trim();
    const wordCount = plainText.length > 0 ? plainText.split(/\s+/).filter(w => w.length > 0).length : 0;
    const pagesEst = (wordCount / 275).toFixed(1);

    const chapterCustomMeta = (metaConfig.chaptersMeta || []).find(m => m.id === num);

    const meta = {
      id: num,
      title: chapterCustomMeta?.title || chapterTitle,
      act: chapterCustomMeta?.act || "Acto Principal",
      pov: chapterCustomMeta?.pov || "Protagonista",
      location: chapterCustomMeta?.location || "Ubicación Principal",
      readTime: chapterCustomMeta?.readTime || `${Math.max(1, Math.ceil(wordCount / 250))} min`,
      povImage: chapterCustomMeta?.povImage || "img/char_protagonista.png"
    };

    chapters.push({
      ...meta,
      words: wordCount,
      pages: pagesEst,
      content: content,
      desglose: desglose
    });
  });
}

const now = new Date();
const formattedDate = new Intl.DateTimeFormat('es-ES', {
  day: '2-digit',
  month: '2-digit',
  year: 'numeric',
  hour: '2-digit',
  minute: '2-digit',
  second: '2-digit',
  timeZone: 'Europe/Madrid'
}).format(now);

const novelData = {
  title: metaConfig.title || "NUEVA NOVELA",
  subtitle: metaConfig.subtitle || "EL COMIENZO DE LA AVENTURA",
  director: metaConfig.director || "Tu Nombre",
  author: metaConfig.author || "Tu Nombre",
  coverImage: metaConfig.coverImage || "cover.png",
  lastUpdated: formattedDate,
  buildTimestamp: now.toISOString(),
  totalChapters: chapters.length,
  totalWords: chapters.reduce((acc, c) => acc + c.words, 0),
  totalPages: chapters.reduce((acc, c) => acc + parseFloat(c.pages), 0).toFixed(1),
  personajesRaw: personajesText,
  biografiasRaw: biografiasText,
  escaletaRaw: escaletaText,
  genesisRaw: genesisText,
  notasCientificasRaw: notasCientificasText,
  chapters: chapters
};

const outputContent = `// Archivo generado automáticamente para ${novelData.title}\nconst NOVEL_DATA = ${JSON.stringify(novelData, null, 2)};\n`;

fs.writeFileSync(path.join(projectRoot, 'chapters-data.js'), outputContent, 'utf-8');
console.log(`Successfully updated chapters-data.js for ${novelData.title} with ${chapters.length} chapter(s)!`);

