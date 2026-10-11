# Verziózott arany tesztadat JSON-deltákból

A story-nkénti tesztkörnyezet egy verziózott arany adatbázisból klónoz. Az aranyat nem kézzel készített snapshot, hanem build adja: az előző arany, majd merge-sorrendben minden story saját migrációi és utána a story kurált tesztadat-deltája. A delta a tesztelés végén a tesztkörnyezet és az alap arany különbségéből készül, a tesztelő vagy a BA válogatja ki, JSON-ként a rögzítési sémaverzióval együtt gitben mergelődik, és csak az üzleti táblákat tartalmazza. Minden kulcs UUID; ez az új rekordok azonosítóütközésének esélyét csökkenti, de a meglévő rekordok párhuzamos módosítását nem oldja fel. A delta az érintett rekordok elvárt kiinduló állapotát is rögzíti, új rekordnál annak hiányát. Eltéréskor az alkalmazás blokkol, a konfliktust a tesztelő vagy a BA kézzel oldja fel, majd az ellenőrzés újrafut.

## Mérlegelt lehetőségek

- Közös alap tesztadat-csomag importja: olcsó, de kevésbé életszerű.
- Adatbázis-snapshotok merge-e: két elágazott adatbázisállapot nem egyesíthető megbízhatóan.
- Kézzel írt tesztadat-szkriptek: a kézi tesztelés során keletkező életszerű adat elveszne.
- Később mergelt delta automatikus elsőbbsége: egyszerű alkalmazás, de észrevétlenül felülírhat korábban kiválogatott tesztadatot.

## Következmények

- Ha egy migráció a meglévő tesztadaton elbukik, az a production adaton is elbukna; a hiba a story-gyűjtőbranch merge-kapujánál jelentkezik.
- Ha a `develop` a story tesztelése után változott, a merge előtt az aranyat újra kell építeni, és a story deltáját újra kell játszani.
- Ütközéskor a story merge-kapuja a kézi feloldás és a frissített delta sikeres ellenőrzéséig blokkol.
