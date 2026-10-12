# HRN-001: Enabler – Harness repó alapstruktúra és a specifikáció véleményezése

## Cél

A harness saját repóban, a Trinity frameworktől és a prototípusoktól elkülönítve fejlődjön, és a specifikáció a csapat véleményezése után elfogadott alapja legyen a további storyknak.

## Elfogadási feltételek

- **1** A `trinity-harness` repó tartalmazza a specifikációt, a fogalomtárat, az ADR-eket, a fejlesztési workflow-t, az `AGENTS.md`-t és a `HRN-*` story-indexet; a Trinity repóban nem marad harness-dokumentáció.
- **2** ~~A `trinity-harness`, a `proto-planning` és a `proto-product` repó GitHubon létezik, és a helyi repók remote-ja be van állítva.~~ (2026-10-12)
- **2a** A `trinity-harness`, a `trn-proto-planning` és a `trn-proto-monorepo` repó GitHubon létezik, és a helyi repók (`trinity-harness`, `proto-planning`, `proto-product`) remote-ja be van állítva.
- **3** ~~A `proto-planning` és a `proto-product` üres; szerkezetüket a harness-pluginok hozzák létre.~~ (2026-10-12)
- **3a** A `trn-proto-planning` és a `trn-proto-monorepo` szerkezetét a harness-pluginok hozzák létre, kézi szerkezet nélkül.
- **4** A specifikációt legalább egy BA, egy designer és egy fejlesztő véleményezte; az elfogadott észrevételek a repó dokumentumaiba kerültek.

## Megvalósítási terv

- [x] A harness repó létrehozása és a dokumentáció átköltöztetése a Trinity repóból.
- [x] A két üres prototípus repó létrehozása helyben.
- [x] A GitHub-repók létrehozása és a remote-ok beállítása.
- [x] A specifikáció véleményezése és az észrevételek átvezetése.

## Ellenőrzés

- A Senior BA (BA-01–BA-13) és a designer (DS-01–DS-08) 21 észrevétele elbírálva és átvezetve az üzleti és a technikai specifikációba, a `CONTEXT.md`-be és az ADR 0004-be. Döntések: a PO dönt, a BA delegációval hagy jóvá; minden AC-szövegváltozás új betűt kap, tiszta nézettel; visszalépés, `Blokkolva` jelző és `Lezárva` epicállapot.
