import os
import platform
import tempfile
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static" / "images"
PRODUKTY_DIR = STATIC_DIR / "produkty"


jinja_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))

PRODUKT_MAPA = [
    (
        ["Z-90", "Z-70", "NOVAL", "zaluzi"],
        "Vonkajšie žalúzie",
        "vonkajsie_zaluzie.jpg",
        "Vonkajšie hliníkové žalúzie poskytujú maximálnu ochranu pred slnkom a teplom. "
        "Lamelky sú vyrobené z vysokopevnostného hliníka s povrchovou úpravou odolnou voči poveternostným vplyvom. "
        "Vhodné pre rodinné domy aj komerčné priestory.",
    ),
    (
        ["rolet", "UNIROL", "Roller"],
        "Vonkajšie rolety",
        "vonkajsie_rolety.jpg",
        "Vonkajšie rolety z hliníkových lamiel zaručujú dokonalé zatienenie a tepelnú izoláciu. "
        "Cassette systém chráni mechanizmus pred počasím. Dostupné v motorickej aj ručnej verzii.",
    ),
    (
        ["screen", "Screen"],
        "Screenové rolety",
        "screenove_rolety.jpg",
        "Screenové rolety filtrujú slnečné žiarenie a zachovávajú výhľad z okna. "
        "Špeciálna tkanina redukuje tepelné zisky a oslnenie bez straty denného svetla.",
    ),
    (
        ["EXT", "siet", "hmyz", "okenn"],
        "Siete proti hmyzu (okenné)",
        "okenne_siete.jpg",
        "Okenné siete proti hmyzu chránia interiér a umožňujú prirodzené vetranie. "
        "Hliníkový rám a kvalitná sieťovina zaručujú dlhú životnosť. Montáž bez vŕtania.",
    ),
    (
        ["PS Z", "posuvn", "dvern"],
        "Siete proti hmyzu (dverné)",
        "dverne_siete.jpg",
        "Posuvné dverné siete umožňujú pohodlný prechod bez použitia rúk. "
        "Automatické zatváranie zabraňuje prieniku hmyzu. Vhodné pre balkónové aj vstupné dvere.",
    ),
    (
        ["markiz"],
        "Markízy",
        "markizy.jpg",
        "Vonkajšie markízy poskytujú tieň na terase alebo balkóne. "
        "Odolná akrylová tkanina je vodoodpudivá a UV-stabilná. "
        "Motorický pohon s diaľkovým ovládaním alebo automatickým senzorom.",
    ),
    (
        ["pergol", "Lamelino"],
        "Pergoly",
        "pergoly.jpg",
        "Bioklimatické pergoly s otočnými lamelami regulujú množstvo slnečného svetla a vetrania. "
        "Hliníková konštrukcia odolá aj náročným poveternostným podmienkam.",
    ),
    (
        ["vnutorn", "interier"],
        "Vnútorné žalúzie",
        "vnutorne_zaluzie.jpg",
        "Vnútorné hliníkové žalúzie umožňujú presnú reguláciu svetla v interiéri. "
        "Dostupné v širokej škále farieb. Jednoduché ovládanie šnúrkou alebo tyčkou.",
    ),
    (
        ["latkove", "tienenie"],
        "Látkové tienenie",
        "latkove_tienenie.jpg",
        "Látkové rolety poskytujú elegantné tienenie v interiéri. "
        "Dostupné v priepustných aj zatemňovacích variantoch. Široký výber farieb.",
    ),
    (
        ["komponent", "motor", "ovladac", "EVB", "receiver", "Slim"],
        "Komponenty / elektro",
        "komponenty.jpg",
        "Motorické pohony, diaľkové ovládače, senzory a príslušenstvo pre tieniacu techniku. "
        "Kompatibilné so systémami SOMFY a Climax. Profesionálna inštalácia a nastavenie.",
    ),
]


def zisti_produkt(typ_produktu: str) -> tuple[str, str | None, str]:
    tp = typ_produktu.lower()
    for klucove_slova, nazov, fotka, popis in PRODUKT_MAPA:
        if any(k.lower() in tp for k in klucove_slova):
            foto_path = PRODUKTY_DIR / fotka
            return nazov, str(foto_path) if foto_path.exists() else None, popis
    return typ_produktu, None, ""


def _link_callback(uri: str, rel: str) -> str:
    p = Path(uri)
    if p.is_absolute() and p.exists():
        return str(p)
    candidate = BASE_DIR / uri.lstrip("/")
    if candidate.exists():
        return str(candidate)
    return uri


def generuj_pdf(data: dict) -> bytes:
    slovensky_nazov, foto_path, popis = zisti_produkt(data.get("typ_produktu", ""))

    priplatky = data.get("priplatky") or []
    priplatky_suma = sum(p.get("suma", 0) for p in priplatky)

    # Predpocitaj zobrazovane retazce — template ma len jednoduche {{ var }}
    rozmery = ""
    s, v = data.get("rozmer_sirka_cm"), data.get("rozmer_vyska_cm")
    if s and v:
        rozmery = f"{int(s)} x {int(v)} cm"

    zlava_str = ""
    if data.get("zlava_percent"):
        zlava_str = f"{int(data['zlava_percent'])}%  -  {data.get('zlava_suma', 0):.2f} €"

    suhrn_bez_dph = data.get("cena_po_zlave") or data.get("cena_bez_dph") or 0

    template = jinja_env.get_template("ponuka.html")
    html_content = template.render(
        logo_path=str(STATIC_DIR / "logo_onlyservis.jpg"),
        foto_path=foto_path,
        cislo_ponuky=data.get("cislo_ponuky", ""),
        datum_ponuky=data.get("datum_ponuky", ""),
        zakaznik_meno=data.get("zakaznik_meno", ""),
        zakaznik_mesto=data.get("zakaznik_mesto", ""),
        typ_produktu=data.get("typ_produktu", ""),
        slovensky_nazov=slovensky_nazov,
        popis=popis,
        pocet_ks=data.get("pocet_ks", 1),
        rozmery=rozmery,
        cena_bez_dph_str=f"{data.get('cena_bez_dph', 0):.2f} €",
        zlava_str=zlava_str,
        cena_s_dph_str=f"{data.get('cena_s_dph', 0):.2f} €",
        ma_priplatky=len(priplatky) > 0,
        priplatky=priplatky,
        suhrn_bez_dph_str=f"{suhrn_bez_dph:.2f} €",
        priplatky_suma_str=f"{priplatky_suma:.2f} €" if priplatky_suma else "",
        dph_percent=int(data.get("dph_percent") or 23),
        dph_suma_str=f"{data.get('dph_suma', 0):.2f} €",
        cena_s_dph_celkom_str=f"{data.get('cena_s_dph', 0):.2f} €",
    )

    # Ulož HTML do docasneho suboru a konvertuj cez Playwright/Chromium
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as f:
        f.write(html_content)
        tmp_html = Path(f.name)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(tmp_html.as_uri(), wait_until="networkidle")
            pdf_bytes = page.pdf(
                format="A4",
                margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"},
                print_background=True,
            )
            browser.close()
    finally:
        tmp_html.unlink(missing_ok=True)

    return pdf_bytes
