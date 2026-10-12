# Demo – Szabadságkérelem az igénytől a kész storyig

Ez a demo egy egyszerű, új domainbeli igény útját mutatja be a rövid üzleti leírástól a kész, elfogadott storyig. A harness cél-működését írja le a [specifikáció](../uzleti-specifikacio.md) szerint; ahol az MVP ettől eltér, a **MVP-ben** jelölés mondja meg a kézi helyettesítést. A szereplők, az időpontok és az artefaktumok kitaláltak.

Állapot: 1. kör. A bontásig mindhárom story, a fejlesztés és a tesztelés az 1. storyra szerepel; a 2. és a 3. story későbbi körökben kerül be.

## 0. Bevezető

### Szereplők

| Név | Szerep |
|---|---|
| Anna | Product owner (PO) |
| Bence | BA |
| Dóra | Designer |
| Péter | Fejlesztő, story-felelős |
| Gábor | Fejlesztő, második reviewer |
| Tímea | Tesztelő |
| Kata | HR-szakértő (domain-szakértő) |

Agentek: beküldő agent, feldolgozó agent, AI-szakértők (jogi, UX, hibaút-kereső), AI-projektspecialista, fejlesztő agent.

### Kiinduló állapot

- A tervezési tér (`trn-proto-planning`) bootstrapolva, üres: nincs domain, nincs epic.
- A termékrepó (`trn-proto-monorepo`) a Trinity-sablonból indult; szabadságkezelés még nincs benne.
- A harness-konfiguráció: story-prefix `PRT`, PO Anna, helyettese Kata; az epicre Bence kap delegációt a `Pontosítva` átmenetre és a story-elfogadásra.

### Jelmagyarázat

- **Grill-kivonat:** az agent kérdése → ajánlott válasz → a szereplő válasza → az eredmény (forrásjelölés vagy döntés).
- **Csatorna:** ami a fejezetben megjelent a közös csatornán, vagyis amit a többi szereplő lát.
- **MVP-ben:** ahol az MVP kézi lépéssel helyettesíti a cél-működést.

## 1. Rövid üzleti leírás

Anna a story-szerkesztő felületen három mondatban rögzíti az igényt:

> A dolgozók ma e-mailben kérnek szabadságot, a vezetők táblázatban vezetik, és gyakori a keret túllépése. Szeretnénk, ha a dolgozó a rendszerben adná be a kérelmét, a rendszer ellenőrizné a keretét, és a közvetlen vezetője jóváhagyhatná vagy elutasíthatná. A dolgozó lássa a saját kérelmeit, és amíg nem bírálták el, visszavonhassa.

A harness létrehozza az `EP-001` epicet `Vázlat` állapotban. Bence `/next`-je:

```
Következő teendő: Az első domain felvétele
  A tervezési térben még nincs domain; az epicek a domain szótárára és határaira épülnek.
  Célhely: domains/<domain>/context.md
Utána: Pontosítás folytatása (epics/EP-001)
```

Mivel a szabadságkezelés új domain, Bence felfedező event stormingot kér; Anna Katát is meghívja.

> **MVP-ben:** a leírást Bence rögzíti a Claude projektben a `/harness-ba` skillekkel; az online felület helyett a beküldő agent commitolja a draft branchre.

**Csatorna**

| Időpont | Esemény | Szereplő | Átadás vagy várakozás | Hivatkozás |
|---|---|---|---|---|
| 10-13 09:10 | Epic létrehozva | Anna | Anna → Bence: pontosítás | `EP-001` |
| 10-13 09:25 | Felfedező event storming kérve | Bence | Várakozás: Anna, Kata időpontja | `EP-001` |

## 2. Felfedező event storming

Workshop Annával, Bencével, Katával és Dórával, 90 perc. Az AI-projektspecialista jelzi, hogy a termékrepóban van `users` modul, de vezetői kapcsolat nincs benne. Az AI-szakértők a workshop előtt vázlatot és hotspotlistát adnak.

**Események időrendben:** Kérelem beadva → Kérelem jóváhagyva | Kérelem elutasítva | Kérelem visszavonva.

**Hotspotok**

| Hotspot | Nyitotta | Lezárás |
|---|---|---|
| H1: Kérhető-e fél nap? | AI-szakértő (hibaút-kereső) | Anna: az első változatban nem; scope-on kívül |
| H2: A beadott, még el nem bírált kérelem csökkenti-e a keretet? | AI-szakértő (hibaút-kereső) | Anna: igen, különben két kérelemmel túl lehet lépni a keretet → `EP-001:DEC-1` |
| H3: Az ünnepnapok munkanapnak számítanak? | Kata | Nyitva marad, a pontosítás kérdése lesz |
| H4: A munkáltató jogszabály szerint maga is kiadhat szabadságot | AI-szakértő (jogi) | Anna: tudomásul vesszük, ez az epic csak a dolgozói kérelmet kezeli; scope-on kívül |
| H5: Mi történik, ha a dolgozónak nincs közvetlen vezetője? | AI-szakértő (hibaút-kereső) | Kata: minden dolgozónak van, a HR biztosítja [megerősített: Kata] |

