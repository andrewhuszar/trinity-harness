# Agent harness

Az a munkakörnyezet, amelyben AI-agentek és fejlesztői, illetve BA-tapasztalattal rendelkező emberi csapattagok közösen jutnak el az üzleti igénytől a kiadott szoftverig.

## Nyelv

### Terek és repók

**Tervezési tér**:
Külön git repóban élő, előre meghatározott, többszintű markdown-struktúra, amelyben a BA az üzleti artefaktumokat készíti.
_Kerülendő_: projekt, tervezési projekt

**Termékrepó**:
A fejlesztett szoftver kódbázisa, amelyen a fejlesztő agentek és a fejlesztők dolgoznak.
_Kerülendő_: projekt

**Harness repó**:
A harness specifikációját, pluginjait és szolgáltatását tartalmazó repó.

**Harness-plugin**:
Szerepenként (`harness-ba`, `harness-dev`) globálisan telepített, verziózott Claude Code plugin, amely a harness skilljeit, parancsait és hookjait adja.
_Kerülendő_: kit, projektskill

**Harness-konfiguráció**:
A projektben tárolt beállítás (story-prefix, repócímek, struktúra), amely alapján a harness-plugin az adott projektben működik.

**Framework-skill**:
A Trinity frameworkkel együtt változó és terjedő eszközskill, generátor vagy arany példa.

**Claude projekt**:
A Claude Code Desktop munkaterülete, amelyben a BA a tervezési tér saját checkoutjával, instrukcióival és skilljeivel dolgozik.
_Kerülendő_: projekt (önmagában)

**Draft branch**:
A tervezési tér epicenként és BA-nként külön branche (`draft/<epic>/<ba>`), amelyre a beküldő agent a BA még nem publikált változását commitolja.

**Publikálás**:
A BA online felületen kiváltott művelete, amely a draft branchből PR-t nyit a tervezési tér `main`-jére; zöld determinisztikus kapu és lezárt szemantikus javaslatok esetén automatikusan mergelődik.

### Tervezési szintek

**Domain**:
A tervezési tér legfelső szintje: a Big Picture event storming eredménye, az üzleti szótár és a domainhatárok.

**Epic**:
A tervezés egysége: egy üzleti cél és scope, amelyhez üzleti igény, folyamatmodell, funkcionális specifikáció, design és technikai specifikáció tartozik; storykra bomlik.
_Kerülendő_: feature

**Story**:
Egy epic önállóan szállítható és a BA által elfogadható része céllal és részletes elfogadási feltételekkel; a tervezés után, a bontáskor jön létre.

**Task**:
Egy story technikai specifikációból származó, egyetlen PR-ban megvalósított és átnézhető fejlesztési egysége.

### Üzleti artefaktumok

**Üzleti igény**:
Egy epic pontosított üzleti célja, scope-ja és korlátai, amely a rövid üzleti leírásból a BA-val folytatott kérdezz-felelek során születik.
_Kerülendő_: business requirement, story (ebben a fázisban)

**Felfedező event storming**:
Új domain vagy nagyon nagy epic indításakor tartott klasszikus, szinkron workshop, amely a fogalmakat és az eseményeket gyűjti; az AI-szakértők és az AI-projektspecialista javaslattal segítik, és az agent-feldolgozás után újabb workshop következik.

**Hotspot-workshop**:
Rövid szinkron alkalom, amelyen a domain-szakértők csak az agent által előkészített folyamatmodell-vázlat nyitott hotspotjait döntik el.

**Hotspot**:
Egy event storming során nyitott, emberi döntést igénylő kérdés vagy ellentmondás.

**Folyamatmodell**:
Egy epic Process Level event storming eredménye: szereplők, commandok, policy-k, események, read modellek és üzleti szabályok.

**Folyamatelem**:
A folyamatmodell egy stabil azonosítójú eleme, amelyre a funkcionális specifikáció, az elfogadási feltételek és a technikai specifikáció hivatkoznak.

**Funkcionális specifikáció**:
Egy epic üzleti működésének részletes leírása, amely a végleges designnal egyezik, és amelyből a storyk elfogadási feltételei származnak.
_Kerülendő_: üzleti spec, spec (önmagában)

**Design**:
Egy epic Claude Designban készülő felületterve, amelyet a designer készít és a BA-val együtt fogad el.
_Kerülendő_: architektúra, technikai design

