# Útmutató agenteknek

Ez a fájl a repository egészére érvényes. A fejlesztési folyamatot a [`docs/development-workflow.md`](docs/development-workflow.md), a harness működését az [üzleti](docs/uzleti-specifikacio.md) és a [technikai specifikáció](docs/technikai-specifikacio.md), a fogalmakat a [`CONTEXT.md`](CONTEXT.md), a döntéseket a [`docs/adr/`](docs/adr/) írja le. Ellentmondás esetén a story és a felhasználó aktuális utasítása az elsődleges.

## A repository szerepe

A `trinity-harness` a harness saját repója: a specifikáció, a fogalomtár és az ADR-ek, a `harness-ba` és a `harness-dev` Claude Code plugin, valamint később a harness-szolgáltatás. Termékkód, generált tervezési artefaktum és Trinity framework-skill nem kerül ide; a framework-skillek a `trinity` repóban, a kipróbálás eredményei a prototípus repókban élnek.

## Munkafolyamat

1. Fejlesztés előtt olvasd el a kapcsolódó story teljes tartalmát és a fenti dokumentumokat.
2. Ha a cél, a scope vagy egy lényegi döntés nem egyértelmű, a workflow szerinti rövid `A`, `B`, `C` opciókkal kérj pontosítást. Bizonytalan feltételezést ne rögzíts követelményként.
3. A megvalósítás kezdetén állítsd a storyt `Folyamatban` állapotba a `plan/stories/README.md` fájlban.
4. A story megvalósítási tervét kövesd. Új, önálló célt ne adj hozzá menet közben; ahhoz készüljön külön story.
5. Csak sikeres, releváns ellenőrzések után jelöld készre a tervpontokat és a storyt.
6. A végső összefoglaló nevezze meg a story azonosítóját.

A storyk azonosítója `HRN-<n>`. Az elfogadási feltételek a harness AC-formátumát követik: explicit szöveges azonosító, a pont hierarchiát, a `-xN` beszúrt testvért, a betű módosítást jelöl; az azonosító nem számozódik át és nem használható újra.

## Dokumentáció

- A storyk és a dokumentumok magyarul, helyes ékezetekkel készülnek. A kódazonosítók és a publikus technikai nevek angolul maradnak.
- A specifikáció a harness működését jelen időben, önállóan érthetően írja le. A még meg nem valósított képességet egyértelműen tervezettként jelöld.
- Fejlesztési naplót, beszélgetési előzményt, elvetett alternatívát a leírásba ne írj. A döntési indoklás ADR-be, a feladat és az ellenőrzési eredmény storyba kerül.
- Új vagy megváltozott fogalmat a `CONTEXT.md`-ben rögzíts; a kerülendő szinonimákat ott jelöld.
- Dokumentáció módosításakor a teljes érintett szakaszt igazítsd az aktuális állapothoz.

## Commit

```text
type(scope): rövid leírás

* opcionális részlet

Refs: HRN-001
```

A subject ne tartalmazza a story azonosítóját; az kizárólag a `Refs:` sorba kerüljön.