**A felvett domain** (`domains/szabadsag/context.md`, kivonat):

```md
# Szabadság

**Szabadságkérelem**: Egy dolgozó kérése egy dátumtartományra eső munkanapok kiadására.
_Kerülendő_: távollét, szabi

**Munkanap**: Hétfőtől péntekig tartó nap. (SZAB:DATA-1)

**Szabadságkeret**: A dolgozó tárgyévi szabadsága napokban; az elérhető keret a jóváhagyott és a beadott, még el nem bírált kérelmek munkanapjaival csökken. (SZAB:DATA-2)

**Közvetlen vezető**: Az a dolgozó, aki a kérelmet elbírálja; minden dolgozónak pontosan egy van.
```

**Közös szabályok** (`domains/szabadsag/kozos-szabalyok.md`, kivonat):

- **SZAB:PERM-1** A dolgozó csak a saját kérelmét adhatja be, láthatja és vonhatja vissza.
- **SZAB:PERM-2** Kérelmet csak a dolgozó közvetlen vezetője bírálhat el.
- **SZAB:DATA-3** A kérelem állapotai: Beadva, Jóváhagyva, Elutasítva, Visszavonva.

A H2 és a H4 lezárása döntésnapló-bejegyzést kap:

```md
### EP-001:DEC-1 – A beadott kérelem csökkenti a keretet
- Döntéshozó: Anna (PO), 2026-10-14
- Érintett verzió: domains/szabadsag/context.md @ 3c1e9a0
- Indok: két párhuzamos kérelemmel különben túl lehetne lépni a keretet.
- Fennmaradó kockázat: elutasításkor a keret visszaáll; a dolgozó ezt csak frissítés után látja.
```

> **MVP-ben:** a workshop táblaképét Bence tölti fel; az agentfeldolgozás és a hotspotok rögzítése a Claude projektben történik.

**Csatorna**

| Időpont | Esemény | Szereplő | Átadás vagy várakozás | Hivatkozás |
|---|---|---|---|---|
| 10-14 10:00 | Hotspot nyitva (5) | AI-szakértők, Kata | Várakozás: workshop | `H1`–`H5` |
| 10-14 11:30 | Hotspotok lezárva (4), egy nyitva | Anna, Kata | H3 → Bence: pontosítás | `H3` |
| 10-14 11:40 | Döntés rögzítve | Anna | — | `EP-001:DEC-1` |
| 10-14 12:15 | Domain publikálva | Bence | — | `domains/szabadsag` |

## 3. Pontosítás

Bence a `/next` javaslatára elindítja a pontosítást. A grill egyszerre egy kérdést tesz fel, ajánlott válasszal.

**Grill-kivonat**

| # | Agent kérdése | Ajánlott válasz | Válasz | Eredmény |
|---|---|---|---|---|
| 1 | Ki bírálja el a kérelmet? | A közvetlen vezető | Igen, Kata megerősítette | `[megerősített: Kata]` |
| 2 | Mekkora időre előre lehet kérelmet beadni? | 90 nap | Anna: 180 nap | `[megerősített: Anna]` |
| 3 | Kezeljük-e az ünnepnapokat a munkanap-számításban? | Halasszuk el; a beadás e nélkül is működik | Bence elhalasztja | Elhalasztott kérdés, lásd lent |
| 4 | Visszavonható-e a már jóváhagyott kérelem? | Nem, csak elbírálás előtt | Anna: egyetért, csak elbírálás előtt | `[megerősített: Anna]` |
| 5 | Kell-e értesíteni a vezetőt a beadásról? | Az elbírálandó listában jelenjen meg; e-mail scope-on kívül | Anna: igen | `[megerősített: Anna]` |

Az üzleti igény (`epics/EP-001/uzleti-igeny.md`, kivonat):

```md
## Jelenlegi és kívánt folyamat
- Jelenleg: kérelem e-mailben, vezetői nyilvántartás táblázatban, a keretet senki nem ellenőrzi. [megerősített: Anna, Kata]
- Kívánt: kérelem a rendszerben, automatikus keret- és átfedés-ellenőrzés, elbírálás a rendszerben.

## Sikerességi mérőszám
- A kerettúllépések száma nullára csökken az első negyedévben. [megerősített: Anna]
- A kérelem beadásától az elbírálásig eltelt idő mediánja 2 munkanap alatt marad. [agentjavaslat]

## Nyitott kérdések
- Ünnepnapok kezelése a munkanap-számításban. Elhalasztva; felelős: Anna; határidő: 2026-10-21; feloldási pont: `Tervezés alatt` → `Bontva`.
```

