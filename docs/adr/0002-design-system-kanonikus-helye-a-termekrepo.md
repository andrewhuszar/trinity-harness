# A design system kanonikus helye a termékrepó

A design system a termékrepóban él, és a kódja kanonikus: a production ezt futtatja, és a fejlesztők által hozzáadott dinamikus, shadcn-szerű részek csak itt maradnak meg. A Claude Design design-system projektje a kódról szinkronizált munkafelület: a fejlesztői változás merge után komponensenként visszaszinkronizálódik, a designer módosítása pedig exportból nyitott design-PR-ként érkezik, amelyet a fejlesztés hagy jóvá. Egy DS-komponens változása csak akkor mergelhető, ha a Claude Design szinkron renderellenőrzése sikeres, hogy a designer továbbra is használni tudja.

## Mérlegelt lehetőségek

- A Claude Design mint kanonikus forrás: a fejlesztői dinamikus részek elvesznének, vagy a Claude Designnak kellene értenie őket.
- Megosztott forrás (a vizuális döntések a Claude Designban, a szerkezet a kódban): két igazságforrás finom, nehezen ellenőrizhető határral.
- Külön design-system repó: harmadik szinkronpont és önálló release-folyamat második fogyasztó nélkül. Akkor indokolt, ha egy második termék is ugyanazt a design systemet használja.
