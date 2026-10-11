# Story-gyűjtőbranch és stacked task PR-ok

Minden story saját gyűjtőbranchet kap; a taskok onnan indulnak, és egyenként, emberi review után kerülnek vissza bele, így a gyűjtőben csak átnézett kód van, és a story atomikusan, feature flag nélkül érkezik a `develop` branchre. Ha egy task egy még nem mergelt taskra épül, stacked PR-ként a függőség branchéből indul: a fejlesztés és a review nem vár, csak a merge sorrendje kötött; a harness a függőség változásakor automatikusan restackel, mergelésekor átállítja a célt és kaszkádszerűen mergel. A gyűjtő → `develop` merge mechanikus kapukkal történik, újbóli soronkénti review nélkül.

## Mérlegelt lehetőségek

- Task PR-ok közvetlenül a `develop`-ra: félkész story feature flaget igényel, és nincs storyszintű integrációs és tesztelési pont.
- Nem mergelt task kézi behúzása: a függő PR diffje a másik task kódját is tartalmazza, és a review-változások után elavul.
- Task-commitok automatikus merge-e a gyűjtőbe: megszünteti a review-kaput, és a végén egy nagy story-PR-t kellene átnézni.

## Következmények

- A technikai specifikáció PR-sorrendje határozza meg a stackeket; ahol lehet, a szerződés külön, előre mergelhető taskba kerül.
- A harness a `develop` branchet rendszeresen behúzza a gyűjtőkbe, és ütközéskor jelez.
