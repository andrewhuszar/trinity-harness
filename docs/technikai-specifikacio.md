# Agent harness – technikai specifikáció

Állapot: specifikáció. A leírt képességek tervezettek; az MVP vágását a [MVP és Enabler backlog](#mvp-és-enabler-backlog) fejezet rögzíti. Az üzleti folyamatot az [üzleti specifikáció](./uzleti-specifikacio.md), a fogalmakat a [CONTEXT.md](../CONTEXT.md), a döntéseket az [ADR-ek](./adr/) írják le.

## Architektúra

```
GitHub (tervezési tér)          Azure DevOps (termékrepó)
        │ webhook                        │ service hook
        ▼                                ▼
┌──────────────── Harness-szolgáltatás (Azure Container Apps) ────────────────┐
│  Mag: állapotgép · kapuk · tervezési szinkron · eltérésdetektálás ·          │
│       stacklogika · release · tesztadat-build · tartós saga-folyamatok       │
│  Adapterek: RepoHost(GitHub) · RepoHost(AzureDevOps) · CI · Environment ·    │
│             AgentRunner · DesignSync · Notification                          │
│  Postgres: eseménynapló · munkasor · sagaállapot                             │
└──────────────────────────────────────────────────────────────────────────────┘
        │ Container Apps Jobs                    │
        ▼                                        ▼
  Agent-futtatások (feldolgozó, fejlesztő,   Tesztkörnyezetek (Container Apps +
  review, AI-szakértő)                       PostgreSQL Flexible Server klónok)
```

- **Mag:** platformfüggetlen. Az állapotot és minden átmenetet eseményként naplózza. A több rendszert érintő műveletek (szinkron-PR és állapot-visszaírás, environment-létrehozás és -lebontás, kaszkádmerge) tartós, újrapróbálható, kompenzálható sagaként futnak.
- **RepoHost:** branch, commit, PR létrehozása és célváltása, merge (fast-forward is), komment, címke, státuszellenőrzés, webhookfogadás. Implementációk: GitHub és Azure DevOps REST.
- **CI:** a pipeline-futások indítása és eredményük fogadása (GitHub Actions, Azure Pipelines).
- **Environment:** tesztkörnyezet létrehozása, frissítése, leállítása és törlése; adatbázisklónozás.
- **AgentRunner:** agent-munkamenet indítása rövid életű konténerben (Claude Agent SDK vagy Claude Code headless) adott repóval, branch-csel, skillkészlettel és utasítással; az eredmény és a napló visszaküldése.
- **DesignSync:** a termékrepó design systemjének komponensenkénti szinkronja a Claude Design design-system projektjébe, renderellenőrzéssel.
- **Notification:** visszajelzés a BA Claude-munkamenetébe, az online felületre és a PR-kommentekbe.

A harness-szolgáltatás a Trinity backend mintáira épülhet (NestJS, CQRS, tartós saga, portok és adapterek).

## Repók és elrendezés

### Terjesztés

| Repó | Tartalom | Terjesztés |
|---|---|---|
| `harness` | Specifikáció, fogalomtár, ADR-ek; a `harness-ba` és a `harness-dev` Claude Code plugin; a harness-szolgáltatás | Plugin-marketplace, szerepenként globálisan telepítve |
| `trinity` | A framework csomagjai, a framework-specifikus eszközskillek, generátorok és arany példák | A frameworkkel együtt; a termékrepó sablonmásolatból indul |
| Tervezési tér | Üzleti artefaktumok és harness-konfiguráció | — |
| Termékrepó | Termékkód, technikai artefaktumok és harness-konfiguráció | — |

A projekt csak a harness-konfigurációt tartalmazza a `.harness/config.json` fájlban (séma- és struktúraverzió, szerep, projektnév, story-prefix, kapcsolódó repó, workflow, a létrehozó plugin verziója, döntési jogkörök, támogatási kapcsolat); a skilleket, a parancsokat és a hookokat a pluginok adják. A konfigurációt a `/harness-ba:init`, illetve a `/harness-dev:init` hozza létre, és a pluginfrissítés nem módosítja.

A döntési jogkörök a konfigurációban szerepelnek: a PO és helyettese, valamint az epicenkénti delegációk. A kapuk ebből döntik el, hogy az átmenetet kérő szereplő jogosult-e rá; ha nem, a harness a döntéshozónak jelzi.

```json
{
  "roles": {
    "productOwner": "kovacs.anna",
    "productOwnerDeputy": "nagy.peter",
    "delegations": [{ "epic": "EP-001", "to": "szabo.eva", "decisions": ["Pontosítva", "story-elfogadás"] }]
  },
  "support": "harness-support csatorna"
}
```

### Tervezési tér (GitHub)

```
domains/<domain>/
  context.md                      # üzleti szótár, határok (Big Picture)
  event-storming/                 # workshop-anyagok és feldolgozott eredmény
  kozos-szabalyok.md              # jogosultságok, adatfogalmak, külső rendszerkapcsolatok
epics/<EPIC-ID>/
  epic.md                         # állapot, sávstátuszok, bevezetési felelős, hivatkozások
  uzleti-igeny.md                 # forrásjelölt állítások, jelenlegi és kívánt folyamat
  folyamatmodell.md               # azonosítós folyamatelemek
  minosegi-elvarasok.md           # az epic mérhető minőségi elvárásai
  funkcionalis-specifikacio.md
  dontesnaplo.md                  # döntések, verzióval, indokkal és fennmaradó kockázattal
  design/<SCR-ID>@<n>/            # design-pillanatkép: képernyőkód, állapotok, képernyőképek, meta.yaml
  stories/<STORY-ID>.md           # cél, elfogadási feltételek, állapot
  test-scenarios/<STORY-ID>.md    # jóváhagyott tesztforgatókönyvek
.harness/config.json              # harness-konfiguráció
AGENTS.md                         # projektinstrukciók; a skilleket a harness-ba plugin adja
```

- A `main` védett, közvetlen push nincs. A változás draft branchről (`draft/<epic>/<ba>`) publikálási PR-ral érkezik.
- Az állapotmezőket csak a harness identitása írhatja; a determinisztikus kapu elutasítja a más szerzőtől érkező állapotváltozást.

### Termékrepó (Azure DevOps)

```
.harness/config.json              # harness-konfiguráció
planning/                         # tervezési másolatok, csak a harness írja
  domains/… epics/…               # a tervezési tér tükre, forrás-SHA-val
docs/epics/<EPIC-ID>/
  technikai-specifikacio.md       # architektúraterv, taskok, eszközök, végrehajtási mód, PR-sorrend
docs/adr/
e2e/                              # Playwright-tesztek AC-címkékkel
test-data/deltas/                 # tesztadat-delták
```

- A `planning/` útvonalat branch policy és a CI védi: csak a harness identitása módosíthatja.
- Branchek: `main` (production), `develop` (integráció), `story/<STORY-ID>` (story-gyűjtő), `task/<STORY-ID>/<TASK-ID>`, `hotfix/<verzió>`.

## Azonosítók és verziók

| Elem | Formátum | Egyediség |
|---|---|---|
| Epic | `EP-<n>` | tervezési tér |
| Story | `<PROJEKT>-<n>`, például `TRN-045` | tervezési tér |
| Task | `<STORY-ID>-T<n>` | story |
| Folyamatelem | `<DOMAIN>:<TÍPUS>-<n>`, például `DOC:POL-4`; típus: `ACT`, `CMD`, `EVT`, `POL`, `RM`, `RULE`, `EXT` | domain |
| Közös szabály | `<DOMAIN>:PERM-<n>` (jogosultság), `<DOMAIN>:DATA-<n>` (adatfogalom); a külső rendszerkapcsolat a folyamatelem `EXT` azonosítóját használja | domain |
| Minőségi elvárás | `<EPIC-ID>:NFR-<n>` | epic |
| Döntés | `<EPIC-ID>:DEC-<n>` | epic |
| Képernyőverzió | `SCR-<n>@<verzió>`, a forráskoncepcióval (`← C1`) | tervezési tér |
| Elfogadási feltétel | `<STORY-ID>#<azonosító>`, például `TRN-045#2.1-x1`, `TRN-045#2.2a` | story |
| Artefaktumverzió | a tervezési tér commit-SHA-ja, amelyben az artefaktum utoljára változott | — |

- Minden tervezési másolat front matterben hordozza a forrását: `source: <repó>@<sha>:<útvonal>`.
- Minden technikai artefaktum front matterben hivatkozik a felhasznált verziókra:

```yaml
references:
  epic: EP-012@4f2c9e1
  process-model: EP-012@4f2c9e1
  functional-spec: EP-012@9ab03d2
  screens: [SCR-12@3, SCR-13@1]
  stories: [TRN-045@9ab03d2]
```

- **AC-azonosító szabályai:** felsorolásjeles sor félkövér szöveges címkével; pont: hierarchia; `-xN`: beszúrt testvér; betű: minden szövegváltozás; nincs átszámozás és újrafelhasználás. A determinisztikus kapu az előző story-verzióval összevetve ellenőrzi. Az ellenőrzési mód a sor végén: alapértelmezés e2e, egyébként `[integrációs]`, `[kézi]` vagy `[monitorozás]`.
- **Forrásjelölés:** az üzleti igény állításai `[megerősített: <forrás>]`, `[feltételezés]` vagy `[agentjavaslat]` jelölést kapnak; a scope-ot vagy megvalósíthatóságot eldöntő nyitott kérdés `[scope]` jelölést.
- **Blokkolás:** az epic, story és task front mattere `blocked_reason`, `blocked_owner` és `blocked_until` mezőt kaphat; a jelző nem állapot, és bármely állapotban beállítható.

## Tervezési szinkron és eltérésdetektálás

1. Egy publikálási PR mergelődik a tervezési tér `main`-jére (GitHub webhook).
2. A harness meghatározza a változott üzleti artefaktumokat, és a termékrepóban PR-t nyit a `develop`-ra a frissített `planning/` másolatokkal. Ez a PR automatikusan mergelődik.
3. A harness az érintett story-gyűjtőbranchekre is mergeli a másolatot.
4. Eltérésdetektálás minden érintett branchen: ha egy technikai artefaktum `references` verziója régebbi, mint a branch másolatának `source` SHA-ja, a harness:
   - az érintett taskokat megállítja, és a fejlesztő agent nem indul rájuk;
   - eltéréskommentet tesz a gyűjtőbranch nyitott PR-jaira az artefaktum diffjével;
   - beállít egy kötelező státuszellenőrzést (`planning-drift`), amely a tervmegerősítésig, vagyis a `references` frissítéséig blokkolja a mergelést.
5. Képernyőverzió-emelésnél a változás típusa szerint:
   - **megjelenítési pontosítás:** nem állít meg taskot, csak a `screen-version` ellenőrzés követeli meg, hogy a view a legfrissebb képernyőverzióra hivatkozzon;
   - **viselkedési változás:** a 4. pont szerint jár el.
6. A termékrepó eseményei (task branch létrehozva, PR nyitva, mergelve, pipeline-eredmény, telepítés) a tervezési térbe írt állapotváltozást váltanak ki; ezt csak a harness identitása commitolja. A story az első task branch létrehozásakor lép `Fejlesztés alatt` állapotba.

**Hatáslista publikálás előtt:** a feldolgozó agent a draft branch diffjéből meghatározza az érintett storykat, közös szabályokat, minőségi elvárásokat, képernyőket és teszteket (a hivatkozási gráf és az AC-címkék alapján), valamint a prioritásra és vállalásra gyakorolt hatást. Scope-változás esetén a publikálás a PO jóváhagyására vár.

## Kapuk

A determinisztikus ellenőrzések CI-ban és a harness magjában futnak, és blokkolnak. A szemantikus ellenőrzést a feldolgozó agent végzi, és javaslatot ad.

| Átmenet | Determinisztikus | Szemantikus |
|---|---|---|
| Beküldés (minden push) | Struktúra, kötelező szakaszok, front matter, hivatkozott azonosítók létezése, AC-azonosító szabályai, forrásjelölés, állapotmezőt nem a harness írt | Szótár-ütközés, ellentmondás, kimaradt hibaút, homályos megfogalmazás |
| Publikálás | Hatáslista elkészült; scope-változásnál PO-jóváhagyás | A hatás teljessége |
| `Vázlat` → `Pontosítva` | Az üzleti igény minden kötelező szakasza kitöltött, a jelenlegi és a kívánt folyamattal; minden állítás forrásjelölt, és nincs `[agentjavaslat]`; nincs megválaszolatlan kérdés; az elhalasztott kérdésnek van felelőse, határideje és feloldási pontja; `[scope]` kérdés nincs elhalasztva; a folyamatelemek azonosítósak; nincs nyitott hotspot; UI-t érintő epicnél a designer reviewja rögzítve; a léptető a konfiguráció szerint jogosult | Ütközés meglévő epickel vagy folyamatmodellel; megalapozatlan feltételezés |
| `Tervezés alatt` → `Bontva` | A funkcionális specifikáció csak létező folyamatelemekre, közös szabályokra és képernyőverziókra hivatkozik; UI-t érintő epicnél van elfogadott design, egyébként a design-sáv „nem szükséges”; kockázatosnak jelölt felhasználói folyamatnál a használhatósági validáció eredménye rögzítve; a tervezési egyeztetés döntésnapló-bejegyzése megvan; tervmegerősítési kapu zöld; minden storynak van legalább egy taskja és jóváhagyott tesztforgatókönyve | A funkcionális specifikáció és a design egyezése; a storybontás üzleti eredmény szerinti szeletelése; kb. öt flow-lépés fölötti story; üzleti eredmény nélküli backend- vagy frontend-story; hiányzó állapot az átadási csomagban |
| Tervmegerősítés | Minden task pontosan egy storyhoz tartozik; a függőségi gráf aciklikus; minden tasknak van eszköze, végrehajtási módja és becsült mérete; nincs nyitott spike | AC-lefedettség; ADR- és AGENTS.md-megfelelés; contract-first bontás; migrációs kockázat; PR-méret |
| Task PR merge | Typecheck, lint, tesztek, build, architektúra- és importhatár-tesztek, UUID-kulcsok, `planning-drift`, `screen-version`, emberi elfogadás | Agentes előreview; PR-méret jelzés (nem blokkol) |
| `Fejlesztés alatt` → `Tesztelés alatt` | Minden task mergelve; a gyűjtő pipeline-ja zöld; minden automata ellenőrzési módú (e2e, integrációs) érvényes AC-hez és jóváhagyott forgatókönyvhöz van címkézett teszt; nincs gyanús tesztkapcsolat | — |
| `Tesztelés alatt` → `Fejlesztés alatt` | Sikertelen elfogadás; a talált hibákból javító task készül | — |
| Gyűjtő → `develop` | A `develop` behúzva, a pipeline zöld; az arany tesztadat a story deltájával újraépül; tesztelői elfogadás a `[kézi]` feltételek rögzített eredményével; UI-t érintő storynál designer-review működést vagy hozzáférhetőséget rontó nyitott eltérés nélkül; BA-elfogadás a vizsgált verzióval, eredménnyel és nyitott hibákkal | — |
| Epic lezárása | `Kiadva`: legalább egy story kiadva, a többi kiadva vagy jegelve; `Lezárva`: minden story jegelve, PO-döntéssel | — |
| Release-PR | A kiadandó commit és image staging regressziója zöld; fast-forward lehetséges | — |

## Branch- és PR-automatizálás

- **Story-gyűjtőbranch:** a story `Fejlesztésre kész` állapotába lépéskor a harness létrehozza a `develop`-ból.
- **Task branch:** a gyűjtőből indul, vagy stack esetén a függőség task branchéből.
- **Stacked PR:** a függő task PR célja a függőség branche. A harness:
  - a függőség minden új commitjánál rebase-eli a függő branchet (restack); ütközéskor a fejlesztő agentet indítja feloldásra;
  - a függőség mergelésekor a függő PR célját a gyűjtőre állítja;
  - ha a függő PR is elfogadott, kaszkádszerűen mergel;
  - a review-sorban előre veszi azokat a PR-okat, amelyekre stack épül.
- **Develop-szinkron:** a harness a `develop` minden változásakor behúzza azt a nyitott gyűjtőkbe, és ütközéskor jelez. A frissített gyűjtőn újrafut a pipeline az integrációs és regressziós ellenőrzésekkel. Másik story integrálása önmagában nem érvényteleníti a tesztelői és BA-elfogadást; a story saját elfogadott üzleti tartalmának változása új üzleti elfogadást igényel.
- **Merge-stratégia:** a task PR squash merge-dzsel kerül a gyűjtőbe; a gyűjtő merge committal kerül a `develop`-ra, így a taskok követhetők; a release-PR fast-forward.
- Azure DevOps oldalon a célváltást, a restacket, a kaszkádmerge-et és a PR-kommentre reagáló agentindítást a RepoHost(AzureDevOps) adapter valósítja meg.

## Agentfejlesztés

### Indítás

A harness egy taskot akkor indít, ha `Tervezve` állapotú, a függőségei mergelve vannak vagy stackelhetők, és nincs tervezési eltérésben.

- `agent` módú task: az AgentRunner távoli munkamenetet indít a task branchén.
- `pár` módú task: a story-felelős a saját Claude Code-jában veszi fel a `/next` paranccsal.

A PR-kommentekre ugyanaz a fejlesztő agent reagál, kommentenként külön committal.

### Fejlesztési útmutató

A fejlesztő agent fő skillje. A technikai specifikáció taskonként csak az eszközt jelöli; az útmutató az eszköz alapján választja ki a többit.

1. **Kontextus:** a story-másolat, a task AC-hivatkozásai, a technikai specifikáció szakasza, a képernyőverzió és az érintett ADR-ek. Tervezési eltérés esetén megállás.
2. **Eszköz:** az eszközskill és az arany példa kiválasztása.
3. **Váz:** a generátor futtatása.
4. **Teszt először:** a backend use case-eknél (command, query, saga step, flow) és az AC-alapú e2e-teszteknél kötelező, a piros állapot ellenőrzésével.
5. **Implementáció:** az arany példa szerint, amíg a tesztek zöldek.
6. **Helyi kapuk:** typecheck, lint, tesztek, build.
7. **Agentes előreview** és a megerősített találatok javítása.
8. **PR** review-magyarázattal; a task `Elfogadásra vár` állapotba lép.

Képernyő- és komponensimportnál a 4. lépés helyett vizuális összevetés történik a design-pillanatképpel, azonos fixture-adattal.

### Eszközskillek és arany példák

Az eszközskillek és a generátorok framework-specifikusak, ezért a Trinity repóban élnek, és a frameworkkel együtt kerülnek a termékrepóba; a fejlesztési útmutató a `harness-dev` pluginból indítja őket.

| Eszköz | Arany példa a Trinity frameworkben |
|---|---|
| Command, query | `packages/modules/users/backend` |
| Aggregate flow | Felhasználómódosítás flow-val (TRN-025) |
| Saga és saga step | Dokumentumfeltöltési saga (TRN-028), user-előfizetés saga (TRN-019) |
| Aggregate session | Dokumentumfeltöltés (TRN-029) |
| Contract és kanonikus modell | `packages/modules/users/contract` |
| Web view és data hook | `packages/modules/users/frontend/web` (ADR-0011) |
| Képernyőimport | Kijelölendő az első képernyőimport után |
| Komponensimport | `@trinity/ui` |
| E2E-teszt AC-ból | Kijelölendő az MVP-epic első storyjában |

### Kikényszerítés

- Gépileg ellenőrizhető szabály CI-ban blokkol: importhatárok és rétegfüggések, architektúratesztek, UUID-kulcsok.
- Döntést igénylő minta eszközskillben él.
- Mechanikus váz generátorban él.
- Az AGENTS.md elveket és hivatkozásokat tartalmaz.

## Review

1. A CI-kapuk lefutnak.
2. Agentes előreview (code-review skill); a fejlesztő agent javít.
3. Review-magyarázat PR-kommentben (review-explain): belépési pontok, flow-k, üzleti hatás, kockázatok, tesztrések, olvasási sorrend, megmaradt észrevételek a kiváltó committal.
4. Emberi review: a kommentekre kommentenként javító commit készül.
5. Elfogadás négy szem elve szerint: `agent` módú taskot a story-felelős, `pár` módút másik fejlesztő fogad el. AC-címkés tesztet tartalmazó PR-t a tesztelő is tartalmilag reviewz: a teszt ténylegesen a hivatkozott elvárást igazolja-e.
6. A gyanús tesztkapcsolatot a story-felelős zárja le a tesztet módosító vagy átcímkéző PR-ban; a bizonyíték a teszt diffje.

Kockázatalapú automatikus elfogadás nincs; mérési adatok alapján később vezethető be.

## Tesztelés

### Tesztek és lefedettség

- Az e2e-tesztek Playwright-tesztek. Minden teszt címkézi a lefedett AC-azonosítót vagy forgatókönyvet: `@TRN-045#2.2a`.
- Az integrációs tesztek task-szinten, a task PR részeként készülnek.
- **Lefedettségi kapu:** a story minden érvényes (nem áthúzott), automata ellenőrzési módú AC-jéhez és jóváhagyott forgatókönyvéhez legalább egy címkézett teszt tartozik. A `[kézi]` feltételt a tesztelő rögzített eredménye, a `[monitorozás]` feltételt a megnevezett éles mutató igazolja. Módosított vagy visszavont azonosítóra mutató címke gyanús tesztkapcsolat, amely blokkol.
- **Nyomkövetési nézet:** a harness storynként összeállítja az igény → folyamatelem és közös szabály → AC → forgatókönyv → teszt és eredmény láncot a hivatkozásokból és a címkékből.

### Tesztkörnyezet (Azure)

- **Futtatás:** egy közös Azure Container Apps környezet. Story-nként `web` és `api` Container App scale-to-zero beállítással, a gyűjtőbranch CI-ban buildelt image-éből.
- **Elérés:** wildcard-domain (`<story-id>.test.<domain>`), SSO vagy basic auth mögött.
- **Azonos origin:** a webalkalmazás relatív `/api` útvonalat használ, amelyet az ingress az API-hoz irányít. Így egy image minden környezetben futtatható, és a `NEXT_PUBLIC_API_URL` buildidejű beégetése nem köti környezethez.
- **Adatbázis:** közös Azure Database for PostgreSQL Flexible Server. Story-nként `CREATE DATABASE <story> TEMPLATE golden_<verzió>`, majd `prisma migrate deploy`.
- **Fájlok:** story-nkénti Blob-konténer vagy prefix.
- **Életciklus:**
  - `Tesztelés alatt` → létrehozás;
  - push a gyűjtőre → frissítés;
  - merge vagy jegelés → lebontás és `DROP DATABASE`;
  - TTL-alapú takarítás.
- **Alternatíva nagy adatméretnél:** Neon branching Azure-integrációval. Az elérhetőséget és az árazást a bevezetés előtt ellenőrizni kell.

### Arany tesztadat és tesztadat-delta

- Az arany tesztadat build-termék. `golden_<n+1>` = `golden_<n>`, majd merge-sorrendben minden `develop`-ra került story migrációi, utána a story deltája.
- A tesztadat-build verziója a `develop` commitja; a release-tag rögzíti a hozzá tartozó arany verziót.
- **Delta előállítása:** a tesztelés végén a harness elsődleges kulcs szerint, táblánként összeveti a tesztkörnyezet adatbázisát az alap arannyal. A tesztelő vagy a BA kiválogatja a megtartandó rekordokat, és a delta task PR-ként kerül a gyűjtőbe.
- **Delta tartalma:** csak a kanonikus modellekhez tartozó üzleti táblák. A technikai táblák (saga run, outbox, upload session) kimaradnak; a modellmetaadat határozza meg, melyek ezek.
- **Formátum:**

```json
{
  "story": "TRN-045",
  "schemaVersion": "20261101093000_add_document_category",
  "tables": {
    "Document": {
      "before": {
        "0b9c…": null,
        "5e1a…": { "id": "5e1a…", "title": "Lejárt szerződés", "status": "UPLOADED" }
      },
      "upsert": [{ "id": "0b9c…", "title": "Bérleti szerződés", "status": "UPLOADED" }],
      "delete": ["5e1a…"]
    }
  }
}
```

- Minden kulcs UUID; ezt CI-ellenőrzés kényszeríti ki.
- A `before` minden érintett rekord elvárt kiinduló állapotát rögzíti a delta sémaverzióján; új rekordnál `null` jelzi az elvárt hiányt. Az alkalmazás ezt összeveti az aktuális arannyal. Eltéréskor a delta nem alkalmazható, a story merge-kapuja blokkol; a tesztelő vagy a BA kézzel feloldja a konfliktust, és a döntés szerint frissíti a deltát és az elvárt kiinduló állapotot. Ezután az arany újraépítése és a delta ellenőrzése újrafut. Az `upsert` nem írhat felül ellenőrizetlenül közben módosult rekordot.
- Ha egy migráció a meglévő tesztadaton elbukik, a gyűjtő → `develop` kapu blokkol. Ha a `develop` a story tesztelése után változott, a merge előtt a harness újraépíti az aranyat, és újrajátssza a deltát.

## Release és környezetek

- **Staging:** a `develop` minden merge-ét automatikusan telepíti, a teljes e2e regressziós készlettel, a legfrissebb arany tesztadaton.
- **Release:**
  1. Az online felületen kért release-re a harness release-PR-t nyit `develop` → `main` irányba. A generált release note tartalmazza a storykat, a képernyőverziókat, a migrációkat és az arany tesztadat verzióját.
  2. A harness rögzíti a kiadandó commitot és image-et, és ezek sikeres staging regressziója mellett a release-PR fast-forward módon mergelődik. A release céljának változásakor az új összeállítás sikeres regressziós eredménye szükséges; korábbi commit zöld eredménye nem használható fel.
  3. A harness `vX.Y.Z` taget tesz a `main`-re, és a stagingen futott image-et telepíti productionbe; az image nem épül újra. Az MVP-ben, az azonos origin bevezetéséig, a webalkalmazás image-e környezetenként a release-commitból épül; a commit azonos, az image nem.
  4. Az érintett storykat `Kiadva` állapotba lépteti.
- **Hotfix:** `hotfix/<verzió>` a `main`-ből, patch-tag, majd merge a `main`-re és a `develop`-ra.

## Pilotmérés

A pilot mérőszámai a harness eseménynaplójából származnak: az állapotátmenetek és a döntésnapló időbélyegeiből az átfutási és döntési idő, a visszalépésekből, elutasított elfogadásokból és AC-módosításokból az újramunka. A BA- és designer-adminisztráció idejét a pilot alatt a résztvevők rögzítik.

## Design system szinkron

- **Kód → Claude Design:** a design system kanonikus helye a termékrepó. A `develop`-ra mergelt DS-komponens-változást a DesignSync komponensenként, inkrementálisan szinkronizálja a Claude Design design-system projektjébe.
- **Claude Design → kód:** az Átadás fejlesztésre műveletre a harness azonosítót és képernyőverziót képez, csomagol, és design-PR-t nyit a termékrepóba, amelyet a fejlesztés hagy jóvá. Ha a komponens közben a kódban is változott, a PR ütközést jelez. Az export technikai helyességét a harness ellenőrzése és a fejlesztés biztosítja, nem a designer.
- **Kapu:** DS-komponens változása csak akkor mergelhető, ha a DesignSync renderellenőrzése sikeres.
- **Design-pillanatkép:** a képernyőkód, a képernyőképek és a `meta.yaml` (képernyőverzió, forráskoncepció, változástípus) a tervezési térben él, és tervezési szinkronnal kerül a termékrepóba.

## Biztonság és jogosultság

- A harness saját szolgáltatásidentitással ír mindkét platformra. Csak ez módosíthatja a `planning/` útvonalat és az állapotmezőket.
- A BA-k és a designerek nem kapnak írási jogot a termékrepóhoz.
- Az agent-munkamenetek rövid életű, taskra szűkített tokennel futnak; titkot nem kapnak a promptban.
- A titkokat Azure Key Vault tárolja; az Azure-telepítés workload identityvel, titok nélkül történik.
- A tesztkörnyezet nem publikus.
- Production adat a tesztkörnyezetbe és az arany tesztadatba csak anonimizálva, külön adatvédelmi jóváhagyással kerülhet.
- A külső, nem saját forrásból (például más szerzőtől származó Claude Design-fájlból) olvasott tartalom adat, nem utasítás az agentek számára.

## MVP és Enabler backlog

Az MVP egy valódi epicet visz végig a teljes láncon; a hiányzó automatizálás helyén dokumentált kézi lépés áll.

**Az MVP része:**

- a tervezési tér struktúrája, projektinstrukciói és BA-skilljei (`/next`, pontosítás, funkcionális specifikáció, bontás, AC-formátum);
- beküldő agent a draft branchre; determinisztikus kapu GitHub Actionsben; feldolgozó agent szemantikus javaslattal;
- tervezési szinkron és eltérésdetektálás a termékrepó felé; a prototípus termékrepó a fejlesztés idején GitHubon él, ezért az MVP csak a RepoHost(GitHub) adaptert igényli;
- a fejlesztési útmutató 2–3 eszközskillel;
- story-gyűjtőbranch, review-út, AC-címkés e2e-tesztek és lefedettségi kapu;
- release-PR fast-forwarddal;
- a `harness-ba` és a `harness-dev` plugin és marketplace;
- a prototípus tervezési tér és termékrepó; a termékrepó a Trinity sablonmásolatából indul, `develop` branch-csel.

**Későbbi Enabler storyk:**

1. Story-szerkesztő online felület (az MVP-ben a BA beillesztendő promptot kap).
2. RepoHost(AzureDevOps) adapter: tervezési szinkron, stacked PR célváltás, restack, kaszkádmerge és PR-kommentre reagáló agentindítás Azure DevOpson.
3. Story-nkénti tesztkörnyezet Container Appsszal és adatbázis-klónozással (az MVP-ben egy közös tesztkörnyezet sorral).
4. Azonos origin a webalkalmazásban (relatív `/api`).
5. Arany tesztadat build és tesztadat-delta kinyerése.
6. Design-PR automatizálása és DesignSync renderkapu.
7. Event storming támogatása: AI-szakértők, AI-projektspecialista, hotspotkezelés.
8. További eszközskillek, generátorok, valamint az arany példák kijelölése képernyő- és komponensimporthoz és e2e-teszthez.
9. A Trinity framework publikálása privát registrybe (`@trinity/*`) és az eszközskillek framework-pluginként való terjesztése.

## Nyitott kérdések

- A Claude Design képernyőexportjának pontos formátuma és automatizálhatósága.
- A PR-méret jelzési küszöbe (kiindulás: kb. 400 módosított sor generált fájlok és fixture-ök nélkül).
- A Neon Azure-integráció elérhetősége és árazása, ha a template-klónozás lassú.
- Az online felület technológiája, és hogy a Trinity frameworkjére épül-e.
