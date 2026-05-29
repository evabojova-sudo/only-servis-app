# OnlyServis — Úlohy a feedback

## Pravidlá
- Úlohy vykonávaj v poradí ako sú uvedené
- Po dokončení každej úlohy:
  1. Zaznač ju ako ✅ hotovo
  2. Opýtaj sa Evy či potvrdzuje že úloha je hotová
  3. Až po potvrdení pokračuj na ďalšiu úlohu
- Pred každou zmenou vysvetli čo chceš zmeniť a prečo
- Nerob zmeny mimo rozsah aktuálnej úlohy

## 🔴 Otvorené (bugy)
- [ ] Pomalé spracovanie — Roman, 7.5.2026
      (upresniť: je pomalá extrakcia PDF, generovanie, alebo celý flow?)

- [x] Bug: zisti_produkt() padá keď typ_produktu je None — 26.5.2026
      Fix: guard na začiatku funkcie, vracia bezpečné defaulty ("", None, None, "").

- [x] Bug: manuálne príplatky sa nezapočítavali do celkovej sumy PDF — 26.5.2026
      Fix: pridané pole priplatky_v_cene (frontend sleduje sumu extrahovaných príplatkov),
      pdf_generator.py prepočítava suhrn_bez_dph a CELKOVÚ CENU S DPH správne.

- [x] Bug: sieť CN (s36, ROLO DS) zobrazovala komponentovú tabuľku — 29.5.2026
      Fix A (pdf_generator.py): je_komponenty závisí od sirka_cm v polozky, nie od typ_produktu.
      Fix B (main.py): extraction prompt — typ_produktu sa extrahuje IBA z tabuľky, nie zo suffixu CN čísla.

- [x] Bug: servisné CNy (MAX21, DS servis) zobrazovali produktovú tabuľku — 29.5.2026
      Fix: je_servis detekcia podľa typ_vyrobku v polozky má prednosť pred je_komponenty.

- [x] Bug: Dveřní EXTRA matchovala okenne_siete namiesto dverne_siete — 29.5.2026
      Fix: odstránené príliš generické "extra" z okenne_siete, pridané "dveřní"/"dveřní extra" do dverne_siete.

- [x] Bug: príplatková tabuľka servisných CNov bola užšia — 29.5.2026
      Fix: col_count=7 pre je_servis (7 stĺpcov), col_count=6 pre je_komponenty (6 stĺpcov).

## 📋 Nové úlohy (poradie záväzné)

### 1. ✅ BUG: poznámka — stratené riadkovanie
**Súbor:** templates/ponuka.html
Poznámka extrahovaná z Climax PDF sa zobrazuje ako jeden riadok. Zachovaj pôvodné riadkové zlomy tak ako sú v zdrojovom texte.

### 2. ✅ NOVÁ FUNKCIONALITA: podpora pre ponuky typu komponenty — 26.5.2026
**Súbory:** extract prompt, pdf_generator.py, templates/ponuka.html
Hotovo: extrakcia polozky[], je_komponenty flag, tabuľka komponentov v PDF.
Fix: col_count=6 pre komponenty CNs — príplatky sekcia zarovnaná na plnú šírku.

### 3. ✅ VIZUÁL: zmenšiť text v hlavičke — 26.5.2026
**Súbor:** templates/ponuka.html
Hotovo: .hdr-firma 13pt→10pt, .hdr-right 11pt→9pt.

### 4. ✅ VIZUÁL: QR kód — WhatsApp dizajn — 26.5.2026
Hotovo: QR 60pt→45pt (rovnaká výška ako logo), popisok "Napíšte nám na WhatsApp" pod QR kódom.

### 5. ✅ VIZUÁL: záverečný text na samostatnú stranu — 26.5.2026
Hotovo: page-break-before na .podmienky div — statický záverečný blok vždy začína na novej strane. Extrahovaná poznámka zostáva pred súhrnom.

### 6. ✅ OBSAH: texty produktov — 27.5.2026
**Súbor:** templates/ponuka.html
Vlož texty produktov do šablóny. Každý text obsahuje úvodný odsek aj bullet pointy — zobraz oboje, oddelené čiarou. Mapovanie na typ_produktu už existuje v kóde.

Texty:

