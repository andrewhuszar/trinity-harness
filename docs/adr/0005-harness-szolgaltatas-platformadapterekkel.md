# Harness-szolgáltatás platformadapterekkel

A harness egyetlen, Azure Container Appsban futó szolgáltatás saját Postgres eseménynaplóval és munkasorral. Platformfüggetlen magja az állapotgépet, a kapukat, a tervezési szinkront és a stacked PR-logikát tartalmazza; a GitHub (tervezési tér) és az Azure DevOps (termékrepó), a CI, a tesztkörnyezetek és az agentfuttatás adaptereken keresztül kapcsolódik. Az agentek taskonként rövid életű Container Apps Jobsban futnak. A platformközi szinkron és állapot-visszaírás tartós, újrapróbálható és kompenzálható folyamat, ezért szolgáltatás és tartós sagaállapot kell hozzá, nem csak pipeline-szkript.

## Mérlegelt lehetőségek

- Pipeline-natív megoldás GitHub Actions és Azure Pipelines szkriptekkel: nincs futó szolgáltatás, de a logika két CI-dialektusban duplikálódna, és a platformközi újrapróbálás, illetve kompenzáció nem lenne megbízható.

## Következmények

- Az Azure DevOps oldalon a stacked PR célváltást, restacket, kaszkádmerge-et és a PR-kommentre reagáló agentindítást a harness valósítja meg.
