# OnlyServis — Úlohy a feedback

## 🔴 Otvorené
- [ ] Pomalé spracovanie — Roman, 7.5.2026
      (upresniť: je pomalá extrakcia PDF, generovanie, alebo celý flow?)

- [ ] Doplniť všeobecný text na koniec vygenerovaného PDF — 11.5.2026
      Text (zachovať presné znenie):

      Termín dodania je udávaný ako obvyklý jeho skutočná dĺžka môže byť iná (o.i. obmedzenia z vyššej moci - napr.COVID19 ). Vzhľadom k aktuálnej situácii na trhu, sú v súčasnosti sú termíny jednotlivých dodávok tovaru potvrdzované výrobcom priebežne.

      GDPR
      Zákonným dôvodom spracovania osobných údajov je poskytnutie plnenia služby v rámci dopytového konania podľa čl.6 odst. 1 písm. a) GDPR a oprávnený záujem only servis, s.r.o., dopytujúceho a registrovaných dodávateľov na sprostredkovanie kontaktov za účelom plnenia služby podľa čl. 6 odst. 1 písm. f) GDPR.
      Záruka 24mesiacov. Nadštandardná záruka na výrobok sa riadi záručnými podmienkami výrobcov CLIMAX a SOMFY.
      Cenovú kalkuláciu sme spracovali na základe predložených podkladov a preto nenesieme zodpovednosť za prípadné nezrovnalosti podkladov so skutočným stavom na stavbe.

      Likvidácia odpadu (obal je súčasť výrobku podľa zák. č. 56/2018 Z. z. ) nie je predmetom CP ak nie je uvedené inak.

      DÔLEŽITÉ!
      V prípade objednávky zákazník potvrdzuje prevedenie a farebnosť výrobku a prehlasuje, že sa pred objednaním oboznámil s prevedením výrobku ako aj jeho farebným vyhotovením. V prípade akýchkoľvek pochybností a nezrovnalostí je potrebné tieto pred potvrdením objednávky zmeniť v opačnom prípade prevedenie zostáva podla poslednej odsúhlasenéj verzie.

      Cena montáže nezahŕňa prácu vo výškach (nad 5m pracovná výška).
      Cenová ponuka nezahŕňa vyhotovenie elektrického napájania , úpravu existujúceho napájania ani takú jeho úpravu, ktorá vyžaduje certifikáciu, odbornú spôsobilosť, skúšky prípadne atesty spôsobilosti v zmysle zákonov a vyhlášky, ktorá predmetnú činnosť upravuje.

      r machala _
      0903 533 534

## 🟡 V riešení
(prázdne)

## ✅ Dokončené
- [x] Fáza 1 — POST /extract-pdf (Claude API extrakcia z PDF)
- [x] Fáza 2 — POST /generate-pdf (WeasyPrint generovanie PDF)
- [x] Fáza 3 — Databáza PostgreSQL na Railway
- [x] Fáza 4 — Email cez Resend.com API
- [x] Fáza 5 — Frontend na Railway
- [x] Fáza 6 — Deploy Railway + Dockerfile
- [x] Webhook Railway-GitHub opravený
- [x] CLAUDE.md vytvorený a synchronizovaný

## 📝 Poznámky
- SMTP nefunguje na Railway — email len cez Resend
- Claude Code: vždy aktualizuj TASKS.md po dokončení úlohy. pytaj si potvrdenie odo mna.
- Pred každou zmenou kódu skontroluj TASKS.md čo je priorita
