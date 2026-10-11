# HRN-002: Spike – Claude Design képernyőexport és automatizálhatóság

## Cél

Derüljön ki, milyen formában és mennyire automatizáltan adható ki egy elfogadott Claude Design-képernyő statikus React kódként, és hogyan szinkronizálható a design system a termékrepóból a Claude Designba. Az eredmény alapján a design-pillanatkép, a képernyőimport és a design-PR modellje megerősíthető vagy módosítható.

## Elfogadási feltételek

- **1** Dokumentált, kipróbált út egy képernyő exportjára statikus React kódként, amely a `@trinity/ui` komponenseit, tokenjeit és Tailwind classait használja.
- **2** Kipróbált út a `@trinity/ui` legalább két komponensének szinkronjára a Claude Design design-system projektjébe.
- **3** Döntés arról, hogy az export kézi, félautomatikus vagy automatikus lépés; a döntés a technikai specifikációba vagy ADR-be kerül.
- **4** A specifikáció design-szakaszai az eredményhez igazodnak, vagy a szükséges módosítás új storyként rögzített.

## Megvalósítási terv

- [ ] Képernyőexport kipróbálása egy egyszerű képernyőn.
- [ ] Design system szinkron kipróbálása két komponensen.
- [ ] Döntés és dokumentáció.
