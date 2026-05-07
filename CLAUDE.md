# OnlyServis — Automatizácia cenových ponúk

## Aktuálny stav (máj 2026)
Fáza 1 ✅ — POST /extract-pdf (Claude API extrakcia z PDF)
Fáza 2 ✅ — POST /generate-pdf (WeasyPrint generovanie PDF)
Fáza 3 ✅ — Databáza PostgreSQL na Railway
Fáza 4 ❌ — Gmail/email — padá: [Errno 101] Network is unreachable
             SMTP prístup (GMAIL_SENDER + GMAIL_APP_PASSWORD v Railway env vars)
             Fungovalo predtým — rozbil sa počas WeasyPrint opráv dňa 6.5.2026
Fáza 5 ⚠️  — Frontend — deploy na Railway, testujeme
Fáza 6 ✅ — Deploy Railway + Dockerfile funguje

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
- Email: SMTP s app password (premenné: GMAIL_SENDER, GMAIL_APP_PASSWORD)
- Frontend: HTML/JS na Railway (Fáza 5 — testujeme)
- Obrázky produktov: /static/images/produkty/
- Logo: /static/images/logo_onlyservis.jpg

## Pravidlá práce
- Pred zmenou akéhokoľvek existujúceho súboru sa ma opýtaj a vysvetli prečo
- Nerob zmeny mimo rozsah aktuálnej úlohy
- Po každej zmene mi povedz presne čo si zmenil
- Pri chybe najprv vyčerpaj existujúce riešenia, nezavadzaj nové patterny

## Aktuálna úloha
Testujeme a dopĺňame frontend (Fáza 5).
Email (Fáza 4) odložený — riešiť v samostatnej session.
Pred akoukoľvek zmenou mi vysvetli čo chceš zmeniť a prečo.

## Firemné údaje (používaj v generovaných PDF a emailoch)
Only Servis s.r.o.
Adresa: Lermontovova 911/3, 811 05 Bratislava
Kontakt: Machala Roman
Telefón: 0903 533 534
Email: info@climaxsk.sk
IČO: 55639461
Farby: modrá #1B3A8C, žltá #FFD700
