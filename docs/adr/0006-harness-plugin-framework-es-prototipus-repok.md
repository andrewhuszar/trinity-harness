# Harness-pluginok, framework-skillek és külön prototípus repók

A harness saját repóban él, és Claude Code pluginként terjed: a `harness-ba` és a `harness-dev` plugin globálisan, szerepenként telepíthető, verziózott és egy marketplace-ből frissül. A projekt csak konfigurációt hordoz (story-prefix, repócímek, struktúra), skillt nem. A Trinity framework-specifikus eszközskillek, generátorok és arany példák a framework kódjával együtt változnak, ezért a Trinity repóban élnek, és a frameworkkel terjednek. A harness kipróbálása két külön, nulláról harness-eszközökkel felépített prototípus repóban (tervezési tér és termékrepó) történik, így a generált tartalom nem keveredik a framework fejlesztésével. A prototípus termékrepó a Trinity sablonmásolatából indul; a framework publikálása privát registrybe későbbi Enabler.

## Mérlegelt lehetőségek

- Minden egy repóban, prototípus mappákkal: a valódi kétrepós git-mechanika nem tesztelhető, és a generált tartalom a framework historyjába és az agentek kontextusába kerülne.
- Projektenként másolt skillek: verziók szétcsúsznak, frissítés kézi.
- Az eszközskillek a harness pluginban: framework-változáskor két helyen kellene módosítani.
- Azonnali csomagpublikálás: a gyorsan változó framework kiadási folyamata az MVP kritikus útjára kerülne.