Bence `Pontosítva` állapotba lépteti az epicet. **A determinisztikus kapu blokkol:**

```
Vázlat → Pontosítva: elutasítva
  uzleti-igeny.md 9. sor: megerősítetlen [agentjavaslat] („A kérelem beadásától az elbírálásig eltelt idő mediánja 2 munkanap alatt marad.”)
  Teendő: erősítse meg vagy törölje az állítást.
```

Bence megkérdezi Annát, aki 3 munkanapot ad meg; a sor `[megerősített: Anna]` jelölést kap. **Szemantikus javaslat:** a feldolgozó agent jelzi, hogy a leírásban a „távollét” szó is szerepel, amely a szótárban kerülendő. Bence elfogadja, és a szöveget javítja.

Dóra a felhasználói feladat szempontjából reviewzza a folyamatmodellt: a beadás egy lépésben, élő munkanap-számlálóval történjen, hogy a dolgozó ne csak a beadás után tudja meg, hogy túllépte a keretet. A javaslat bekerül a folyamatmodellbe (`SZAB:RM-3` Elérhető keret).

**Folyamatmodell** (`epics/EP-001/folyamatmodell.md`, kivonat):

| Azonosító | Elem |
|---|---|
| `SZAB:ACT-1` | Dolgozó |
| `SZAB:ACT-2` | Közvetlen vezető |
| `SZAB:CMD-1` | Kérelem beadása |
| `SZAB:CMD-2`, `SZAB:CMD-3` | Kérelem jóváhagyása, elutasítása |
| `SZAB:CMD-4` | Kérelem visszavonása |
| `SZAB:EVT-1`…`SZAB:EVT-4` | Kérelem beadva, jóváhagyva, elutasítva, visszavonva |
| `SZAB:RULE-1` | Munkanap-számítás (hétvége nélkül) |
| `SZAB:RULE-2` | A munkanapok száma nem haladhatja meg az elérhető keretet |
| `SZAB:RULE-3` | A kérelem nem fedhet át a dolgozó másik kérelmével |
| `SZAB:RULE-4` | Visszavonás csak elbírálás előtt |
| `SZAB:RM-1`…`SZAB:RM-3` | Saját kérelmek, Elbírálandó kérelmek, Elérhető keret |

A második kísérletre a kapu átengedi az átmenetet; Bence a delegációja alapján jogosult rá.

> **MVP-ben:** a grill a Claude projektben fut; a kapu GitHub Actionsben ellenőriz, és a hibát a beküldő agent jelzi vissza Bence munkamenetébe.

**Csatorna**

| Időpont | Esemény | Szereplő | Átadás vagy várakozás | Hivatkozás |
|---|---|---|---|---|
| 10-15 09:00 | Kérdés elhalasztva | Bence | Felelős: Anna, határidő 10-21 | `uzleti-igeny.md` |
| 10-15 10:20 | Kapu blokkolt | Feldolgozó agent | Várakozás: Anna megerősítése | `uzleti-igeny.md:9` |
| 10-15 11:05 | Állítás megerősítve | Anna | — | `uzleti-igeny.md:9` |
| 10-15 11:30 | Folyamatmodell-review | Dóra | — | `folyamatmodell.md` |
| 10-15 11:45 | Epic `Pontosítva` | Bence | Bence → Dóra, Péter: tervezés indul | `EP-001` |

## 4. Tervezés

A három sáv párhuzamosan halad.

### Funkcionális specifikáció (Bence)

Kivonat:

```md
## Kérelem beadása
A dolgozó egy képernyőn adja meg az időszakot. A rendszer azonnal kiszámolja a munkanapok számát (SZAB:RULE-1)
és a beadás utáni elérhető keretet (SZAB:DATA-2). A beadás feltétele, hogy az időszakban legyen munkanap, a keret
elegendő legyen (SZAB:RULE-2), és ne legyen átfedés a dolgozó másik kérelmével (SZAB:RULE-3). — SCR-1
```

**Minőségi elvárás** (`epics/EP-001/minosegi-elvarasok.md`):

- **EP-001:NFR-1** A beadási képernyő billentyűzettel teljesen kezelhető, és megfelel a WCAG 2.1 AA szintnek.

### Design (Dóra)

Két koncepció készül az SCR-1 (Kérelem beadása) képernyőre:

- **A1:** űrlap két dátummezővel, mellette élő számláló (munkanapok, maradó keret).
- **B1:** naptárnézet, amelyben a dolgozó kijelöli az időszakot.

Anna és Bence a review-n az A1-et választja; a B1 a mobilon nehezen kezelhető. Dóra finomítja (**A1.2**: a hibaüzenet a mező alatt jelenik meg, a számláló az űrlap tetején). A folyamat nem kockázatos, ezért használhatósági validáció nem kötelező.