**Design-pillanatkép**:
Egy elfogadott design verziózott exportja a tervezési térben: képernyők, képernyőképek és a képernyők statikus React kódja, amely a design system komponenseire, tokenjeire és Tailwind classokra épül.

**Design system**:
A designer és a fejlesztés közös, importálható UI-komponenskönyvtára tokenekkel; a termékrepóban él, a Claude Design pedig a róla szinkronizált változatból épít.

**Design-PR**:
A designer Claude Design-exportjából a harness által nyitott PR a termékrepó design systemjére, amelyet a fejlesztés hagy jóvá.

**DS-komponens**:
A design system tiszta, megjelenítési komponense, amelyet a designer készít vagy léptet elő, és mindkét fél módosíthat.

**Komponensimport**:
Az a kezdeti fejlesztési lépés, amely egy DS-komponenst apró javításokkal a termékrepó design systemjébe emel; ettől kezdve fejleszthető rá.

**Képernyőimport**:
Az a fejlesztési lépés, amely a design-pillanatkép statikus képernyőkódját véglegesíti, komponensekre bontja és a view-ba építi.

**Képernyő**:
A design-pillanatkép egy stabil azonosítójú felülete, amelyre a funkcionális specifikáció és az elfogadási feltételek hivatkoznak.

**Koncepcióverzió**:
Egy képernyő design review alatti, a Claude Designban élő változata (például `A1.2`, `C1`), amelyet az üzlet véleményez.
_Kerülendő_: verzió (önmagában)

**Képernyőverzió**:
Egy képernyő elfogadott, monoton növekvő verziója a design-pillanatképben (például `SCR-12@3`), amely rögzíti, melyik koncepcióverzióból született.

**Megjelenítési pontosítás**:
Képernyőverzió-emelés, amely csak vizuális eltérést hoz, funkcionális specifikációt és elfogadási feltételt nem érint; nem blokkol, de a view-ban át kell vezetni.

**Viselkedési változás**:
Képernyőverzió-emelés, amely új adatot, interakciót, állapotot vagy folyamatot hoz; tervezési eltérésnek minősül.

**Design-frissítési story**:
Automatikusan nyitott kis story, amely egy már `Elfogadva` vagy `Kiadva` állapotú story képernyőjén átvezeti a megjelenítési pontosítást.

**Elfogadási feltétel**:
Egy story explicit, tömör, ellenőrizhető elvárása; storyn belül stabil azonosítóval (`2.1`, `2.1-x1`, `2.2a`) és a story azonosítójával együtt hivatkozható (`TRN-045#2.2a`).
_Kerülendő_: követelmény, AC (önálló azonosítóként)

**AC-azonosító**:
Az elfogadási feltétel címkéje, amelyben a pont hierarchiát (`2.1`), a `-xN` utótag beszúrt testvért (`2.1-x1`), a betű módosítást (`2.2a`) jelöl.

**Gyanús tesztkapcsolat**:
Olyan tesztcímke, amely egy módosított vagy visszavont AC-azonosítóra mutat; felülvizsgálatig blokkolja a lefedettségi kaput.

**Flow-lépés**:
Felső szintű elfogadási feltétel, amely egy folyamatlépés előfeltételét, a láthatót, a lehetséges műveleteket és minden eredményágát rögzíti; az eredményágak alpontok.

**Szabály**:
Felső szintű, „Ha …, akkor …” formájú elfogadási feltétel, amely nem flow-lépéshez kötött.

**Tesztforgatókönyv**:
Az elfogadási feltételekből bontáskor generált, a tesztelő által jóváhagyott pozitív, negatív vagy határeset-forgatókönyv a tervezési térben.

### Technikai artefaktumok

**Technikai specifikáció**:
Epic szintű technikai artefaktum a termékrepóban, amely meghatározza a storykat megvalósító taskokat, spike-okat és a PR-sorrendet.
_Kerülendő_: technikai terv, tech spec

**Architektúraterv**:
A technikai specifikáció szakasza, amely a folyamatmodellt aggregátumokra, commandokra és sagákra képezi le; új modult vagy domainhatárt érintő epicnél kötelező.
_Kerülendő_: design (az a UI-tervet jelenti)

