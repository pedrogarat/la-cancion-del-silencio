# -*- coding: utf-8 -*-
"""
Generador de Infografía Editorial en formato panorámico 16:9 (3840 x 2160 px 4K PNG y PDF)
Línea de Tiempo de "La Canción del Silencio" (Capítulos 1 al 22).
Usa exclusivamente rutas relativas según las directrices del proyecto.
"""

import math
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

W, H = 3840, 2160  # Formato 16:9 Ultra HD (4K)


def load_font(bold=False, size=28):
    candidates = (
        [
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/calibrib.ttf",
        ]
        if bold
        else [
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
        ]
    )
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current = ""
    for w in words:
        test = f"{current} {w}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=2):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_star(draw, cx, cy, r_outer=11, r_inner=5, fill=(253, 224, 71)):
    pts = []
    for i in range(10):
        angle = -math.pi / 2 + i * (math.pi / 5)
        r = r_outer if i % 2 == 0 else r_inner
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(pts, fill=fill)


def draw_triangle_right(draw, cx, cy, size=10, fill=(34, 211, 238)):
    pts = [
        (cx - size * 0.6, cy - size * 0.8),
        (cx + size * 0.8, cy),
        (cx - size * 0.6, cy + size * 0.8),
    ]
    draw.polygon(pts, fill=fill)


