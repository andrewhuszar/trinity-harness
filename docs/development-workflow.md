# Fejlesztési workflow

Ez a workflow segít abban, hogy a fejlesztés kis, követhető story-kra bomoljon, és minden kódváltozás visszaköthető legyen egy döntéshez. A story a kívánt eredményt és az elkészülés feltételeit rögzíti, nem a részletes implementációt.

## 1. Tervezés

A munka rövid felhasználói inputtal indul. Ez tartalmazhat üzleti célt, technikai problémát, ismert hibát, korlátot vagy elfogadási elvárást.

A story megírása előtt az agent vizsgálja meg, hogy a cél, a scope, az elvárt működés és a szükséges döntések egyértelműek-e. Ha bármi nem világos, többféleképpen értelmezhető, vagy felhasználói döntést igényel, előbb tegyen fel rövid, célzott tisztázó kérdéseket. A story csak a válaszok és döntések után készüljön el; az agent ne rögzítsen bizonytalan feltételezést követelményként.

Minden tisztázó kérdéshez adjon rövid, egymástól egyértelműen elkülönülő válaszlehetőségeket `A`, `B`, `C` stb. azonosítókkal. Ha a felsorolt lehetőségek nem fednek le minden ésszerű választ, az utolsó lehetőség engedjen saját választ. A választások szükség esetén röviden jelezzék a lényegi következményt vagy kompromisszumot, hogy a felhasználó az azonosító megadásával is megalapozottan dönthessen.

Csak a story célját vagy terjedelmét érdemben befolyásoló bizonytalanságokat kell tisztázni. A már egyértelmű vagy a projekt dokumentációjából és kódjából biztonságosan megállapítható részletekre nem szükséges rákérdezni. A cél nem hosszú specifikáció készítése, hanem a szükséges döntések gyors meghozatala.

## 2. Story írás

Minden fejlesztéshez rövid, magyar nyelvű story készül a `plan/` mappába. Minden magyar nyelvű szöveget helyes ékezetekkel kell írni.

A story legyen:

- rövid és lényegre törő,
- önállóan érthető,
- eredményorientált,
- a megvalósítás módjában csak a szükséges mértékben előíró.

Az önállóan érthető story elegendő információt ad a cél és az elkészülés megértéséhez, de nem helyettesíti a forráskódot, az implementációs terv részleteit vagy az architekturális dokumentációt.

Minden story egyedi azonosítót kap, például `HRN-001`.

Ha a story jellege nem felhasználói feature, a címben szerepeljen a típusa:

- `Spike`: kutatási vagy bizonytalanságot csökkentő munka, ahol a kimenet lehet döntés vagy terv.
- `Enabler`: technikai alapozás, amely későbbi story-kat tesz lehetővé.

Példa:

```md
# HRN-002: Spike – Claude Design képernyőexport és automatizálhatóság

# HRN-003: Enabler – Harness-pluginok váza és marketplace
```

### Kötelező story-szerkezet

```md
# HRN-001: Rövid cím

## Cél

1–3 mondat arról, hogy milyen problémát oldunk meg, és mi a kívánt eredmény.

## Elfogadási feltételek

**1** Első ellenőrizhető, eredményorientált feltétel.
**2** Második feltétel.

## Megvalósítási terv

- [ ] Első önálló fejlesztési részfeladat.
- [ ] Második önálló fejlesztési részfeladat.
- [ ] A szükséges tesztek és ellenőrzések elvégzése.
```

### Elfogadási feltételek

Egy story jellemzően 3–7 elfogadási feltételt tartalmaz. Minden feltétel explicit, tömör és ellenőrizhető, töltelék nélkül.

- Az azonosító a sor elején álló, félkövér szöveges címke, nem markdown-listaszám: `**1**`, `**2**`, alpont esetén `**2.1**`.
- A pont hierarchiát jelöl: `**2.1**` a 2. feltétel részelvárása vagy eredményága.
- Utólag beszúrt feltétel az előző elem után `-xN` utótagot kap: `**2.1-x1**`, `**2.1-x2**`.
- Módosításkor az eredeti szöveg áthúzva, dátummal megmarad, az új változat a következő betűt kapja: `**2.2**` → `**2.2a**` → `**2.2b**`.
- Pótlás nélkül kivezetett feltétel áthúzva, `Visszavonva <dátum>` jelöléssel marad.
- Azonosító nem számozódik át és nem használható újra; a teljes hivatkozás `HRN-003#2.2a`.

```md
**1** A marketplace-ből a `harness-ba` és a `harness-dev` plugin külön telepíthető.
**2** ~~A `/next` a következő storyt mutatja.~~ (2026-11-01)
**2a** A `/next` a konfiguráció és az állapotok alapján a következő teendőt mutatja.
**2-x1** Üres tervezési térben a `/next` a domain felvételét javasolja.
```

### Opcionális story-rész

Csak akkor szerepeljen, ha valóban szükséges:

```md
## Korlátok

A megoldást érdemben befolyásoló scope-, kompatibilitási vagy kötelező technikai korlátok.
```

### Rövidségi szabályok

