import base64
import io
from pathlib import Path

import qrcode
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static" / "images"
PRODUKTY_DIR = STATIC_DIR / "produkty"

jinja_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))

PRODUKT_MAPA = {
    "vonkajsie_zaluzie": {
        "nazov": "Vonkajšie žalúzie",
        "obrazok": "vonkajsie_zaluzie.jpg",
        "klucove_slova": ["z-90", "z-70", "t-80", "c-80", "c-60", "f-80", "ext-50", "protal"],
    },
    "vonkajsie_rolety": {
        "nazov": "Vonkajšie rolety",
        "obrazok": "vonkajsie_rolety.jpg",
        "klucove_slova": ["m 328", "m 317", "m 442", "mpvc"],
    },
    "screenove_rolety": {
        "nazov": "Screenové rolety",
        "obrazok": "screenove_rolety.jpg",
        "klucove_slova": ["unirol", "sunrol", "v-rol"],
    },
    "okenne_siete": {
        "nazov": "Siete proti hmyzu (okenné)",
        "obrazok": "okenne_siete.jpg",
        "klucove_slova": [
            "ext 16", "ext-16", "lux", "extra", "ultra",
            "rolo magnet", "síť 25", "síť 36", "sit 25", "sit 36",
            "rolo hák", "rolo klik",
        ],
    },
    "dverne_siete": {
        "nazov": "Siete proti hmyzu (dverné)",
        "obrazok": "dverne_siete.jpg",
        "klucove_slova": [
            "plisé", "plise", "posuvná", "posuvna",
            "ps r1", "ps r2", "dverní", "dverni",
        ],
    },
    "markizy": {
        "nazov": "Markízy",
        "obrazok": "markizy.jpg",
        "klucove_slova": ["prima t", "prima box", "noveta", "kaseta", "klasik"],
    },
    "pergoly": {
        "nazov": "Pergoly",
        "obrazok": "pergoly.jpg",
        "klucove_slova": ["lamelino"],
    },
    "vnutorne_zaluzie": {
        "nazov": "Vnútorné žalúzie",
        "obrazok": "vnutorne_zaluzie.jpg",
        "klucove_slova": [
            "idx", "harmony", "super", "mono sc",
            "int-35", "int-50", "max 25", "max 21", "18 max", "18 idx",
        ],
    },
    "latkove_tienenie": {
        "nazov": "Látkové tienenie",
        "obrazok": "latkove_tienenie.jpg",
        "klucove_slova": [
            "varieta", "orion", "calypso", "apollo", "v-63",
            "fantazie", "vertikálne žalúzie", "verticalne zaluzie",
        ],
    },
    "komponenty": {
        "nazov": "Komponenty / príslušenstvo",
        "obrazok": "komponenty.jpg",
        "klucove_slova": [
            "lamela z-90", "lamela z-70", "síťovina", "sietovina",
            "guma zatlačovacia", "guma zatlac",
            "motor", "ovládač", "ovladac", "komponent", "nabídka komponenty",
        ],
    },
}


def zisti_produkt(typ_produktu: str) -> tuple[str, str | None, str | None, str]:
    if not typ_produktu:
        return "", None, None, ""
    tp = typ_produktu.lower()
    for produkt in PRODUKT_MAPA.values():
        if any(k.lower() in tp for k in produkt["klucove_slova"]):
            fotka = produkt["obrazok"]
            foto_path = PRODUKTY_DIR / fotka
            detail_fotka = fotka.replace(".jpg", "_detail.jpg")
            foto_detail_path = PRODUKTY_DIR / detail_fotka
            return (
                produkt["nazov"],
                str(foto_path) if foto_path.exists() else None,
                str(foto_detail_path) if foto_detail_path.exists() else None,
                "",
            )
    return typ_produktu, None, None, ""