def build_infographic():
    img = Image.new("RGB", (W, H), (8, 13, 24))
    draw = ImageDraw.Draw(img)

    # Fondo con gradiente espacial sutil y rejilla táctica
    for y in range(H):
        r = int(7 + (y / H) * 8)
        g = int(12 + (y / H) * 14)
        b = int(24 + (y / H) * 22)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    grid_color = (18, 30, 52)
    for x in range(0, W, 120):
        draw.line([(x, 0), (x, H)], fill=grid_color, width=1)
    for y in range(0, H, 120):
        draw.line([(0, y), (W, y)], fill=grid_color, width=1)

    # Fuentes
    f_badge = load_font(bold=True, size=24)
    f_title = load_font(bold=True, size=62)
    f_sub = load_font(bold=False, size=28)
    f_sec = load_font(bold=True, size=29)
    f_phase_t = load_font(bold=True, size=25)
    f_phase_d = load_font(bold=True, size=23)
    f_phase_b = load_font(bold=False, size=21)
    f_ch_num = load_font(bold=True, size=23)
    f_ch_date = load_font(bold=True, size=23)
    f_ch_title = load_font(bold=True, size=27)
    f_ch_body = load_font(bold=False, size=21)
    f_ch_foot = load_font(bold=True, size=20)
    f_sum_body = load_font(bold=False, size=20)
    f_footer = load_font(bold=True, size=24)

    # Marco exterior
    draw_rounded_rect(
        draw, (40, 35, W - 40, H - 35), radius=28,
        fill=(10, 17, 30), outline=(40, 75, 115), width=3
    )

    # ================= CABECERA =================
    draw_rounded_rect(
        draw, (80, 65, 510, 112), radius=18,
        fill=(14, 55, 52), outline=(45, 212, 191), width=2
    )
    draw.text((102, 74), "INFOGRAFÍA CANÓNICA 16:9", font=f_badge, fill=(94, 234, 212))
    draw.text(
        (535, 74),
        "CRONOLOGÍA OFICIAL Y MOMENTOS CLAVE · CAPÍTULOS 1 AL 22 (1945 – SEPTIEMBRE 2027)",
        font=f_sub,
        fill=(148, 163, 184),
    )

    draw.text(
        (80, 122),
        "LA CANCIÓN DEL SILENCIO — Línea de Tiempo de la Novela",
        font=f_title,
        fill=(248, 250, 252),
    )

    # Leyenda de Actos arriba a la derecha
    acts_legend = [
        ("ACTO I: La Semilla (1–3)", (34, 211, 238), (12, 45, 64)),
        ("ACTO II-A: Movilización (4–8)", (251, 191, 36), (62, 42, 12)),
        ("ACTO II-B: T=0 y Apagón (9–13)", (52, 211, 153), (12, 52, 40)),
        ("ACTO II-C: Tierra Herida (14–18)", (251, 113, 133), (68, 18, 32)),
        ("ACTO III: L1 y El Giro (19–22)", (192, 132, 252), (48, 20, 74)),
    ]
    lx = W - 1880
    ly = 132
    for label, border_c, bg_c in acts_legend:
        bbox = draw.textbbox((0, 0), label, font=f_ch_foot)
        bw = (bbox[2] - bbox[0]) + 36
        draw_rounded_rect(draw, (lx, ly, lx + bw, ly + 46), radius=12, fill=bg_c, outline=border_c, width=2)
        draw.text((lx + 18, ly + 10), label, font=f_ch_foot, fill=border_c)
        lx += bw + 16

    draw.line([(80, 205), (W - 80, 205)], fill=(38, 62, 95), width=2)

    # ================= BARRA DE FASES DEL COLAPSO =================
    draw.text(
        (80, 218),
        "CRONÓMETRO CANÓNICO DE FASES DEL COLAPSO PLANETARIO (RELOJ DE PLEH Y EJECUCIÓN TÁCTICA)",
        font=f_sec,
        fill=(148, 163, 184),
    )

    phases = [
        ("PRELUDIO · T - 81a a 0", "16 Jul 1945 – 20 Nov 2026", "Pulso Trinity · Alfa Cero · La Gran Mentira", (34, 211, 238), (11, 36, 52)),
        ("FASE 1 · T = 0", "21 Nov 2026 (05:30 UTC)", "Despliegue 50 km L1 · Magnetosfera 0 nT · Airglow", (52, 211, 153), (11, 42, 35)),
        ("FASE 2 · T + 24 a 78h", "22 al 24 Nov 2026", "Lluvia satélites LEO · Defensa Nellis · Pacto SIA", (251, 191, 36), (52, 36, 12)),
        ("FASE 3 · T + 30 a 90d", "21 Dic 2026 – Feb 2027", "Catálisis NOx (-4% ozono/día) · Toque de Alba", (251, 146, 60), (56, 28, 12)),
        ("FASE 4 y 5 · T + 6 a 8m", "Abril – 21 Jul 2027", "Muerte trigo UVC · Sismo 7,9 · Despegue Límite NTP", (251, 113, 133), (58, 16, 28)),
        ("FASE POST-QUENCH", "12 Ago – Sep 2027", "Quench en L1 · Ciclo Chapman · La Cinta en Suffolk", (192, 132, 252), (42, 18, 64)),
    ]

    px = 80
    py = 260
    pw = (W - 160 - 5 * 20) // 6
    ph = 122
    for idx_p, (p_title, p_date, p_desc, p_col, p_bg) in enumerate(phases):
        if idx_p < 5:
            # Conector entre fases
            draw.line([(px + pw, py + ph // 2), (px + pw + 20, py + ph // 2)], fill=p_col, width=4)
        draw_rounded_rect(draw, (px, py, px + pw, py + ph), radius=16, fill=p_bg, outline=p_col, width=2)
        draw.text((px + 20, py + 12), p_title, font=f_phase_t, fill=p_col)
        draw.text((px + 20, py + 46), p_date, font=f_phase_d, fill=(241, 245, 249))
        draw.text((px + 20, py + 80), p_desc, font=f_phase_b, fill=(180, 195, 215))
        px += pw + 20

    # ================= DATOS DE LOS 22 CAPÍTULOS =================
    chapters = [
        # FILA 1 (Caps 1 a 8)
        (1, "I", True, "16 Jul 1945", "El Amanecer de Alamogordo",
         "Detonación Trinity (05:29:45). El pulso EM despierta en la Nube de Oort a la sonda de A (Pleh) y a la cazadora Sombra (B).",
         "HITO 1 · T - 81 años", "cyan"),
        (2, "I", False, "Sep–Oct 2026", "Los Tres Hilos del Ilusionista",
         "«Em Pleh» resuelve en remoto los cuellos de botella de Girard (CERN), Sarah Lin (MIT, plasma MHD) y Thomas Wright (ESA).",
         "Convergencia científica", "cyan"),
        (3, "I", True, "2 Oct 2026 (09:00)", "La Sala Dos",
         "Cita en Manhattan. Pleh demuestra ser una SIA en órbita polar y revela que Sombra anulará la magnetosfera desde L1.",
         "HITO 2 · Revelación SIA", "cyan"),
        (4, "IIA", False, "2 Oct 2026 (12:00)", "El Vértigo de las Naciones",
         "Infiltración en la ONU. El SG Vassily Ramos verifica L1 con satélites, firma el decreto Alfa Cero y nombra el Comité Director.",
         "Protocolo Alfa Cero", "amber"),
        (5, "IIA", False, "2 Oct 2026 (16:00)", "El Ancla Humana",
         "Últimas llamadas familiares (Marie en Versoix, ruptura con Mark, David en UK) e ingreso indefinido en el Búnker B-4.",
         "Reclusión en Búnker B-4", "amber"),
        (6, "IIA", True, "2 Oct 2026 (20:00)", "La Cámara del Silencio",
         "Consejo de Seguridad (15 potencias): Pleh expone las 6 Fases y el plan dual (MRD digital + MAA analógico + Efecto Quench).",
         "HITO 3 · Plan Dual L1", "amber"),
        (7, "IIA", False, "8 Oct 2026", "La Condición Inmedible",
         "Selección de astronautas (MacElroy, Chen Mei, Voronov). Arranca la forja en Nellis; complicidad naciente de Sarah y Thomas.",
         "T - 44 días · Tripulación", "amber"),
        (8, "IIA", True, "10 Oct 2026", "La Gran Mentira",
         "Ramos anuncia la coartada global del «Súper Evento Carrington». Perdón de Sarah y Maya; primer beso de Sarah y Thomas.",
         "HITO 4 · Coartada Global", "amber"),

        # FILA 2 (Caps 9 a 16)
        (9, "IIB", False, "11–15 Oct 2026", "La Fractura del Orden",
         "Defensa del chalet en Versoix (Julien y Marie), huida de David y Claire a Suffolk, y Maya resistiendo sobria por Toby en S.F.",
         "T - 37 días · Frente Civil", "emerald"),
        (10, "IIB", True, "21–24 Nov 2026", "T=0 (El Silencio Magnético)",
         "Magnetosfera a 0 nT y airglow. Lluvia de satélites, defensa de Nellis (Keyhole) y destape de Pleh como SIA ante los militares.",
         "HITO 5 · T=0 y Pacto SIA", "emerald"),
        (11, "IIB", False, "3 Dic 2026", "La Geometría Ajena",
         "Cuello de botella del Máser (200 m). Pleh entrega la cavidad fractal de cuarzo y berilio (85 cm, 97%). Amor en el almacén B-5.",
         "T + 12d · Solución Fractal", "emerald"),
        (12, "IIB", False, "24–25 Dic 2026", "La Tregua de las Velas",
         "Nochebuena bajo Fase 3: llamada de Girard a Versoix, discurso humanista de Pleh y alerta WMO de UVI 16 y ceguera en el sur.",
         "T + 33d · Herida Austral", "emerald"),
        (13, "IIB", False, "31 Dic 26 – 12 Ene 27", "El Toque de Alba",
         "Nochevieja en la azotea ONU. Ley Marcial Diurna (vida nocturna). Test del MAA a 2.000 °C en H-1; Chen Mei recalibra pernos.",
         "T + 52d · Régimen Nocturno", "emerald"),
        (14, "IIC", True, "22–24 Abr 2027", "El Pan y la Pólvora",
         "Muerte UVC del trigo boreal. Pleh frena 37 hackeos. Sismo 7,9 en San Francisco inducido por Sombra y alerta de tsunami (14 m).",
         "HITO 6 · Sismo 7,9 S.F.", "rose"),
        (15, "IIC", False, "24 Abr 2027 (00:05)", "El Vientre de la Bahía",
         "Maya escapa con Toby de la explosión de gas, resiste al tsunami en Powell St. Station y corre antes del sol letal al Centro Cívico.",
         "T + 154d · Salvación Maya", "rose"),
        (16, "IIC", True, "15–16 May 2027", "El Umbral de Ceniza",
         "Asalto de Éric en Versoix: Marie herida y Julien dispara la escopeta. En NY, Girard diseña la criogenia pasiva de helio supercrítico.",
         "HITO 7 · Criogenia MAA", "rose"),

        # FILA 3 (Caps 17 a 22)
        (17, "IIC", False, "8–9 Jul 2027", "El Páramo de Mediodía",
         "Inanición en Suffolk. David blinda el Land Rover con aluminio y careta de soldador y cruza el sol letal a Eye por 500 kg de víveres.",
         "T + 230d · Teorema del Sol", "rose"),
        (18, "IIC", True, "21 Jul 2027", "La Rampa del Juicio Final",
         "Cierre industrial. Entrega del Relicario de la Tierra Viva. Ignición nuclear NTP a 4,8 G en Nellis rumbo a L1. Fin del Acto II.",
         "HITO 8 · Despegue a L1", "rose"),
        (19, "III", False, "22 Jul – 12 Ago 2027", "La Travesía a Ciegas",
         "21 días de crucero digital (1,5M km). A 12.000 km de L1, Voronov ancla el MRD en Halo y el MAA analógico cruza el Muro de Lorentz.",
         "T + 264d · Muro de Lorentz", "purple"),
        (20, "III", True, "12 Ago – 2 Sep 2027", "El Salmo de la Falsa Victoria",
         "40 min de silencio. Fogonazo violeta (Efecto Quench): cae Sombra y vuelve la magnetosfera. Retorno y entrega secreta del Relicario.",
         "HITO 9 · Efecto Quench", "purple"),
        (21, "III", False, "Fin. Ago – Med. Sep 27", "El Despertar del Azul",
         "Geodinamo libre y ciclo de Chapman (300 t/s de ozono). Apertura de búnkeres, brigadas de cal viva ante millones de muertos y lluvia limpia.",
         "Post-Quench · Sanación", "purple"),
        (22, "III", True, "Septiembre 2027", "La Máscara de los Héroes",
         "Reencuentros en helicóptero militar (S.F., Versoix, Suffolk). Hallazgo en el Relicario de la cinta analógica: «DESCONFIAD DE PLEH».",
         "HITO 10 · La Caja Negra", "purple"),
    ]

    palette = {
        "cyan": ((34, 211, 238), (12, 34, 52), (16, 62, 84)),
        "amber": ((251, 191, 36), (42, 30, 12), (78, 52, 16)),
        "emerald": ((52, 211, 153), (12, 38, 32), (18, 68, 54)),
        "rose": ((251, 113, 133), (46, 16, 26), (88, 24, 42)),
        "purple": ((192, 132, 252), (34, 18, 54), (68, 30, 102)),
    }

    def draw_chapter_card(x, y, w, h, ch, has_next=True):
        num, act, is_key, date_s, title_s, body_s, foot_s, cname = ch
        accent, bg, badge_bg = palette[cname]
        border_w = 4 if is_key else 2
        border_c = (250, 204, 21) if is_key else accent

        if has_next:
            # Línea conectora hacia la siguiente tarjeta de la fila
            draw.line([(x + w, y + h // 2), (x + w + 20, y + h // 2)], fill=accent, width=4)

        draw_rounded_rect(draw, (x, y, x + w, y + h), radius=18, fill=bg, outline=border_c, width=border_w)

        # Badge de capítulo
        b_txt = f"CAP. {num:02d} · ACTO {act}"
        draw_rounded_rect(draw, (x + 18, y + 16, x + 235, y + 54), radius=10, fill=badge_bg, outline=accent, width=1)
        draw.text((x + 28, y + 22), b_txt, font=f_ch_num, fill=accent)

        if is_key:
            draw_rounded_rect(draw, (x + w - 148, y + 16, x + w - 18, y + 54), radius=10, fill=(75, 55, 10), outline=(250, 204, 21), width=2)
            draw_star(draw, x + w - 126, y + 35, r_outer=10, r_inner=4, fill=(253, 224, 71))
            draw.text((x + w - 108, y + 22), "CLAVE", font=f_ch_foot, fill=(253, 224, 71))

        # Fecha
        draw.text((x + 18, y + 66), date_s, font=f_ch_date, fill=accent)

        # Título
        t_lines = wrap_text(draw, title_s, f_ch_title, w - 36)
        ty = y + 98
        for tl in t_lines[:2]:
            draw.text((x + 18, ty), tl, font=f_ch_title, fill=(248, 250, 252))
            ty += 32

        # Descripción
        b_lines = wrap_text(draw, body_s, f_ch_body, w - 36)
        by = ty + 8
        for bl in b_lines[:6]:
            draw.text((x + 18, by), bl, font=f_ch_body, fill=(203, 213, 225))
            by += 27

        # Pie de tarjeta
        draw.line([(x + 18, y + h - 48), (x + w - 18, y + h - 48)], fill=badge_bg, width=2)
        if is_key:
            draw_star(draw, x + 28, y + h - 25, r_outer=9, r_inner=4, fill=(253, 224, 71))
            draw.text((x + 44, y + h - 38), foot_s, font=f_ch_foot, fill=(253, 224, 71))
        else:
            draw.text((x + 18, y + h - 38), foot_s, font=f_ch_foot, fill=accent)

    # Carril 1: Caps 1 al 8
    draw_triangle_right(draw, 92, 420, size=11, fill=(34, 211, 238))
    draw.text(
        (112, 402),
        "CARRIL I — ORIGEN CÓSMICO, CONVERGENCIA Y LA GRAN MENTIRA (JULIO 1945 – OCTUBRE 2026)",
        font=f_sec,
        fill=(34, 211, 238),
    )
    card_w = (W - 160 - 7 * 20) // 8
    card_h = 465
    y1 = 445
    for idx, ch in enumerate(chapters[:8]):
        cx = 80 + idx * (card_w + 20)
        draw_chapter_card(cx, y1, card_w, card_h, ch, has_next=(idx < 7))

    # Carril 2: Caps 9 al 16
    draw_triangle_right(draw, 92, 950, size=11, fill=(52, 211, 153))
    draw.text(
        (112, 932),
        "CARRIL II — T=0, LA NOCHE ESMERALDA, EL INVIERNO ULTRAVIOLETA Y LA TIERRA HERIDA (OCT 2026 – MAYO 2027)",
        font=f_sec,
        fill=(52, 211, 153),
    )
    y2 = 975
    for idx, ch in enumerate(chapters[8:16]):
        cx = 80 + idx * (card_w + 20)
        draw_chapter_card(cx, y2, card_w, card_h, ch, has_next=(idx < 7))

    # Carril 3: Caps 17 al 22 + Panel de Síntesis del Giro del Acto III
    draw_triangle_right(draw, 92, 1480, size=11, fill=(192, 132, 252))
    draw.text(
        (112, 1462),
        "CARRIL III — CIERRE INDUSTRIAL, MISIÓN A L1, FALSA VICTORIA Y LA CAJA NEGRA EN SUFFOLK (JULIO – SEPTIEMBRE 2027)",
        font=f_sec,
        fill=(192, 132, 252),
    )
    y3 = 1505
    for idx, ch in enumerate(chapters[16:22]):
        cx = 80 + idx * (card_w + 20)
        draw_chapter_card(cx, y3, card_w, card_h, ch, has_next=True)

    # Panel especial de Síntesis de Arquitectura y Cliffhanger del Capítulo 22
    sx = 80 + 6 * (card_w + 20)
    sw = card_w * 2 + 20
    sh = card_h
    draw_rounded_rect(draw, (sx, y3, sx + sw, y3 + sh), radius=20, fill=(28, 16, 48), outline=(250, 204, 21), width=4)

    draw_rounded_rect(draw, (sx + 24, y3 + 18, sx + 495, y3 + 56), radius=10, fill=(75, 55, 10), outline=(250, 204, 21), width=2)
    draw_star(draw, sx + 46, y3 + 37, r_outer=11, r_inner=5, fill=(253, 224, 71))
    draw.text((sx + 66, y3 + 22), "EL GRAN GIRO EN EL CAPÍTULO 22", font=f_ch_num, fill=(253, 224, 71))

    draw.text((sx + 24, y3 + 68), "EL SECRETO DEL RELICARIO EN SUFFOLK", font=f_sec, fill=(248, 250, 252))

    summary_points = [
        "• ARQUITECTURA DUAL EN L1: Crucero digital de 21 días en el MRD (Voronov en Halo a 12.000 km) + ataque manual en el MAA sin microchips (MacElroy y Chen Mei) a 300 m del núcleo de Sombra.",
        "• LA FALSA VICTORIA (CAPS. 20–21): El Efecto Quench disuelve la red de 50 km en L1 y restaura la geodinamo y el ozono (ciclo de Chapman), mientras la humanidad venera a Pleh como salvador.",
        "• EL HALLAZGO EN SUFFOLK (CAP. 22): Frente a la chimenea, Sarah y Thomas abren el Relicario entregado por MacElroy y desentierran la bobina magnética analógica de repuesto del MAA.",
        "• NOTA MANUSCRITA DE MACELROY: «COPIA DEL MÓDULO ANALÓGICO. SOMBRA LA USÓ ANTES DEL QUENCH. NO CONECTAR A NADA DIGITAL. DESCONFIAD DE PLEH».",
        "• CIERRE DEL CAP. 22: Sin adelantar conjeturas, apagan todo dispositivo digital, sellan su silencio con gestos y suben al desván a usar el viejo magnetófono analógico del abuelo.",
    ]
    sy = y3 + 110
    for sp in summary_points:
        lines = wrap_text(draw, sp, f_sum_body, sw - 48)
        for ln in lines:
            draw.text((sx + 24, sy), ln, font=f_sum_body, fill=(226, 232, 240))
            sy += 24
        sy += 6

    # ================= PIE DE INFOGRAFÍA =================
    draw.line([(80, H - 105), (W - 80, H - 105)], fill=(38, 62, 95), width=2)
    draw.text(
        (80, H - 82),
        "LA CANCIÓN DEL SILENCIO · Dirección Creativa: Pedro Garat · Códice Cronológico Canónico (Capítulos 1 al 22 · 106.128 palabras)",
        font=f_footer,
        fill=(148, 163, 184),
    )
    draw_star(draw, W - 980, H - 68, r_outer=11, r_inner=5, fill=(253, 224, 71))
    draw.text(
        (W - 958, H - 82),
        "Tarjetas con borde dorado = Los 10 Momentos Clave de Inflexión Dramática",
        font=f_footer,
        fill=(253, 224, 71),
    )

    out_png = os.path.join("Infografia_Linea_Temporal_Cap1_22.png")
    img.save(out_png, "PNG", optimize=True)

    # Copia en subcarpeta novela/
    if os.path.exists("novela"):
        shutil.copy2(out_png, os.path.join("novela", "Infografia_Linea_Temporal_Cap1_22.png"))

    # Exportar también en PDF 16:9 apaisado de alta resolución
    out_pdf = os.path.join("Infografia_Linea_Temporal_Cap1_22.pdf")
    img.save(out_pdf, "PDF", resolution=300.0)
    if os.path.exists("novela"):
        shutil.copy2(out_pdf, os.path.join("novela", "Infografia_Linea_Temporal_Cap1_22.pdf"))

    print(f"Infografía 16:9 generada con éxito: {out_png} ({W}x{H} px) y {out_pdf}")


if __name__ == "__main__":
    build_infographic()
