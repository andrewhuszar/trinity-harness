# Agent harness – üzleti specifikáció

Állapot: specifikáció. A leírt működés tervezett; az MVP-ben kézi lépéssel helyettesített részeket az [MVP](#mvp) fejezet sorolja fel. A fogalmak pontos jelentését a [CONTEXT.md](../CONTEXT.md), a döntések indoklását az [ADR-ek](./adr/) rögzítik.

## Cél

Az agent harness az a munkakörnyezet, amelyben AI-agentek és emberi csapattagok (BA, product owner, designer, fejlesztő, tesztelő) közösen jutnak el egy rövid üzleti leírástól a kiadott szoftverig. Az agentek elvégzik a kérdezést, a vázlatkészítést, az ellenőrzést, a fejlesztést és az összefoglalást; az emberek döntenek, jóváhagynak és elfogadnak. Minden lépés eredménye verziózott, hivatkozható dokumentum, ezért mindig visszakövethető, melyik kód melyik elvárásra és designra készült.

A harness célja a jobb döntés és a kevesebb újramunka, nem a több generált artefaktum. A sikerét a [Pilot és mérés](#pilot-és-mérés) fejezet mérőszámai igazolják.

## Szereplők

| Szereplő | Felelősség |
|---|---|
| Product owner (PO) | Prioritás, scope-változás, üzleti szabály és release döntése; a sávok közötti ellentmondás feloldása; az epic üzleti bevezetésének gazdája, ha mást nem jelöl ki. |
| BA | Az igény elemzése és előkészítése: üzleti igény, folyamatmodell, funkcionális specifikáció, közös szabályok, storyk és elfogadási feltételek; a story elfogadása. Más jóváhagyást csak a PO kifejezett, epicenként rögzített delegációjával ad. Git-művelet nélkül dolgozik. |
| Domain-szakértő | Event storming, hotspotok lezárása, a domainszabályok megerősítése. |
| Designer | A felhasználói feladat és interakció képviselete a pontosítástól kezdve: az üzleti igény és a folyamatmodell reviewja, koncepciók, képernyő- és komponensdesign, átadás fejlesztésre, DS-komponensek előléptetése, review a működő felületen. Felel a megjelenésért, az interakcióért, az állapotokért és az érthetőségért; az export technikai helyességéért nem. |
| Story-felelős (fejlesztő) | Technikai specifikáció, tervmegerősítés, végrehajtási mód kiválasztása, task PR-ok elfogadása, gyanús tesztkapcsolatok lezárása. |
| Tesztelő | Tesztforgatókönyvek jóváhagyása, a tesztek tartalmi reviewja, feltáró tesztelés, a megtartandó tesztadat kiválogatása. |
| Beküldő agent | A BA változását a tervezési tér draft branchére commitolja. |
| Feldolgozó agent | A beküldött változást ellenőrzi, hibát, javaslatot és hatáslistát ad vissza. |
| AI-szakértő | Egy perspektívából (jogi, biztonsági, üzemeltetési, UX, hibaút-kereső) hotspotot nyit és javasol; nem dönt. |
| AI-projektspecialista | A jelenlegi működés ismeretében iránymutatást ad és ütközést jelez. |
| Fejlesztő agent | Taskot valósít meg, tesztet ír, PR-t nyit, a review-kommentekre javít. |

Agent nem fogadhatja el az általa vagy más agent által generált tartalmat emberi felülvizsgálat nélkül.

### Döntési jogkörök

| Döntés | Döntéshozó | Előkészítő | Helyettesítés, eszkaláció |
|---|---|---|---|
| Prioritás és vállalás | PO | BA | A PO helyettese; vitában a termékfelelős vezető |
| Scope-változás | PO | BA | Mint fent |
| Üzleti szabály | PO, a domain-szakértő megerősítésével | BA | Domain-szakértő hiányában a PO dönt, a fennmaradó kockázat rögzítésével |
| A tervezési sávok közötti ellentmondás | PO | BA, designer, story-felelős | Mint fent |
| Vitás designváltozás besorolása | Designer és BA közösen | Feldolgozó agent | Egyet nem értés esetén a PO |
| Story elfogadása | BA | Tesztelő | Delegálással a PO által kijelölt BA |
| Release | PO | BA | A PO helyettese |

A delegációt és a helyettesítést a harness-konfiguráció rögzíti; a harness ez alapján tudja, kinek a döntésére vár egy átmenet.

## Munkaterek

- **Tervezési tér:** külön GitHub-repó az üzleti artefaktumokkal (domain, epic, üzleti igény, folyamatmodell, közös szabályok és minőségi elvárások, funkcionális specifikáció, design-pillanatkép, story, tesztforgatókönyv, döntésnapló). Itt él minden epic, story és task állapota.
- **Termékrepó:** Azure DevOps-repó a kóddal és a technikai artefaktumokkal (technikai specifikáció, ADR, task). Az üzleti artefaktumokat csak olvasható tervezési másolatként tartalmazza.
- **Claude projekt:** a BA a Claude Code Desktopban, a tervezési tér checkoutjával és a projekt skilljeivel dolgozik.
- **Story-szerkesztő felület:** online alkalmazás, ahol a BA a beküldött változás ellenőrzési eredményét és hatáslistáját látja, kérdésekre válaszol és publikál.
- **Claude Design:** a designer munkafelülete, amely a termékrepó design systemjéből szinkronizált komponenseket használja.

A `/next` a szereplő egyetlen belépési pontja. Egy helyen mutatja a döntésére váró kérdéseket, az érintett artefaktumokat, a blokkolások üzleti okát és felelősét, valamint a következő teendőt. A megszakadt munka a draft branch állapotából folytatható; a `/next` ott veszi fel, ahol abbamaradt. Két BA ugyanazon az epicen saját draft branchen dolgozik; ütközéskor a feldolgozó agent mindkettőnek javasol, de nem dönt. Sikertelen beküldés vagy szinkron esetén a hibaüzenet megnevezi a harness-konfigurációban rögzített támogatási kapcsolatot. Az azonosítókat és a verzióhivatkozásokat az eszköz kezeli, nem a szereplő.

## Folyamat

```
Rövid üzleti leírás
  → Pontosítás: grill a BA-val, designer-review → üzleti igény + folyamatmodell (event storming)
  → Tervezés, három párhuzamos sávban:
      funkcionális specifikáció | design (Claude Design) | technikai specifikáció (grill a fejlesztővel, spike-ok)
  → Tervezési egyeztetés: BA, designer, story-felelős ugyanazon a flow-n és verziókon
  → Bontás: storyk elfogadási feltételekkel, tesztforgatókönyvek, taskok és PR-sorrend
  → Fejlesztés: task PR-ok a story-gyűjtőbranchre, agentes előreview, magyarázott emberi review
  → Tesztelés: story-nkénti tesztkörnyezet, automata tesztek, feltáró teszt, designer-review, BA-elfogadás
  → Elfogadás: a story a develop branchre kerül
  → Release és bevezetés: develop → main, production-telepítés, üzleti bevezetés
```

### Pontosítás

A BA rövid üzleti leírásból indul. Az agent egyesével kérdez, minden kérdéshez ajánlott választ ad, és a válaszokból üzleti igényt állít össze. Az ajánlott válasz javaslat, nem bizonyíték.

Az üzleti igény kötelező szakaszai: cél, érintettek, jelenlegi és kívánt folyamat az eltérésekkel, scope (benne és kívül), sikerességi mérőszám, korlátok, nyitott kérdések. Minden állítás forrásjelölést kap:

- **Megerősített:** stakeholder vagy dokumentum igazolja; a forrás meg van nevezve.
- **Feltételezés:** még nem igazolt, ellenőrzése nyitott kérdés.
- **Agentjavaslat:** az agent ajánlása, amelyet ember még nem erősített meg.

A pontosítás akkor zárható, ha minden szakasz kitöltött, nincs megerősítetlen agentjavaslat, és minden nyitott kérdés megválaszolt vagy elhalasztott. Az elhalasztott kérdésnek felelőse, határideje és feloldási pontja van (az az állapotátmenet, amely előtt meg kell válaszolni). A scope-ot vagy a megvalósíthatóságot eldöntő kérdés nem halasztható. Felhasználói felületet érintő epicnél a designer reviewja is a lezárás feltétele.

### Event storming

- **Big Picture (domain szint):** a domain eseményei, határai és az üzleti szótár. Új domain esetén klasszikus, szinkron **felfedező event storming** gyűjti a fogalmakat; az AI-szakértők és az AI-projektspecialista javaslattal segítik. Az agent feldolgozza és előkészíti az eredményt, majd újabb workshop következik.
- **Process Level (epic szint):** az epic folyamatmodellje stabil azonosítójú folyamatelemekkel (szereplő, command, policy, esemény, read modell, üzleti szabály). Az agent az üzleti igényből és a meglévő domainből vázlatot készít, az AI-szakértők hotspotokat nyitnak, majd egy rövid **hotspot-workshop** csak a nyitott kérdéseket dönti el. A designer a felhasználói feladat lépésszáma, információigénye és hibajavítási módja szempontjából reviewzza.
- **Software Design Level:** a technikai specifikáció architektúraterve, a fejlesztés feladata.

Hotspotot AI is nyithat, de csak ember zárhatja le; a lezárás döntésnapló-bejegyzést kap.

### Közös szabályok és minőségi elvárások

Az elfogadási feltételek nem helyettesítik a közös szabályokat. Ezek saját, stabil azonosítójú helyen élnek, és a storyk hivatkoznak rájuk, nem másolják őket.

- **Domain szinten:** jogosultsági szabályok, adatfogalmak, külső rendszerkapcsolatok.
- **Epic szinten:** az epicre releváns minőségi elvárások (teljesítmény, hozzáférhetőség, üzemeltetés), mérhető értékkel.

A story elfogadási feltétele az adott helyzetben ellenőrizhető eredményt rögzíti, a szabályra hivatkozva.

### Tervezés

A három sáv párhuzamosan halad, és mindhárom a folyamatelemekre hivatkozik.

- **Funkcionális specifikáció:** az epic üzleti működése, amely a végleges designnal egyezik. Képernyőverziókra, folyamatelemekre és közös szabályokra hivatkozik.
- **Design:** lásd [Design](#design). Képernyő nélküli (háttérfeldolgozási, integrációs) epicnél a sáv „nem szükséges” jelölést kap, és designhivatkozás nem követelmény.
- **Technikai specifikáció:** az agent vázlatot készít, majd a story-felelőssel grill-munkamenetben egyesével lezárják a döntéseket. A bizonytalan pontokból időkorlátos spike készül, amely a tervmegerősítés előtt lefut. A technikai specifikáció taskonként rögzíti az eszközt (például command, saga, képernyőimport), a végrehajtási módot (`agent` vagy `pár`), a függőségeket és a PR-sorrendet.

**Tervezési egyeztetés:** a bontás előtt a BA, a designer és a story-felelős közösen végigmegy ugyanazon a flow-n ugyanazokkal a verziókkal, a kivételekkel és a hibaágakkal együtt. A talált ellentmondást a PO oldja fel; az eredmény döntésnapló-bejegyzés.

### Bontás

A funkcionális specifikációból storyk készülnek részletes elfogadási feltételekkel, a technikai specifikációból pedig taskok. A szeletelés elsődleges szempontja az önállóan ellenőrizhető üzleti eredmény, a kockázat és a függőség. A flow-lépések száma (kb. öt fölött) review-jelzés, nem automatikus elutasítás. A technikai taskbontás nem alakítja a storykat üzleti eredmény nélküli backend- és frontend-szeletekké. Az elfogadási feltételekből tesztforgatókönyvek (pozitív, negatív, határeset) készülnek, amelyeket a tesztelő jóváhagy.

## Design

A koncepcióalkotás szabad; a verziózás, az azonosítás, a csomagolás és a szinkron az eszköz feladata, nem a designeré.

1. A designer a Claude Designban képernyőt vagy komponenst tervez a design system már productionben használt primitív és összetett, tiszta komponenseiből.
2. Új képernyőről koncepcióverziók készülnek üzleti reviewra (például `A1.2`, `C1`).
3. Új vagy kockázatosnak jelölt felhasználói folyamatnál a képernyőverzió elfogadása előtt a bizonytalansággal arányos **használhatósági validáció** történik, például prototípus-teszt célfelhasználókkal; az eredmény rögzítésre kerül. Más esetben a validáció opcionális.
4. Elfogadáskor a designer az **Átadás fejlesztésre** művelettel adja ki a választott koncepciót. Az eszköz képernyőverziót képez (például `SCR-12@3 ← C1`), azonosítót ad, csomagol és előkészíti a PR-t. A képernyő statikus React kódja a design system komponenseire, tokenjeire és Tailwind classaira épül; technikai helyességét az eszköz és a fejlesztés biztosítja. A fejlesztés **képernyőimporttal** véglegesíti, komponensekre bontja és beköti az adatot.
5. Az **átadási csomag** a képernyőkód mellett a flow szempontjából releváns állapotokat és interakciókat is tartalmazza: betöltés, üres, hiba és siker; jogosultságfüggő megjelenés; hosszú szöveg és nagy adatmennyiség; reszponzív viselkedés; fókusz, billentyűzetes használat és interakciós visszajelzés. Az agent jelzi a hiányt, de csak a releváns állapotokat követeli meg.
6. A designer által design system szintre léptetett új komponens importálható UI-lib elemként kerül a termékrepóba (**komponensimport**). Ettől kezdve a designer és a fejlesztés is módosíthatja; a fejlesztés a dinamikus részeket alacsony szintű, shadcn-szerű komponensekkel adja hozzá, és a Claude Design továbbra is használni tudja.
7. A design system kanonikus helye a termékrepó. A fejlesztői változás merge után visszaszinkronizálódik a Claude Designba, a designer változása design-PR-ként érkezik.

**Designváltozás:** minden képernyőverzió-emeléskor a designer jelöli a változás típusát, és külön azt, hogy van-e **használhatósági vagy akadálymentességi hatása** (például kisebb betűméret, gyengébb kontraszt, átrendezett gombsor).

- **Megjelenítési pontosítás:** csak vizuális eltérés. Nem blokkolja a fejlesztést; a fejlesztés vizuális diffet kap, és átvezeti. Ha a story már `Elfogadva` vagy `Kiadva` állapotú, automatikusan design-frissítési story nyílik.
- **Viselkedési változás:** új adat, interakció, állapot vagy folyamat. Ez tervezési eltérés: a BA frissíti a funkcionális specifikációt, a fejlesztő megerősíti a tervet.

Használhatósági vagy akadálymentességi hatással járó megjelenítési pontosítás a designer és a BA jóváhagyását igényli. A feldolgozó agent indokolja a besorolást, és viselkedési változásként kezeli a pontosításnak jelölt, de új adatot vagy interakciót hozó változást. Vitás esetben a designer és a BA közösen, egyet nem értésnél a PO dönt.

**A designer napi munkája:** az aktuális brief és a nyitott kérdések megtekintése a `/next`-ben → szabad koncepcióalkotás → review → a választott változat átadása → a működő implementáció ellenőrzése. A hivatkozásokat és az értesítéseket a harness kezeli.

## Elfogadási feltételek

Az elfogadási feltételek explicitek és tömörek: minden lényeges elvárást lefednek, töltelék nélkül, a domain szótárának szavaival, konkrét értékekkel. Indoklás, pixelleírás és implementációs utalás nem kerül beléjük; a közös szabályokra és minőségi elvárásokra hivatkoznak.

**Flow-lépés:** előfeltétel, látható, művelet, és minden eredményág alpontként. Üres mező helyén `—` áll.
**Szabály:** egyetlen „Ha …, akkor …” mondat.

```md
- **2** Fájl kiválasztása — SCR-12@3, DOC:CMD-3
   - Előfeltétel: bejelentkezett ügyintéző (DOC:PERM-2); az ügy nyitott; nincs folyamatban lévő feltöltés.
   - Látható: ügy neve; engedett típusok (PDF, JPG); méretkorlát 20 MB; „Feltöltés” inaktív.
   - Művelet: fájl kiválasztása; mégse.
- **2.1** Engedett fájl → fájlnév és méret látható, „Feltöltés” aktív.
- **2.1-x1** Jelszóval védett PDF → hibaüzenet a mező alatt, „Feltöltés” inaktív.
- **2.2** ~~Nem engedett típus vagy 20 MB fölött → hibaüzenet a mező alatt.~~ (2026-11-01)
- **2.2a** Nem engedett típus vagy 20 MB fölött → hibaüzenet a mező alatt, a kiválasztás törlődik.
- **2.3** ~~Mégse → vissza az 1-re.~~ Visszavonva 2026-11-01.
- **3** Ha az ügy lezárt, a feltöltés nem indítható, és a gomb nem jelenik meg. [kézi]
```

**Azonosítás:**

- Minden feltétel külön felsorolásjeles sor, félkövér szöveges azonosítóval; az azonosító storyn belül egyedi, és a storyval együtt hivatkozható: `TRN-045#2.2a`.
- A pont hierarchiát jelöl, a `-xN` az adott elem után beszúrt testvért (korlátlanul: `-x1`, `-x2`), a betű módosítást (`2.2a`, `2.2b`).
- Minden szövegváltozás új betűt kap; az eredeti szöveg áthúzva, dátummal megmarad. Visszavont feltétel áthúzva, `Visszavonva <dátum>` jelöléssel marad.
- Azonosító nem számozódik át és nem használható újra.
- A BA, a tesztelő és a fejlesztő az eszközben tiszta nézetben, az áthúzott sorok nélkül látja az érvényes feltételeket; a korábbi változatok és a kapcsolódó döntések külön elérhetők.

**Ellenőrzési mód:** alapértelmezés szerint minden feltételt automata e2e-teszt igazol. Ha az elvárás böngészős teszttel nem igazolható, a sor végén jelölt mód érvényes: `[integrációs]`, `[kézi]` (a tesztelő rögzített eredménye) vagy `[monitorozás]` (élesben mért mutató).

**Gyanús tesztkapcsolat:** módosítás vagy visszavonás után a régi azonosítóra mutató teszt felülvizsgálatig blokkolja a story továbblépését. A felülvizsgálatot a story-felelős zárja le a tesztet módosító vagy átcímkéző PR-ban; a bizonyíték a teszt diffje, amelyet a review lát.

## Állapotok

### Epic

| Állapot | Belépési feltétel | Léptető |
|---|---|---|
| `Vázlat` | A rövid üzleti leírás beküldve. | BA |
| `Pontosítva` | Az üzleti igény és a folyamatmodell elfogadva. | BA, delegáció szerint |
| `Tervezés alatt` | A funkcionális specifikáció, a design és a technikai specifikáció sávja fut. | Harness |
| `Bontva` | A tervezési egyeztetés lezárult; a funkcionális specifikáció elfogadva és egyezik a képernyőverziókkal; a technikai specifikáció megerősítve; a storyk, a tesztforgatókönyvek és a taskok létrejöttek. | BA és story-felelős |
| `Fejlesztés alatt` | Legalább egy story fejlesztése elindult. | Harness |
| `Kiadva` | Legalább egy story `Kiadva`, a többi `Kiadva` vagy `Jegelve`. | Harness |
| `Lezárva` | Minden story `Jegelve`; az epic szállítás nélkül zárult (például visszavont igény). | PO |
| `Jegelve` | Bármikor; a munka szünetel. | PO |

### Story

| Állapot | Belépési feltétel | Léptető |
|---|---|---|
| `Fejlesztésre kész` | Bontáskor létrejött; az elfogadási feltételek folyamatelemekre és képernyőverziókra hivatkoznak; legalább egy task tartozik hozzá. | Harness |
| `Fejlesztés alatt` | Az első task fejlesztése elindult. | Harness |
| `Tesztelés alatt` | Minden task mergelve a story-gyűjtőbranchbe, a pipeline zöld, és minden automata ellenőrzési módú elfogadási feltételhez és jóváhagyott forgatókönyvhöz tartozik teszt. A story saját tesztkörnyezetet kap. | Harness |
| `Elfogadva` | A tesztelő, UI-t érintő storynál a designer, majd a BA elfogadta; a story-gyűjtőbranch a `develop`-ra került. | BA, majd harness |
| `Kiadva` | A story a production release része. | Harness |
| `Jegelve` | A `Kiadva` kivételével bármikor, indoklással (például elutasított vagy visszavont igény). | PO vagy story-felelős |

- **Visszalépés:** sikertelen elfogadás (UAT) esetén a story `Tesztelés alatt` → `Fejlesztés alatt` állapotba lép, a talált hibákból javító task készül.
- **Blokkolás:** a `Blokkolva` jelző, nem állapot. Az epic, a story vagy a task bármely állapotában beállítható ok, felelős és várt feloldás megadásával; a harness értesíti a felelőst, és a `/next` megmutatja.
- `Elfogadva` vagy `Kiadva` story nem nyílik újra; a későbbi változás új story.

### Task

`Tervezve` → `Fejlesztés alatt` → `Elfogadásra vár` (a task PR review alatt) → `Mergelve`.

## Kapuk és döntések

Minden állapotátmenet kétszintű kapun megy át.

- **Determinisztikus ellenőrzés:** struktúra, kötelező mezők, forrásjelölések, hivatkozások, azonosítók. Hiba esetén az átmenet blokkolt, és a beküldő agent kapja vissza. A determinisztikus kapu a szerkezetet ellenőrzi, nem az üzleti helyességet.
- **Szemantikus javaslat:** a feldolgozó agent észrevétele szótár-ütközésről, ellentmondásról, kimaradt hibaútról, hiányos lefedettségről.

**Döntésnapló:** minden elutasított szemantikus javaslat, lezárt hotspot, tervezési egyeztetés és vitás besorolás bejegyzést kap: döntéshozó, érintett verzió, indok és fennmaradó kockázat. Az elutasítás nem egyenértékű a kockázat megszüntetésével; a fennmaradó kockázat látható marad. Ha a döntés nem a szereplő jogköre, a harness a [döntési jogkörök](#döntési-jogkörök) szerinti döntéshozóhoz irányítja.

## Változáskezelés

Az üzleti artefaktum bármikor módosítható. Publikálás előtt a feldolgozó agent **hatáslistát** ad: az érintett storyk, közös szabályok, képernyők és tesztek köre, valamint a prioritásra és a vállalásokra gyakorolt hatás. Scope-változás a PO jóváhagyásával publikálható.

A publikált változás automatikusan eljut a termékrepóba és a folyamatban lévő story-gyűjtőbranchekre. Ha egy technikai specifikáció vagy task régebbi verzióra hivatkozik, mint ami a branchen van (**tervezési eltérés**), az érintett taskok megállnak, és a story csak a fejlesztő tervmegerősítése után mergelhető. A tervmegerősítés a technikai érvényességet igazolja, az üzleti jóváhagyást nem helyettesíti. Változás nem csúszhat át észrevétlenül.

## Tesztelés és elfogadás

- Minden `Tesztelés alatt` story saját, eldobható tesztkörnyezetet kap saját URL-lel, egy verziózott, életszerű **arany tesztadat** klónjával.
- Ott futnak az automata tesztek, ott végez a tesztelő feltáró tesztelést, UI-t érintő storynál ott reviewzza a designer a működő felületet, és ott fogad el a BA.
- **Tartalmi tesztreview:** a tesztelő a teszt PR-ban ellenőrzi, hogy a teszt ténylegesen a hivatkozott elvárást igazolja; egy AC-címke létezése önmagában nem bizonyíték.
- **Nyomkövetés:** az igény → folyamatelem és közös szabály → story és elfogadási feltétel → forgatókönyv → teszteredmény lánc a story nézetében áttekinthető.
- **Designer-review:** a designer tesztlinket és vizuális összevetést kap, és helyben jelez vissza. A működést vagy a hozzáférhetőséget rontó eltérés javítandó; a kisebb esztétikai pontosítás design-frissítési storyba kerül.
- **Elfogadás bizonyítéka:** a BA-elfogadás rögzíti a vizsgált verziót, az eredményt és a nyitott hibákat; a `[kézi]` ellenőrzésű feltételeknél a tesztelő rögzített eredményét is.
- A tesztelés végén a tesztelő vagy a BA kiválogatja a megtartandó új adatot. Ez **tesztadat-deltaként** bekerül a következő arany tesztadatba, így a tesztadat a valós tesztelésből gazdagodik.
- Ha a delta által módosított vagy törölt rekord közben megváltozott az aranyban, illetve egy új rekord azonosítója már létezik, a story merge-kapuja blokkol. A tesztelő vagy a BA kézzel feloldja a konfliktust és frissíti a deltát; ezután az arany újraépítése és a delta ellenőrzése újrafut. Automatikus felülírás nincs.
- Az elfogadás után a story a `develop` branchre kerül.
- Másik story integrálása nem igényli a korábban elfogadott story ismételt BA-elfogadását. Az integrációs és regressziós ellenőrzés azt vizsgálja, hogy az elfogadott működések együtt is helyesek; az eltérés javítandó hiba.
- A story saját elfogadott üzleti tartalmának vagy elfogadási feltételeinek változása új üzleti elfogadást igényel. `Elfogadva` vagy `Kiadva` story esetén a változás új storyban készül el.

## Release és bevezetés

- A `develop` csak elfogadott storykat tartalmaz, ezért bármely pontja kiadható.
- Minden `develop`-merge automatikusan a stagingre települ, ahol a teljes e2e regressziós készlet fut.
- A release-ről a PO dönt; az online felületen a PO vagy megbízásából a BA indítja. A harness generált release note-tal (storyk, képernyőverziók, migrációk, tesztadat-verzió) release-PR-t nyit `develop` → `main` irányba.
- A kiadandó összeállítás zöld staging regressziója mellett a release-PR mergelődik, a `main` verziótagot kap, és ugyanaz a build kerül productionbe, amely a stagingen futott. Korábbi összeállítás zöld eredménye nem elegendő. Az érintett storyk `Kiadva` állapotba lépnek. Az MVP-ben, amíg a webalkalmazás nem használ azonos origint, a build környezetenként külön készül; a commit azonos, az image nem.
- Hotfix a `main`-ből indul, és a `main`-re és a `develop`-ra is visszakerül.
- **Üzleti bevezetés:** minden epicnek van bevezetési felelőse (alapértelmezés szerint a PO), aki gondoskodik az érintettek tájékoztatásáról, az oktatásról és a támogatás felkészítéséről.

## MVP

Az MVP egy valódi epicet visz végig minden fázison. Ahol még nincs automatizálás, dokumentált kézi lépés vagy prompt áll a helyén; minden kézi lépésnek kijelölt felelőse van, és nem minden apró iteráció vár rá.

| Terület | MVP-ben automatizált | MVP-ben kézi | A kézi lépés felelőse |
|---|---|---|---|
| Tervezés | Tervezési tér struktúra, BA-skillek (`/next`, pontosítás, funkcionális specifikáció, bontás, AC-formátum), beküldés draft branchre, determinisztikus kapu | Online felület: a BA beillesztendő promptot kap a válaszokhoz; event storming: workshop és utólagos agentfeldolgozás | BA |
| Szinkron | Tervezési szinkron és eltérésjelzés a termékrepó felé | — | — |
| Design | — | Az átadás fejlesztésre: a designer exportját egy kijelölt fejlesztő commitolja | Kijelölt fejlesztő |
| Fejlesztés | Fejlesztési útmutató 2–3 eszközskillel, story-gyűjtőbranch, review-út | Stacked PR célváltás és restack | Story-felelős |
| Tesztelés | AC-címkés e2e-tesztek és lefedettségi kapu | Egy közös tesztkörnyezet sorral; a tesztadat-delta kézi | Tesztelő |
| Release | Release-PR és fast-forward | Környezetenkénti build az azonos origin bevezetéséig | Story-felelős |

## Pilot és mérés

A pilot egyetlen valódi flow-val indul, és a mostani fejlesztési workflow-val összevetve mér. Kiindulási értéket (baseline) a pilot előtt egy hasonló méretű, a mostani workflow-val készült igényen rögzítünk; a célértékeket a PO a pilot indulása előtt jóváhagyja.

| Mérőszám | Mit mér |
|---|---|
| Átfutási idő | Az igény beküldésétől a story elfogadásáig eltelt idő |
| Újramunka | Félreértésből eredő AC-módosítások, visszalépések és elutasított elfogadások száma |
| BA-adminisztráció | A BA nem döntésre és nem elemzésre fordított ideje |
| Design-átadás | Az export és az adminisztráció ideje, a fejlesztővel szükséges tisztázó körök száma, az implementációban maradó designeltérések |
| Döntési idő | A döntésre váró kérdés megnyitásától a lezárásáig eltelt idő |

A pilot akkor sikeres, ha a célértékek teljesülnek, és a szereplők napi munkájában a verziók, azonosítók és szinkronhibák kezelése nem jelenik meg teherként.