def _qr_data_uri(url: str) -> str:
    qr = qrcode.QRCode(box_size=4, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{b64}"


def _parse_popis(popis: str) -> tuple[str, list[str], str]:
    intro_parts, bullets, closing = [], [], ""
    in_bullets = False
    for line in popis.split("\n"):
        if line.startswith("- "):
            in_bullets = True
            bullets.append(line[2:])
        elif in_bullets and line.strip():
            closing = line.strip()
        elif not in_bullets and line.strip():
            intro_parts.append(line.strip())
    return " ".join(intro_parts), bullets, closing


def generuj_pdf(data: dict) -> bytes:
    slovensky_nazov, foto_path, foto_detail_path, popis = zisti_produkt(data.get("typ_produktu", ""))
    popis_intro, popis_bullets, popis_closing = _parse_popis(popis) if popis else ("", [], "")

    priplatky = data.get("priplatky") or []
    priplatky_suma = sum(p.get("suma", 0) for p in priplatky)

    polozky = data.get("polozky") or []
    je_komponenty = not data.get("typ_produktu") and bool(polozky)
    ma_popis_col = any(p.get("popis") for p in polozky)
    ma_rozmery_col = any(p.get("sirka_cm") for p in polozky)
    col_count = (2 + (1 if ma_popis_col else 0) + (1 if ma_rozmery_col else 0)) if polozky else 6
    if je_komponenty:
        col_count = 6

    rozmery = ""
    s, v = data.get("rozmer_sirka_cm"), data.get("rozmer_vyska_cm")
    if s and v:
        rozmery = f"{int(s)} x {int(v)} cm"

    zlava_str = ""
    if data.get("zlava_percent"):
        zlava_str = f"{int(data['zlava_percent'])}%  -  {data.get('zlava_suma') or 0:.2f} €"

    suhrn_bez_dph_base = data.get("cena_po_zlave") or data.get("cena_bez_dph") or 0

    # Zľava — zobrazenie v súhrne (cena pred zľavou + suma zľavy)
    _zlava_percent_num = data.get("zlava_percent") or 0
    _cena_bez_dph_raw = data.get("cena_bez_dph") or 0
    _cena_po_zlave_raw = data.get("cena_po_zlave") or 0
    _zlava_suma_num = data.get("zlava_suma") or 0
    # Fallback: ak cena_bez_dph > cena_po_zlave, rozdiel = suma zľavy
    if _zlava_percent_num and not _zlava_suma_num and _cena_bez_dph_raw > _cena_po_zlave_raw > 0:
        _zlava_suma_num = round(_cena_bez_dph_raw - _cena_po_zlave_raw, 2)
    ma_zlavu = bool(_zlava_percent_num) and _zlava_suma_num > 0
    cena_pred_zlavou_str = f"{_cena_bez_dph_raw:.2f} €" if ma_zlavu else ""
    zlava_suma_display_str = f"{_zlava_suma_num:.2f} €" if ma_zlavu else ""
    dph_percent = int(data.get("dph_percent") or 23)

    # priplatky_v_cene = príplatky už zahrnuté v cena_po_zlave (z extrakcie PDF)
    # manuálne príplatky = priplatky_suma - priplatky_v_cene
    pvc = data.get("priplatky_v_cene")
    priplatky_v_cene = pvc if pvc is not None else priplatky_suma

    produkt_bez_dph = suhrn_bez_dph_base - priplatky_v_cene
    produkt_s_dph = round(produkt_bez_dph * (1 + dph_percent / 100), 2)
    suhrn_bez_dph = suhrn_bez_dph_base + (priplatky_suma - priplatky_v_cene)
    dph_suma = round(suhrn_bez_dph * dph_percent / 100, 2)
    cena_s_dph_celkom = round(suhrn_bez_dph + dph_suma, 2)

    template = jinja_env.get_template("ponuka.html")
    html_content = template.render(
        logo_path=str(STATIC_DIR / "logo_onlyservis.jpg"),
        climax_zaruka_path=str(STATIC_DIR / "climax_zaruka.jpg"),
        qr_data_uri=_qr_data_uri("https://wa.me/421903533534"),
        foto_path=foto_path,
        foto_detail_path=foto_detail_path,
        cislo_ponuky=data.get("cislo_ponuky", ""),
        datum_ponuky=data.get("datum_ponuky", ""),
        zakaznik_meno=data.get("zakaznik_meno", ""),
        zakaznik_mesto=data.get("zakaznik_mesto", ""),
        typ_produktu=data.get("typ_produktu", ""),
        slovensky_nazov=slovensky_nazov,
        popis=popis,
        popis_intro=popis_intro,
        popis_bullets=popis_bullets,
        popis_closing=popis_closing,
        pocet_ks=data.get("pocet_ks", 1),
        rozmery=rozmery,
        cena_bez_dph_str=f"{produkt_bez_dph:.2f} €",
        zlava_str=zlava_str,
        ma_zlavu=ma_zlavu,
        zlava_percent_disp=int(_zlava_percent_num) if _zlava_percent_num else 0,
        cena_pred_zlavou_str=cena_pred_zlavou_str,
        zlava_suma_display_str=zlava_suma_display_str,
        cena_s_dph_str=f"{produkt_s_dph:.2f} €",
        ma_priplatky=len(priplatky) > 0,
        priplatky=priplatky,
        suhrn_bez_dph_str=f"{suhrn_bez_dph:.2f} €",
        dph_percent=dph_percent,
        dph_suma_str=f"{dph_suma:.2f} €",
        cena_s_dph_celkom_str=f"{cena_s_dph_celkom:.2f} €",
        poznamka=data.get("poznamka") or None,
        polozky=polozky,
        je_komponenty=je_komponenty,
        ma_popis_col=ma_popis_col,
        ma_rozmery_col=ma_rozmery_col,
        col_count=col_count,
    )

    return HTML(string=html_content, base_url=str(BASE_DIR)).write_pdf()
