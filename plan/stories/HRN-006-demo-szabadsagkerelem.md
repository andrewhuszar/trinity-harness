# HRN-006: Demo – Szabadságkérelem az igénytől a kész storyig

## Cél

Egy kézzel írt, cél-működést bemutató demo-forgatókönyv mutassa meg egy egyszerű, új domainbeli igény (szabadságkérelem) útját a rövid üzleti leírástól a kész, elfogadott storykig, a szereplők közötti átadásokkal együtt. A demo a harness betanító anyaga, és a közös csatorna tervezésének bemenete.

## Elfogadási feltételek

- **1** A demo egyetlen markdown-dokumentum a `docs/demo/` alatt, beágyazott példa-artefaktumokkal, amelyek a specifikáció formátumait követik.
- **2** Megnevezett szereplők (PO, BA, designer, story-felelős, fejlesztő, tesztelő) és agentek szerepelnek; a grill-munkamenetek kivonatként, kérdés–ajánlott válasz–döntés formában jelennek meg.
- **3** A fejezetek: bevezető, rövid üzleti leírás, felfedező event storming, pontosítás, tervezés, tervezési egyeztetés, bontás, fejlesztés, tesztelés és elfogadás, összegzés.
- **4** Minden fejezet „Csatorna” blokkal zárul (esemény, szereplő, átadás vagy várakozás, hivatkozás); az összegzés ezekből eseménytípus-listát és átadási térképet állít össze.
- **5** Ahol az MVP eltér a cél-működéstől, „MVP-ben” jelölés mondja meg a kézi helyettesítést és felelősét; az összegzés felsorolja ezeket.
- **6** Az 1. kör az epic bontásáig mindhárom storyt, a fejlesztésben és a tesztelésben az 1. storyt mutatja be részletesen, benne egy AC-módosítással, tervezési eltéréssel és gyanús tesztkapcsolattal.
- **7** A 2. és a 3. story fejlesztése és tesztelése ugyanilyen részletességgel, külön körökben kerül be.

## Megvalósítási terv

- [x] 1. kör: 0–9. fejezet, a fejlesztés és a tesztelés az 1. storyra.
- [ ] 2. kör: a 2. story (vezetői elbírálás) fejlesztése és tesztelése.
- [ ] 3. kör: a 3. story (visszavonás és saját kérelmek) fejlesztése és tesztelése; az összegzés véglegesítése.
