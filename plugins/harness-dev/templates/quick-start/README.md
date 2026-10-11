# Gyorsindító workflow-sablon

A Trinity alap fejlesztési workflow-jának projektfüggetlen változata: rövid, magyar nyelvű storyk, `A`/`B`/`C` tisztázó kérdések, közös Definition of Done és `Refs:` sorral kapcsolt commitok. Olyan projekt gyors indításához való, amely még nem a teljes harness workflow-t (epic, tervezési tér, kapuk, tervezési szinkron) használja.

## Tartalom

| Fájl | Szerep |
| --- | --- |
| `AGENTS.md` | Agentutasítások vázlata; a toolchain és a repository-szerkezet kitöltendő |
| `docs/development-workflow.md` | A fejlesztési workflow |
| `plan/stories/README.md` | Üres story-index |
| `plan/stories/_story-sablon.md` | Másolható story-sablon |

## Használat

1. Másold a sablon tartalmát az új repó gyökerébe.
2. Cseréld a `<PREFIX>` helyőrzőt a projekt story-prefixére (például `ABC`) minden fájlban.
3. Töltsd ki az `AGENTS.md` megjelölt szakaszait.
4. Az első storyt a `_story-sablon.md` másolatából írd meg, és vedd fel az indexbe.

## Különbség a harness workflow-tól

- Az elfogadási feltételek egyszerű felsorolások, stabil azonosító nélkül.
- Nincs epic, tervezési tér, design-folyamat, kapu és tervezési szinkron.
- A teljes harness workflow-ra a projekt bármikor átállhat; a folyamatban lévő storyk ilyenkor ezen a workflow-n fejeződnek be.