Dóra az **Átadás fejlesztésre** művelettel adja ki: a harness létrehozza az `SCR-1@1 ← A1.2` képernyőverziót, csomagol, és előkészíti a design-PR-t. Ugyanígy készül az `SCR-2@1` (Saját kérelmek) és az `SCR-3@1` (Elbírálandó kérelmek).

Az **átadási csomag** ellenőrzésekor az agent hiányt jelez: „Az SCR-1-hez nincs állapot arra az esetre, ha az elérhető keret nem tölthető be.” Dóra hozzáadja a hibaállapotot „Újrapróbálás” gombbal.

| Állapot | SCR-1@1 |
|---|---|
| Betöltés | Számláló helyén töltésjelző |
| Hiba | „A keret nem tölthető be” + Újrapróbálás |
| Érvényes időszak | Számláló, aktív Beadás |
| Érvénytelen időszak | Hibaüzenet a mező alatt, inaktív Beadás |
| Siker | Visszaigazolás az új elérhető kerettel |
| Billentyűzet | Tab-sorrend: kezdő dátum → záró dátum → megjegyzés → Beadás |

### Technikai specifikáció (Péter)

**Grill-kivonat**

| # | Agent kérdése | Ajánlott válasz | Péter válasza | Eredmény |
|---|---|---|---|---|
| 1 | Új modul vagy a `users` bővítése? | Új `leave` modul; a vezetői kapcsolat a saját `EmployeeProfile` modelljében | Igen | Architektúraterv: új modul |
| 2 | Hol éljen a munkanap-számítás, ha a web élő számlálója és a backend is használja? | Tiszta függvény a `leave` contract package-ben | Igen | Egy forrás, nincs eltérés a kettő között |
| 3 | Aggregate session vagy egyszerű command? | Command handler repository portokkal; az átfedés- és keretellenőrzés serializable tranzakcióban | Igen | Párhuzamos beadás ellen védett |
| 4 | A migráció kockázatos-e? | Új táblák, meglévő adat nem változik | Mégis `pár` mód, mert ez a modul első migrációja | Végrehajtási mód rögzítve |

**Taskok a PRT-001-hez** (`docs/epics/EP-001/technikai-specifikacio.md`, kivonat):

| Task | Eszköz | Mód | Függés |
|---|---|---|---|
| PRT-001-T1 | Contract és kanonikus modell, munkanap-függvény | `agent` | — (contract-first) |
| PRT-001-T2 | Command és query (`SubmitLeaveRequest`, `GetLeaveBalance`), migráció | `pár` | T1 |
| PRT-001-T3 | Képernyőimport `SCR-1@1`, data hook | `agent` | T1 |
| PRT-001-T4 | E2E-tesztek AC-ból | `agent` | T3 (stack) |

PR-sorrend: T1 → T2 és T3 párhuzamosan → T4 a T3-ra stackelve. A spike-ra nincs szükség. Péter megerősíti a tervet; a tervmegerősítési kapu zöld.

> **MVP-ben:** a design-PR-t a kijelölt fejlesztő (Gábor) commitolja Dóra exportjából.

**Csatorna**

| Időpont | Esemény | Szereplő | Átadás vagy várakozás | Hivatkozás |
|---|---|---|---|---|
| 10-16 14:00 | Koncepciók reviewra | Dóra | Dóra → Anna, Bence: review | `A1`, `B1` |
| 10-17 10:00 | Koncepció kiválasztva | Anna, Bence | — | `A1.2` |
| 10-17 15:30 | Átadás fejlesztésre | Dóra | Dóra → Péter: képernyőverziók | `SCR-1@1`, `SCR-2@1`, `SCR-3@1` |
| 10-17 15:35 | Átadási csomag hiány | Feldolgozó agent | Várakozás: Dóra | `SCR-1@1` |
| 10-18 11:00 | Technikai specifikáció megerősítve | Péter | — | `technikai-specifikacio.md` |

## 5. Tervezési egyeztetés

Bence, Dóra és Péter együtt végigmennek a beadási flow-n az `SCR-1@1` és a specifikációk aktuális verzióival. **Két ellentmondás** derül ki:

1. A technikai specifikáció az elérhető keretet csak a jóváhagyott kérelmekkel csökkenti, a funkcionális specifikáció és a design a beadottakkal is.
2. Az ünnepnapok kérdése még nyitott, pedig a feloldási pontja ez az átmenet.

Anna dönt:

```md
### EP-001:DEC-2 – A technikai specifikáció a DEC-1-hez igazodik
- Döntéshozó: Anna (PO), 2026-10-18
- Érintett verzió: technikai-specifikacio.md @ 8b20d4f
- Indok: a DEC-1 már rögzítette; a technikai specifikáció elavult feltételezésre épült.
- Fennmaradó kockázat: nincs.

### EP-001:DEC-3 – Az első változat nem kezeli az ünnepnapokat
- Döntéshozó: Anna (PO), 2026-10-18
- Érintett verzió: uzleti-igeny.md @ 51f7c22
- Indok: a beadás és az elbírálás ünnepnapok nélkül is használható; az ünnepnapnaptár külön epic.
- Fennmaradó kockázat: ünnepnapra eső kérelem többet von le a keretből; a HR kézzel korrigál.
```

