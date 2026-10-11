# Külön tervezési tér, story-másolat és artefaktum-határ

Az üzleti artefaktumok (domain, epic, üzleti igény, folyamatmodell, funkcionális specifikáció, story) a termékrepótól külön git repóban, a tervezési térben élnek, hogy a BA a kód nélkül, tiszta üzleti struktúrában dolgozhasson. A technikai artefaktumok (technikai specifikáció az architektúratervvel, ADR, task, spike, PR-sorrend) a termékrepóban maradnak, a kód mellett. Az üzleti artefaktumok (domain, epic, folyamatmodell, story) minden elfogadott változása automatikusan PR-ként kerül a termékrepóba csak olvasható tervezési másolatként, onnan pedig az érintett folyamatban lévő story-gyűjtőbranchekre; a termékrepó a másolatot nem módosítja, a technikai artefaktumok verzióval hivatkoznak rá. A story állapotát, a fejlesztési állapotot is beleértve, kizárólag a tervezési tér tárolja.

## Mérlegelt lehetőségek

- Közös repó branch-szintű hozzáféréssel: egyszerűbb nyomkövetés, de a BA-munka a kódhistoryval keveredik, és a hozzáférés-kezelés a git-szolgáltató képességein múlik.
- Git submodule: a fejlesztő agent helyben látja a storyt, de a submodule-kezelés embernek és agentnek is hibalehetőség.
- Befagyasztott story, változás csak új storyként: egyszerűbb, de a fejlesztés közbeni pontosítás is új story-t igényelne.

## Következmények

- A fejlesztő agent és a review a tervezési másolatot helyben, verziózottan látja.
- Az üzleti artefaktum változása futó fejlesztés közben is megérkezik a story-gyűjtőbranchre; a hivatkozott verziótól eltérő másolat esetén az érintett taskok megállnak, és a PR csak tervmegerősítés után mergelhető.