**vonkajsie_zaluzie**
Vonkajšie žalúzie zastavujú slnečné lúče ešte pred oknami – tam, kde to robí najväčší rozdiel. Vďaka naklopeniu lamiel môžete vetrať a pritom plynule regulovať množstvo svetla aj teplotu v interiéri. Sú funkčným aj estetickým doplnkom každého rodinného domu či kancelárskej budovy.
- V lete zabraňujú prehrievaniu interiéru – teplota v miestnosti môže klesnúť o niekoľko stupňov Celzia
- V zime fungujú ako ďalšia vrstva tepelnej izolácie okna a šetria náklady na kúrenie
- Umožňujú vetranie otvoreným oknom pri zachovaní regulácie svetla a súkromia
- Chránia vaše súkromie – zvonku nikto nevidí dnu, vy vidíte von
- Spoľahlivo chránia okno pred prudkým dažďom, vetrom, krupobitím a UV žiarením
- Bezpečnostný efekt – sú neľahkou prekážkou pri pokuse o neoprávnené vniknutie
- Široký výber modelov (Z-90 Noval, Z-70, T-80, C-80, C-60, F-80, PROTAL a ďalšie) a farieb lamiel
Záruka 4 roky. Montáž zabezpečujeme v Bratislavskom a Trnavskom kraji.

**vonkajsie_rolety**
Vonkajšie rolety neprepustia slnečné lúče a doprajú vám ničím nerušený spánok. Blokujú až 100 % slnečného žiarenia ešte pred sklom, čím v lete výrazne znižujú teplotu v interiéri a v zime fungujú ako tepelná izolácia. Vyrábajú sa z kvalitných hliníkových alebo PVC lamiel presne na mieru.
- 100 % zatienenie interiéru – pre dokonalý spánok a odpočinok kedykoľvek počas dňa
- V lete výrazne znižujú teplotu v miestnosti a šetria náklady na klimatizáciu
- V zime tvoria ďalšiu vrstvu tepelnej izolácie okna – preukázateľná úspora na vykurovaní
- Znižujú hluk z okolia – vhodné pre rušné ulice a mestské lokality
- Chránia okno pred dažďom, krupobitím a silným vetrom
- Poistka proti vytiahnutiu sťažuje neoprávnený vstup – aktívna bezpečnostná ochrana
- Možnosť doplniť o integrovanú sieť proti hmyzu a motorické ovládanie Somfy (systém Tahoma)
Záruka 4 roky na výrobok, 5 rokov na motory Somfy.

**markizy**
Markíza je najrýchlejší spôsob, ako si na terase alebo balkóne vytvoriť tienistý kút. Chráni pred priamym slnkom, zabraňuje prehrievaniu interiéru a predlžuje životnosť záhradného nábytku. V ponuke sú kazetové aj otvorené markízy vo viac ako 100 farebných kombináciách.
- Vytvárajú príjemný tieň na terase, balkóne či záhrade – bez nutnosti stavebných úprav
- Zabraňujú prenikaniu slnečných lúčov do interiéru a znižujú teplotu vo vnútri domu
- Kazetová konštrukcia (box) chráni látku pred poveternostnými vplyvmi, keď markíza nie je v prevádzke
- Motorické ovládanie so senzorom vetra a slnka – markíza sa automaticky zroluje pri nepohode
- Látky sú impregnované, odolné voči plesniam a UV žiareniu – stálofarebné po celú dobu životnosti
- Maximálna šírka až 6,5 m a výsuv až 4 m – vhodné aj pre veľké terasy a reštaurácie
- Možnosť montáže na stenu, krokvy alebo strop – riešenie pre každý typ objektu
Záruka 4 roky. Chráni záhradný nábytok pred UV žiarením a predlžuje jeho životnosť.

**markizy_gardena**
Gardena 350 je robustná kazetová markíza s hlbokým boxom 350 mm, určená pre náročných zákazníkov, ktorí hľadajú spoľahlivé a elegantné riešenie pre veľkú terasu. Motorika Somfy io zaručuje pohodlné ovládanie a možnosť prepojenia so smart home systémom.
- Šírka až 600 cm v jednodielnom prevedení – pokryje veľkú terasu rodinného domu jedným ťahom
- Hlboká kazeta (box 350 mm) chráni látku pred dažďom, prachom a UV žiarením počas zrolovania
- Motorické ovládanie Somfy io – diaľkový ovládač, mobilný telefón alebo riadiaca automatika
- Možnosť doplniť o senzor slnka a vetra – automatické zrolovanie pri silnom vetre alebo búrke
- Bohatý výber akrylátových látok odolných voči vyblednutiu a plesniam
- Dostupná v mnohých farbách konštrukcie vrátane RAL odtieňov podľa požiadavky
- Certifikované komponenty európskej výroby – dlhá životnosť a overená spoľahlivosť
Záruka 4 roky na výrobok, 5 rokov na motor Somfy.

