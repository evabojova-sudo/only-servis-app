# OnlyServis — Automatizácia cenových ponúk

## Aktuálny stav (máj 2026)
Fáza 1 ✅ — POST /extract-pdf (Claude API extrakcia z PDF)
Fáza 2 ✅ — POST /generate-pdf (WeasyPrint generovanie PDF)
Fáza 3 ✅ — Databáza PostgreSQL na Railway
Fáza 4 ✅ — Email — funguje cez Resend API (RESEND_API_KEY + GMAIL_SENDER v Railway env vars)
             SMTP nahradený Resend HTTP API — Railway blokoval port 587
Fáza 5 ✅ — Frontend — funguje na Railway
Fáza 6 ✅ — Deploy Railway + Dockerfile funguje
Fáza 7 ✅ — Všeobecný text (Poznámka / GDPR / DÔLEŽITÉ!) doplnený na koniec PDF (11.5.2026)
             Priečinok static/images/produkty/ vytvorený, čaká na obrázky od Romana

## Zmeny z 12–13.5.2026 (Roman's pripomienky)
- Hlavička PDF: DIČ 2122069488, IČ DPH SK2122069488 — každý údaj na vlastnom riadku
- Súhrnná tabuľka: "Spolu bez DPH" (bolo "Medzisúčet"), príplatky nie sú samostatný riadok
- Cena produktu v riadku = len produkt bez príplatkov; súhrnná suma zahŕňa príplatky
- Termín dodania: "obvykle do 14 prac. dní", Záruka: "48 mesiacov"
- Odstránený podpis "r machala _" z poznámky
- Climax "4 ROKY ZÁRUKA" logo pri odberateľovi (static/images/climax_zaruka.jpg)
- WhatsApp QR kód v hlavičke (generovaný dynamicky pre wa.me/421903533534, knižnica qrcode[pil])
- Súhrnná tabuľka: page-break-inside avoid
- Extrakcia + zobrazenie poľa `poznamka` (Romanov text z CN, nie boilerplate)
- Položkový rozpis produktov: pole `polozky` v extrakcii, tabuľka Produkt|Miestnosť|Rozmery|Cena/ks v PDF
  Miestnosť stĺpec iba ak CN obsahuje štítky; fallback na starý riadok ak polozky prázdne
- DB: polozky_ponuky rozšírená o stĺpce poznamka, popis_polozky, cena_ks

## Čo NESMIEŠ meniť bez môjho súhlasu
- endpoint /extract-pdf — funguje
- endpoint /generate-pdf — funguje
- endpoint /process — funguje
- Dockerfile — Railway deploy funguje, WeasyPrint správne nakonfigurovaný
- databázová štruktúra (tabuľky: zakaznici, ponuky, polozky_ponuky)
- email_sender.py — nemeň kým nedostaneš explicitnú inštrukciu

## Technická architektúra
- Backend: Python FastAPI na Railway
- PDF čítanie: Claude API (claude-sonnet-4-5) — vizuálne čítanie
- PDF generovanie: WeasyPrint z HTML šablóny
- DB: PostgreSQL na Railway
- Email: Resend API (premenné: RESEND_API_KEY, GMAIL_SENDER)
- Frontend: HTML/JS na Railway (Fáza 5 — funguje)
- Obrázky produktov: /static/images/produkty/
- Logo: /static/images/logo_onlyservis.jpg

## Pravidlá práce
- Pred zmenou akéhokoľvek existujúceho súboru sa ma opýtaj a vysvetli prečo
- Nerob zmeny mimo rozsah aktuálnej úlohy
- Po každej zmene mi povedz presne čo si zmenil
- Pri chybe najprv vyčerpaj existujúce riešenia, nezavadzaj nové patterny

## Aktuálna úloha
Pozri TASKS.md — tam sú všetky otvorené úlohy a feedback.

## Firemné údaje (používaj v generovaných PDF a emailoch)
only servis s.r.o.
Adresa: Lermontovova 911/3, 811 05 Bratislava
Kontakt: Machala Roman
Telefón: 0903 533 534
Email: info@onlyservis.sk
IČO: 55639461
Farby: modrá #1B3A8C, žltá #FFD700
