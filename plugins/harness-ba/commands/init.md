---
description: A jelenlegi repó bootstrapolása harness-tervezési térként (konfiguráció és alapszerkezet)
argument-hint: [story-prefix] [projektnév]
allowed-tools: Bash(python3:*)
---

A jelenlegi munkakönyvtárat harness-tervezési térként készíted elő. Meglévő fájlt és meglévő harness-konfigurációt soha nem írsz felül.

1. Gyűjtsd össze a hiányzó adatokat, egyszerre egy kérdéssel, ajánlott válasszal:
   - **story-prefix**: 2–10 karakter, nagybetűvel kezdődik, csak nagybetű és számjegy (például `PRT`); ha `$ARGUMENTS` tartalmazza, azt használd;
   - **projektnév**: rövid, emberi név;
   - **kapcsolódó repó** (nem kötelező): a termékrepó címe vagy útvonala.
2. Futtasd:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/harness_ba.py" init --prefix <PREFIX> --project "<projektnév>" [--linked-repo <cím>]
   ```

3. Az eredmény JSON. Ha `ok` hamis, mondd el a hibát egy mondatban, és ne próbáld megkerülni. Ha igaz, sorold fel röviden a létrehozott (`created`) és a meglévő, érintetlenül hagyott (`skipped`) fájlokat, a plugin nevével és verziójával.
4. Végül futtasd a `/harness-ba:next` parancsot, és mutasd meg az első teendőt. Ne kezdj bele, ne tegyél fel kérdést a teendőről, és ne írj le olyan lépést, amely nem szerepel a szkript eredményében.

Git-műveletet (commit, push) ne végezz. Emojit ne használj.