**Végrehajtási mód**:
A task technikai specifikációban rögzített jelölése: `agent` esetén a fejlesztő agent autonóm, távoli munkamenetben dolgozik; `pár` esetén a fejlesztő a saját Claude Code-jában vezeti.

**Tervmegerősítési kapu**:
A technikai specifikáció kétszintű kapuja: determinisztikusan minden task pontosan egy storyhoz tartozik, a függőségi gráf aciklikus, minden task becsült mérete a PR-korlát alatt van, és nincs nyitott spike; szemantikusan az AC-lefedettséget, az ADR- és rétegszabály-megfelelést, a contract-first bontást és a migrációs kockázatot vizsgálja.

**Spike**:
Bizonytalanságot csökkentő, időkorlátos task, amely a tervmegerősítés előtt fut; kimenete döntés, ADR vagy a technikai specifikáció frissítése, nem termékkód.

### Kapuk

**Kétszintű kapu**:
Minden állapotátmenet ellenőrzési mintája: a determinisztikus ellenőrzés blokkol, a szemantikus ellenőrzés javaslatot ad.

**Determinisztikus ellenőrzés**:
Struktúra, kötelező mezők, hivatkozások és azonosítók gépi ellenőrzése; hibája blokkolja az átmenetet, és a beküldő agenthez kerül vissza.

**Szemantikus javaslat**:
A feldolgozó agent észrevétele szótár-ütközésről, ellentmondásról vagy kimaradt hibaútról; a BA indoklással elutasíthatja, és az elutasítás rögzítésre kerül.

**Elhalasztott kérdés**:
Nyitott kérdés, amelyet felelőssel és határidővel kifejezetten későbbre tesznek; nem blokkolja a pontosítás lezárását.

### Branchek és PR-ok

**`develop`**:
A termékrepó integrációs branche, amely kizárólag elfogadott storykat tartalmaz, és bármely pontja release-jelölt.
_Kerülendő_: development, dev

**`main`**:
A termékrepó productiont tükröző branche; csak release vagy hotfix változtatja.

**Release**:
A `develop` egy pontjának a `main`-re juttatása és production-telepítése, amelyet a `main` verziótagje azonosít.

**Staging**:
A `develop` minden merge-ét automatikusan futtató környezet, ahol a teljes e2e regressziós készlet fut.

**Release-PR**:
A harness által a BA vagy a product owner kérésére nyitott `develop` → `main` PR generált release note-tal; fast-forward módon mergelődik.

**Story-gyűjtőbranch**:
Egy story saját branche, amelyből a task branchek indulnak, amelybe az átnézett task PR-ok mergelődnek, és amely egyben kerül a `develop` branchre.
_Kerülendő_: feature branch

**Task PR**:
Egy task egyetlen, emberi review-val elfogadott PR-ja a story-gyűjtőbranchre vagy stack esetén a függőség branchére.

**Stacked PR**:
Egy még nem mergelt task branchére épülő task PR, amelynek fejlesztése és reviewja nem vár a függőségre, csak a merge-e.

**Contract-first task**:
Egy függőség szerződését (contract, application contract, kanonikus modell) külön, gyorsan mergelhető taskba emelő bontás, amely a ráépülő taskokat párhuzamosíthatóvá teszi.

### Agentfejlesztés

**Fejlesztési útmutató**:
A fejlesztő agent fő skillje, amely a task eszközjelölése alapján kiválasztja az eszközskillt, az arany példát és a generátort, és meghatározza a fejlesztés lépéseinek sorrendjét.
_Kerülendő_: coding guideline (önálló dokumentumként)

**Eszköz**:
A technikai specifikációban taskonként megjelölt megvalósítási minta, például command, query, saga, aggregate flow, képernyőimport vagy komponensimport.

**Eszközskill**:
Egy eszköz megvalósítási szabályait tartalmazó skill, amelyet a fejlesztési útmutató indít.

**Arany példa**:
A termékrepó egy hivatkozott, mintaszerű megvalósítása, amelyet az eszközskill követendőként jelöl meg.

**Generátor**:
Egy eszköz mechanikus vázát előállító kódgenerátor, amelyet a fejlesztő agent kézi írás helyett használ.

### Tesztelés

**Tesztkörnyezet**:
Egy `Tesztelés alatt` állapotú story saját, eldobható környezete, amely a story-gyűjtőbranchet futtatja az arany tesztadat klónján.
_Kerülendő_: preview (önmagában), test környezet (közösként értve)

