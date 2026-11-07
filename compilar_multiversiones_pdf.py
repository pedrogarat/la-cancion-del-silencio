import os
import shutil
from generar_todos_capitulos_pdf import CHAPTER_METADATA, generate_chapter_pdf, FONT_BODY

def compile_edition(edition_name, md_folder, pdf_folder, copy_to_root_novela=False):
    print(f"\n=======================================================")
    print(f"Compilando edición: {edition_name} con {FONT_BODY} (Sans-Serif Inter)")
    print(f"Directorio origen: {md_folder}")
    print(f"Directorio destino: {pdf_folder}")
    print(f"=======================================================")
    os.makedirs(pdf_folder, exist_ok=True)
    
    success_count = 0
    for chap_num in range(1, 26):
        md_file = os.path.join(md_folder, f"capitulo_{chap_num}.md")
        meta = CHAPTER_METADATA[chap_num]
        pdf_name = meta["new_pdf"]
        temp_pdf = f"temp_{chap_num}.pdf"
        dest_pdf = os.path.join(pdf_folder, pdf_name)
        
        ok = generate_chapter_pdf(chap_num, md_file, temp_pdf)
        if ok and os.path.exists(temp_pdf):
            shutil.move(temp_pdf, dest_pdf)
            if copy_to_root_novela:
                shutil.copyfile(dest_pdf, os.path.join("novela", pdf_name))
            print(f"[OK] Cap {chap_num:2d}: {meta['titulo']} -> {pdf_name}")
            success_count += 1
        else:
            print(f"[ERROR] Cap {chap_num:2d}: Falló la generación de {md_file}")
            
    print(f"Completados {success_count}/25 capítulos para {edition_name}.\n")
    return success_count

if __name__ == "__main__":
    print("Compilación integral de las 3 ediciones oficiales de SILENCIO MAGNÉTICO...")
    c1 = compile_edition("Hard Sci-Fi (Canon Original)", os.path.join("novela", "capitulos"), os.path.join("novela", "pdf_hard"), copy_to_root_novela=True)
    c2 = compile_edition("Sci-Fi (Divulgativa / Narrativa)", os.path.join("novela", "capitulos_scifi"), os.path.join("novela", "pdf_scifi"))
    c3 = compile_edition("Juvenil / Adolescente", os.path.join("novela", "capitulos_juvenil"), os.path.join("novela", "pdf_juvenil"))
    print(f"TOTAL: {c1 + c2 + c3}/75 PDFs generados con éxito con la nueva tipografía Inter y detalles diferenciados.")
