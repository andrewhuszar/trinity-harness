---
description: A következő BA-teendő a harness-konfiguráció és az állapotok alapján
allowed-tools: Bash(python3:*)
---

Futtasd:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/harness_ba.py" next
```

Az eredmény JSON. Válaszolj magyarul, röviden, emoji nélkül:

1. **Következő teendő:** a `next.action`, egy mondatban az indokkal (`next.reason`) és a célhellyel (`next.target`), ha van. Ha `next.command` szerepel, azt ajánld.
2. **Utána:** az `other` lista legfeljebb három eleme, egy-egy sorban; ha üres, hagyd el.
3. **Figyelmeztetés:** a `warnings` elemei, ha vannak.
4. Egy sorban a plugin neve és verziója (`plugin`).

Ajánld fel egy mondatban, hogy belekezdesz a következő teendőbe, de ne kezdd el és ne kérdezz rá a részleteire kérés nélkül. Csak azt írd le, ami a szkript eredményében szerepel; a folyamatról, a szinkronról vagy más repóról ne tegyél hozzá saját magyarázatot vagy lépést. Ha az állapot nem egyértelmű, mondd ki.