**screenove_rolety**
Screenové rolety predstavujú trend vo vonkajšom tienení posledných rokov. Nielenže výborne tienia, ale vďaka veľkej farebnej škále látok aj konštrukcií skvele vyzerajú a dodávajú fasáde moderný vzhľad. Na výber sú systémy s vedením v lanku, lište alebo so zipom pre maximálnu odolnosť voči vetru.
- Výborne tienia a znižujú tepelnú záťaž – interiér ostáva chladný aj v horúcich letných dňoch
- Umožňujú súčasne tieniť aj vetrať pri otvorenom okne – bez kompromisov
- Zachovávajú výhľad von – zvnútra vidíte, zvonka nie
- ZIP systém zvyšuje odolnosť voči vetru a zabraňuje prenikaniu svetla cez okraje clony
- Moderný estetický vzhľad – dostupné v širokej škále farieb a typov látok (akryl, black-out)
- Látky sú UV stabilné, impregnované a ľahko udržiavateľné
- Motorické ovládanie Somfy s možnosťou automatizácie podľa intenzity slnečného žiarenia
Záruka 4 roky. Systémy: UNIROL, SUNROL, V-ROL s vedením v lanku, lište alebo ZIP.

**pergoly_vitalia**
Vitalia je pergola s pevnou hliníkovou konštrukciou a sťahujúcou sa PVC strechou, ktorá terasu premení na plnohodnotný pobytový priestor. Chráni pred slnkom aj ľahkým dažďom a predlžuje sezónu na terase. Vyrába sa na mieru – šírky od 150 do 1 300 cm.
- Chráni pred slnkom aj ľahkým dažďom – terasa ostáva využiteľná aj pri menšej nepohode
- Predlžuje sezónu na terase – naplno ju využijete od jari do neskorej jesene
- Pevná hliníková konštrukcia je odolná voči poveternostným vplyvom a nevyžaduje žiadnu údržbu
- Vodoodolné PVC látky v základných farbách, možnosť polopriesvitnej varianty
- Motorické ovládanie elektromotorom 230V – diaľkový ovládač alebo systém Tahoma
- Voliteľný senzor slnka, vetra alebo dažďa – automatické stiahnutie strechy pri nepohode
- Možnosť integrovaného LED osvetlenia HDD LUX so stmievačom pre večerné posedenie
Záruka 4 roky. Kotvenie na stenu aj voľne stojace na betónových pätkách.

**pergoly_lamelino**
Lamelino je prémiová bioklimatická pergola s otočnými hliníkovými lamelami, ktoré sa plynulo naklápajú od 0° do 125°. Umožňujú presné riadenie tienenia, vetrania aj ochrany pred dažďom jedným ovládačom. Je bezúdržbová a udrží zaťaženie až 1,5 tony na lamelách – rýdzo český výrobok.
- Otočné hliníkové lamely (0°–125°) regulujú svetlo, vzduch aj ochranu pred dažďom podľa aktuálnej potreby
- Dostupná v dvoch vyhotoveniach: Lamelino single (4 stojky) a Lamelino wall (kotvená do steny, 2 stojky)
- Hliníková konštrukcia nepodlieha korózii a nevyžaduje žiadnu údržbu po celú dobu životnosti
- Odtokový systém v stojkách odvedie dažďovú vodu mimo terasy – priestor ostáva suchý
- Motorické ovládanie 24V s diaľkovým ovládačom, automatikou alebo smart home systémom (Tahoma)
- Voliteľné senzory slnka, vetra a dažďa – pergola automaticky reaguje na počasie
- 6 základných farieb + možnosť lakovania v ľubovoľnom odtieni RAL
Záruka 4 roky na výrobok, 5 rokov na motor Somfy/Geiger. Odolnosť voči vetru trieda 6 Beaufortovej stupnice.