- Egy információ csak egy helyen szerepeljen.
- Az egyszerű story célmérete a megvalósítási tervvel együtt legfeljebb körülbelül 300 szó.
- Egy egyszerű story megvalósítási terve jellemzően 2–5 rövid fejlesztési részfeladatból álljon.
- A részfeladatok önállóan implementálható és ellenőrizhető eredményt írjanak le, ne fájlonkénti módosításokat.
- Ne szerepeljen külön üzleti és technikai specifikáció, ha ugyanaz az információ a célból és az elfogadási feltételekből már érthető.
- Ne kerüljön a story-ba tervezett interface, metóduslista, részletes hívási sorrend, teljes fájllista vagy minden lehetséges teszteset felsorolása.
- Technikai megoldást csak akkor kell rögzíteni, ha az már meghozott, kötelező döntés vagy a story lényegi korlátja.
- Az általános tesztelési, accessibility-, build- és commit-szabályokat nem kell minden story-ba bemásolni.
- Üres vagy nem szükséges fejezetet el kell hagyni.
- Összetett migráció, több rendszert érintő változás, külső szerződés, security- vagy adatvesztési kockázat esetén a story lehet hosszabb.
- Ha a story túl nagyra nő, először a részletek elhagyását, külön story-kra bontását vagy tartós technikai döntés esetén ADR készítését kell megfontolni.

## 3. Megvalósítás

A fejlesztés a story `Megvalósítási terv` részében szereplő részfeladatok szerint halad. A tervet csak akkor kell bővíteni vagy módosítani, ha implementáció közben új, a story teljesítéséhez szükséges munka derül ki.

Ha az új munka önálló célt alkot vagy jelentősen növeli a scope-ot, ne bővítsük tovább az eredeti story-t: készüljön új story.

A később is fontos technikai döntéseket külön ADR-ben vagy dokumentációban kell rögzíteni. Az átmeneti, alacsony szintű implementációs részleteknek nem kell a story-ba kerülniük.

### Az aktuális dokumentáció megfogalmazása

A használati és architektúraleírás a rendszer aktuális működését, API-ját és korlátait mutassa be jelen időben. A leírás legyen a beszélgetés és a fejlesztés menetének ismerete nélkül is érthető. A 0.0.1 verzió dokumentációja sem fejlesztési napló: a „továbbra is”, „most már” és „átálltunk” fordulatok helyett közvetlenül a működést írd le. Változtatáskor az érintett szakaszt dolgozd át, ne a korábbi leírás után fűzd hozzá, mi módosult.

A döntési indoklás és a mérlegelt alternatívák helye az ADR; a megvalósítási tervé és ellenőrzési eredményeké a story. Külön kiadási vagy migrációs dokumentum akkor szükséges, ha valós verzióváltást vagy üzemeltetői teendőt ír le. Egy tervezett képesség státuszát egyértelműen jelöld, és ne keverd a működő API bemutatásával.

## 4. Általános Definition of Done

Ezeket a szabályokat nem kell minden story-ban megismételni:

- A módosított plugin a marketplace-ből telepíthető és frissíthető, a projekt harness-konfigurációja frissítéskor változatlan marad.
- A módosított skill, parancs vagy hook legalább egy prototípus repóban kipróbálva, a kipróbálás eredménye a storyban rögzítve.
- A változáshoz tartozó automatizált ellenőrzések (ha vannak) sikeresen lefutnak.
- A dokumentáció hivatkozásai élnek, az új vagy megváltozott fogalmak a `CONTEXT.md`-ben szerepelnek, a tartós döntések ADR-ben.
- A változás nem okoz ismert regressziót a kapcsolódó működésben.
- A megvalósítási terv részfeladatai elkészültek.
- A story csak a kapcsolódó ellenőrzések után kerülhet `Kész` állapotba.

Story-specifikus teszt vagy ellenőrzés csak akkor kerüljön az elfogadási feltételek vagy a megvalósítási terv közé, ha nem következik egyértelműen ezekből az általános szabályokból.

## 5. Commit kapcsolás

Minden story-hoz kapcsolódó commit üzenetében szerepeljen a story azonosítója `Refs:` sorban. Ezt a szabályt nem kell minden story dokumentumába bemásolni.

A commit üzenet formátuma:

```text
type(scope): rövid leírás

* részlet, ha szükséges
* második részlet, ha szükséges

Refs: HRN-001
```

Szabályok:

- A subject sor legyen rövid és konkrét.
- A subject sor ne tartalmazza a story azonosítóját.
- A story azonosítója mindig a `Refs:` sorban szerepeljen.
- A részletező bullet lista opcionális.
- Ha egy commit több story-hoz tartozik, a `Refs:` sorban vesszővel válasszuk el őket.

## 6. Story-követés

- A `plan/stories/README.md` listázza a story-kat és az állapotukat.
- A story állapota: `Tervezve`, `Folyamatban`, `Kész` vagy `Jegelve`.
- Nagy story helyett lehetőleg több, önállóan értelmezhető kis story készüljön.
- A végső fejlesztői összefoglaló mindig nevezze meg a kapcsolódó story azonosítóját.
