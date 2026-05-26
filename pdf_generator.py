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

PRODUKT_MAPA = [
    (
        ["Z-90", "Z-70", "NOVAL", "zaluzi"],
        "Vonkajšie žalúzie",
        "vonkajsie_zaluzie.jpg",
        "Vonkajšie žalúzie zastavujú slnečné lúče ešte pred oknami – tam, kde to robí najväčší rozdiel. "
        "Vďaka naklopeniu lamiel môžete vetrať a pritom plynule regulovať množstvo svetla aj teplotu v interiéri. "
        "Sú funkčným aj estetickým doplnkom každého rodinného domu či kancelárskej budovy.\n"
        "- V lete zabraňujú prehrievaniu interiéru – teplota v miestnosti môže klesnúť o niekoľko stupňov Celzia\n"
        "- V zime fungujú ako ďalšia vrstva tepelnej izolácie okna a šetria náklady na kúrenie\n"
        "- Umožňujú vetranie otvoreným oknom pri zachovaní regulácie svetla a súkromia\n"
        "- Chránia vaše súkromie – zvonku nikto nevidí dnu, vy vidíte von\n"
        "- Spoľahlivo chránia okno pred prudkým dažďom, vetrom, krupobitím a UV žiarením\n"
        "- Bezpečnostný efekt – sú neľahkou prekážkou pri pokuse o neoprávnené vniknutie\n"
        "- Široký výber modelov (Z-90 Noval, Z-70, T-80, C-80, C-60, F-80, PROTAL a ďalšie) a farieb lamiel\n"
        "Záruka 4 roky. Montáž zabezpečujeme v Bratislavskom a Trnavskom kraji.",
    ),
    (
        ["rolet", "UNIROL", "Roller"],
        "Vonkajšie rolety",
        "vonkajsie_rolety.jpg",
        "Vonkajšie rolety neprepustia slnečné lúče a doprajú vám ničím nerušený spánok. "
        "Blokujú až 100 % slnečného žiarenia ešte pred sklom, čím v lete výrazne znižujú teplotu v interiéri "
        "a v zime fungujú ako tepelná izolácia. Vyrábajú sa z kvalitných hliníkových alebo PVC lamiel presne na mieru.\n"
        "- 100 % zatienenie interiéru – pre dokonalý spánok a odpočinok kedykoľvek počas dňa\n"
        "- V lete výrazne znižujú teplotu v miestnosti a šetria náklady na klimatizáciu\n"
        "- V zime tvoria ďalšiu vrstvu tepelnej izolácie okna – preukázateľná úspora na vykurovaní\n"
        "- Znižujú hluk z okolia – vhodné pre rušné ulice a mestské lokality\n"
        "- Chránia okno pred dažďom, krupobitím a silným vetrom\n"
        "- Poistka proti vytiahnutiu sťažuje neoprávnený vstup – aktívna bezpečnostná ochrana\n"
        "- Možnosť doplniť o integrovanú sieť proti hmyzu a motorické ovládanie Somfy (systém Tahoma)\n"
        "Záruka 4 roky na výrobok, 5 rokov na motory Somfy.",
    ),
    (
        ["screen", "Screen"],
        "Screenové rolety",
        "screenove_rolety.jpg",
        "Screenové rolety predstavujú trend vo vonkajšom tienení posledných rokov. "
        "Nielenže výborne tienia, ale vďaka veľkej farebnej škále látok aj konštrukcií skvele vyzerajú "
        "a dodávajú fasáde moderný vzhľad. Na výber sú systémy s vedením v lanku, lište alebo so zipom "
        "pre maximálnu odolnosť voči vetru.\n"
        "- Výborne tienia a znižujú tepelnú záťaž – interiér ostáva chladný aj v horúcich letných dňoch\n"
        "- Umožňujú súčasne tieniť aj vetrať pri otvorenom okne – bez kompromisov\n"
        "- Zachovávajú výhľad von – zvnútra vidíte, zvonka nie\n"
        "- ZIP systém zvyšuje odolnosť voči vetru a zabraňuje prenikaniu svetla cez okraje clony\n"
        "- Moderný estetický vzhľad – dostupné v širokej škále farieb a typov látok (akryl, black-out)\n"
        "- Látky sú UV stabilné, impregnované a ľahko udržiavateľné\n"
        "- Motorické ovládanie Somfy s možnosťou automatizácie podľa intenzity slnečného žiarenia\n"
        "Záruka 4 roky. Systémy: UNIROL, SUNROL, V-ROL s vedením v lanku, lište alebo ZIP.",
    ),
    (
        ["EXT", "siet", "hmyz", "okenn"],
        "Siete proti hmyzu (okenné)",
        "okenne_siete.jpg",
        "Siete proti hmyzu Climax sú nenápadná a účinná ochrana pred hmyzom a pylovými alergiami. "
        "Nekazí výhľad, ľahko sa udržujú a sú vhodné pre všetky typy okien aj dverí. "
        "V ponuke sú pevné, rolovacie, dverné, posuvné aj plisé varianty pre každý typ otvoru.\n"
        "- Spoľahlivo bránia vstupu hmyzu do interiéru – pokojný spánok bez komárov a mušiek\n"
        "- Špeciálna protipylová sieťovina – ideálna pre alergikov na peľ\n"
        "- Neblokujú výhľad ani prúdenie vzduchu – okno funguje bežným spôsobom\n"
        "- Rolovacie varianty sa rýchlo stiahnu do boxu, keď sieť nepotrebujete\n"
        "- Dverná sieť s magnetom a samozatváracím systémom – praktická pri rušných vstupoch\n"
        "- Možnosť dvierok pre psa alebo mačku – špeciálny priechod priamo v dvernej sieti\n"
        "- Hliníkový rám vo farbách RAL – farebne zladiteľný s oknami alebo fasádou\n"
        "Záruka 4 roky. Vhodné pre plastové, hliníkové aj drevené okná a dvere.",
    ),
    (
        ["PS Z", "posuvn", "dvern"],
        "Siete proti hmyzu (dverné)",
        "dverne_siete.jpg",
        "Posuvné dverné siete umožňujú pohodlný prechod bez použitia rúk. "
        "Automatické zatváranie zabraňuje prieniku hmyzu. Vhodné pre balkónové aj vstupné dvere.\n"
        "- Pohodlný prechod bez použitia rúk – automatické zatváranie po každom prechode\n"
        "- Spoľahlivá ochrana pred hmyzom pri otvorených dverách\n"
        "- Hliníkový rám vo farbách RAL – farebne zladiteľný s dverami alebo fasádou\n"
        "- Vhodné pre balkónové, terasové aj vstupné dvere\n"
        "Záruka 4 roky. Vhodné pre plastové, hliníkové aj drevené dvere.",
    ),
    (
        ["markiz"],
        "Markízy",
        "markizy.jpg",
        "Markíza je najrýchlejší spôsob, ako si na terase alebo balkóne vytvoriť tienistý kút. "
        "Chráni pred priamym slnkom, zabraňuje prehrievaniu interiéru a predlžuje životnosť záhradného nábytku. "
        "V ponuke sú kazetové aj otvorené markízy vo viac ako 100 farebných kombináciách.\n"
        "- Vytvárajú príjemný tieň na terase, balkóne či záhrade – bez nutnosti stavebných úprav\n"
        "- Zabraňujú prenikaniu slnečných lúčov do interiéru a znižujú teplotu vo vnútri domu\n"
        "- Kazetová konštrukcia (box) chráni látku pred poveternostnými vplyvmi, keď markíza nie je v prevádzke\n"
        "- Motorické ovládanie so senzorom vetra a slnka – markíza sa automaticky zroluje pri nepohode\n"
        "- Látky sú impregnované, odolné voči plesniam a UV žiareniu – stálofarebné po celú dobu životnosti\n"
        "- Maximálna šírka až 6,5 m a výsuv až 4 m – vhodné aj pre veľké terasy a reštaurácie\n"
        "- Možnosť montáže na stenu, krokvy alebo strop – riešenie pre každý typ objektu\n"
        "Záruka 4 roky. Chráni záhradný nábytok pred UV žiarením a predlžuje jeho životnosť.",
    ),
    (
        ["pergol", "Lamelino"],
        "Pergoly",
        "pergoly.jpg",
        "Lamelino je prémiová bioklimatická pergola s otočnými hliníkovými lamelami, ktoré sa plynulo naklápajú "
        "od 0° do 125°. Umožňujú presné riadenie tienenia, vetrania aj ochrany pred dažďom jedným ovládačom. "
        "Je bezúdržbová a udrží zaťaženie až 1,5 tony na lamelách – rýdzo český výrobok.\n"
        "- Otočné hliníkové lamely (0°–125°) regulujú svetlo, vzduch aj ochranu pred dažďom podľa aktuálnej potreby\n"
        "- Dostupná v dvoch vyhotoveniach: Lamelino single (4 stojky) a Lamelino wall (kotvená do steny, 2 stojky)\n"
        "- Hliníková konštrukcia nepodlieha korózii a nevyžaduje žiadnu údržbu po celú dobu životnosti\n"
        "- Odtokový systém v stojkách odvedie dažďovú vodu mimo terasy – priestor ostáva suchý\n"
        "- Motorické ovládanie 24V s diaľkovým ovládačom, automatikou alebo smart home systémom (Tahoma)\n"
        "- Voliteľné senzory slnka, vetra a dažďa – pergola automaticky reaguje na počasie\n"
        "- 6 základných farieb + možnosť lakovania v ľubovoľnom odtieni RAL\n"
        "Záruka 4 roky na výrobok, 5 rokov na motor Somfy/Geiger. Odolnosť voči vetru trieda 6 Beaufortovej stupnice.",
    ),
    (
        ["vnutorn", "interier"],
        "Vnútorné žalúzie",
        "vnutorne_zaluzie.jpg",
        "Vnútorné hliníkové žalúzie plynulo regulujú množstvo svetla v interiéri a chránia pred slnkom "
        "aj zvedavými pohľadmi. Hodia sa takmer na akýkoľvek typ okna a lákajú cenovou dostupnosťou, "
        "jednoduchou obsluhou aj nenáročnou údržbou. Ideálny doplnok k vonkajšiemu tieneniu.\n"
        "- Plynulá regulácia svetla a súkromia – žalúzie otočíte i spustíte presne podľa potreby\n"
        "- Cenovo dostupné tienenie vhodné pre byty, rodinné domy, kancelárie aj reštaurácie\n"
        "- Hliníkové lamely šírky 25 mm, 35 mm alebo 50 mm – výber podľa typu okna a preferencie\n"
        "- Detská poistka zabraňuje nebezpečnému omotaniu šnúry – bezpečnosť pre celú rodinu\n"
        "- Minimálna údržba – jednoduché čistenie bežnou vlhkou utierkou\n"
        "- Možnosť montáže na rám okna, do ostenia alebo do medziokenného priestoru\n"
        "- Bohatý výber farieb a imitácií dreva – jednoduché ladenie s interiérom\n"
        "Záruka 4 roky. Modely: IDX, MAX, Harmony, Super Eko, Mono SC, INT-35, INT-50.",
    ),
    (
        ["latkove", "tienenie"],
        "Látkové tienenie",
        "latkove_tienenie.jpg",
        "Vnútorné látkové tienenie je dekoratívny aj praktický prvok každého domova. "
        "Účinne reguluje množstvo svetla v miestnosti, dotvára atmosféru interiéru a je ideálnym doplnkom "
        "k vonkajšiemu tieneniu. Vyberať môžete zo širokého množstva farieb, dekorov, typov látok i druhov tienenia.\n"
        "- Plynulá regulácia denného svetla – od jemného pološera až po úplné zatemnenie\n"
        "- Látkové rolety sú elegantným doplnkom pre byty, domy aj komerčné priestory\n"
        "- Vertikálne žalúzie sú ideálne na francúzske okná, posuvné dvere a veľké presklené plochy\n"
        "- Bohatý výber látok – priehľadné, polotienivé, zatemňujúce (black-out) aj dekorované\n"
        "- Impregnované látky odpudzujú prach a sú ľahko udržiavateľné\n"
        "- Vhodné ako doplnok k vonkajšiemu tieneniu – interiér dostane ucelený, harmonický vzhľad\n"
        "- Vyhotovenie presne na mieru pre každý typ okna alebo dverí\n"
        "Záruka 4 roky. Typy: látkové rolety, vertikálne žalúzie.",
    ),
    (
        ["komponent", "motor", "ovladac", "EVB", "receiver", "Slim"],
        "Komponenty / elektro",
        "komponenty.jpg",
        "Motorické pohony, diaľkové ovládače, senzory a príslušenstvo pre tieniacu techniku. "
        "Kompatibilné so systémami SOMFY a Climax. Profesionálna inštalácia a nastavenie.",
    ),
]


def zisti_produkt(typ_produktu: str) -> tuple[str, str | None, str | None, str]:
    if not typ_produktu:
        return "", None, None, ""
    tp = typ_produktu.lower()
    for klucove_slova, nazov, fotka, popis in PRODUKT_MAPA:
        if any(k.lower() in tp for k in klucove_slova):
            foto_path = PRODUKTY_DIR / fotka
            detail_fotka = fotka.replace(".jpg", "_detail.jpg")
            foto_detail_path = PRODUKTY_DIR / detail_fotka
            return (
                nazov,
                str(foto_path) if foto_path.exists() else None,
                str(foto_detail_path) if foto_detail_path.exists() else None,
                popis,
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