**okenne_siete**
Siete proti hmyzu Climax sú nenápadná a účinná ochrana pred hmyzom a pylovými alergiami. Nekazí výhľad, ľahko sa udržujú a sú vhodné pre všetky typy okien aj dverí. V ponuke sú pevné, rolovacie, dverné, posuvné aj plisé varianty pre každý typ otvoru.
- Spoľahlivo bránia vstupu hmyzu do interiéru – pokojný spánok bez komárov a mušiek
- Špeciálna protipylová sieťovina – ideálna pre alergikov na peľ
- Neblokujú výhľad ani prúdenie vzduchu – okno funguje bežným spôsobom
- Rolovacie varianty sa rýchlo stiahnu do boxu, keď sieť nepotrebujete
- Dverná sieť s magnetom a samozatváracím systémom – praktická pri rušných vstupoch
- Možnosť dvierok pre psa alebo mačku – špeciálny priechod priamo v dvernej sieti
- Hliníkový rám vo farbách RAL – farebne zladiteľný s oknami alebo fasádou
Záruka 4 roky. Vhodné pre plastové, hliníkové aj drevené okná a dvere.

**vnutorne_zaluzie**
Vnútorné hliníkové žalúzie plynulo regulujú množstvo svetla v interiéri a chránia pred slnkom aj zvedavými pohľadmi. Hodia sa takmer na akýkoľvek typ okna a lákajú cenovou dostupnosťou, jednoduchou obsluhou aj nenáročnou údržbou. Ideálny doplnok k vonkajšiemu tieneniu.
- Plynulá regulácia svetla a súkromia – žalúzie otočíte i spustíte presne podľa potreby
- Cenovo dostupné tienenie vhodné pre byty, rodinné domy, kancelárie aj reštaurácie
- Hliníkové lamely šírky 25 mm, 35 mm alebo 50 mm – výber podľa typu okna a preferencie
- Detská poistka zabraňuje nebezpečnému omotaniu šnúry – bezpečnosť pre celú rodinu
- Minimálna údržba – jednoduché čistenie bežnou vlhkou utierkou
- Možnosť montáže na rám okna, do ostenia alebo do medziokenného priestoru
- Bohatý výber farieb a imitácií dreva – jednoduché ladenie s interiérom
Záruka 4 roky. Modely: IDX, MAX, Harmony, Super Eko, Mono SC, INT-35, INT-50.

**latkove_tienenie**
Vnútorné látkové tienenie je dekoratívny aj praktický prvok každého domova. Účinne reguluje množstvo svetla v miestnosti, dotvára atmosféru interiéru a je ideálnym doplnkom k vonkajšiemu tieneniu. Vyberať môžete zo širokého množstva farieb, dekorov, typov látok i druhov tienenia.
- Plynulá regulácia denného svetla – od jemného pološera až po úplné zatemnenie
- Látkové rolety sú elegantným doplnkom pre byty, domy aj komerčné priestory
- Vertikálne žalúzie sú ideálne na francúzske okná, posuvné dvere a veľké presklené plochy
- Bohatý výber látok – priehľadné, polotienivé, zatemňujúce (black-out) aj dekorované
- Impregnované látky odpudzujú prach a sú ľahko udržiavateľné
- Vhodné ako doplnok k vonkajšiemu tieneniu – interiér dostane ucelený, harmonický vzhľad
- Vyhotovenie presne na mieru pre každý typ okna alebo dverí
Záruka 4 roky. Typy: látkové rolety, vertikálne žalúzie.

### 6b. ⬜ OVERENIE: výpočet a zobrazenie zliav
**Súbory:** main.py (extraction prompt), pdf_generator.py, templates/ponuka.html
Otestovať na reálnej CN s zľavou (napr. Lukáčková Z90io).

Čo treba overiť:
1. Extrakcia: `cena_bez_dph` = cena PRED zľavou, `zlava_suma` = správna suma, `cena_po_zlave` = cena po zľave
2. Príplatky: `suma` = celková (nie jednotková) cena za položku
3. PDF súhrn: zobrazuje riadky "Cena pred zľavou / Zľava X% / Spolu bez DPH"
4. Výsledná cena s DPH = správna hodnota zhodná s originálom

Ak extrakcia stále vracia nesprávne hodnoty, upresniť prompt ďalej.