Péter frissíti a technikai specifikációt, és újra megerősíti.

**Csatorna**

| Időpont | Esemény | Szereplő | Átadás vagy várakozás | Hivatkozás |
|---|---|---|---|---|
| 10-18 13:00 | Ellentmondás jelezve (2) | Bence, Dóra, Péter | Várakozás: Anna döntése | `EP-001` |
| 10-18 13:40 | Döntés rögzítve (2) | Anna | Anna → Péter: specifikáció frissítése | `EP-001:DEC-2`, `EP-001:DEC-3` |
| 10-18 14:10 | Elhalasztott kérdés lezárva | Anna | — | `uzleti-igeny.md` |

## 6. Bontás

Bence a funkcionális specifikációból három storyt készít, Péter a taskokat rendeli hozzájuk, Tímea jóváhagyja a tesztforgatókönyveket.

### PRT-001 – Szabadságkérelem beadása

- **1** Beadási képernyő megnyitása — SCR-1@1, SZAB:RM-3
   - Előfeltétel: bejelentkezett dolgozó (SZAB:PERM-1).
   - Látható: elérhető keret napokban; kezdő és záró dátum; megjegyzés (nem kötelező, legfeljebb 200 karakter); „Beadás” inaktív.
   - Művelet: időszak megadása; mégse.
- **1.1** A keret nem tölthető be → „A keret nem tölthető be” üzenet és „Újrapróbálás”, „Beadás” inaktív.
- **2** Időszak megadása — SCR-1@1, SZAB:RULE-1
   - Előfeltétel: a keret betöltve.
   - Látható: a munkanapok száma és a beadás utáni elérhető keret.
   - Művelet: kezdő és záró dátum kiválasztása.
- **2.1** Érvényes időszak → munkanapok száma és maradó keret látható, „Beadás” aktív.
- **2.2** A záró dátum a kezdő előtt van → hibaüzenet a záró dátum alatt, „Beadás” inaktív.
- **2.3** A kezdő dátum a mai napnál korábbi vagy 180 napnál későbbi → hibaüzenet a kezdő dátum alatt, „Beadás” inaktív.
- **2.4** Az időszakban nincs munkanap → „A kiválasztott időszakban nincs munkanap”, „Beadás” inaktív.
- **2.5** A munkanapok száma meghaladja az elérhető keretet (SZAB:RULE-2) → hibaüzenet a hiányzó napok számával, „Beadás” inaktív.
- **2.6** Átfedés a dolgozó jóváhagyott kérelmével (SZAB:RULE-3) → hibaüzenet az ütköző kérelem időszakával, „Beadás” inaktív.
- **3** Beadás — SCR-1@1, SZAB:CMD-1
   - Előfeltétel: 2.1 teljesül.
   - Látható: összefoglaló (időszak, munkanapok, maradó keret).
   - Művelet: beadás megerősítése; vissza.
- **3.1** Sikeres beadás → a kérelem „Beadva” állapotú (SZAB:EVT-1), megjelenik a vezető elbírálandó listájában, a dolgozó visszaigazolást lát az új elérhető kerettel.
- **3.2** Közben elfogyott a keret vagy átfedés keletkezett → hibaüzenet, a kérelem nem jön létre, az űrlap adatai megmaradnak.
- **4** A beadási képernyő billentyűzettel teljesen kezelhető (EP-001:NFR-1). [kézi]

Tesztforgatókönyvek (kivonat): pozitív – 5 munkanap, 20 napos keret; határeset – a munkanapok száma pontosan a keret; negatív – péntektől hétfőig tartó időszak 0 elérhető kerettel; negatív – két böngészőfülről egyszerre beadott, átfedő kérelem.

### PRT-002 – Kérelem elbírálása

- **1** Elbírálandó kérelmek listája — SCR-3@1, SZAB:RM-2
   - Előfeltétel: bejelentkezett közvetlen vezető (SZAB:PERM-2).
   - Látható: a beosztottak „Beadva” állapotú kérelmei a beadás sorrendjében: név, időszak, munkanapok, megjegyzés.
   - Művelet: jóváhagyás; elutasítás.
- **1.1** Nincs elbírálandó kérelem → „Nincs elbírálandó kérelem”.
- **2** Jóváhagyás — SZAB:CMD-2
   - Előfeltétel: a kérelem „Beadva” állapotú.
   - Látható: —
   - Művelet: jóváhagyás megerősítése; mégse.
