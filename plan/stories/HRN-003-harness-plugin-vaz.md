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

- [ ] Marketplace és a két plugin váza.
- [ ] Harness-konfiguráció formátuma és bootstrap parancs.
- [ ] `/next` alapváltozata.
- [ ] Telepítés és frissítés kipróbálása a prototípus repókban.
