# <PROJEKT> – tervezési tér

Ez a repó a <PROJEKT> tervezési tere: az üzleti artefaktumok (domain, epic, üzleti igény, folyamatmodell, funkcionális specifikáció, design-pillanatkép, story, tesztforgatókönyv) és állapotuk helye. Kódot és technikai artefaktumot nem tartalmaz.

## Munkamód

- A következő teendőt a `/harness-ba:next` parancs mutatja; munkakezdéskor és lépés lezárásakor futtasd.
- A BA git-műveletet nem végez; a változást a harness juttatja a tervezési térbe.
- Kérdezéskor egyszerre egy kérdést tegyél fel, ajánlott válasszal.
- A szóhasználat a domain `context.md` szótárát követi; ütközésnél jelezd, és pontosítsd a fogalmat.
- Bizonytalan feltételezést ne rögzíts követelményként; a nyitott kérdés megválaszolt vagy felelőssel és határidővel elhalasztott.

## Szerkezet

```
domains/<domain>/context.md        üzleti szótár, határok
epics/<EPIC-ID>/epic.md            epic, állapottal
epics/<EPIC-ID>/stories/<ID>.md    storyk, állapottal
```

Az epic és a story állapota a fájl elején álló front matter `status` mezője:

```md
---
id: EP-001
title: Dokumentumfeltöltés
status: Vázlat
---
```

- Epic: `Vázlat`, `Pontosítva`, `Tervezés alatt`, `Bontva`, `Fejlesztés alatt`, `Kiadva`, `Lezárva`, `Jegelve`.

Blokkolás esetén a front matter `blocked_reason`, `blocked_owner` és `blocked_until` mezőt kap; ez jelző, nem állapot.
- Story: `Fejlesztésre kész`, `Fejlesztés alatt`, `Tesztelés alatt`, `Elfogadva`, `Kiadva`, `Jegelve`.

A storyk azonosítója `<PREFIX>-<n>`.

## Elfogadási feltételek

Az elfogadási feltétel explicit, tömör, a domain szavaival és konkrét értékekkel. Minden feltétel külön felsorolásjeles (`-`) sor, félkövér azonosítóval kezdve; számozott markdown-lista nem használható. Az azonosító a pont hierarchiát (`**2.1**`), a `-xN` utólag beszúrt testvért (`**2.1-x1**`), a betű módosítást (`**2.2a**`) jelöl. Módosításkor az eredeti szöveg áthúzva, dátummal marad; azonosító nem számozódik át és nem használható újra.