- **2.1** Sikeres jóváhagyás → a kérelem „Jóváhagyva” (SZAB:EVT-2), eltűnik a listából.
- **2.2** A kérelmet közben visszavonták → „A kérelmet visszavonták”, a lista frissül.
- **3** Elutasítás — SZAB:CMD-3
   - Előfeltétel: a kérelem „Beadva” állapotú.
   - Látható: indoklásmező.
   - Művelet: indoklás megadása (kötelező, legfeljebb 500 karakter); elutasítás megerősítése; mégse.
- **3.1** Sikeres elutasítás → a kérelem „Elutasítva” (SZAB:EVT-3), a dolgozó elérhető kerete a kérelem munkanapjaival nő.
- **3.2** Üres indoklás → hibaüzenet, az elutasítás nem indítható.
- **4** Más dolgozó vezetője nem láthatja és nem bírálhatja el a kérelmet (SZAB:PERM-2).

### PRT-003 – Visszavonás és saját kérelmek

- **1** Saját kérelmek listája — SCR-2@1, SZAB:RM-1
   - Előfeltétel: bejelentkezett dolgozó (SZAB:PERM-1).
   - Látható: a saját kérelmek legújabb elöl: időszak, munkanapok, állapot, elutasításnál az indoklás.
   - Művelet: visszavonás a „Beadva” állapotú kérelemnél.
- **1.1** Nincs kérelem → „Még nincs szabadságkérelme” és hivatkozás a beadásra.
- **2** Visszavonás — SZAB:CMD-4, SZAB:RULE-4
   - Előfeltétel: a kérelem „Beadva” állapotú.
   - Látható: megerősítő kérdés az időszakkal.
   - Művelet: visszavonás megerősítése; mégse.
- **2.1** Sikeres visszavonás → „Visszavonva” (SZAB:EVT-4), az elérhető keret nő.
- **2.2** A kérelmet közben elbírálták → „A kérelmet már elbírálták”, a lista frissül, az állapot az új.
- **3** Jóváhagyott, elutasított vagy visszavont kérelemnél a visszavonás nem jelenik meg.

Az epic `Bontva` állapotba lép; a három story `Fejlesztésre kész`.

**Csatorna**

| Időpont | Esemény | Szereplő | Átadás vagy várakozás | Hivatkozás |
|---|---|---|---|---|
| 10-20 10:00 | Storyk létrehozva (3) | Bence | Bence → Tímea: forgatókönyvek | `PRT-001`…`PRT-003` |
| 10-20 15:00 | Forgatókönyvek jóváhagyva | Tímea | — | `test-scenarios/` |
| 10-20 15:10 | Epic `Bontva` | Bence, Péter | Péter: fejlesztés indul | `EP-001` |

## 7. Fejlesztés – PRT-001

A tervezési szinkron a termékrepó `develop`-jára hozza a tervezési másolatokat. A harness létrehozza a `story/PRT-001` gyűjtőbranchet.

**T1 (contract-first, `agent`).** A fejlesztő agent a fejlesztési útmutató szerint dolgozik: kontextus → eszközskill (contract és kanonikus modell) → váz → teszt először (a munkanap-függvényre: hétvége, hónapváltás, szökőév) → implementáció → helyi kapuk → agentes előreview → PR. Péter fél óra alatt átnézi, mergelve. A story `Fejlesztés alatt`, mert a T1 elindult.

**T2 és T3 párhuzamosan.** A T2-t (`pár`) Péter a saját Claude Code-jában vezeti; a reviewer Gábor (négy szem elve). A T3-at a fejlesztő agent készíti a képernyőimporttal: az `SCR-1@1` statikus kódját komponensekre bontja, és beköti a data hookot.

**T4 stackelve.** A T4 (e2e) a T3 branchéből indul, miközben a T3 még reviewra vár. Amikor Gábor kér egy módosítást a T3-ban, a harness restackeli a T4-et; a T3 merge-e után a T4 célja automatikusan a gyűjtő lesz.

**Review-magyarázat a T2 PR-jához** (kivonat):

```md
Belépési pont: SubmitLeaveRequest command (leave backend)
Flow: munkanap-számítás (contract) → keret és átfedés lekérdezése → mentés, serializable tranzakcióban
Üzleti hatás: a beadott kérelem azonnal csökkenti az elérhető keretet (EP-001:DEC-1)
Kockázat: a modul első migrációja; új táblák, meglévő adat nem változik
Tesztrés: párhuzamos beadás integrációs teszttel lefedve; e2e a T4-ben
Olvasási sorrend: migráció → kanonikus modell → handler → repository
```

Gábor egy kommentet tesz: a hibaüzenet ne tartalmazza a belső tranzakcióhibát. Az agent egy javító committal kezeli; Gábor elfogadja.

Mind a négy task mergelve, a pipeline zöld, minden automata ellenőrzésű AC-hez van címkézett teszt (például `@PRT-001#2.6`). A story `Tesztelés alatt` állapotba lép.

