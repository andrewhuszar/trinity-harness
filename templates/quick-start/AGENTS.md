# Útmutató agenteknek

Ez a fájl a repository egészére érvényes. A fejlesztési folyamatot a [`docs/development-workflow.md`](docs/development-workflow.md) írja le. Ellentmondás esetén a story és a felhasználó aktuális utasítása az elsődleges.

## Munkafolyamat

1. Fejlesztés előtt olvasd el a kapcsolódó story teljes tartalmát és a workflow-t.
2. Ha a cél, a scope vagy egy lényegi döntés nem egyértelmű, a workflow szerinti rövid `A`, `B`, `C` opciókkal kérj pontosítást. Bizonytalan feltételezést ne rögzíts követelményként.
3. A megvalósítás kezdetén állítsd a storyt `Folyamatban` állapotba a `plan/stories/README.md` fájlban.
4. A story megvalósítási tervét kövesd. Új, önálló célt ne adj hozzá menet közben; ahhoz készüljön külön story.
5. Csak sikeres, releváns ellenőrzések után jelöld készre a tervpontokat és a storyt.
6. A végső összefoglaló nevezze meg a story azonosítóját.

## Toolchain és parancsok

<!-- Töltsd ki: runtime és package manager verziója, telepítés, fejlesztési mód, teszt, typecheck, build, lint. -->

- Telepítés: `…`
- Fejlesztési mód: `…`
- Ellenőrzés: `…`

## Repository-szerkezet

<!-- Töltsd ki: a fő könyvtárak és szerepük, valamint a függési határok. -->

## Ellenőrzés és scope

- Minden módosítás után futtasd a releváns ellenőrzéseket.
- Ne javíts a storyhoz nem kapcsolódó kódot ugyanabban a változásban.
- Ne konfigurálj előre olyan könyvtárat, amelyet az aktuális story csak dependencyként kér.

## Dokumentáció és commit

- A storyk és a projekt-dokumentumok magyarul, helyes ékezetekkel készülnek. A kódazonosítók angolul maradnak.
- A dokumentáció az aktuális működést írja le jelen időben; fejlesztési napló és elvetett alternatíva nem kerül bele. A döntési indoklás ADR-be (`docs/adr/`), a feladat és az ellenőrzési eredmény storyba kerül.

```text
type(scope): rövid leírás

* opcionális részlet

Refs: <PREFIX>-001
```

A subject ne tartalmazza a story azonosítóját; az kizárólag a `Refs:` sorba kerüljön.