**Arany tesztadat**:
Verziózott, buildből előálló adatbázis, amely az előző aranyra merge-sorrendben a storyk migrációit és tesztadat-deltáit építi.
_Kerülendő_: snapshot (kézzel készítettként értve)

**Tesztadat-delta**:
Egy story tesztelése végén kiválogatott új, módosított és törölt üzleti rekordok JSON-leírása a rögzítési sémaverzióval és az érintett rekordok elvárt kiinduló állapotával.

**Review-magyarázat**:
A review-explain skill által a task PR-hoz írt összefoglaló a belépési pontokról, flow-król, üzleti hatásról, kockázatokról, tesztrésekről, olvasási sorrendről és a megmaradt észrevételekről.

**Agentes előreview**:
Az emberi review előtti agentes hibakeresés, amelynek megerősített találatait a fejlesztő agent kijavítja.

### Szinkron és verziók

**Üzleti artefaktum**:
A tervezési térben élő domain, epic, üzleti igény, folyamatmodell, funkcionális specifikáció, design-pillanatkép vagy story.

**Technikai artefaktum**:
A termékrepóban élő technikai specifikáció, ADR vagy task.

**Tervezési másolat**:
Egy üzleti artefaktum adott verziójának csak olvasható másolata a termékrepóban; story esetén **story-másolat**.

**Tervezési szinkron**:
Az az automatikus folyamat, amely az üzleti artefaktumok változását PR-ként a termékrepó `develop` branchére, majd az érintett folyamatban lévő story-gyűjtőbranchekre juttatja.
_Kerülendő_: hook, story-szinkron

**Tervezési eltérés**:
Az az állapot, amikor egy branch tervezési másolata újabb verzió, mint amelyre egy technikai artefaktum hivatkozik; story esetén **story-eltérés**.

**Tervmegerősítés**:
Egy fejlesztő jóváhagyása arról, hogy a technikai artefaktum az aktuális hivatkozott verzióra érvényes.

**Állapot**:
Egy epic, story vagy task életciklus-pozíciója a fejlesztési állapottal együtt, amelyet kizárólag a tervezési tér tárol.

### Állapotok

- **Epic**: `Vázlat` → `Pontosítva` (üzleti igény és folyamatmodell elfogadva) → `Tervezés alatt` (funkcionális specifikáció, design és technikai specifikáció párhuzamos sávjai) → `Bontva` (storyk és taskok létrehozva) → `Fejlesztés alatt` → `Kiadva`; bármikor `Jegelve`.
- **Story**: `Fejlesztésre kész` → `Fejlesztés alatt` → `Tesztelés alatt` (minden task mergelve a gyűjtőbe, a pipeline zöld; a tesztkörnyezetben tesztelő és BA dolgozik) → `Elfogadva` (a gyűjtő mergelve a `develop`-ra) → `Kiadva`; a `Kiadva` kivételével bármikor `Jegelve`.
- **Task**: `Tervezve` → `Fejlesztés alatt` → `Elfogadásra vár` (task PR review alatt) → `Mergelve`.

### Szereplők

**AI-szakértő**:
Egy előre definiált perspektívát (például jogi, biztonsági, üzemeltetési, UX vagy hibaút-kereső) képviselő agent, amely hotspotot nyithat és javasolhat, de döntést nem hoz.

**AI-projektspecialista**:
A rendszer jelenlegi működését a tervezési térből és a termékrepóból ismerő agent, amely az event stormingon iránymutatást ad és ütközéseket jelez.

**Story-felelős**:
A story emberi fejlesztő felelőse, aki a technikai döntéseket hozza és a task PR-okat elfogadja.

**Fejlesztő agent**:
Egy taskot a task branchén megvalósító agent, amely kódot és tesztet ír, lefuttatja a minőségkapukat, PR-t nyit és a review-kommentekre reagál.

**BA**:
Üzleti elemző vagy üzleti szereplő, aki a tervezési térben a Claude projekten keresztül dolgozik, és soha nem végez közvetlen git-műveletet.

**Beküldő agent**:
A BA gépén futó agent, amely a BA változását a tervezési térbe juttatja és commitolja.

**Feldolgozó agent**:
Szerveroldali agent, amely a beküldött változást ellenőrzi, a hibát a beküldő agentnek, a hiányosságot javaslatként a BA-nak jelzi vissza.