> **MVP-ben:** a T4 célváltását és restackjét Péter kézzel végzi.

**Csatorna**

| Időpont | Esemény | Szereplő | Átadás vagy várakozás | Hivatkozás |
|---|---|---|---|---|
| 10-21 09:00 | Story `Fejlesztés alatt` | Fejlesztő agent | — | `PRT-001` |
| 10-21 09:40 | PR reviewra (T1) | Fejlesztő agent | → Péter: review | `PRT-001-T1` |
| 10-21 13:00 | PR reviewra (T2) | Péter | → Gábor: review | `PRT-001-T2` |
| 10-21 13:30 | PR reviewra (T3), stack (T4) | Fejlesztő agent | → Péter: review; T4 vár a T3-ra | `PRT-001-T3`, `PRT-001-T4` |
| 10-22 11:00 | Story `Tesztelés alatt` | Harness | → Tímea, Dóra, Bence: tesztkörnyezet | `prt-001.test` |

## 8. Tesztelés és elfogadás – PRT-001

A harness tesztkörnyezetet indít (`prt-001.test.<domain>`) az arany tesztadat klónjával: 3 dolgozó, 1 vezető, 2 korábbi kérelem.

**Tímea** feltáró tesztelés közben észreveszi: ha a dolgozónak van egy **beadott, még el nem bírált** kérelme, egy vele átfedő második kérelmet is be tud adni. A 2.6 csak a jóváhagyott kérelmekkel való átfedést tiltja. Jelzi Bencének.

**Bence** pontosítja az AC-t. Ez szövegváltozás, ezért új betűt kap:

```md
- **2.6** ~~Átfedés a dolgozó jóváhagyott kérelmével (SZAB:RULE-3) → hibaüzenet az ütköző kérelem időszakával, „Beadás” inaktív.~~ (2026-10-22)
- **2.6a** Átfedés a dolgozó jóváhagyott vagy beadott, még el nem bírált kérelmével (SZAB:RULE-3) → hibaüzenet az ütköző kérelem időszakával, „Beadás” inaktív.
```

A **hatáslista** publikálás előtt: érintett a PRT-001#2.6, a `@PRT-001#2.6` címkéjű e2e-teszt és a PRT-003 (a visszavont kérelem nem számít átfedésnek); prioritásra nincs hatás. Nem scope-változás, így Bence publikálja.

A tervezési szinkron után:

- **tervezési eltérés:** a technikai specifikáció a régebbi story-verzióra hivatkozik, a `planning-drift` ellenőrzés blokkol;
- **gyanús tesztkapcsolat:** a `@PRT-001#2.6` címke visszavont azonosítóra mutat;
- **visszalépés:** a story sikertelen elfogadás miatt `Fejlesztés alatt` állapotba lép, és javító task készül (PRT-001-T5).

Péter megerősíti a tervet (a változás a meglévő taskok szerkezetét nem érinti). A fejlesztő agent a T5-ben bővíti az átfedés-ellenőrzést, a tesztet `@PRT-001#2.6a`-ra címkézi, és új esetet ad hozzá. A PR-ban Tímea tartalmilag is reviewzza a tesztet: valóban a függő kérelemmel való átfedést ellenőrzi-e. Péter lezárja a gyanús tesztkapcsolatot; a bizonyíték a teszt diffje.

Az új tesztkörnyezetben:

- **Tímea** rögzíti a 4. (`[kézi]`) feltétel eredményét: a teljes beadás billentyűzettel elvégezhető, a fókusz látható. Elfogad.
- **Dóra** a designer-reviewn egy eltérést talál: mobilon a „maradó keret” felirat két sorba törik. Ez esztétikai, nem rontja a működést, ezért design-frissítési story lesz belőle (PRT-004).
- **Bence** elfogadja a storyt:

```md
Elfogadás – PRT-001
- Vizsgált verzió: story/PRT-001 @ e41b7a9, tesztkörnyezet prt-001.test
- Eredmény: elfogadva
- Nyitott hibák: nincs blokkoló; PRT-004 (esztétikai, mobil felirat)
```

**Tesztadat-delta.** Tímea megtartja a tesztelés során felvett két életszerű esetet (egy hosszú, hónapváltó kérelmet és egy kimerített keretű dolgozót). A delta kivonata:

```json
{
  "story": "PRT-001",
  "schemaVersion": "20261021090000_leave_module",
  "tables": {
    "LeaveRequest": {
      "before": { "7d2e…": null },
      "upsert": [{ "id": "7d2e…", "employeeId": "b91c…", "from": "2026-11-27", "to": "2026-12-04", "workdays": 6, "status": "SUBMITTED" }]
    }
  }
}
```

