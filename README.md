# Trinity harness

Az agent harness az a munkakörnyezet, amelyben AI-agentek és emberi csapattagok (BA, üzlet, designer, fejlesztő, tesztelő) közösen jutnak el egy rövid üzleti leírástól a kiadott szoftverig.

Állapot: specifikáció; a pluginok és a harness-szolgáltatás tervezettek.

## Tartalom

| Hely | Tartalom |
|---|---|
| [`docs/uzleti-specifikacio.md`](docs/uzleti-specifikacio.md) | Szerepek, folyamat, állapotok, kapuk, artefaktumformátumok |
| [`docs/technikai-specifikacio.md`](docs/technikai-specifikacio.md) | Architektúra, adapterek, szinkron, automatizálás, MVP |
| [`CONTEXT.md`](CONTEXT.md) | A harness fogalomtára |
| [`docs/adr/`](docs/adr/) | Architekturális döntések |
| [`docs/development-workflow.md`](docs/development-workflow.md) | A harness saját fejlesztésének workflow-ja |
| [`plan/stories/`](plan/stories/) | A harness storyjai (`HRN-*`) |
| [`plugins/`](plugins/) | A `harness-ba` és a `harness-dev` Claude Code plugin; a gyorsindító workflow-sablon a `harness-dev` része |

## Telepítés

```bash
claude plugin marketplace add <a trinity-harness repó útvonala vagy GitHub-címe>
claude plugin install harness-ba@trinity-harness    # BA és üzleti szerep
claude plugin install harness-dev@trinity-harness   # fejlesztői szerep
```

Egy új repóban a `/harness-ba:init` (tervezési tér) vagy a `/harness-dev:init` (termékrepó, teljes vagy gyorsindító workflow-val) hozza létre a `.harness/config.json` konfigurációt és az alapszerkezetet. A következő teendőt a `/harness-ba:next`, illetve a `/harness-dev:next` mutatja.

A közös szkriptmodul forrása a `shared/harness_core.py`; módosítás után a `scripts/sync-shared.sh` másolja a pluginokba, a `scripts/sync-shared.sh --check` jelzi az eltérést.

## Kapcsolódó repók

- `trinity`: a framework, a framework-skillekkel és az arany példákkal.
- `proto-planning`: prototípus tervezési tér.
- `proto-product`: prototípus termékrepó, a Trinity sablonmásolatából.
