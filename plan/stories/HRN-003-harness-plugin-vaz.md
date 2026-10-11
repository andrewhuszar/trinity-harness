# HRN-003: Enabler – Harness-pluginok váza és marketplace

## Cél

A `harness-ba` és a `harness-dev` plugin egy marketplace-ből globálisan telepíthető legyen, és egy projektben a harness-konfiguráció alapján működjön, hogy a prototípus repók már harness-eszközökkel épülhessenek fel.

## Elfogadási feltételek

**1** A `trinity-harness` repó plugin-marketplace-ként telepíthető, és a `harness-ba`, illetve a `harness-dev` plugin külön telepíthető.
**2** Egy üres repóban egy bootstrap parancs létrehozza a harness-konfigurációt (story-prefix, szerep, kapcsolódó repó) és a szerephez tartozó alapszerkezetet.
**3** A `/next` a konfiguráció és az állapotok alapján megmondja a következő teendőt; üres tervezési térben a domain felvételét javasolja.
**4** A plugin verziója látható, és frissítéskor a projekt konfigurációja változatlan marad.

## Korlátok

Üzleti skillek (pontosítás, funkcionális specifikáció, bontás) nem részei ennek a storynak.

## Megvalósítási terv

- [x] Marketplace és a két plugin váza.
- [x] Harness-konfiguráció formátuma (`.harness/config.json`) és bootstrap parancs.
- [x] `/next` alapváltozata.
- [x] Telepítés és frissítés kipróbálása eldobható repókban.
- [ ] A prototípus repók bootstrapolása a telepített pluginokkal.

## Ellenőrzés

- `claude plugin validate`: a marketplace és mindkét plugin manifestje érvényes.
- Szkriptek eldobható repókban: bootstrap konfiguráció nélkül, hibás prefix elutasítása, meglévő konfiguráció védelme, `/next` üres tervezési térben (domain felvétele), prioritás (BA-elfogadás a pontosítás előtt), ismeretlen állapot jelzése, szerepváltás, teljes és gyorsindító fejlesztői workflow.
- Helyi marketplace-ről `local` scope-pal telepítve mindkét plugin; a verzió (0.1.0) a `claude plugin list` kimenetében látható; a `/harness-ba:next` és a `/harness-ba:init` headless munkamenetben a telepített pluginból lefutott.
- 0.1.0 → 0.1.1 frissítés után a plugin az új verziót jelenti, a `.harness/config.json` bájtra azonos maradt.