**Harness-szolgáltatás**:
Az Azure-on futó szerveroldali komponens, amely az állapotgépet, a kapukat, a tervezési szinkront, a stacked PR-automatizálást, az agentindítást és a tesztkörnyezetek életciklusát kezeli, platformadaptereken keresztül.

**Story-szerkesztő felület**:
Online alkalmazás, ahol a BA a beküldött változás eredményét látja, kérdésekre válaszol és a változást publikálja.

## Kapcsolatok

- Egy **BA** egy **Claude projektben** dolgozik, amely a **tervezési tér** checkoutja.
- A **beküldő agent** a változást egy **draft branchre** commitolja; a **feldolgozó agent** minden push után lefuttatja a kaput.
- Párhuzamos BA-módosítás ütközésekor a feldolgozó agent rebase-el, szöveges ütközésnél mindkét BA-nak javasol, de nem dönt.
- A **tervezési tér** GitHubon, a **termékrepó** Azure DevOpsban él; a **tervezési szinkron** a két platform között fut.
- A **tervezési tér** és a **termékrepó** külön repó; **üzleti artefaktum** csak az előbbiben, **technikai artefaktum** csak az utóbbiban él.
- Egy **domain** több **epicet** szolgál ki; egy **epic** egy **üzleti igényt**, **folyamatmodellt**, **funkcionális specifikációt** és **technikai specifikációt** kap, majd több **storyra** bomlik.
- A **storyk** és **taskok** az epic tervezése után, a funkcionális és a technikai specifikáció alapján jönnek létre.
- Egy **story** egy vagy több **taskból** áll; egy **task** pontosan egy PR. Ha egy task nem fér egy átnézhető PR-ba, a technikai specifikációban kell tovább bontani.
- A **funkcionális specifikáció** és a **design-pillanatkép** egyezik; a design változása új verzió és **tervezési eltérést** vált ki.
- A **design-pillanatkép** képernyőkódja felhasználható kiindulópont: a fejlesztő **képernyőimporttal** véglegesíti, és a dinamikus részeket alacsony szintű, shadcn-szerű komponensekkel adja a statikus vázhoz.
- Elfogadáskor egy **koncepcióverzióból** új **képernyőverzió** lesz; a funkcionális specifikáció, az elfogadási feltételek és a taskok csak **képernyőverzióra** hivatkoznak.
- A designer jelöli, hogy a képernyőverzió-emelés **megjelenítési pontosítás** vagy **viselkedési változás**; a feldolgozó agent új adat vagy interakció esetén emberi jóváhagyásig viselkedési változásként kezeli.
- **Megjelenítési pontosítás** esetén a PR akkor mergelhető, ha a view a legfrissebb képernyőverzióra hivatkozik; `Elfogadva` vagy `Kiadva` storynál **design-frissítési story** nyílik.
- Egy **task PR** csak review után kerül a **story-gyűjtőbranchbe**; függőség esetén **stacked PR** készül, a harness restackel, célt vált és kaszkádszerűen mergel.
- A task PR útja: CI-kapuk → **agentes előreview** → **review-magyarázat** → emberi review kommentenkénti javító commitokkal → elfogadás. A PR-méretkorlát túllépése szemantikus jelzés, nem blokkol.
- `agent` módú task PR-t a story-felelős, `pár` módút másik fejlesztő fogad el.
- A **story-gyűjtőbranch** → `develop` merge mechanikus kapukkal, soronkénti újbóli review nélkül történik.
- A **release** a `develop` → `main` merge; release branch nincs. A release igény szerint, a **release-PR**-rel indul, csak zöld **staging** regresszió mellett; a fast-forward merge miatt élesben ugyanaz a commit és image fut, mint a stagingen. A hotfix a `main`-ből indul, és a `main`-re és a `develop`-ra is visszakerül.
- Minden **tesztkörnyezet** az **arany tesztadat** aktuális verziójából klónoz; a **tesztadat-delta** gitben mergelődik, és a story merge-kapuja az arany újraépítésével ellenőrzi.
- A **tesztadat-delta** alkalmazása blokkol, ha az érintett rekord aktuális állapota eltér az elvárt kiinduló állapottól; a tesztelő vagy a BA kézzel oldja fel az ütközést, majd az ellenőrzés újrafut.
- A **DS-komponensnek** nincs külön verziószáma; változása a termékrepó PR-ja.
- A **design system** kódja kanonikus; a fejlesztői változás merge után visszaszinkronizálódik a Claude Designba, a designer változása **design-PR**-ként érkezik.
- A **DS-komponens** **komponensimport** után fejleszthető; utána a designer és a fejlesztés is módosíthatja, és a Claude Designnak továbbra is használnia kell tudni.
- Új domainnél vagy nagyon nagy epicnél **felfedező event storming** indul, egyébként agent-vázlat, **AI-szakértői** kritika és **hotspot-workshop** készíti a **folyamatmodellt**.
- Az **üzleti igény** akkor `Pontosítva`, ha minden kötelező szakasza kitöltött, és minden nyitott kérdés megválaszolt vagy **elhalasztott kérdés**.
- Minden kapu **kétszintű kapu**.
- A technikai specifikáció taskonként csak az **eszközt** jelöli; a skillt, az **arany példát**, a **generátort** és a lépéssorrendet a **fejlesztési útmutató** adja.
- A **fejlesztési útmutató** lépései: kontextus (tervezési eltérésnél megállás) → eszköz → váz → teszt először → implementáció → helyi kapuk → agentes előreview → PR.
- Backend use case-nél és AC-alapú e2e-tesztnél a teszt először kötelező, a piros állapot ellenőrzésével; képernyő- és komponensimportnál a design-pillanatképpel való vizuális összevetés az ellenőrzés.
- Gépileg ellenőrizhető szabály CI-ban blokkol; döntést igénylő minta **eszközskillben**, mechanikus váz **generátorban** él.
- Az alapértelmezett **végrehajtási mód** `agent`; migrációs, biztonsági, új architektúrát bevezető vagy spike-ban bizonytalannak talált task `pár`, a story-felelős döntése szerint.
- Az **AC-azonosító** nem számozódik át és nem használható újra; az azonosító explicit szöveges címke, nem markdown-listaszám.
- Beszúrt feltétel az előző elem utáni `-xN` azonosítót kapja; módosításkor az eredeti szöveg áthúzva, dátummal megmarad, az új változat a következő betűt kapja; visszavont feltétel áthúzva, `Visszavonva <dátum>` jelöléssel marad.
- Módosítás vagy visszavonás után a régi azonosítóra mutató teszt **gyanús tesztkapcsolat**.
- Egy story legfeljebb kb. öt **flow-lépést** tartalmaz; ennél nagyobb storyt a bontáskor tovább kell szedni.
- Minden **elfogadási feltételhez** és jóváhagyott **tesztforgatókönyvhöz** címkézett automata teszt tartozik; enélkül a story nem léphet `Tesztelés alatt` állapotba.
- **Hotspotot** AI is nyithat, de csak ember zárhatja le.
- A Software Design Level event storming eredménye az **architektúraterv** része, nem a tervezési téré.
- A **termékrepó** a **tervezési másolatot** soha nem módosítja; azt csak a **tervezési szinkron** frissíti.
- Minden **technikai artefaktum** verzióval hivatkozik a **tervezési másolatra**.
- **Tervezési eltérés** esetén az érintett taskok megállnak, és a PR csak **tervmegerősítés** után mergelhető.
- `Elfogadva` vagy `Kiadva` story nem nyílik újra; a későbbi változás új story.
- Másik **story** integrálása nem érvényteleníti az üzleti elfogadást; az együttműködést integrációs és regressziós ellenőrzés védi. A story saját elfogadott üzleti tartalmának változása új üzleti elfogadást igényel; `Elfogadva` vagy `Kiadva` story esetén ehhez új story készül.
- A **release** regressziós eredménye a kiadandó összeállításra érvényes; korábbi összeállítás sikeres ellenőrzése nem helyettesíti ezt.

## Kétértelműségek

- A „projekt” egyszerre jelölte a tervezési teret, a termékrepót és a Claude Desktop projektet; ezek külön fogalmak.
- A „business repó” a **tervezési tér**, a „codebase repó” a **termékrepó**.
- A „feature” és az „epic” ugyanazt a tervezési egységet jelölte; a kanonikus név az **epic**.
- A „tech spec” és a „technikai terv” ugyanaz: **technikai specifikáció**.