### 7. ✅ OBSAH: záverečný text — informačné podmienky — 27.5.2026
Hotovo: nahradený starý text (Poznámka/GDPR/DÔLEŽITÉ!) novými 8 sekciami "Informačné podmienky k cenovej ponuke". Fix page-break-after: avoid na nadpisoch sekcií.
**Súbor:** templates/ponuka.html
Nahraď aktuálnu sekciu (Poznámka / GDPR / DÔLEŽITÉ!) novou samostatnou stranou s nadpisom "Informačné podmienky k cenovej ponuke" a týmto textom:

1. Ochrana osobných údajov (GDPR)
Osobné údaje sú spracúvané v súlade s Nariadením Európskeho parlamentu a Rady (EÚ) 2016/679 (GDPR) a zákonom č. 18/2018 Z. z. o ochrane osobných údajov. Právnym základom spracúvania je plnenie zmluvy alebo vykonanie predzmluvných opatrení na žiadosť dotknutej osoby podľa čl. 6 ods. 1 písm. b) GDPR a oprávnený záujem prevádzkovateľa na sprostredkovaní kontaktov a komunikácii s dodávateľmi v rámci dopytového konania podľa čl. 6 ods. 1 písm. f) GDPR. Dotknutá osoba má právo na prístup k údajom, ich opravu, vymazanie, obmedzenie spracúvania, prenosnosť, ako aj právo namietať proti spracúvaniu. Bližšie informácie poskytne prevádzkovateľ na vyžiadanie.

2. Záručné podmienky
Záručná doba na dodané výrobky a vykonané práce je 24 mesiacov a začína plynúť dňom prevzatia diela, ak nie je písomne dohodnuté inak. Na výrobky značiek CLIMAX a SOMFY sa vzťahujú aj záručné podmienky príslušných výrobcov. V prípade rozporu medzi týmito podmienkami a podmienkami výrobcu platia podmienky, ktoré sú pre zákazníka výhodnejšie. Záruka sa nevzťahuje na vady spôsobené bežným opotrebovaním, neodbornou manipuláciou, zásahom tretej osoby alebo nedodržaním pokynov výrobcu.

3. Podklady pre cenovú ponuku
Cenová ponuka je vypracovaná na základe podkladov, rozmerov a informácií poskytnutých zákazníkom. Dodávateľ nezodpovedá za nepresnosti kalkulácie spôsobené neúplnými, nesprávnymi alebo zastaranými podkladmi. Cenová ponuka je platná 30 dní od dátumu vystavenia, ak nie je uvedené inak. Pred realizáciou diela je zákazník povinný umožniť dodávateľovi vykonanie obhliadky alebo zabezpečiť overenie skutočného stavu na mieste; dodatočné práce vyplývajúce z odlišného skutočného stavu budú nacenené samostatne.

4. Servis a zásahy do existujúcich zariadení
Servisné zásahy do existujúcich zariadení sú svojou povahou rizikové, najmä pri kombinácii komponentov rôznych výrobcov, starších systémov alebo zariadení s neznámou históriou. Dodávateľ vykonáva všetky práce s maximálnou odbornou starostlivosťou, avšak vzhľadom na povahu zásahov nemôže vopred zaručiť plnú funkčnosť systému po vykonaní servisu. Dodávateľ nezodpovedá za: skryté vady existujúcich zariadení, ktoré sa prejavia počas alebo po servisnom zásahu, škody spôsobené nekompatibilitou komponentov, ktorú nebolo možné pri obhliadke zistiť, obmedzenú funkčnosť systému spôsobenú stavom existujúcej inštalácie alebo zastaraním komponentov. Zákazník berie uvedené riziká na vedomie a vyjadruje s nimi súhlas záväzným potvrdením objednávky servisného zásahu.

5. Likvidácia odpadu
Likvidácia obalového a montážneho odpadu nie je súčasťou cenovej ponuky, pokiaľ nie je výslovne dohodnuté inak. Obalové materiály a odpad vzniknutý pri montáži je povinný zlikvidovať zákazník v súlade so zákonom č. 79/2015 Z. z. o odpadoch v znení neskorších predpisov. Likvidáciu odpadu môže na základe samostatnej dohody zabezpečiť dodávateľ za príplatok.

6. Záväznosť objednávky a schválenie technického prevedenia
Potvrdením objednávky zákazník potvrdzuje, že sa oboznámil s technickým prevedením, rozmermi, farebnosťou a ďalšími parametrami výrobku a tieto bez výhrad akceptuje. Prípadné nejasnosti, pripomienky alebo požiadavky na zmenu je zákazník povinný uplatniť pred potvrdením objednávky. Po potvrdení objednávky sa za záväzné považuje naposledy odsúhlasené technické prevedenie. Akékoľvek dodatočné zmeny po potvrdení objednávky môžu byť spoplatnené a môžu predĺžiť termín dodania.

