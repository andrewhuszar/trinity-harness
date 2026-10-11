# Agent harness – üzleti specifikáció

Állapot: specifikáció. A leírt működés tervezett; az MVP-ben kézi lépéssel helyettesített részeket az [MVP](#mvp) fejezet sorolja fel. A fogalmak pontos jelentését a [CONTEXT.md](../CONTEXT.md), a döntések indoklását az [ADR-ek](./adr/) rögzítik.

## Cél

Az agent harness az a munkakörnyezet, amelyben AI-agentek és emberi csapattagok (BA, üzlet, designer, fejlesztő, tesztelő) közösen jutnak el egy rövid üzleti leírástól a kiadott szoftverig. Az agentek elvégzik a kérdezést, a vázlatkészítést, az ellenőrzést, a fejlesztést és az összefoglalást; az emberek döntenek, jóváhagynak és elfogadnak. Minden lépés eredménye verziózott, hivatkozható dokumentum, ezért mindig visszakövethető, melyik kód melyik elvárásra és designra készült.

## Szereplők

| Szereplő | Felelősség |
|---|---|
| BA, üzlet | Üzleti igény, folyamatmodell, funkcionális specifikáció, storyk és elfogadási feltételek; a story elfogadása; release indítása. Git-művelet nélkül dolgozik. |
| Domain-szakértő | Event storming, hotspotok lezárása. |
| Designer | Képernyő- és komponensdesign a Claude Designban, koncepcióverziók, design-pillanatkép kiadása, DS-komponensek előléptetése. |
| Story-felelős (fejlesztő) | Technikai specifikáció, tervmegerősítés, végrehajtási mód kiválasztása, task PR-ok elfogadása. |
| Tesztelő | Tesztforgatókönyvek jóváhagyása, feltáró tesztelés, a megtartandó tesztadat kiválogatása. |
| Product owner | Release indítása (a BA-val közösen). |
| Beküldő agent | A BA változását a tervezési tér draft branchére commitolja. |
| Feldolgozó agent | A beküldött változást ellenőrzi, hibát és javaslatot jelez vissza. |
| AI-szakértő | Egy perspektívából (jogi, biztonsági, üzemeltetési, UX, hibaút-kereső) hotspotot nyit és javasol; nem dönt. |
| AI-projektspecialista | A jelenlegi működés ismeretében iránymutatást ad és ütközést jelez. |
| Fejlesztő agent | Taskot valósít meg, tesztet ír, PR-t nyit, a review-kommentekre javít. |

## Munkaterek

- **Tervezési tér:** külön GitHub-repó az üzleti artefaktumokkal (domain, epic, üzleti igény, folyamatmodell, funkcionális specifikáció, design-pillanatkép, story, tesztforgatókönyv). Itt él minden epic, story és task állapota.
- **Termékrepó:** Azure DevOps-repó a kóddal és a technikai artefaktumokkal (technikai specifikáció, ADR, task). Az üzleti artefaktumokat csak olvasható tervezési másolatként tartalmazza.
- **Claude projekt:** a BA a Claude Code Desktopban, a tervezési tér checkoutjával és a projekt skilljeivel dolgozik. A `/next` mindig a következő teendőhöz vezet.
- **Story-szerkesztő felület:** online alkalmazás, ahol a BA a beküldött változás ellenőrzési eredményét látja, kérdésekre válaszol és publikál.
- **Claude Design:** a designer munkafelülete, amely a termékrepó design systemjéből szinkronizált komponenseket használja.

## Folyamat

```
Rövid üzleti leírás
  → Pontosítás: grill a BA-val → üzleti igény + folyamatmodell (event storming)
  → Tervezés, három párhuzamos sávban:
      funkcionális specifikáció | design (Claude Design) | technikai specifikáció (grill a fejlesztővel, spike-ok)
  → Bontás: storyk elfogadási feltételekkel, tesztforgatókönyvek, taskok és PR-sorrend
  → Fejlesztés: task PR-ok a story-gyűjtőbranchre, agentes előreview, magyarázott emberi review
  → Tesztelés: story-nkénti tesztkörnyezet, automata e2e, feltáró teszt, BA-elfogadás
  → Elfogadás: a story a develop branchre kerül
  → Release: develop → main, production-telepítés
```

### Pontosítás

A BA rövid üzleti leírásból indul. Az agent egyesével kérdez, minden kérdéshez ajánlott választ ad, és a válaszokból üzleti igényt állít össze. Az üzleti igény kötelező szakaszai: cél, érintettek, scope (benne és kívül), sikerességi mérőszám, korlátok, nyitott kérdések. A pontosítás akkor zárható, ha minden szakasz kitöltött, és minden nyitott kérdés megválaszolt vagy felelőssel és határidővel elhalasztott.

### Event storming

- **Big Picture (domain szint):** a domain eseményei, határai és az üzleti szótár. Új domain esetén klasszikus, szinkron **felfedező event storming** gyűjti a fogalmakat; az AI-szakértők és az AI-projektspecialista javaslattal segítik. Az agent feldolgozza és előkészíti az eredményt, majd újabb workshop következik.
- **Process Level (epic szint):** az epic folyamatmodellje stabil azonosítójú folyamatelemekkel (szereplő, command, policy, esemény, read modell, üzleti szabály). Az agent az üzleti igényből és a meglévő domainből vázlatot készít, az AI-szakértők hotspotokat nyitnak, majd egy rövid **hotspot-workshop** csak a nyitott kérdéseket dönti el.
- **Software Design Level:** a technikai specifikáció architektúraterve, a fejlesztés feladata.

Hotspotot AI is nyithat, de csak ember zárhatja le.

### Tervezés

A három sáv párhuzamosan halad, és mindhárom a folyamatelemekre hivatkozik.

- **Funkcionális specifikáció:** az epic üzleti működése, amely a végleges designnal egyezik. Képernyőverziókra és folyamatelemekre hivatkozik.
- **Design:** lásd [Design](#design).
- **Technikai specifikáció:** az agent vázlatot készít, majd a story-felelőssel grill-munkamenetben egyesével lezárják a döntéseket. A bizonytalan pontokból időkorlátos spike készül, amely a tervmegerősítés előtt lefut. A technikai specifikáció taskonként rögzíti az eszközt (például command, saga, képernyőimport), a végrehajtási módot (`agent` vagy `pár`), a függőségeket és a PR-sorrendet.

### Bontás

A funkcionális specifikációból storyk készülnek részletes elfogadási feltételekkel, a technikai specifikációból pedig taskok. Egy story legfeljebb körülbelül öt flow-lépést tartalmaz. Az elfogadási feltételekből tesztforgatókönyvek (pozitív, negatív, határeset) készülnek, amelyeket a tesztelő jóváhagy.

## Design

1. A designer a Claude Designban képernyőt vagy komponenst tervez a design system már productionben használt primitív és összetett, tiszta komponenseiből.
2. Új képernyőről koncepcióverziók készülnek üzleti reviewra (például `A1.2`, `C1`).
3. Elfogadáskor a választott koncepcióból **képernyőverzió** lesz (például `SCR-12@3`). A designer statikus React kódként adja ki, a design system komponenseire, tokenjeire és Tailwind classokra építve. Ez a design-pillanatkép része, és a fejlesztés **képernyőimporttal** véglegesíti, komponensekre bontja és bekötik az adatot.
4. A designer által design system szintre léptetett új komponens importálható UI-lib elemként kerül a termékrepóba (**komponensimport**). Ettől kezdve a designer és a fejlesztés is módosíthatja; a fejlesztés a dinamikus részeket alacsony szintű, shadcn-szerű komponensekkel adja hozzá, és a Claude Design továbbra is használni tudja.
5. A design system kanonikus helye a termékrepó. A fejlesztői változás merge után visszaszinkronizálódik a Claude Designba, a designer változása design-PR-ként érkezik.

**Designváltozás:** minden képernyőverzió-emeléskor a designer jelöli a változás típusát.

- **Megjelenítési pontosítás:** csak vizuális eltérés. Nem blokkolja a fejlesztést; a fejlesztés vizuális diffet kap, és átvezeti. Ha a story már `Elfogadva` vagy `Kiadva` állapotú, automatikusan design-frissítési story nyílik.
- **Viselkedési változás:** új adat, interakció, állapot vagy folyamat. Ez tervezési eltérés: a BA frissíti a funkcionális specifikációt, a fejlesztő megerősíti a tervet. A feldolgozó agent viselkedési változásként kezeli a pontosításnak jelölt, de új adatot vagy interakciót hozó változást, amíg ember nem dönt.

## Elfogadási feltételek

Az elfogadási feltételek explicitek és tömörek: minden lényeges elvárást lefednek, töltelék nélkül, a domain szótárának szavaival, konkrét értékekkel. Indoklás, pixelleírás és implementációs utalás nem kerül beléjük.

**Flow-lépés:** előfeltétel, látható, művelet, és minden eredményág alpontként. Üres mező helyén `—` áll.
**Szabály:** egyetlen „Ha …, akkor …” mondat.

```md
2. Fájl kiválasztása — SCR-12@3, DOC:CMD-3
   - Előfeltétel: bejelentkezett ügyintéző; az ügy nyitott; nincs folyamatban lévő feltöltés.
   - Látható: ügy neve; engedett típusok (PDF, JPG); méretkorlát 20 MB; „Feltöltés” inaktív.
   - Művelet: fájl kiválasztása; mégse.
   2.1 Engedett fájl → fájlnév és méret látható, „Feltöltés” aktív.
   2.1-x1 Jelszóval védett PDF → hibaüzenet a mező alatt, „Feltöltés” inaktív.
   2.2 ~~Nem engedett típus vagy 20 MB fölött → hibaüzenet a mező alatt.~~ (2026-11-01)
   2.2a Nem engedett típus vagy 20 MB fölött → hibaüzenet a mező alatt, a kiválasztás törlődik.
   2.3 ~~Mégse → vissza az 1-re.~~ Visszavonva 2026-11-01.
3. Ha az ügy lezárt, a feltöltés nem indítható, és a gomb nem jelenik meg.
```

**Azonosítás:**

- Az azonosító explicit szöveges címke, storyn belül egyedi, és a storyval együtt hivatkozható: `TRN-045#2.2a`.
- A pont hierarchiát jelöl, a `-xN` az adott elem után beszúrt testvért (korlátlanul: `-x1`, `-x2`), a betű módosítást (`2.2a`, `2.2b`).
- Módosításkor az eredeti szöveg áthúzva, dátummal megmarad. Visszavont feltétel áthúzva, `Visszavonva <dátum>` jelöléssel marad.
- Azonosító nem számozódik át és nem használható újra.
- Minden szövegváltozás új betűt kap; a régi azonosítóra mutató automata teszt gyanús lesz, és felülvizsgálatig blokkolja a story továbblépését.

## Állapotok

### Epic

| Állapot | Belépési feltétel | Léptető |
|---|---|---|
| `Vázlat` | A rövid üzleti leírás beküldve. | BA |
| `Pontosítva` | Az üzleti igény és a folyamatmodell elfogadva. | BA |
| `Tervezés alatt` | A funkcionális specifikáció, a design és a technikai specifikáció sávja fut. | Harness |
| `Bontva` | A funkcionális specifikáció elfogadva és egyezik a képernyőverziókkal; a technikai specifikáció megerősítve; a storyk, a tesztforgatókönyvek és a taskok létrejöttek. | BA és story-felelős |
| `Fejlesztés alatt` | Legalább egy story fejlesztése elindult. | Harness |
| `Kiadva` | Minden story `Kiadva` vagy `Jegelve`. | Harness |
| `Jegelve` | Bármikor. | BA |

### Story

| Állapot | Belépési feltétel | Léptető |
|---|---|---|
| `Fejlesztésre kész` | Bontáskor létrejött; az elfogadási feltételek folyamatelemekre és képernyőverziókra hivatkoznak; legalább egy task tartozik hozzá. | Harness |
| `Fejlesztés alatt` | Az első task PR megnyílt. | Harness |
| `Tesztelés alatt` | Minden task mergelve a story-gyűjtőbranchbe, a pipeline zöld, és minden elfogadási feltételhez és jóváhagyott forgatókönyvhöz tartozik automata teszt. A story saját tesztkörnyezetet kap. | Harness |
| `Elfogadva` | A tesztelő és a BA elfogadta; a story-gyűjtőbranch a `develop`-ra került. | BA, majd harness |
| `Kiadva` | A story a production release része. | Harness |
| `Jegelve` | A `Kiadva` kivételével bármikor. | BA vagy story-felelős |

`Elfogadva` vagy `Kiadva` story nem nyílik újra; a későbbi változás új story.

### Task

`Tervezve` → `Fejlesztés alatt` → `Elfogadásra vár` (a task PR review alatt) → `Mergelve`.

## Kapuk

Minden állapotátmenet kétszintű kapun megy át.

- **Determinisztikus ellenőrzés:** struktúra, kötelező mezők, hivatkozások, azonosítók. Hiba esetén az átmenet blokkolt, és a beküldő agent kapja vissza.
- **Szemantikus javaslat:** a feldolgozó agent észrevétele szótár-ütközésről, ellentmondásról, kimaradt hibaútról, hiányos lefedettségről. A BA vagy a fejlesztő indoklással elutasíthatja; az elutasítás rögzítésre kerül.

## Változáskezelés

Az üzleti artefaktum bármikor módosítható. A publikált változás automatikusan eljut a termékrepóba és a folyamatban lévő story-gyűjtőbranchekre. Ha egy technikai specifikáció vagy task régebbi verzióra hivatkozik, mint ami a branchen van (**tervezési eltérés**), az érintett taskok megállnak, és a story csak a fejlesztő tervmegerősítése után mergelhető. Változás nem csúszhat át észrevétlenül.

## Tesztelés és elfogadás

- Minden `Tesztelés alatt` story saját, eldobható tesztkörnyezetet kap saját URL-lel, egy verziózott, életszerű **arany tesztadat** klónjával.
- Ott fut az automata e2e-készlet, ott végez a tesztelő feltáró tesztelést, és ott fogad el a BA.
- A tesztelés végén a tesztelő vagy a BA kiválogatja a megtartandó új adatot. Ez **tesztadat-deltaként** bekerül a következő arany tesztadatba, így a tesztadat a valós tesztelésből gazdagodik.
- Ha a delta által módosított vagy törölt rekord közben megváltozott az aranyban, illetve egy új rekord azonosítója már létezik, a story merge-kapuja blokkol. A tesztelő vagy a BA kézzel feloldja a konfliktust és frissíti a deltát; ezután az arany újraépítése és a delta ellenőrzése újrafut. Automatikus felülírás nincs.
- Az elfogadás után a story a `develop` branchre kerül.
- Másik story integrálása nem igényli a korábban elfogadott story ismételt BA-elfogadását. Az integrációs és regressziós ellenőrzés azt vizsgálja, hogy az elfogadott működések együtt is helyesek; az eltérés javítandó hiba.
- A story saját elfogadott üzleti tartalmának vagy elfogadási feltételeinek változása új üzleti elfogadást igényel. `Elfogadva` vagy `Kiadva` story esetén a változás új storyban készül el.

## Release

- A `develop` csak elfogadott storykat tartalmaz, ezért bármely pontja kiadható.
- Minden `develop`-merge automatikusan a stagingre települ, ahol a teljes e2e regressziós készlet fut.
- A release-t a BA vagy a product owner indítja az online felületen. A harness generált release note-tal (storyk, képernyőverziók, migrációk, tesztadat-verzió) release-PR-t nyit `develop` → `main` irányba.
- A kiadandó összeállítás zöld staging regressziója mellett a release-PR mergelődik, a `main` verziótagot kap, és ugyanaz a build kerül productionbe, amely a stagingen futott. Korábbi összeállítás zöld eredménye nem elegendő. Az érintett storyk `Kiadva` állapotba lépnek.
- Hotfix a `main`-ből indul, és a `main`-re és a `develop`-ra is visszakerül.

## MVP

Az MVP egy valódi epicet visz végig minden fázison. Ahol még nincs automatizálás, dokumentált kézi lépés vagy prompt áll a helyén.

| Terület | MVP-ben automatizált | MVP-ben kézi |
|---|---|---|
| Tervezés | Tervezési tér struktúra, BA-skillek (`/next`, pontosítás, funkcionális specifikáció, bontás, AC-formátum), beküldés draft branchre, determinisztikus kapu | Online felület: a BA beillesztendő promptot kap a válaszokhoz; event storming: workshop és utólagos agentfeldolgozás |
| Szinkron | Tervezési szinkron és eltérésjelzés a termékrepó felé | — |
| Design | — | A design-pillanatkép és a design-PR: a designer exportját egy fejlesztő commitolja |
| Fejlesztés | Fejlesztési útmutató 2–3 eszközskillel, story-gyűjtőbranch, review-út | Stacked PR célváltás és restack |
| Tesztelés | AC-címkés e2e-tesztek és lefedettségi kapu | Egy közös tesztkörnyezet sorral; a tesztadat-delta kézi |
| Release | Release-PR és fast-forward | — |
