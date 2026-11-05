import os
import shutil
from generar_todos_capitulos_pdf import generate_chapter_pdf, CHAPTER_METADATA

if __name__ == "__main__":
    chap_num = 24
    meta = CHAPTER_METADATA[chap_num]
    md_file = os.path.join("novela", "capitulos", f"capitulo_{chap_num}.md")
    new_pdf = meta["new_pdf"]
    legacy_pdf = meta["legacy_pdf"]

    print(f"Generando Capítulo {chap_num}: {meta['titulo']}...")
    success = generate_chapter_pdf(chap_num, md_file, new_pdf)
    if success:
        shutil.copyfile(new_pdf, os.path.join("novela", new_pdf))
        print(f"PDF generado: {new_pdf} y replicado en novela/")
        if legacy_pdf != new_pdf:
            shutil.copyfile(new_pdf, legacy_pdf)
            shutil.copyfile(new_pdf, os.path.join("novela", legacy_pdf))
            print(f"Sincronizado legacy: {legacy_pdf}")
