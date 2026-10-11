# HRN-004: Enabler – Gyorsindító workflow-sablon

## Cél

Egy új projekt a Trinity alap fejlesztési workflow-jával percek alatt elindulhasson, mielőtt a teljes harness workflow-ra áll át.

## Elfogadási feltételek

**1** A `templates/quick-start/` tartalmazza az `AGENTS.md` vázát, a fejlesztési workflow-t, az üres story-indexet és egy story-sablont.
**2** A sablon projektfüggetlen: Trinity-specifikus azonosító és példa nincs benne, a story-prefix `<PREFIX>` helyőrző.
**3** A sablon `README.md`-je leírja a használat lépéseit és a különbséget a harness workflow-tól.
**4** A harness saját workflow-ja a harness AC-formátumát, harness-példákat és harness-specifikus Definition of Done-t tartalmaz.

## Megvalósítási terv

- [x] A harness workflow-jának igazítása (AC-formátum, példák, Definition of Done).
- [x] A gyorsindító sablon elkészítése a Trinity workflow-jából.
- [x] A helyőrzők és a hivatkozások ellenőrzése.