7. Montážne podmienky
Cena montáže zahŕňa práce do pracovnej výšky 5 m. Práce vo výškach nad 5 m, vrátane použitia lešenia, vysokozdvižnej plošiny alebo inej špeciálnej techniky, nie sú súčasťou cenovej ponuky a budú nacenené samostatne na základe podmienok konkrétnej realizácie. Zákazník je povinný zabezpečiť bezpečný prístup k miestu montáže, voľný priestor pre realizáciu prác a primerané podmienky pre prácu.

8. Elektroinštalačné práce
Cenová ponuka nezahŕňa zriadenie nového elektrického napájania, úpravu existujúceho rozvodu, ani akékoľvek elektroinštalačné práce vyžadujúce odbornú spôsobilosť podľa vyhlášky č. 508/2009 Z. z. Tieto práce je zákazník povinný zabezpečiť na vlastné náklady prostredníctvom osoby s príslušným osvedčením. Dodávateľ nezodpovedá za škody spôsobené nevyhovujúcim alebo neodborne vyhotoveným elektrickým napájaním.

Strana má mať menší font ako zvyšok PDF, profesionálny vzhľad, konzistentný so šablónou.

### 8. ✅ OBSAH: šablóna emailu — 27.5.2026
Hotovo: Claude generuje text emailu automaticky, bez markdownu. Fallback na starý text ak AI zlyhá.
⚠️ Čaká na vyjadrenie Romana: chce v podpise len "only servis" alebo celý podpis (Roman Machala, only servis, tel, email)?
Aktuálny podpis: "S pozdravom, Machala Roman, only servis s.r.o., Tel: 0903 533 534, info@onlyservis.sk"

### 8b. ✅ PODPIS EMAILU: vyriešené — 29.5.2026
**Súbory:** main.py alebo email_sender.py
Nahraď existujúci email prompt týmto systémovým promptom:

Napíš stručný a profesionálny sprievodný e-mail k cenovej ponuke pre zákazníka firmy only servis. Dodrž tieto pravidlá:
- Začni presne textom: Dobrý deň,
- Použi formálny, stručný a priateľský tón.
- Uveď, že v prílohe posielaš cenovú ponuku alebo viac cenových ponúk.
- Pri každej ponuke uveď: presný názov súboru, krátky popis obsahu ponuky, najdôležitejšie parametre produktu, či je v cene montáž, doprava, servis, demontáž, ovládač alebo iné služby, celkovú cenu s DPH.
- Nepíš zbytočné detaily.
- Na konci vždy napíš: V prípade otázok alebo záujmu o realizáciu ma neváhajte kontaktovať. Ďakujem a prajem príjemný deň. only servis
- Ak je ponuka jedna, použi jednu odrážku. Ak je ponúk viac, použi prehľadný zoznam s odrážkami.
- Výstup má byť hotový e-mail bez vysvetľovania.

Ukážka 1 — jedna ponuka:
Dobrý deň,
v prílohe Vám posielam cenovú ponuku:
- CP_13052026_Kmetova_servisZ90 – servis žalúzií Z90 vrátane demontáže, montáže, výmeny, nastavenia dorazov, dopravy a nastavenia kovania GU/Rehau. Celková cena s DPH je 244,77 EUR.
V prípade otázok alebo záujmu o realizáciu ma neváhajte kontaktovať.
Ďakujem a prajem príjemný deň.
only servis

Ukážka 2 — viac ponúk:
Dobrý deň,
v prílohe Vám posielam cenové ponuky:
- CP_09052026_Pastorekova_IDX – vnútorné hliníkové žalúzie IDX domyka vrátane brzdy, montáže, demontáže a servisu. Celková cena s DPH je 523,58 EUR.
- CP_08052026_Alexieva_EXT16-oprava – oprava siete proti hmyzu EXT16 vrátane výmeny komponentov. Celková cena s DPH je 51,91 EUR.
V prípade otázok alebo záujmu o realizáciu ma neváhajte kontaktovať.
Ďakujem a prajem príjemný deň.
only servis