A gyűjtő → `develop` kapu zöld: a `develop` behúzva, az arany tesztadat a deltával újraépült, megvannak a tesztelői, a designer- és a BA-elfogadás. A gyűjtőbranch a `develop`-ra kerül; a story `Elfogadva`.

> **MVP-ben:** egy közös tesztkörnyezet van sorral; a delta kinyerését Tímea kézzel végzi.

**Csatorna**

| Időpont | Esemény | Szereplő | Átadás vagy várakozás | Hivatkozás |
|---|---|---|---|---|
| 10-22 14:20 | Hiba jelezve | Tímea | Tímea → Bence: AC pontosítása | `PRT-001#2.6` |
| 10-22 15:00 | AC módosítva, hatáslista | Bence | — | `PRT-001#2.6a` |
| 10-22 15:05 | Tervezési eltérés, gyanús tesztkapcsolat | Harness | → Péter: tervmegerősítés | `PRT-001` |
| 10-22 15:05 | Story vissza `Fejlesztés alatt` | Harness | → fejlesztő agent: T5 | `PRT-001-T5` |
| 10-23 10:30 | Tesztreview | Tímea | — | `PRT-001-T5` |
| 10-23 14:00 | Designer-eltérés | Dóra | Új story | `PRT-004` |
| 10-23 16:00 | Story elfogadva | Bence | — | `PRT-001` |
| 10-23 16:10 | Story `Elfogadva`, `develop`-on | Harness | — | `PRT-001` |

## 9. Összegzés (1. kör)

### Nyomkövetési lánc – PRT-001#2.6a

Üzleti igény (`EP-001`) → `SZAB:RULE-3` és `SZAB:DATA-2`, `EP-001:DEC-1` → `PRT-001#2.6a` → tesztforgatókönyv „átfedő függő kérelem” → `@PRT-001#2.6a` e2e-teszt → elfogadás `e41b7a9`.

### A közös csatorna eseménytípusai

| Eseménytípus | Példa a demóban | Kinek fontos |
|---|---|---|
| Artefaktum létrehozva vagy publikálva | Epic, domain, storyk | Mindenki |
| Állapotváltás | `Pontosítva`, `Bontva`, `Tesztelés alatt` | Mindenki |
| Átadás | Bence → Dóra, Péter: tervezés indul | A címzett |
| Várakozás döntésre | Kapu blokkolt Anna megerősítésére | A döntéshozó |
| Hotspot nyitva vagy lezárva | H1–H5 | PO, BA, domain-szakértő |
| Döntés rögzítve | `EP-001:DEC-1`…`DEC-3` | Mindenki |
| Elhalasztott kérdés és határideje | Ünnepnapok | A felelős |
| Kapu blokkolt | Megerősítetlen agentjavaslat | A léptető |
| PR reviewra, stack | T1–T5 | A reviewer |
| Tervezési eltérés, gyanús tesztkapcsolat | PRT-001#2.6 → 2.6a | Story-felelős |
| Visszalépés | `Tesztelés alatt` → `Fejlesztés alatt` | Fejlesztés, BA |
| Elfogadás és bizonyíték | PRT-001 elfogadva | PO, BA |

### Átadási térkép

```
Anna (PO) ──igény──▶ Bence (BA) ──pontosított epic──▶ Dóra (designer), Péter (fejlesztő)
Dóra ──koncepció──▶ Anna, Bence ──választás──▶ Dóra ──átadás fejlesztésre──▶ Péter
Bence, Dóra, Péter ──ellentmondás──▶ Anna ──döntés──▶ Péter
Bence ──storyk──▶ Tímea (forgatókönyvek) ──jóváhagyás──▶ Péter, fejlesztő agent
Fejlesztő agent, Péter ──PR──▶ Péter, Gábor ──merge──▶ Harness ──tesztkörnyezet──▶ Tímea, Dóra, Bence
Tímea ──hiba──▶ Bence ──AC-módosítás──▶ Harness ──eltérés──▶ Péter
```

### Kézi lépések az MVP-ben

| Fejezet | Kézi lépés | Felelős |
|---|---|---|
| 1, 3 | A BA a Claude projektben dolgozik, a válaszokat promptként illeszti be | Bence |
| 2 | Workshop-anyag feltöltése, hotspotok rögzítése | Bence |
| 4 | A design-PR commitolása Dóra exportjából | Gábor |
| 7 | Stacked PR célváltás és restack | Péter |
| 8 | Közös tesztkörnyezet sorral, kézi tesztadat-delta | Tímea |

### A demo tanulságai a közös csatorna tervezéséhez

- A legtöbb várakozás döntésre vár (Anna); a csatornán a „kire vár” a legfontosabb mező.
- Az átadásoknak mindig van címzettje; a csatorna szűrhető legyen „nekem szóló” eseményekre.
- A kapuhibák és az eltérések okát üzleti nyelven kell mutatni, a fájl- és sorhivatkozás csak részlet.