### 9. 🔄 ARCHITEKTÚRA: databáza — ukladať až pri objednávke

**9A. ✅ Odstránené DB ukladanie z /process — 29.5.2026**
Ponuky sa viac neukladajú do DB pri generovaní PDF.
Tabuľky zakaznici/ponuky/polozky_ponuky ostávajú pre budúci /objednavka endpoint.

**9B. ⬜ Nový endpoint POST /objednavka — čaká na upresnenie**
Implementovať až keď bude jasné:
- Čo je vstup? (PDF z Climax? manuálne potvrdenie cez frontend? iné?)
- Čo presne sa uloží do DB pri potvrdení objednávky?

---

## 🟡 V riešení
- [ ] Obrázky produktov do PDF — 11.5.2026
      Väčšina dodaná ✅. Chýbajú (nahrať do static/images/produkty/):
      POVINNÉ:
        markizy_gardena.jpg
        pergoly_vitalia.jpg
      VOLITEĽNÉ (detail):
        markizy_gardena_detail.jpg
        pergoly_vitalia_detail.jpg
        latkove_tienenie_detail.jpg
      Komponenty nemajú obrázok (príliš široká škála produktov).

## ✅ Dokončené (29.5.2026 — servisné CNy + bugy siete)

- [x] NOVÁ FUNKCIONALITA: servisná tabuľka pre Climax O24 servis CNy — 29.5.2026
      Detekcia: je_servis = polozky majú typ_vyrobku pole
      Extrakcia: typ_vyrobku, vyrobok, oprava_1/2/3, pocet_ks, cena_ks, cena_riadok
      Template: nová tabuľka Č.|Typ výrobku|Výrobok|Popis opravy|Ks|Cena/ks|Cena
      Foto/popis produktu sa pre servisné CNy NEzobrazuje
      page-break-inside: avoid na riadkoch servisnej tabuľky

- [x] PRODUKT_MAPA prepracovaná z listu tuplov na dict (klucove_slova / nazov / obrazok / popis) — 29.5.2026
- [x] Kľúčové slová aktualizované podľa reálnych Climax kódov z CN PDF — 29.5.2026
      Vonkajšie žalúzie: pridané T-80, C-80 (+ VENTAL, CC), C-60, F-80, EXT-50, PROTAL
      Rolety, siete, markízy, vnútorné žalúzie: nahradené generické slová reálnymi kódmi
      ROLO DS, s36, s25: pridané do okenne_siete / dverne_siete
      dveřní, dveřní extra: pridané do dverne_siete (oprava Dveřní EXTRA)
- [x] Oprava popis pre dverne_siete — starý generický text nahradený textom z DOCX — 29.5.2026
- [x] Pridané chýbajúce kategórie markizy_gardena a pergoly_vitalia s textami z DOCX — 29.5.2026
- [x] Odstránené DB ukladanie z /process — 29.5.2026 (úloha 9A)
- [x] Produktová tabuľka: explicitné % šírky stĺpcov (Rozmery 17%, Cena/ks 13%) — 29.5.2026

## ✅ Dokončené
- [x] Fáza 1 — POST /extract-pdf (Claude API extrakcia z PDF)
- [x] Fáza 2 — POST /generate-pdf (WeasyPrint generovanie PDF)
- [x] Fáza 3 — Databáza PostgreSQL na Railway
- [x] Fáza 4 — Email cez Resend.com API
- [x] Fáza 5 — Frontend na Railway
- [x] Fáza 6 — Deploy Railway + Dockerfile
- [x] Webhook Railway-GitHub opravený
- [x] CLAUDE.md vytvorený a synchronizovaný
- [x] Romanov pripomienky z PDF (12.5.2026): DIČ/IČ DPH, súhrnná tabuľka, termíny, logo Climax, QR kód, poznámka, položkový rozpis
- [x] Doplniť všeobecný text na koniec vygenerovaného PDF — 11.5.2026

## 📝 Poznámky
- SMTP nefunguje na Railway — email len cez Resend
- Claude Code: vždy aktualizuj TASKS.md po dokončení úlohy, pýtaj si potvrdenie od Evy
- Pred každou zmenou kódu skontroluj TASKS.md čo je priorita
- Úlohy vykonávaj v poradí 1→9, po každej čakaj na potvrdenie od Evy

## Legenda
⬜ = čaká
🔄 = v procese
✅ = hotovo
