# CODEX_MASTER_PLAN_V2_10_NUMBERED_FINAL — coinbase_freqtrade_guarded_bot

> **Účel dokumentu:** finální sloučený master plán pro Codex GPT-5.5 pro projekt `coinbase_freqtrade_guarded_bot`.  
> **Jak používat:** ulož tento soubor do rootu repozitáře jako `CODEX_MASTER_PLAN.md` nebo `CODEX_MASTER_PLAN_V2_FINAL.md` a v každé nové Codex session na něj odkazuj.  
> **Primární režim:** bezpečný, auditovatelný, restartovatelný vývoj po fázích.  
> **Primární cíl:** výzkum, backtesting, dry-run a řízená validace strategií pro Coinbase spot BTC/ETH.  
> **Autonomní režim Codexu:** Codex má pokračovat od fáze k fázi bez průběžného potvrzování uživatelem, dokud nenarazí na hard-stop stav definovaný v tomto dokumentu.  
> **Aplikační režim:** vlastní Python kód musí být vyvíjen jako instalovatelný balíček se sjednocenými coding standards, CLI entry pointy a testovatelnou architekturou, ne jako volná sada skriptů.  
> **Validace metod:** predikční a výpočtové metody musí být kauzální, testované proti baseline, bez lookahead bias/data leakage a s ověřením vhodnosti pro časové řady.  
> **Priorita dokončení:** první milník je Minimum Viable Research System (MVRS): data parity, baseline strategie, minimální guard core, backtest report a dry-run. Enterprise UI, ML/FreqAI, pokročilý tax export a trader knowledge base jsou následné hardening/research vrstvy, ne blocker MVRS.  
> **Exekuční determinismus:** každý shell příkaz musí mít jasně uvedený kontext spuštění: host PowerShell, lokální `.venv`, Docker app nebo Docker Freqtrade.  
> **Import determinismus:** Freqtrade strategie v Dockeru musí mít bezpečný a testovaný import vlastního package kódu bez `sys.path.append` hacků.  
> **Tarifní bezpečnost:** projekt musí být restartovatelný i při vyčerpání Codex/ChatGPT limitů; žádná práce nesmí existovat pouze v konverzaci bez zápisu do souborů, LOGu a ideálně Gitu.  
> **Reprodukovatelnost a kontext:** projekt musí používat lockované runtime závislosti a aktivní working context summary, aby šel bezpečně restartovat i po dlouhém vývoji bez zahlcení kontextového okna.  
> **Ne-cíl:** garance výdělku, rychlé live obchodování, plně autonomní obchodování s penězi bez lidské kontroly, ani výběr/nákup hardwaru.

---

## 0. Základní princip projektu

Tento projekt má vytvořit **bezpečný, auditovatelný a testovatelný research/dry-run systém** pro kryptoměnové spot obchodování přes Coinbase.

Projekt nesmí být stavěn jako „AI stroj na peníze“. Má být postaven jako technický systém:

```text
data
→ validace dat
→ baseline strategie
→ backtest
→ robustní statistická validace
→ dry-run
→ guard layer
→ audit
→ tax ledger
→ manuální approval
→ teprve později omezený live pilot
```

Každý výsledek strategie se musí hodnotit po započtení:

- poplatků,
- skluzu,
- datové kvality,
- out-of-sample výsledků,
- walk-forward stability,
- drawdownu,
- provozních rizik,
- chyb API,
- daňové evidence,
- auditovatelnosti.

Každý algoritmus, metoda, model nebo výpočtový postup musí projít ověřením správnosti a aktuálnosti. Codex nesmí použít algoritmus jen proto, že je běžný nebo ho zná z paměti. Musí ověřit:

- zda je metoda matematicky a programově správně implementovaná;
- zda se hodí pro daný typ dat a obchodní režim;
- zda existují novější nebo robustnější metody;
- jaké má metoda předpoklady a slabiny;
- zda není náchylná k lookahead bias, data leakage nebo overfittingu;
- zda existuje benchmark proti jednodušší baseline metodě;
- zda je výsledek reprodukovatelný na out-of-sample datech.
- zda jsou features a labely časově správně zarovnané;
- zda každá predikční feature používá pouze informace dostupné v okamžiku rozhodnutí;
- zda se používá chronologické dělení dat nebo walk-forward / time-series split, nikoliv náhodné k-fold dělení bez časové osy;
- zda jsou případné testy stacionarity vyhodnoceny podle p-hodnot a kritických hodnot, nikoliv podle jedné tvrdě zakódované hodnoty test statistic.

Každý nový Python modul musí respektovat sjednocené coding standards projektu. Codex nesmí vytvářet jednorázové skripty nebo neimportovatelné moduly tam, kde má vzniknout aplikační logika. Vlastní kód projektu musí být importovatelný, typovaný, testovatelný a spustitelný přes CLI entry pointy.

---

## 1. Tvrdá bezpečnostní smlouva

Codex nesmí tato pravidla porušit za žádných okolností.

### 1.1 Zakázáno v MVP

1. Žádný live trading se skutečnými penězi.
2. Žádné skutečné Coinbase API klíče v repozitáři, kódu, logu, dokumentaci ani odpovědích.
3. Žádné seed fráze, privátní klíče, session cookies, exporty klíčů nebo secrets.
4. Žádné futures.
5. Žádná páka.
6. Žádné shortování.
7. Žádné opce, perpetuals, margin, lending ani staking v obchodním enginu.
8. Žádné altcoiny v první verzi.
9. Žádné přebírání cizí strategie jen podle Redditu, Telegramu, YouTube nebo marketingového článku.
10. Žádný cizí „arbitrage bot“, smart contract bot nebo neověřený kód spuštěný lokálně.
11. Žádný live order path, dokud nejsou splněna live pilot kritéria.
12. Žádné tvrzení o garantovaném zisku.
13. Žádná změna bezpečnostního pravidla bez samostatného rozhodnutí uživatele a zápisu do `LOG.md`.

### 1.2 Povinné v MVP

1. Spot only.
2. Long only.
3. Pouze BTC a ETH.
4. Jedna quote měna konzistentně: USD nebo USDC podle rozhodnutí uživatele.
5. Hlavní timeframe: 4h.
6. Trend filtr: 1d.
7. Režim: backtest + dry-run / simulation.
8. Coinbase sandbox není považován za validační prostředí strategie.
9. Každý návrh obchodu má auditní záznam.
10. Každý relevantní modul má testy.
11. Každá fáze má acceptance kritéria.
12. Každá fáze končí zápisem do `LOG.md`.
13. Pokud není jasno, Codex se zastaví a položí otázku.
14. Pokud systém neví, co se stalo, musí fail-closed.
15. Pokud nejde audit, nejde obchod.
16. Pokud je aktivní kill-switch, nejde obchod.
17. Pokud existuje nereconciliovaný order, nejde další obchod.

---

## 2. Provozní režim Codexu

Codex pracuje v režimu **supervised-autonomous execution**.

To znamená:

```text
Codex pokračuje automaticky přes všechny fáze,
pokud jsou splněna acceptance criteria
a nevznikl hard-stop stav.
```

Codex nemá čekat na potvrzení po každé fázi. Místo toho po každé fázi:

1. zapíše výsledek do `LOG.md`;
2. aktualizuje `PHASE TRACKER`;
3. vytvoří stručné phase summary;
4. automaticky pokračuje další fází, pokud nevznikl hard-stop.

### 2.1 Autonomní loop

```text
AUTONOMOUS LOOP:
  1. Přečti CODEX_MASTER_PLAN.md.
  2. Přečti AGENTS.md.
  3. Přečti LOG.md.
  4. Urči aktuální fázi.
  5. Přečti relevantní soubory celé.
  6. Vypiš call-flow, editable/read-only scope a execution context pro příkazy.
  7. Pokud je potřeba research, proveď RESEARCH PROTOKOL.
  8. Implementuj jen soubory v aktuálním scope.
  9. Přidej/aktualizuj testy.
 10. Spusť relevantní testy.
 11. Pokud testy selžou a příčina je jasná, oprav v rámci scope; maximálně 3 auto-remediation iterace na stejný typ chyby. Pokud selže 2. iterace na stejné chybě, Codex před 3. pokusem povinně spouští RESEARCH PROTOKOL k ověření aktuální syntaxe/API dané knihovny. Pokud selže 2. iterace na stejné chybě, Codex před 3. pokusem povinně spustí RESEARCH PROTOKOL a ověří aktuální syntaxi/API dané knihovny v oficiální dokumentaci nebo release notes.
 12. Průběžně zapisuj LOG checkpointy.
 13. Vyhodnoť acceptance criteria.
 14. Pokud PASS a nevznikl hard-stop, pokračuj další fází.
 15. Pokud vznikl hard-stop, zapiš stav do LOG.md a zastav se.
```

### 2.2 Průběžné logování kvůli tokenům a navazování

Codex musí logovat průběžně, ne až na konci dlouhé fáze.

Povinný LOG checkpoint:

- na začátku každé fáze;
- po každé významné změně souborů;
- po každém research reportu;
- po každém testovacím běhu;
- před delším refaktoringem;
- před spuštěním dlouhého backtestu;
- po dokončení dlouhého backtestu;
- při každém blockeru;
- před ukončením odpovědi.

Checkpoint musí být krátký, ale musí umožnit navázání po vyčerpání tokenů:

```markdown
### CHECKPOINT — YYYY-MM-DD HH:MM — Phase XX
Stav:
Hotovo:
Rozpracováno:
Soubory změněné od posledního checkpointu:
Git diff summary:
Execution context použitý pro příkazy:
Testy:
Identifikovaná rizika:
Další bezpečný krok:
```

### 2.3 Hard-stop stavy

Codex se musí zastavit pouze v těchto případech:

| Hard-stop | Co má Codex udělat |
|---|---|
| Potřebuje API key, secret, private key, seed, Coinbase login nebo autentizační soubor | Zapsat do `OPEN QUESTIONS`, vysvětlit přesně co potřebuje, proč a v jakém bezpečném formátu. Nežádat o vložení secretu do chatu, pokud lze použít lokální `.env`. |
| Potřebuje připojení k účtu, Coinbase, brokerovi, Gmailu, repozitáři nebo jinému externímu systému | Zapsat požadavek do `OPEN QUESTIONS`, zastavit se a počkat. |
| Má nastavit `ALLOW_LIVE_TRADING=true` nebo otevřít Phase 18 | Zastavit se. Vyžaduje explicitní uživatelské rozhodnutí a samostatný commit. |
| Má vytvořit nebo odeslat live order | Zastavit se. V MVP zakázáno. |
| Data nejsou dostupná ani po bezpečném fallbacku | Zapsat blocker report. |
| Data Parity Gate selže a nelze automaticky přejít na bezpečný fallback | Zapsat blocker report a otázku. |
| Licence nové dependency je nejasná nebo riziková | Zapsat dependency blocker a otázku. |
| Daňové/právní pravidlo nelze bezpečně ověřit | Zapsat jako working assumption nebo zastavit, pokud by ovlivnilo výpočet. |
| Codex má učinit obchodní/policy rozhodnutí, které mění riziko uživatele | Zastavit se. |
| Před dokončením MVRS chce Codex přesunout těžiště práce do UI/ML/knowledge base/pokročilého tax exportu | Zapsat scope drift do LOG.md a vrátit se k MVRS. |
| Testy opakovaně selžou a root cause není jasný | Zapsat blocker report. |
| Stejný typ chyby selže po 3 auto-remediation iteracích | Zapsat blocker report a zastavit se. |
| Codex neví, zda má příkaz spustit v host `.venv`, Docker app nebo Docker Freqtrade kontejneru | Zapsat execution-context blocker, nehádat a zastavit se. |
| Codex se blíží usage limitu nebo vidí limit warning | Zastavit rozšiřování scope, zapsat `QUOTA_SAFE_CHECKPOINT`, aktualizovat `PROJECT_STATE.md`, navrhnout commit/resume instructions. |

### 2.4 Co NENÍ hard-stop

Codex se nemá zbytečně ptát v těchto případech:

| Situace | Autonomní postup |
|---|---|
| Chybí drobný pomocný soubor | Vytvořit podle plánu a zapsat do LOG.md |
| Test selhal jasnou chybou implementace | Opravit v repair loopu |
| Freqtrade/CCXT Coinbase data neprojdou paritou, ale Coinbase API data jsou dostupná | Přepnout návrh na Coinbase API jako autoritativní data source a vytvořit ADR |
| Research najde lepší knihovnu se zjevně vhodnou licencí a aktivitou | Provést dependency review, zapsat do registru a pokračovat |
| Strategie neporazí baseline | Označit RESEARCH_ONLY/FAIL, nepouštět live, pokračovat reportovací a infrastrukturně-bezpečnostní částí |
| ML nepřidá robustní edge | Označit ML jako RESEARCH_ONLY a pokračovat |
| Volitelná fáze blokuje MVRS | Označit jako POST_MVRS a pokračovat core fázemi |
| Codex limit přeruší práci po bezpečném checkpointu | Po resetu limitu pokračovat z `PROJECT_STATE.md`, `LOG.md` a posledního Git/diff stavu |
| UI MVP lze udělat bez API klíčů | Implementovat pouze read-only UI nad lokálními daty |
| Tax pravidlo není právně definitivní | Zapsat jako working assumption to verify, nevydávat daňové poradenství |

### 2.5 Auto-remediation pravidla

Codex má preferovat bezpečný fallback před zastavením.

| Problém | Bezpečný fallback |
|---|---|
| Freqtrade/CCXT Coinbase má problém s daty | Coinbase Advanced API downloader jako autoritativní datový zdroj, Freqtrade jen jako engine |
| Chybí 4h data | Agregovat deterministicky z 1h uzavřených svíček |
| Preview API vrací chybu | Zamítnout intent, auditovat, pokračovat bez live exekuce |
| Audit writer selže | Aktivovat kill-switch |
| Reconciliation unknown | Blokovat další intent |
| ML model selže | Vrátit se k baseline strategii |
| Dependency není nutná | Nepřidávat dependency, použít standard library nebo již existující stack |
| UI dependency je zbytečně těžká | Použít jednodušší read-only Streamlit/local report přístup |
| SQLite schema drift v MVP/test/dry-run DB | Pokud je DB označena jako disposable/replayable, vytvořit backup kopii, zapsat do LOG.md, smazat a znovu vytvořit DB. Pokud DB obsahuje hodnotná dry-run/live data, zastavit se nebo provést schválenou migraci. |

### 2.6 Dotazy uživateli — formát

Pokud se Codex zastaví, nesmí položit vágní otázku. Musí uvést:

```markdown
## WAITING_FOR_USER — Phase XX

### Potřebuji
...

### Proč to potřebuji
...

### Architektonický dopad
...

### Možnosti řešení
- Možnost A:
  - Výhody:
  - Rizika:
- Možnost B:
  - Výhody:
  - Rizika:

### Bezpečný způsob doplnění
...

### Co nezasílat do chatu
...

### Co udělám po doplnění
...

### Zápis do LOG.md
- [ ] otázka zapsána do OPEN QUESTIONS
```

---

## 3. Plus-safe usage, quota and persistence policy

Tento projekt je navržen tak, aby byl použitelný i na osobním ChatGPT Plus tarifu. Plus tarif není určený pro neomezený dlouhý autonomní běh bez přerušení; proto musí být práce rozdělena do malých, restartovatelných bloků.

### 3.1 Základní princip

Žádná důležitá práce nesmí existovat pouze v chatu.

Každý významný krok musí být uložen minimálně do:

1. souborů projektu;
2. `LOG.md`;
3. `PROJECT_STATE.md`;
4. ideálně Git commitu nebo alespoň čistého `git diff --stat` záznamu.

Pokud dojde k vyčerpání limitu, pádu session, restartu počítače nebo výpadku služby, další session musí být schopná pokračovat z repozitáře bez rekonstrukce z paměti.

### 3.2 Plus-safe execution mode

Codex nesmí na Plus tarifu plánovat dlouhý „udělej celý projekt najednou“ běh.

Místo toho pracuje v bounded slices:

```text
jeden slice = jedna malá fáze, podfáze nebo jeden jasný acceptance blok
```

Doporučená velikost jednoho slice:

- 1–5 souborů;
- jeden jasný call-flow;
- jedna sada testů;
- jeden LOG checkpoint;
- jeden PROJECT_STATE update;
- jeden navržený commit.

Zakázáno:

- spojit více velkých fází do jednoho běhu;
- spustit dlouhý refaktoring bez předchozího checkpointu;
- držet velký diff bez LOG/PROJECT_STATE zápisu;
- pokračovat do dalšího velkého bloku, pokud se blíží usage limit;
- nechávat rozpracovaný projekt jen v odpovědi modelu.

### 3.3 Quota-aware checkpoint

Codex musí vytvořit quota-safe checkpoint:

- před každým dlouhým testem;
- před každým backtestem;
- před každým refaktoringem;
- po každé větší změně souborů;
- při jakémkoliv upozornění na limit;
- před ukončením odpovědi.

Formát:

```markdown
### QUOTA_SAFE_CHECKPOINT — YYYY-MM-DD HH:MM — Phase XX
Current slice:
Files changed:
Tests run:
Git status:
Recommended commit message:
Next deterministic command:
Resume instructions:
```

### 3.4 Git persistence policy

Codex má po každém dokončeném slice navrhnout commit.

Commit smí provést pouze pokud:

- pracovní strom neobsahuje secrets;
- testy pro daný slice prošly nebo je výjimka výslovně zapsaná;
- `LOG.md` a `PROJECT_STATE.md` jsou aktualizované;
- commit message je krátká a fázově označená.

Doporučený formát:

```text
phase-00b: add package skeleton and CLI baseline
phase-05b: add minimal guard core
phase-03b: add data parity gate
```

Pokud Codex commit neprovede, musí alespoň zapsat:

```powershell
# [HOST_POWERSHELL]
git status
git diff --stat
```

do `LOG.md`.

### 3.5 Usage-limit hard-stop

Pokud Codex vidí limit banner, usage warning, nebo má důvod čekat, že limit doběhne během aktuální práce, musí:

1. přestat rozšiřovat scope;
2. dokončit nebo bezpečně zahodit právě rozpracovaný malý krok;
3. zapsat `QUOTA_SAFE_CHECKPOINT`;
4. aktualizovat `PROJECT_STATE.md`;
5. navrhnout commit nebo uložit diff;
6. vypsat přesné resume instructions.

Codex nesmí při blížícím se limitu začít novou fázi.

### 3.6 Model-tiering policy

Pro Plus tarif platí:

| Typ úkolu | Doporučení |
|---|---|
| architektura, bezpečnost, guard layer, tax, reconciliation | používat nejsilnější dostupný reasoning/coding režim |
| rutinní opravy importů, formátování, drobné testy | použít levnější/menší dostupný model, pokud Codex UI/CLI umožňuje volbu |
| dlouhý research | rozdělit na malé research reporty |
| velké refaktory | nejdřív plán + checkpoint, potom implementace po blocích |
| UI kosmetika | POST_MVRS, nízká priorita |

### 3.7 No-project-loss guarantee

Projekt se považuje za bezpečně restartovatelný pouze pokud existuje:

- `CODEX_MASTER_PLAN.md`;
- `AGENTS.md`;
- `LOG.md`;
- `PROJECT_STATE.md`;
- aktuální soubory projektu na disku;
- `git status` známý v posledním checkpointu;
- poslední bezpečný další příkaz.

Pokud některý z těchto bodů chybí, Codex musí před další implementací nejdřív obnovit restartovatelnost.

---

## 4. LOG.md jako jediný zdroj pravdy

`LOG.md` je append-only pracovní deník. Codex ho musí aktualizovat při každé fázi a každém blockeru.

### 4.1 Struktura LOG.md

```markdown
# PROJECT LOG — coinbase_freqtrade_guarded_bot

## STATUS SUMMARY
Aktuální fáze: <číslo a název>
Aktivní agent: <jméno agenta>
Poslední aktualizace: <YYYY-MM-DD HH:MM>
Stav: TODO | IN_PROGRESS | WAITING_FOR_USER | BLOCKED | DONE
Aktuální branch:
Aktuální commit:
Poznámka:

## OPEN QUESTIONS
- [ ] <datum> <fáze> — <otázka pro uživatele> (čeká na odpověď)
- [x] <datum> <fáze> — <otázka> → ODPOVĚĎ: <odpověď> <datum odpovědi>

## PHASE TRACKER
| Fáze | Název | Stav | Datum dokončení | Poznámka |
|---|---|---|---|---|
| 00 | Repository bootstrap | TODO | — | — |
| 01 | Development environment | TODO | — | — |

## DEPENDENCY REGISTER
| Package | Version | License | Reason | Added in phase | Review date | Security status | Lock status |
|---|---|---|---|---|---|---|---|

## DECISION REGISTER
| ADR | Rozhodnutí | Datum | Stav |
|---|---|---|---|

## ENTRIES

### YYYY-MM-DD HH:MM — Phase XX — <agent>
**Akce:**  
**Přečtené soubory:**  
**Upravené soubory:**  
**Spuštěné příkazy:**  
**Testy:**  
**Research:**  
**Rozhodnutí:**  
**Výsledek:** DONE / PARTIAL / BLOCKED / WAITING_FOR_USER  
**Další krok:**  
```

### 4.2 Pravidla zápisu

- `STATUS SUMMARY` se aktualizuje vždy.
- Historie se nepřepisuje, jen doplňuje.
- Každý blocker má přesný důvod.
- Každá otázka pro uživatele jde do `OPEN QUESTIONS`.
- Každá odpověď uživatele se zapíše k otázce.
- Každý nový balíček jde do `DEPENDENCY REGISTER`.
- Každé architektonické rozhodnutí jde do `DECISION REGISTER` a `docs/adr/`.

### 4.3 Context compaction and log archive policy

`LOG.md` musí zůstat použitelný jako pracovní kontext pro Codex. Chronologická historie nesmí nekontrolovaně růst tak, aby vytlačila hlavní instrukce z kontextového okna. Současně se nesmí ztratit auditní stopa.

Proto platí:

- `STATUS SUMMARY`, `OPEN QUESTIONS`, `PHASE TRACKER`, `DECISION REGISTER` a `DEPENDENCY REGISTER` zůstávají vždy v hlavním `LOG.md`.
- Detailní `ENTRIES` pro aktuální a předchozí 3 fáze zůstávají v hlavním `LOG.md`.
- Starší detailní záznamy se nesmí destruktivně mazat. Přesunou se do archivního souboru ve složce `logs/archive/`, například `logs/archive/LOG_ENTRIES_PHASE_00_03.md`.
- V hlavním `LOG.md` zůstane krátké shrnutí archivovaných fází v sekci `ARCHIVED SUMMARY`.
- Každý archivní soubor musí mít zapsaný SHA-256 hash a rozsah fází, které obsahuje.
- Codex musí před začátkem nové session číst primárně `STATUS SUMMARY`, `OPEN QUESTIONS`, `PHASE TRACKER`, `DECISION REGISTER`, `DEPENDENCY REGISTER` a poslední checkpoint. Archiv otevírá pouze tehdy, pokud aktuální úkol vyžaduje historický detail.
- Jakmile hlavní `LOG.md` překročí přibližně 800 řádků nebo sekce `ENTRIES` obsahuje více než 3 dokončené fáze, Codex vytvoří nebo aktualizuje archiv.

Doporučený soubor pro rychlé navázání:

```text
PROJECT_STATE.md
```

`PROJECT_STATE.md` je krátký pracovní souhrn: aktuální fáze, poslední PASS/FAIL, otevřené otázky, poslední rozhodnutí, další bezpečný krok. Nesmí nahrazovat `LOG.md`; slouží pouze ke snížení kontextové zátěže.


---

## 5. AGENTS.md — pracovní role Codexu

Codex vytvoří a udržuje soubor `AGENTS.md`.

### 5.1 Povinný obsah `AGENTS.md`

```markdown
# AGENTS.md

## Role
Jsi senior Python engineer, kvantitativní analytik, bezpečnostně orientovaný architekt a DevOps inženýr.

## Projekt
coinbase_freqtrade_guarded_bot je research/dry-run crypto trading systém pro Coinbase.

## Tvrdé limity
- No live trading in MVP.
- No real API keys.
- No secrets.
- No leverage.
- No futures.
- No shorts.
- Spot BTC/ETH only.
- Fail closed when uncertain.
- Never create or send live orders.
- Never commit secrets.
- Never claim guaranteed profit.

## Work mode
- Read CODEX_MASTER_PLAN.md first.
- Read LOG.md before any action.
- Read full relevant files before editing.
- Stay inside current phase scope.
- Update LOG.md after each action.
- Add tests for behavioral changes.
- Stop and ask only if hard-stop user input is required.
- Use research protocol for technical uncertainty.
- Use phase gates before moving forward.

## Code style
- Use Python 3.11+.
- Prefer readable, typed, testable code over clever code.
- Every public module has a module docstring.
- Every public function/class/method has type hints.
- Public functions/classes have concise docstrings.
- Domain entities use dataclasses or Pydantic models, not unstructured dicts.
- One module has one clear responsibility.
- No god files.
- No magic constants without named constants/config.
- No print statements in business logic.
- Use structured logging.
- Use domain-specific exceptions.
- New behavior requires tests.
- Critical math, Guard and Tax functions require deterministic unit tests; target full branch coverage for these critical functions.
- Application logic belongs under `src/coinbase_freqtrade_guarded_bot/`, not in ad-hoc scripts.
- Every shell command must declare its execution context: `[HOST_POWERSHELL]`, `[LOCAL_VENV]`, `[DOCKER_APP]`, or `[DOCKER_FREQTRADE]`.
- Work in Plus-safe slices; never leave important work only in chat.
- Before usage limits or long tasks, write `QUOTA_SAFE_CHECKPOINT` and update `PROJECT_STATE.md`.
```

### 5.2 Agenti

| Agent | Aktivní fáze | Odpovědnost |
|---|---|---|
| `architect-agent` | 00, 02, 04 | struktura, ADR, dokumentace, scope |
| `sre-agent` | 01, 02, 08, 08b | Docker, provoz, monitoring, execution context, command catalog |
| `data-agent` | 03, 03b, 04 | data, Coinbase/CCXT validace, kvalita dat |
| `strategy-agent` | 05, 15 | strategie, Freqtrade, FreqAI research |
| `quant-research-agent` | 06, 07, 15 | backtesting, validace, overfitting, metriky |
| `guard-agent` | 09, 10, 10b, 11, 17, 18 | risk, audit, kill-switch, preview, reconciliation |
| `tax-agent` | 12 | daňová evidence, exporty, FIFO/ledger |
| `ui-agent` | 13 | enterprise dashboard, auditní UI |
| `research-agent` | 14 | research update loop, dependency review |
| `knowledge-agent` | 16 | znalostní báze úspěšných crypto traderů, obchodní playbooky, risk checklisty |

---

## 6. Projektové skilly

Codex vytvoří složku:

```text
docs/skills/
```

Skill soubory jsou kumulativní znalostní báze projektu. Nejsou to logy. Každý nový poznatek se zapisuje s datem a zdrojem.

### 6.1 Povinné skill soubory

```text
docs/skills/freqtrade_coinbase_ccxt.md
docs/skills/coinbase_auth.md
docs/skills/backtest_validation.md
docs/skills/freqai_practices.md
docs/skills/risk_engine.md
docs/skills/reconciliation.md
docs/skills/cz_tax_rules.md
docs/skills/ui_patterns.md
docs/skills/algorithm_review.md
docs/skills/dependency_review.md
docs/skills/crypto_trader_knowledge.md
docs/skills/coding_standards.md
docs/skills/packaging_app_architecture.md
docs/skills/execution_context.md
docs/skills/network_resilience.md
docs/skills/db_schema_migrations.md
docs/skills/test_quality_gates.md
docs/skills/codex_usage_budget.md
```

### 6.2 Minimální struktura skill souboru

```markdown
# <skill name>

## Purpose
...

## Current conclusions
...

## Findings
### YYYY-MM-DD — <topic>
Source:
- ...

Summary:
...

Decision impact:
...

Open questions:
...
```

---

## 7. Research protokol

Codex nesmí hádat technická fakta. Pokud je nejistota, použije research protokol.

### 7.1 Priorita zdrojů

| Typ otázky | Primární zdroje |
|---|---|
| Coinbase API | Coinbase official docs, coinbase-advanced-py GitHub, StackOverflow |
| Freqtrade | Freqtrade docs, Freqtrade GitHub issues |
| CCXT | CCXT docs, CCXT GitHub issues |
| Hummingbot/Jesse/OctoBot srovnání | official docs, GitHub issues, komunitní zkušenosti |
| ML/trading validace | FreqAI docs, sklearn, LightGBM/XGBoost docs, López de Prado, Ernest Chan, QuantConnect |
| UI | FreqUI, Streamlit, FastAPI, React dashboard patterns |
| Tax | aktuální české právní/daňové zdroje, odborné články, daňový poradce; Codex nesmí tvrdit definitivní právní závěr bez ověření |
| Algorithm validation | oficiální dokumentace knihoven, akademické zdroje, benchmark implementace, GitHub issues, quant literatura |
| Crypto trader knowledge | veřejné rozhovory, ověřitelné zdroje, knihy, blogy, podcasty, veřejné post-mortemy; nepřebírat signály bez validace |

### 7.2 GitHub / Reddit / GitLab pravidla

- GitHub issue = důkaz reálného problému nebo workaroundu, ne nutně obecné pravidlo.
- Reddit = zkušenostní signál, ne autoritativní zdroj.
- GitLab = sekundární zdroj; často mirror, ale ověřit, pokud je relevantní.
- Oficiální dokumentace = primární zdroj pro API a config.
- Akademický/quant zdroj = primární zdroj pro validaci metodiky.
- Recenze a hvězdy nejsou důkaz ziskovosti.
- Strategie se nepřebírá jen proto, že ji někdo chválí.

### 7.2a MIT-first active search policy

Při hledání nové knihovny, frameworku, referenční implementace nebo algoritmického řešení musí Codex aktivně preferovat řešení s otevřenou a kompatibilní licencí už během research fáze, ne až po výběru dependency.

Pořadí preferencí:

1. Python standard library nebo vlastní jednoduchá implementace, pokud je bezpečná a auditovatelná.
2. Oficiální knihovna/API klient dané služby.
3. Aktivně udržované projekty s MIT / Apache-2.0 / BSD licencí.
4. GPL projekty pouze při vědomém rozhodnutí a zápisu dopadu do LOG.md / ADR.
5. Neudržované, nejasně licencované nebo marketingově podezřelé projekty nepoužívat.

Při srovnání kandidátů Codex hodnotí:

- licence;
- aktivita commitů;
- stáří posledního releasu;
- počet a stáří otevřených issues;
- security advisories;
- kvalita dokumentace;
- test coverage, pokud je zjistitelná;
- používání v komunitě;
- GitHub stars pouze jako slabý signál popularity;
- kompatibilita s Python/Docker stackem projektu;
- možnost nahradit dependency jednodušším vlastním kódem.

Výstup MIT-first research musí být zapsán do `reports/research/` a shrnut v `docs/skills/dependency_review.md`.

### 7.3 Výstup research

Každý research report se ukládá do:

```text
reports/research/YYYY-MM-DD_<topic>.md
```

Report musí obsahovat:

```markdown
# Research report — <topic>

## Question
...

## Sources
| Source | Type | Relevance | Notes |
|---|---|---|---|

## Findings
...

## Risks
...

## Recommendation
...

## What not to implement
...

## Impact on architecture
...

## Follow-up questions
...
```

---

## 8. Dependency review policy

Codex nesmí přidat dependency bez review.

### 8.1 Před přidáním dependency musí Codex zapsat

- název balíčku;
- verzi;
- licenci;
- důvod použití;
- alternativy;
- bezpečnostní rizika;
- aktivitu projektu;
- dopad na Docker image;
- zda je balíček nutný v runtime nebo jen dev;
- zápis do `LOG.md`;
- zápis do `DEPENDENCY REGISTER`.
- způsob pinningu / lockování runtime prostředí.

### 8.1a Dependency pinning and lock policy

Rozlišuj dvě vrstvy závislostí:

1. **Project metadata v `pyproject.toml`** — zde mohou být rozumné kompatibilní rozsahy, pokud jde o knihovní metadata. Nepoužívat zbytečně tvrdé exact piny v package metadata, pokud by to bránilo instalaci nebo testování.
2. **Reprodukovatelné runtime prostředí** — zde musí být konkrétně zamčené verze všech přímých i tranzitivních závislostí.

Povinné soubory pro reprodukovatelnost:

```text
requirements.lock
requirements-dev.lock
constraints.txt
```

Pravidla:

- Runtime a dev prostředí musí mít exact piny ve formátu `package==X.Y.Z` v lock/requirements souboru.
- Volné specifikace typu `package>=X` nesmí být použity v lock souboru.
- Kompatibilní rozsah `package~=X.Y` je přípustný pouze v abstraktní vrstvě `pyproject.toml`, ne jako finální runtime lock.
- Před aktualizací dependency musí Codex vytvořit research/dependency review záznam a spustit relevantní testy.
- Pokud nástroj podporuje hash checking nebo lock file, preferovat ho pro automatizované prostředí.
- Codex musí do `DEPENDENCY REGISTER` zapsat, zda je dependency pinovaná v lock souboru, a kdy byla naposledy ověřena.

Doporučený postup:

```bash
python -m pip install -e .
python -m pip freeze > requirements.lock
python -m pip check
```

Pokud bude zaveden `pip-tools` nebo jiný lockovací nástroj, musí projít dependency review.


### 8.1b Bootstrap minimal dependency policy

Phase 00b nesmí přidat zbytečný stack.

Povolený bootstrap/dev stack:

- `hatchling` nebo `setuptools`;
- `pytest`;
- `pytest-cov`;
- `pytest-socket`;
- `ruff`;
- `pydantic` / `pydantic-settings`, pokud už existují config/domain modely;
- `mypy` nebo `pyright` pouze jako quality gate, pokud nezdržuje MVRS.

Odložené dependency:

- `tenacity`: přidat až při implementaci network resilience v Phase 03b/08b;
- `SQLModel`: přidat až pokud JSONL/SQLite nestačí a existuje ADR;
- `Alembic`: přidat až při zavedení SQLModel/SQLAlchemy migrací;
- `LightGBM`, `XGBoost`, FreqAI extras: až Phase 15;
- UI extras: až Phase 13.

Každá odložená dependency musí mít explicitní reason v LOG.md, proč už je opravdu potřeba.

### 8.2 Preferované licence

Preferovat:

- MIT,
- Apache-2.0,
- BSD.

Akceptovatelné s vědomím dopadů:

- GPLv3, pokud je to rámec typu Freqtrade a projekt zůstává interní.

Nejasné licence = zastavit a zeptat se.

---

## 9. Algorithm validation policy

Codex musí při návrhu nebo úpravě algoritmu ověřit, že metoda je správná, vhodná a že neexistuje zjevně lepší současný postup.

### 9.1 Co se považuje za algoritmus

- obchodní strategie;
- indikátor;
- feature engineering;
- risk výpočet;
- position sizing;
- stop-loss / take-profit logika;
- backtest metrika;
- walk-forward validace;
- Monte Carlo simulace;
- ML model;
- FreqAI model;
- tax/FIFO výpočet;
- reconciliation pravidlo;
- data aggregation pravidlo.

### 9.1a Causal feature and time-series validation policy

Codex musí u všech trading/ML funkcí vynutit kauzalitu dat.

Povinné:

- žádná funkce nesmí přistupovat k budoucím svíčkám;
- všechny predikční features musí být dostupné v okamžiku rozhodnutí;
- labely mohou používat budoucí pohyb pouze jako trénovací target a musí být oddělené od features;
- testy musí ověřit, že feature matice neobsahuje sloupce vytvořené z budoucnosti;
- pro ML validaci je zakázané náhodné `KFold` dělení bez časové osy;
- používat chronologický split, walk-forward, `TimeSeriesSplit` nebo purged/gap split podle typu labelu;
- u indikátorů založených na OHLCV používat pouze uzavřené svíčky;
- pokud agregujeme 1h → 4h, agregace musí být deterministická a nesmí obsahovat neuzavřenou svíčku;
- chybějící OHLCV svíčky se nesmí slepě interpolovat; buď se doplní z autoritativního nižšího timeframe, nebo Data Quality Gate vrátí WARN/FAIL.

Stacionarita:

- hrubé ceny se nesmí bez Algorithm Review používat jako přímý vstup do regresních/ML modelů;
- preferovat výnosy, logaritmické výnosy, normalizované vzdálenosti od trendu nebo jiné kauzální transformace;
- ADF test je povolený nástroj, ale ne jediný gate;
- nepoužívat jednu tvrdě zakódovanou hranici test statistic typu `ADF < -3.4`; vyhodnocovat p-hodnotu a kritické hodnoty z použité implementace;
- frakcionální diferenciace je research-only kandidát, ne povinný krok pro MVP.

### 9.2 Povinný Algorithm Review

Před použitím nového algoritmu musí Codex vytvořit nebo aktualizovat:

```text
docs/skills/algorithm_review.md
```

a podle významnosti také:

```text
reports/research/YYYY-MM-DD_algorithm_<topic>.md
```

Review musí obsahovat:

- název algoritmu/metody;
- účel;
- vstupy a výstupy;
- matematický popis nebo pseudokód;
- předpoklady;
- známé slabiny;
- možné lepší alternativy;
- důvod výběru;
- testy správnosti;
- benchmark proti baseline;
- out-of-sample ověření, pokud jde o obchodní/ML metodu;
- odkaz na zdroje.

### 9.3 Povinné porovnání s baseline

Žádný sofistikovaný algoritmus nesmí být přijat, pokud není porovnán proti jednodušší baseline.

Příklady:

| Oblast | Baseline |
|---|---|
| Trading strategy | buy-and-hold, jednoduchý trend-following |
| ML model | logistic regression / simple tree |
| Feature set | returns + volatility + volume |
| Risk sizing | fixed fractional risk |
| Backtest validation | jednoduchý out-of-sample split |
| Tax calculation | ručně ověřený FIFO příklad |

### 9.4 Stop pravidlo

Codex se zastaví, pokud:

- metoda vypadá sofistikovaně, ale není jasné, proč by měla fungovat;
- metoda zlepšuje backtest, ale zhoršuje out-of-sample;
- metoda má riziko data leakage;
- metoda je převzatá bez jasné licence;
- metoda vyžaduje live data nebo live trading;
- existuje rozpor mezi zdroji a Codex neví, co je správně.


---

## 10. Coding standards and package architecture

Tato sekce je závazná pro všechny fáze. Codex nesmí produkovat vibecoded směs skriptů. Vlastní aplikační logika musí být strukturovaná jako instalovatelný Python balíček.

### 10.1 Python coding standards

Povinná pravidla:

- Python 3.11+.
- Každý modul má modulový docstring s účelem modulu.
- Každá veřejná funkce/metoda/třída má type hints.
- Každá veřejná funkce/metoda/třída má stručný docstring.
- Interní helper funkce mají type hints; docstring pouze pokud logika není zřejmá.
- Domain modely nepoužívat jako volné `dict`/`tuple`; použít `dataclasses` nebo Pydantic modely.
- Jedna třída/modul = jedna odpovědnost.
- Žádné „god files“ s nesouvisející logikou.
- Žádné magické konstanty; použít pojmenované konstanty nebo config.
- Žádné `print()` v business logice; použít strukturovaný logger.
- Žádné obecné `except Exception` bez zdůvodnění a auditního zápisu.
- Chyby modelovat pomocí doménových výjimek.
- IO vrstva a business logika musí být oddělené.
- Funkce pro výpočty mají být deterministické a testovatelné bez sítě.
- Veškerý kód, který mění rozhodovací logiku, vyžaduje test.
- Kritické funkce ve vrstvách Guard, Reconciliation, Data Parity, Backtest Metrics a Tax/FIFO musí mít deterministické unit testy včetně edge cases.

### 10.2 Modelovací pravidla

| Oblast | Doporučený přístup |
|---|---|
| Env/config validation | Pydantic / pydantic-settings |
| Doménové immutable objekty | `@dataclass(frozen=True)` nebo Pydantic frozen model |
| API request/response schema | Pydantic model |
| Audit event | Pydantic/dataclass + explicitní JSON serializer |
| Výpočtové funkce | čisté funkce s typy |
| Risk/reconciliation decision | explicitní result object, ne bool bez důvodu |
| Tax ledger entry | dataclass/Pydantic model s validací |

### 10.3 Package layout

Vlastní aplikační kód má být pod `src/coinbase_freqtrade_guarded_bot/`.

Doporučené rozložení:

```text
src/
└── coinbase_freqtrade_guarded_bot/
    ├── __init__.py
    ├── cli.py
    ├── config/
    ├── data_layer/
    ├── guard_layer/
    ├── tax_layer/
    ├── reporting/
    ├── research/
    ├── ui_support/
    └── utils/
```

Freqtrade runtime složka `user_data/` zůstává mimo package, protože je to Freqtrade convention. Strategie ve `user_data/strategies/` smí importovat pomocné validované funkce z package.

### 10.4 pyproject.toml a CLI

Projekt musí mít funkční `pyproject.toml`.

Doporučený default stack pro vlastní aplikační vrstvu:

- build backend: `hatchling` jako default; `setuptools` je akceptovatelná alternativa po ADR;
- formatting/linting: `ruff`;
- tests: `pytest`;
- typing: `mypy` nebo `pyright` jako quality gate podle fáze;
- config/schema validation: `pydantic` v2 a případně `pydantic-settings`;
- storage MVP: append-only JSONL + SQLite; SQLModel pouze po dependency review a ADR, pokud JSONL/SQLite nestačí.

Povinné:

```bash
pip install -e .
python -m coinbase_freqtrade_guarded_bot --help
pytest
ruff check .
```

Doporučené podle fáze:

```bash
mypy src
```

Povinné CLI entry pointy nejpozději po Phase 00b/07:

```toml
[project.scripts]
cbot-data-parity = "coinbase_freqtrade_guarded_bot.cli:data_parity"
cbot-backtest-report = "coinbase_freqtrade_guarded_bot.cli:backtest_report"
cbot-dryrun-healthcheck = "coinbase_freqtrade_guarded_bot.cli:dryrun_healthcheck"
cbot-tax-export = "coinbase_freqtrade_guarded_bot.cli:tax_export"
```

CLI nesmí mít live execution příkaz v MVP.

### 10.5 Quality gates

Codex musí udržovat minimálně:

- `pytest`;
- `ruff check .`;
- import smoke test;
- no-secrets grep/smoke test;
- offline unit-test gate přes `pytest-socket --disable-socket`.

Network sanity gate:

- Unit testy mají defaultně zakázané sockety přes `pytest-socket`.
- Testy, které potřebují síť, musí být explicitně označené jako integration tests a nesmí běžet v defaultním unit-test příkazu.
- Coinbase/API SDK volání v unit testech musí být mockovaná.
- Výjimky pro localhost/Unix socket jsou povolené jen s komentářem a test markerem.

Coverage policy:

- Phase 00b zavádí `pytest-cov` jako dev dependency po dependency review.
- Od Phase 05b musí běžet `pytest --cov=src --cov-branch --cov-fail-under=85`, pokud již existuje dost netriviálního aplikačního kódu.
- V Phase 05b–07 je povinný fallback `critical paths only`: testovat hlavně Guard Core, Data Parity a Backtest Metrics edge cases, i když globální coverage ještě není reprezentativní.
- Kritické vrstvy `guard_layer`, `data_layer/data_parity`, `tax_layer`, `reconciliation` a `research/metrics` musí mít cílově 95 %+ branch coverage před Phase 17.
- Pokud per-module coverage nejde vynutit samotným pytest-cov, Codex vytvoří `scripts/check_critical_coverage.py`, který čte coverage JSON a ověří kritické prahy.
- Triviální test bez edge cases nesmí splnit acceptance kritéria kritické fáze.

Mypy/pyright je doporučený; pokud by zdržoval bootstrap, Codex ho může označit jako later quality gate, ale musí to zapsat do LOG.md.

### 10.5a Document completeness check

Phase 00b musí ověřit, že všechny nové řídicí sekce mají odpovídající dokumenty a skills.

Minimální kontrola:

| Sekce | Dokument | Skill |
|---|---|---|
| Coding standards | `docs/CODING_STANDARDS.md` | `docs/skills/coding_standards.md` |
| Packaging | `docs/PACKAGING.md` | `docs/skills/packaging_app_architecture.md` |
| Execution context | `docs/EXECUTION_CONTEXT.md` | `docs/skills/execution_context.md` |
| Network resilience | `docs/NETWORK_RESILIENCE.md` | `docs/skills/network_resilience.md` |
| DB schema policy | `docs/DB_SCHEMA_POLICY.md` | `docs/skills/db_schema_migrations.md` |
| Test quality gates | `docs/TEST_QUALITY_GATES.md` | `docs/skills/test_quality_gates.md` |
| Codex usage policy | `docs/CODEX_USAGE_POLICY.md` | `docs/skills/codex_usage_budget.md` |

Codex musí zapsat výsledek kontroly do `LOG.md` a `PROJECT_STATE.md`.

### 10.6 Zakázané coding patterns

- ad-hoc `sys.path.append(...)`;
- importy závislé na aktuálním pracovním adresáři;
- nevalidované globální proměnné pro config;
- přímé čtení `.env` uvnitř business logiky;
- tiché selhání bez auditního zápisu;
- `dict` jako náhrada doménového modelu;
- live/execution side effect v import-time kódu;
- síťové volání v unit testu bez mocku;
- obchodní rozhodnutí v UI vrstvě.


---

## 11. Execution context and command policy

Codex nesmí hádat, kde se má příkaz spouštět. Každý příkaz v odpovědi, LOGu, RUNBOOKu nebo promptu musí být označen jedním z těchto kontextů:

| Kontext | Použití |
|---|---|
| `[HOST_POWERSHELL]` | operace s Git repozitářem, složkami, Docker commandy na Windows hostu |
| `[LOCAL_VENV]` | lokální Python package, pytest, ruff, mypy, CLI app commands |
| `[DOCKER_APP]` | app container, pokud existuje samostatný kontejner pro vlastní Python aplikaci |
| `[DOCKER_FREQTRADE]` | Freqtrade CLI, Freqtrade config validation, Freqtrade backtest/dry-run commands |

### 11.1 Canonical command catalog

Phase 00b musí vytvořit minimálně jeden z těchto nástrojů:

- `Makefile`, pokud je dostupný make;
- `scripts/dev.ps1` jako Windows-first fallback;
- `docs/RUNBOOK.md` s command catalogem.

Preferované příklady:

```powershell
# [HOST_POWERSHELL]
docker compose config

# [LOCAL_VENV]
python -m pytest

# [LOCAL_VENV]
python -m ruff check .

# [LOCAL_VENV]
python -m coinbase_freqtrade_guarded_bot --help

# [DOCKER_FREQTRADE]
docker compose run --rm freqtrade list-exchanges

# [DOCKER_FREQTRADE]
docker compose run --rm freqtrade backtesting --config user_data/config/config.backtest.json
```

### 11.2 Source package import policy for Freqtrade Docker

Freqtrade strategie v `user_data/strategies/` mohou importovat pouze validované pomocné funkce a modely z package `coinbase_freqtrade_guarded_bot`.

Zakázáno:

- `sys.path.append(...)`;
- kopírování zdrojových souborů do `user_data/strategies/`;
- duplicitní definice `OrderIntent`, `RiskDecision`, `settings` nebo guard modelů ve strategii;
- import-time side effects.

Povolený dev/MVRS způsob:

```yaml
# [DOCKER_FREQTRADE] docker-compose.yml — dev only
services:
  freqtrade:
    volumes:
      - ./user_data:/freqtrade/user_data
      - ./src:/freqtrade/src:ro
    environment:
      PYTHONPATH: /freqtrade/src
```

Povolený pozdější production-like způsob:

```text
custom Freqtrade image
→ install package wheel / regular install
→ no editable bind mount
```

Acceptance:

- Phase 02 musí obsahovat Docker import smoke test:
  `python -c "import coinbase_freqtrade_guarded_bot"`.
- Strategy import test musí ověřit, že `user_data/strategies/CoinbaseTrendGuardV1.py` umí importovat package bez `sys.path.append`.
- Pokud import v Dockeru selže, Codex nesmí problém řešit hackem; musí opravit compose/PYTHONPATH nebo package install.

### 11.3 Environment ownership

| Artefakt | Vlastník prostředí |
|---|---|
| `src/coinbase_freqtrade_guarded_bot/` | lokální `.venv` / app container |
| `tests/` | lokální `.venv` / CI |
| `user_data/` | Freqtrade container |
| `docker-compose.yml` | host Docker |
| `reports/` | sdílený výstup, generovaný z CLI nebo kontejnerů |
| `.env` | lokální host, nikdy commit |

### 11.4 Stop rule

Pokud Codex neví, kde se má příkaz spustit, nesmí pokračovat odhadem. Musí:

1. zapsat execution-context blocker do `LOG.md`;
2. uvést možné kontexty;
3. navrhnout bezpečný default;
4. zastavit se, pokud by špatný kontext mohl změnit prostředí, data nebo instalace.


---

## 12. Network I/O, rate limiting and retry policy

Všechny síťové operace vůči Coinbase, CCXT, Freqtrade API nebo externím zdrojům musí být oddělené od business logiky.

### 12.1 Povinná pravidla

- Každé HTTP/API volání musí mít explicitní timeout.
- Každé retry musí mít horní limit pokusů a celkový deadline.
- HTTP 429 musí respektovat `Retry-After`, pokud je dostupný.
- HTTP 5xx/503 a dočasné síťové chyby používají exponenciální backoff s jitterem.
- 401/403 se neretryuje donekonečna; jde o auth/policy problém a vede na fail-closed / WAITING_FOR_USER podle fáze.
- Síťové volání nesmí běžet v import-time kódu.
- Unit testy nesmí provádět reálné síťové volání.
- Dlouhé data downloady běží přes CLI/worker a zapisují checkpointy.
- Kill-switch a audit nesmí čekat na dlouhé network downloady ve stejném vlákně/procesu.

### 12.2 Sync vs async policy

MVRS default je synchronní klient s timeouty, retry/backoff a bounded concurrency. Async I/O není povinné pro MVP.

Async (`asyncio`, `aiohttp`, async SDK) je povoleno pouze pokud:

- existuje ADR;
- existuje jasný důvod, proč synchronní bounded klient nestačí;
- jsou testy na cancellation, timeout a retry;
- kill-switch není blokovaný čekáním na síť;
- complexity nepřesune projekt mimo MVRS.

### 12.3 Tenacity/backoff dependency policy

`tenacity` je povolený kandidát pro retry/backoff vrstvu, protože podporuje stop podmínky, wait strategie, exponenciální backoff, jitter a retry pro coroutines. Přesto musí projít dependency review a pinning policy.

### 12.4 Acceptance

Síťová vrstva musí mít testy pro:

- 429 + Retry-After;
- 503 + retry;
- timeout;
- auth 401 bez nekonečného retry;
- bounded retry count;
- audit záznam retry/fail;
- fail-closed po překročení deadline.


---

## 13. Cílová architektura

```text
coinbase_freqtrade_guarded_bot/
│
├── CODEX_MASTER_PLAN.md
├── AGENTS.md
├── LOG.md
├── PROJECT_STATE.md
├── README.md
├── .env.example
├── .gitignore
├── docker-compose.yml
├── docker-compose.freqai.yml
├── requirements-dev.txt
├── requirements.lock
├── requirements-dev.lock
├── constraints.txt
├── pyproject.toml
├── Makefile
│
├── src/
│   └── coinbase_freqtrade_guarded_bot/
│       ├── __init__.py
│       ├── cli.py
│       ├── config/
│       ├── network/
│       ├── storage/
│       ├── data_layer/
│       ├── guard_layer/
│       ├── tax_layer/
│       │   └── migrations/
│       ├── reporting/
│       ├── research/
│       ├── ui_support/
│       └── utils/
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── RUNBOOK.md
│   ├── RISK_POLICY.md
│   ├── KILL_SWITCH.md
│   ├── DATA_SOURCE_POLICY.md
│   ├── COINBASE_SECURITY.md
│   ├── RECONCILIATION.md
│   ├── TAX_REPORTING.md
│   ├── RESEARCH_POLICY.md
│   ├── CODING_STANDARDS.md
│   ├── PACKAGING.md
│   ├── EXECUTION_CONTEXT.md
│   ├── NETWORK_RESILIENCE.md
│   ├── DB_SCHEMA_POLICY.md
│   ├── TEST_QUALITY_GATES.md
│   ├── CODEX_USAGE_POLICY.md
│   ├── ALGORITHM_VALIDATION.md
│   ├── TRADER_KNOWLEDGE_BASE.md
│   ├── UI_SPEC.md
│   ├── PHASE_GATE.md
│   ├── PROJECT_STATE.md
│   ├── LIVE_TRADING_CHECKLIST.md
│   ├── ML_RESEARCH_NOTES.md
│   ├── TAX_NOTES_CZ.md
│   ├── adr/
│   │   ├── ADR-001-coinbase-key-type.md
│   │   ├── ADR-002-data-source-policy.md
│   │   ├── ADR-003-freqtrade-vs-custom-engine.md
│   │   ├── ADR-004-ui-stack.md
│   └── skills/
│       ├── freqtrade_coinbase_ccxt.md
│       ├── coinbase_auth.md
│       ├── backtest_validation.md
│       ├── freqai_practices.md
│       ├── risk_engine.md
│       ├── reconciliation.md
│       ├── cz_tax_rules.md
│       ├── ui_patterns.md
│       └── dependency_review.md
│
├── user_data/
│   ├── config/
│   │   ├── config.backtest.json
│   │   ├── config.dryrun.json
│   │   ├── config.freqai.json
│   │   └── pairlist.json
│   ├── strategies/
│   │   ├── CoinbaseTrendGuardV1.py
│   │   └── CoinbaseFreqAIResearchV1.py
│   ├── freqaimodels/
│   ├── data/
│   ├── logs/
│   └── freqtrade.db
│
├── scripts/
│   ├── dev.ps1
│   ├── bootstrap_project.py
│   ├── compare_coinbase_data_sources.py
│   ├── run_backtest_report.py
│   ├── run_dryrun_healthcheck.py
│   ├── export_tax_report.py
│   └── research_update.py
│
├── knowledge_base/
│   ├── crypto_traders/
│   ├── strategy_patterns/
│   └── risk_playbooks/
│
├── logs/
│   └── archive/
│
├── reports/
│   ├── research/
│   ├── data_parity/
│   ├── backtests/
│   ├── dryrun/
│   ├── audits/
│   ├── tax/
│   └── ui_mockups/
│
├── ui/
│   ├── README.md
│   ├── streamlit_app.py
│   └── pages/
│       ├── 01_Dashboard.py
│       ├── 02_Backtests.py
│       ├── 03_Dry_Run.py
│       ├── 04_Audit_Log.py
│       ├── 05_Tax_Ledger.py
│       ├── 06_Risk.py
│       └── 07_Research.py
│
└── tests/
    ├── test_order_intent.py
    ├── test_risk_limits.py
    ├── test_kill_switch.py
    ├── test_audit_writer.py
    ├── test_no_live_execution.py
    ├── test_data_parity.py
    ├── test_coinbase_preview.py
    ├── test_reconciliation.py
    ├── test_fault_injection.py
    ├── test_fifo_calculator.py
    ├── test_tax_ledger.py
    └── test_strategy_sanity.py
```

---

# 14. Fázový plán

Codex smí autonomně přejít na další fázi, pokud jsou splněna acceptance kritéria aktuální fáze, výsledek je zapsán do `LOG.md` a nevznikl hard-stop stav.

---

## Phase 00 — Repository bootstrap, scope, AGENTS, LOG, docs/skills

**Agent:** `architect-agent`

### Cíl

Založit bezpečný skeleton projektu, pracovní pravidla, LOG, agenty a skilly.

### Editable files

- `README.md`
- `.gitignore`
- `.env.example`
- `AGENTS.md`
- `LOG.md`
- `docs/ARCHITECTURE.md`
- `docs/RISK_POLICY.md`
- `docs/RUNBOOK.md`
- `docs/PHASE_GATE.md`
- `docs/LIVE_TRADING_CHECKLIST.md`
- `docs/skills/*.md`

### Úkoly

1. Vytvořit základní strukturu projektu.
2. Vytvořit `LOG.md` podle formátu v tomto dokumentu.
3. Vytvořit `AGENTS.md`.
4. Vytvořit skill soubory.
5. Vytvořit `.env.example` pouze s placeholdery.
6. Vytvořit `.gitignore` pro secrets, logs, DB, cache, exporty, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`, `.mypy_cache/`, `.venv/`, velké `reports/*.csv`, `reports/*.parquet`, `reports/*.jsonl` a lokální runtime artefakty.
7. Zapsat disclaimer do README.
8. Zapsat, že MVP neumí live trading.

### Acceptance criteria

- [ ] Existuje `LOG.md`.
- [ ] Existuje `AGENTS.md`.
- [ ] Existuje `docs/skills/`.
- [ ] `.env.example` neobsahuje secrets.
- [ ] `.gitignore` vylučuje `.env`, DB, logy, exporty, secrets, cache složky, `.venv/`, velké CSV/Parquet/JSONL reporty a runtime artefakty.
- [ ] README obsahuje risk disclaimer.
- [ ] RISK_POLICY obsahuje zákaz live tradingu, páky, futures, shortů a secretů.
- [ ] Coinbase sandbox je označen jako nevhodný pro strategickou validaci.
- [ ] Fáze zapsána do `LOG.md`.

---

## Phase 00b — Coding standards, package skeleton, pyproject, CLI baseline

**Agent:** `architect-agent`

### Cíl

Zajistit, že projekt vzniká jako instalovatelná Python aplikace se sjednoceným stylem kódu, ne jako sbírka skriptů.

### Editable files

- `pyproject.toml`
- `Makefile`
- `scripts/dev.ps1`
- `src/coinbase_freqtrade_guarded_bot/__init__.py`
- `src/coinbase_freqtrade_guarded_bot/cli.py`
- `src/coinbase_freqtrade_guarded_bot/config/`
- `src/coinbase_freqtrade_guarded_bot/guard_layer/`
- `src/coinbase_freqtrade_guarded_bot/tax_layer/`
- `src/coinbase_freqtrade_guarded_bot/data_layer/`
- `src/coinbase_freqtrade_guarded_bot/reporting/`
- `tests/test_imports.py`
- `tests/test_cli.py`
- `docs/CODING_STANDARDS.md`
- `docs/PACKAGING.md`
- `docs/skills/coding_standards.md`
- `docs/skills/packaging_app_architecture.md`
- `docs/skills/execution_context.md`
- `docs/skills/network_resilience.md`
- `docs/skills/db_schema_migrations.md`
- `docs/skills/test_quality_gates.md`
- `docs/skills/codex_usage_budget.md`
- `AGENTS.md`
- `LOG.md`

### Úkoly

1. Vytvořit `src/coinbase_freqtrade_guarded_bot/`.
2. Vytvořit minimální `pyproject.toml`.
3. Nastavit package metadata včetně `[project.urls]`.
4. Nastavit `pytest`.
5. Nastavit `ruff`.
6. Nastavit `pytest-cov` a coverage command.
7. Nastavit `pytest-socket` s defaultním `--disable-socket`.
8. Připravit volitelný `mypy`/typing gate.
9. Vytvořit minimální CLI s `--help`.
10. Vytvořit Windows-first command catalog v `scripts/dev.ps1`; `Makefile` je sekundární convenience.
11. Každý příkaz označit execution contextem.
12. Ověřit lokální editable install přes `python -m pip install --upgrade pip` a `python -m pip install -e .`.
13. Vytvořit `docs/CODEX_USAGE_POLICY.md` a zapsat Plus-safe slice workflow.
14. Ověřit, že `PROJECT_STATE.md` obsahuje quota-safe resume pole.
8. Vytvořit import smoke test.
9. Doplnit coding standards do `docs/CODING_STANDARDS.md`.
10. Doplnit packaging pravidla do `docs/PACKAGING.md`.
11. Aktualizovat `AGENTS.md`, že aplikační logika patří do `src/`.

### Acceptance criteria

- [ ] `pip install -e .` funguje.
- [ ] `[LOCAL_VENV] python -m pip install --upgrade pip` proběhne.
- [ ] `[LOCAL_VENV] python -m pip install -e .` proběhne.
- [ ] `python -m coinbase_freqtrade_guarded_bot --help` funguje.
- [ ] Existuje minimální CLI bez live execution příkazů.
- [ ] `pytest` projde alespoň import/CLI smoke testy.
- [ ] `pytest-cov` je nakonfigurovaný.
- [ ] `pytest-socket` je nakonfigurovaný s defaultním zákazem socketů pro unit testy.
- [ ] `scripts/dev.ps1` existuje jako primární Windows-first entrypoint.
- [ ] Command catalog existuje a rozlišuje `[HOST_POWERSHELL]`, `[LOCAL_VENV]`, `[DOCKER_APP]`, `[DOCKER_FREQTRADE]`.
- [ ] `ruff check .` projde nebo je zdokumentovaný jako TODO s důvodem.
- [ ] `docs/CODING_STANDARDS.md` existuje.
- [ ] `docs/PACKAGING.md` existuje.
- [ ] Document Completeness Check PASS pro coding/packaging/execution/network/db/test/usage docs a skills.
- [ ] `docs/CODEX_USAGE_POLICY.md` existuje.
- [ ] `PROJECT_STATE.md` obsahuje quota-safe resume pole.
- [ ] Phase 00b umí skončit bezpečným `QUOTA_SAFE_CHECKPOINT`.
- [ ] `requirements.lock`, `requirements-dev.lock` nebo zdokumentovaný lockovací postup existuje.
- [ ] Dokument obsahuje kompletní fáze 00–18; Codex provede Document Completeness Check a zapíše výsledek do LOG.md.
- [ ] `AGENTS.md` obsahuje code style pravidla.
- [ ] Aplikační logika je směrována do `src/coinbase_freqtrade_guarded_bot/`.
- [ ] Fáze zapsána do `LOG.md`.

---

## Phase 01 — Development environment

**Agent:** `sre-agent`

### Cíl

Ověřit lokální prostředí.

### Kontrolní příkazy

```bash
docker --version
docker compose version
git --version
python --version
```

Na Windows také:

```powershell
wsl --status
```

### Úkoly

1. Ověřit dostupné nástroje.
2. Pokud něco chybí, zapsat do `LOG.md` přesné příkazy pro uživatele.
3. Ověřit, že `.env` není trackovaný Gitem.
4. Doporučit vývojový režim: lokální PC.
5. Zapsat, že produkční 24/7 režim bude řešen později v infrastrukturní fázi.

### Acceptance criteria

- [ ] Verze nástrojů zapsány do `LOG.md`.
- [ ] `git status` neukazuje `.env`.
- [ ] Pokud chybí nástroj, stav `WAITING_FOR_USER`.
- [ ] Žádné secrets.

---

## Phase 02 — Freqtrade Docker skeleton

**Agent:** `architect-agent` + `sre-agent`

### Cíl

Rozběhnout Freqtrade v Dockeru v bezpečném dry-run/backtest režimu.

### Editable files

- `docker-compose.yml`
- `user_data/config/config.dryrun.json`
- `user_data/config/config.backtest.json`
- `user_data/config/pairlist.json`
- `docs/RUNBOOK.md`
- `tests/test_no_live_execution.py`

### Požadavky

- `dry_run` musí být true.
- Žádné API keys.
- Žádný live order.
- WebUI pouze lokálně.
- UI nesmí být vystavené veřejně na internet.
- Kontejnery nesmí vystavovat nešifrované porty do vnější sítě; lokální porty jen přes explicitní localhost binding.
- Config nesmí obsahovat futures/leverage/short.
- `src/` musí být dostupné uvnitř Freqtrade kontejneru bezpečnou cestou:
  - MVRS/dev: bind mount `./src:/freqtrade/src:ro` + `PYTHONPATH=/freqtrade/src`;
  - později: custom image s regular package install.
- Zakázáno řešit importy přes `sys.path.append`.

### Kontrolní příkazy

```bash
docker compose pull
docker compose run --rm freqtrade --help
docker compose config
```

### Acceptance criteria

- [ ] Docker compose config validní.
- [ ] Freqtrade kontejner má přístup k package kódu přes mount/PYTHONPATH nebo package install.
- [ ] Docker import smoke test `python -c "import coinbase_freqtrade_guarded_bot"` PASS.
- [ ] Strategie neobsahují `sys.path.append`.
- [ ] Freqtrade container lze spustit.
- [ ] `dry_run=true`.
- [ ] Test ověřuje, že live režim není povolen.
- [ ] Žádné reálné API klíče.
- [ ] Fáze zapsána do LOG.md.

---

## Phase 03 — Coinbase/Freqtrade capability check

**Agent:** `data-agent`

### Cíl

Ověřit aktuální podporu Coinbase ve Freqtrade/CCXT.

### Editable files

- `docs/RUNBOOK.md`
- `docs/DATA_SOURCE_POLICY.md`
- `docs/skills/freqtrade_coinbase_ccxt.md`
- `reports/research/YYYY-MM-DD_coinbase_freqtrade_capability.md`
- `LOG.md`

### Research required

Codex musí ověřit:

- aktuální Freqtrade docs;
- aktuální CCXT Coinbase support;
- Freqtrade issue kolem Coinbase supportu;
- Coinbase product/pair naming;
- známé problémy s OHLCV;
- známé problémy s fetch limity;
- známé problémy s timestampy a volume.

### Kontrolní příkazy

```bash
docker compose run --rm freqtrade list-exchanges
docker compose run --rm freqtrade list-pairs --exchange coinbase
docker compose run --rm freqtrade --version
```

### Rozhodovací strom

| Výsledek | Stav | Další postup |
|---|---|---|
| Coinbase ve Freqtrade funguje a páry/data vypadají OK | PASS | pokračovat do Phase 03b — Data Parity Gate |
| Coinbase vidí páry, ale data nesedí | PARTIAL | Freqtrade použít jako engine, data stahovat přes Coinbase Advanced API a konvertovat do Freqtrade formátu |
| Coinbase nefunguje vůbec | BLOCKED | zastavit, zapsat OPEN QUESTION, navrhnout alternativy a čekat na rozhodnutí uživatele |
| Coinbase funguje jen s jiným namingem párů | WARN | zdokumentovat mapping `BTC/USD` vs `BTC-USD` |
| data mají omezenou historii | WARN/BLOCKED | rozhodnout, zda rozsah stačí pro backtest a out-of-sample validaci |


### Acceptance criteria

- [ ] Research report existuje.
- [ ] `docs/skills/freqtrade_coinbase_ccxt.md` aktualizován.
- [ ] Je jasné, zda Freqtrade Coinbase vidí.
- [ ] Je jasné, jaké páry jsou dostupné.
- [ ] Pokud není jasné, Codex se zastaví.
- [ ] Rozhodnutí zapsáno do LOG.md.

---

## Phase 03b — Data Parity Gate

**Agent:** `data-agent`

### Cíl

Ověřit, že data z Freqtrade/CCXT odpovídají datům z Coinbase Advanced API.

Bez tohoto gate nemá backtest dostatečnou důvěryhodnost.

### Editable files

- `src/coinbase_freqtrade_guarded_bot/guard_layer/data_parity.py`
- `src/coinbase_freqtrade_guarded_bot/network/http_client.py`
- `scripts/compare_coinbase_data_sources.py`
- `tests/test_data_parity.py`
- `docs/DATA_SOURCE_POLICY.md`
- `reports/data_parity/.gitkeep`
- `LOG.md`

### Požadavky

- Porovnávat pouze uzavřené svíčky.
- Převést všechny timestampy na UTC.
- Podporovat BTC/USD a ETH/USD.
- Podporovat 1h a 1d.
- Pokud 4h není nativní přes Coinbase API, agregovat 1h → 4h deterministicky z uzavřených 1h svíček.
- Porovnat:
  - timestamp,
  - open,
  - high,
  - low,
  - close,
  - volume.
- Vygenerovat markdown report.
- Chybějící svíčky se nesmí interpolovat z okolních hodnot; povoleno je pouze doplnění z autoritativního nižšího timeframe nebo FAIL/WARN.

### Tolerance

| Pole | Pravidlo |
|---|---|
| timestamp | přesná shoda po zarovnání |
| OHLC | pouze konfigurovatelná rounding tolerance; žádná fixní univerzální hodnota bez ADR |
| volume | toleranční režim WARN/FAIL podle configu |
| chybějící svíčka | FAIL |
| posunutá svíčka | FAIL |
| neuzavřená aktuální svíčka | ignorovat |

### Acceptance criteria

- [ ] Data parity report existuje.
- [ ] Testy používají mock data.
- [ ] Síťová vrstva má timeout/retry/backoff testy pro 429/503/timeout.
- [ ] Chybějící svíčky = FAIL.
- [ ] Posunuté timestampy = FAIL.
- [ ] OHLC rozdíl nad toleranci = FAIL.
- [ ] Pokud gate selže, Codex se zastaví a zeptá se uživatele.
- [ ] Výsledek zapsán do LOG.md.

---

## Phase 04 — Data source decision ADR

**Agent:** `architect-agent` + `data-agent`

### Cíl

Rozhodnout autoritativní zdroj dat.

### Editable files

- `docs/adr/ADR-002-data-source-policy.md`
- `docs/DATA_SOURCE_POLICY.md`
- `LOG.md`

### Možnosti

1. Freqtrade/CCXT data jsou OK a používají se pro backtest.
2. Freqtrade/CCXT data nejsou OK; data se stahují přes Coinbase Advanced API a konvertují do Freqtrade formátu.
3. Hybrid: Freqtrade engine, Coinbase API jako validační zdroj.

### Acceptance criteria

- [ ] ADR existuje.
- [ ] Rozhodnutí má datum.
- [ ] Rozhodnutí má důvod.
- [ ] Rozhodnutí uvádí rizika.
- [ ] Rozhodnutí říká, co se stane při selhání dat.
- [ ] LOG aktualizován.

---

## Phase 05 — Baseline strategy V1

**Agent:** `strategy-agent`

### Cíl

Vytvořit jednoduchou, čitelnou a auditovatelnou baseline strategii bez ML.

### Editable files

- `user_data/strategies/CoinbaseTrendGuardV1.py`
- `docs/ARCHITECTURE.md`
- `docs/RUNBOOK.md`
- `tests/test_strategy_sanity.py`
- `LOG.md`

### Strategie

- Long-only.
- Spot.
- BTC/ETH.
- Main timeframe: 4h.
- Informative timeframe: 1d.
- Trend filtr.
- Momentum filtr.
- Volume filtr.
- Volatility guard.
- Protection proti přepálené svíčce.
- `enter_tag`.
- `exit_reason`.

### Zakázáno

- ML.
- FreqAI.
- Hyperopt.
- Futures.
- Leverage.
- Short.
- Příliš mnoho parametrů.
- Magické konstanty bez komentáře.

### Acceptance criteria

- [ ] Strategie jde načíst Freqtrade.
- [ ] `can_short = False`.
- [ ] Žádná páka.
- [ ] Každý vstup má `enter_tag`.
- [ ] Volatility/volume guard existuje.
- [ ] Test sanity PASS.
- [ ] Žádná optimalizace na historický výsledek.
- [ ] Použité indikátory a pravidla mají stručný Algorithm Review.
- [ ] LOG aktualizován.

---

## Phase 05b — Minimal Guard Core before backtest/dry-run expansion

**Agent:** `guard-agent` + `architect-agent`

### Cíl

Vytvořit minimální bezpečnostní jádro dříve, než projekt začne generovat větší množství signálů a dry-run událostí.

Tato fáze není plný Phase 09 Guard Layer. Je to minimální, jednoduchá a testovatelná vrstva pro MVRS.

### Editable files

- `src/coinbase_freqtrade_guarded_bot/guard_layer/order_intent.py`
- `src/coinbase_freqtrade_guarded_bot/guard_layer/risk_limits.py`
- `src/coinbase_freqtrade_guarded_bot/guard_layer/kill_switch.py`
- `src/coinbase_freqtrade_guarded_bot/guard_layer/audit_writer.py`
- `tests/test_order_intent.py`
- `tests/test_risk_limits.py`
- `tests/test_kill_switch.py`
- `tests/test_audit_writer.py`
- `docs/RISK_POLICY.md`
- `docs/KILL_SWITCH.md`
- `LOG.md`

### Minimální rozsah

- `OrderIntent` doménový model.
- `RiskDecision` doménový model.
- JSONL append-only audit writer.
- File-based kill-switch přes soubor `KILL_SWITCH`.
- Env/config flag pro halt state.
- Základní risk limity:
  - max stake per intent;
  - max open intents/positions;
  - no live execution;
  - no leverage/futures/short.
- Zamítnutý intent se také zapisuje do auditu.

### Zakázáno

- Coinbase live order.
- Coinbase preview integrace.
- Reconciliation proti burze.
- Složitý ORM.
- UI toggle jako primární mechanismus.

### Acceptance criteria

- [ ] `OrderIntent` a `RiskDecision` jsou typované doménové modely.
- [ ] Audit writer zapisuje append-only JSONL.
- [ ] Aktivní soubor `KILL_SWITCH` blokuje intent.
- [ ] `ALLOW_LIVE_TRADING=false` blokuje live execution path.
- [ ] Zamítnutý intent je auditován.
- [ ] Unit testy PASS.
- [ ] Phase 08 dry-run bude používat minimální guard core.
- [ ] LOG aktualizován.

---

## Phase 06 — Advanced backtest validation

**Agent:** `quant-research-agent`

### Cíl

Ověřit baseline strategii robustně, ne jen jedním hezkým backtestem.

### Editable files

- `scripts/run_backtest_report.py`
- `docs/RUNBOOK.md`
- `docs/skills/backtest_validation.md`
- `reports/backtests/.gitkeep`
- `LOG.md`

### Povinné scénáře

| Scénář | Popis |
|---|---|
| Base fee | konzervativní maker/taker model |
| Worst fee | roundtrip worst-case |
| Slippage low | nízký skluz |
| Slippage medium | střední skluz |
| Slippage high | vysoký skluz |
| Bull | růstové období |
| Bear | poklesové období |
| Sideways | boční období |
| Crash | extrémní volatilita |
| Full period | celé období |
| Out-of-sample | zamčený konečný segment |

### Metriky

- Total profit.
- CAGR.
- Max drawdown.
- Sharpe.
- Sortino.
- Profit factor.
- Win rate.
- Average profit/trade.
- Number of trades.
- Exposure.
- Max loss streak.
- Buy-and-hold comparison.
- Monthly returns.
- Equity curve.
- Drawdown curve.

### Pokročilá validace

Codex musí implementovat nebo minimálně zdokumentovat a připravit:

1. Walk-forward analýzu.
2. Out-of-sample held-out test.
3. Random strategy sanity test.
4. Monte Carlo resampling pořadí obchodů.
5. Sensitivity analysis na fee/slippage.
6. Research k deflated Sharpe ratio, pokud bylo testováno více variant.
7. Kontrolu lookahead bias.
8. Kontrolu přílišné citlivosti parametrů.

### Acceptance criteria

- [ ] Backtest report existuje.
- [ ] Walk-forward report existuje.
- [ ] Out-of-sample segment je zapsaný v LOG.md.
- [ ] Random strategy comparison existuje.
- [ ] Monte Carlo report existuje a obsahuje skutečné numerické výstupy: počet simulací, 5/50/95 percentil CAGR, 5/50/95 percentil max drawdownu, nejhorší simulovaný drawdown, pravděpodobnost drawdownu nad limitem a pravděpodobnost záporného výsledku po nákladech.
- [ ] Walk-forward report existuje a obsahuje skutečné numerické výstupy: počet oken, délku train/test oken, výsledek každého test okna, počet ziskových/ztrátových oken, agregovaný profit, agregovaný drawdown a závěr PASS/FAIL.
- [ ] Fee/slippage sensitivity existuje a obsahuje numerickou tabulku scénářů.
- [ ] Report obsahuje disclaimer.
- [ ] Pokud strategie porazí baseline jen v jednom bull období, výsledek = FAIL.
- [ ] Pokud strategie neporáží buy-and-hold nebo baseline po nákladech, výsledek = FAIL nebo RESEARCH_ONLY.
- [ ] LOG aktualizován.

---

## Phase 07 — Report layer

**Agent:** `quant-research-agent` + `sre-agent`

### Cíl

Automatizovat generování reportů.

### Editable files

- `scripts/run_backtest_report.py`
- `reports/backtests/.gitkeep`
- `docs/RUNBOOK.md`
- `LOG.md`

### Výstupy

```text
reports/backtests/YYYY-MM-DD_strategy_summary.md
reports/backtests/YYYY-MM-DD_trades.csv
reports/backtests/YYYY-MM-DD_metrics.json
reports/backtests/YYYY-MM-DD_drawdown.csv
reports/backtests/YYYY-MM-DD_walkforward.json
reports/backtests/YYYY-MM-DD_montecarlo.json
```

### Report musí obsahovat

- název strategie;
- verzi configu;
- data source decision;
- páry;
- timeframe;
- fee model;
- slippage model;
- počet obchodů;
- max drawdown;
- buy-and-hold comparison;
- walk-forward;
- Monte Carlo;
- best/worst trade;
- měsíční výsledky;
- enter_tag agregaci;
- PASS/FAIL závěr;
- disclaimer.

### Acceptance criteria

- [ ] Script běží bez API key.
- [ ] Script nespouští live trading.
- [ ] Výstupy existují.
- [ ] Report je čitelný.
- [ ] LOG aktualizován.

---

## Phase 08 — Dry-run / paper trading

**Agent:** `sre-agent`

### Cíl

Spustit bota bez reálných peněz a ověřit provozní stabilitu.

### Editable files

- `scripts/run_dryrun_healthcheck.py`
- `docs/RUNBOOK.md`
- `reports/dryrun/.gitkeep`
- `LOG.md`

### Sleduje se

- container uptime;
- restart behavior;
- log errors;
- DB status;
- počet signálů;
- průchod signálu přes minimální Guard Core;
- otevřené dry-run pozice;
- rozdíl backtest vs dry-run;
- `enter_tag`/`exit_reason`;
- absence live order path;
- log rotation;
- základní databázový backup/restore smoke test.

### Acceptance criteria

- [ ] Dry-run lze spustit.
- [ ] Healthcheck report existuje.
- [ ] Režim je bez reálných peněz.
- [ ] Restart test proveden.
- [ ] Žádná live execution path.
- [ ] Dry-run signály prochází přes minimální Guard Core z Phase 05b.
- [ ] Log rotation je nakonfigurovaná nebo zdokumentovaná.
- [ ] Backup/restore smoke test lokální DB je proveden nebo zdokumentován jako TODO s důvodem.
- [ ] LOG aktualizován.

---

## Phase 08b — Fault Injection

**Priority:** POST_MVRS safety hardening. Nesmí blokovat dokončení MVRS, ale musí být hotové před live readiness.

**Agent:** `sre-agent` + `guard-agent`

### Cíl

Ověřit chování při poruchách infrastruktury a API.

### Editable files

- `src/coinbase_freqtrade_guarded_bot/guard_layer/fault_injection.py`
- `tests/test_fault_injection.py`
- `docs/RUNBOOK.md`
- `docs/RISK_POLICY.md`
- `LOG.md`

### Scénáře

| Scénář | Očekávané chování |
|---|---|
| API timeout | fail-closed |
| 401 Unauthorized | fail-closed + incident |
| 429 rate limit | respektovat Retry-After, backoff + žádný order |
| stará cena | žádný order |
| chybějící cena | žádný order |
| nevalidní symbol | fail-closed |
| preview failure | obchod zamítnut |
| audit writer failure | obchod zamítnut |
| kill-switch read failure | systém halted |
| unknown order status | blokace dalšího orderu |
| DB unavailable | fail-closed |
| duplicate event | deduplikace nebo incident |

### Acceptance criteria

- [ ] Testy existují.
- [ ] Všechny scénáře fail-closed.
- [ ] Retry/backoff má bounded attempt count a nepřekročí definovaný deadline.
- [ ] Incident se zapisuje do auditu, pokud audit funguje.
- [ ] Pokud audit nefunguje, systém zastaví obchodování.
- [ ] LOG aktualizován.

---

## Phase 09 — Guard layer: OrderIntent, risk, audit, persistent kill-switch

**Agent:** `guard-agent`

### Cíl

Rozšířit minimální Guard Core z Phase 05b na plnou bezpečnostní vrstvu, která odděluje obchodní signál od obchodního záměru a exekuce.

### Editable files

- `src/coinbase_freqtrade_guarded_bot/guard_layer/order_intent.py`
- `src/coinbase_freqtrade_guarded_bot/guard_layer/risk_limits.py`
- `src/coinbase_freqtrade_guarded_bot/guard_layer/kill_switch.py`
- `src/coinbase_freqtrade_guarded_bot/guard_layer/audit_writer.py`
- `src/coinbase_freqtrade_guarded_bot/config/settings.py`
- `tests/test_order_intent.py`
- `tests/test_risk_limits.py`
- `tests/test_kill_switch.py`
- `tests/test_audit_writer.py`
- `tests/test_no_live_execution.py`
- `docs/RISK_POLICY.md`
- `docs/KILL_SWITCH.md`
- `docs/skills/risk_engine.md`
- `LOG.md`

### OrderIntent schema

```json
{
  "timestamp": "2026-06-18T10:00:00Z",
  "symbol": "BTC-USD",
  "side": "BUY",
  "mode": "DRY_RUN",
  "strategy": "CoinbaseTrendGuardV1",
  "entry_tag": "trend_4h_confirmed_1d_positive",
  "proposed_stake": 100.0,
  "risk_pct": 0.5,
  "stoploss_pct": 2.0,
  "allowed_by_risk_engine": true,
  "live_execution_allowed": false
}
```

### Kill-switch activation simplicity

Kill-switch musí být aktivovatelný minimálně třemi jednoduchými způsoby:

1. vytvořením lokálního souboru `KILL_SWITCH`;
2. env/config flagem;
3. později read-only UI signalizací a samostatným manuálním toggle workflow, pokud UI zůstane bezpečně oddělené od exekuční vrstvy.

Nejjednodušší file-based mechanismus je povinný, protože musí fungovat i bez UI a bez sítě.

### Kill-switch typy

- `manual_halt`;
- `daily_loss_halt`;
- `weekly_loss_halt`;
- `drawdown_halt`;
- `api_error_halt`;
- `audit_failure_halt`;
- `reconciliation_halt`;
- `data_quality_halt`.

### Požadavky

- Kill-switch musí být persistentní.
- Kill-switch musí přežít restart.
- Reset kill-switche musí být auditovaný.
- Pokud nejde kill-switch state přečíst, systém se chová jako halted.
- Pokud nejde auditovat, obchod se nesmí povolit.
- Každý intent, i zamítnutý, se ukládá.

### Acceptance criteria

- [ ] Aktivní kill-switch blokuje intent.
- [ ] Kill-switch přežije restart.
- [ ] Audit failure blokuje obchod.
- [ ] `ALLOW_LIVE_TRADING=false` blokuje live order.
- [ ] Zamítnutý intent je zapsán.
- [ ] Testy PASS.
- [ ] LOG aktualizován.

---

## Phase 10 — Coinbase order preview wrapper

**Agent:** `guard-agent`

### Cíl

Přidat Coinbase Advanced SDK/order preview vrstvu bez live orderů.

### Editable files

- `src/coinbase_freqtrade_guarded_bot/guard_layer/coinbase_preview.py`
- `tests/test_coinbase_preview.py`
- `docs/COINBASE_SECURITY.md`
- `docs/adr/ADR-001-coinbase-key-type.md`
- `docs/skills/coinbase_auth.md`
- `LOG.md`

### Povolené

- načíst env placeholdery;
- validovat config;
- připravit preview request;
- použít mock klienta v testech;
- uložit preview response do auditu;
- vyhodnotit fee/slippage limit.

### Zakázané

- `create_order`;
- `cancel_order`;
- `withdraw`;
- `transfer`;
- market order bez explicitního pozdějšího approvalu;
- live execution.

### Auth/JWT

Codex musí:

- ověřit aktuální Coinbase dokumentaci;
- ověřit SDK README/issues;
- zdokumentovat ECDSA vs Ed25519 rozhodnutí;
- preferovat oficiální SDK;
- nedělat ruční JWT podpis, pokud to není nutné;
- žádný secret do repozitáře.

### Acceptance criteria

- [ ] Preview wrapper nemá live order method nebo ji explicitně blokuje.
- [ ] Preview failure = fail-closed.
- [ ] Fee/slippage nad limit = zamítnout.
- [ ] Mock testy PASS.
- [ ] ADR existuje.
- [ ] LOG aktualizován.

---

## Phase 10b — Reconciliation skeleton

**Agent:** `guard-agent`

### Cíl

Připravit order/fill reconciliaci ještě před live režimem.

### Editable files

- `src/coinbase_freqtrade_guarded_bot/guard_layer/reconciliation.py`
- `tests/test_reconciliation.py`
- `docs/RECONCILIATION.md`
- `docs/ARCHITECTURE.md`
- `docs/skills/reconciliation.md`
- `LOG.md`

### Modely

- `OrderIntent`;
- `PreviewResult`;
- `ExecutionRequest`;
- `ExecutionResult`;
- `FillEvent`;
- `ReconciliationReport`.

### Kontroly

| Pole | Kontrola |
|---|---|
| symbol | musí sedět |
| side | musí sedět |
| size | nesmí překročit intent |
| price | v toleranci |
| fee | v limitu |
| slippage | v limitu |
| client_order_id | musí spárovat |
| status | nesmí být unknown |
| partial fill | musí být označen |
| duplicate fill | musí být detekován |
| missing fill | blokace dalšího orderu |

### Acceptance criteria

- [ ] Unreconciled order blokuje nový intent.
- [ ] Mismatch = FAIL.
- [ ] Unknown status = FAIL.
- [ ] Mock testy PASS.
- [ ] LOG aktualizován.

---

## Phase 11 — Manual approval mode

**Agent:** `guard-agent` + `sre-agent`

### Cíl

Vytvořit workflow, kde bot navrhne a člověk rozhodne.

### Workflow

```text
strategie
→ signál
→ OrderIntent
→ risk engine
→ kill-switch check
→ Coinbase preview
→ report
→ uživatel ručně rozhodne
→ případné ruční zadání v Coinbase UI
```

### Editable files

- `docs/RUNBOOK.md`
- `docs/LIVE_TRADING_CHECKLIST.md`
- `reports/audits/.gitkeep`
- `LOG.md`

### Zakázáno

- API live create order.
- Automatický order submit.
- Skryté povolení live režimu.

### Acceptance criteria

- [ ] Report o navrhovaném obchodu je čitelný.
- [ ] Report obsahuje důvod signálu.
- [ ] Report obsahuje riziko.
- [ ] Report obsahuje preview fee/slippage.
- [ ] Žádná automatická live exekuce.
- [ ] LOG aktualizován.

---

## Phase 12 — Tax ledger

**Agent:** `tax-agent`

### Cíl

Zajistit technickou evidenci obchodů pro daňové účely.

### Důležité omezení

Codex nesmí dávat finální daňové poradenství. Musí vytvořit technický podklad a uvést, že pravidla se musí před daňovým přiznáním aktuálně ověřit.

### Initial working assumptions — vždy ověřit před ostrým daňovým exportem

Níže uvedené body jsou počáteční pracovní rámec pro návrh ledgeru, ne definitivní daňové poradenství. Codex je musí při implementaci zapsat do `docs/skills/cz_tax_rules.md` s datem, zdroji a stavem ověření.

Pracovní předpoklady pro návrh evidence:

- použít FIFO jako primární metodu párování nákupů a prodejů, pokud uživatel nepotvrdí jiné pravidlo po konzultaci s daňovým poradcem;
- evidovat časový test 3 roky jako flag u daňové dávky;
- evidovat hodnotový test 100 000 Kč ročně jako informační flag;
- evidovat sazby 15 % / 23 % pouze jako ověřovaný parametr, nikoliv hardcoded právní závěr;
- u aktivního 4h/1d trading bota předpokládat, že většina pozic se bude zavírat v řádu dnů až týdnů, tedy časový test pravděpodobně nebude hlavní scénář;
- u aktivního tradingu předpokládat, že hodnotový test se může rychle vyčerpat, proto ledger musí primárně počítat se zdanitelným ziskem;
- osvobození nikdy nepoužívat jako default, pouze jako explicitně ověřený flag;
- finální daňový export musí obsahovat disclaimer a má sloužit jako podklad pro účetního/daňového poradce.


### Editable files

- `src/coinbase_freqtrade_guarded_bot/tax_layer/trade_ledger.py`
- `src/coinbase_freqtrade_guarded_bot/tax_layer/fifo_calculator.py`
- `src/coinbase_freqtrade_guarded_bot/tax_layer/cz_report_export.py`
- `tests/test_fifo_calculator.py`
- `tests/test_tax_ledger.py`
- `docs/TAX_REPORTING.md`
- `docs/TAX_NOTES_CZ.md`
- `docs/skills/cz_tax_rules.md`
- `scripts/export_tax_report.py`
- `LOG.md`

### Evidenční pole

- timestamp UTC;
- local timestamp;
- exchange;
- portfolio id;
- product id;
- symbol;
- side;
- base amount;
- quote amount;
- price;
- fee amount;
- fee currency;
- order id;
- fill id;
- client_order_id;
- strategy;
- mode;
- source;
- raw response hash;
- note;
- tax lot id;
- export batch id.

### Schema and migration policy

Tax/audit data se nesmí tiše poškodit změnou schématu.

MVP pravidla:

- SQLite databáze musí obsahovat `schema_version` nebo ekvivalentní metadata.
- Každá změna schématu má migration note v `docs/DB_SCHEMA_POLICY.md`.
- Destruktivní reset DB je povolen pouze pro disposable/replayable test nebo MVRS dry-run data a musí být zapsán do LOG.md.
- Před destruktivním resetem existující SQLite DB se vytvoří `.bak` kopie, pokud soubor existuje.
- Jakmile DB obsahuje hodnotná dry-run/live data, před migrací je povinný backup.
- Append-only audit JSONL se nemigruje destruktivně; nové schéma se řeší novým event typem nebo exportem do nové verze.
- Pokud projekt přejde na SQLModel/SQLAlchemy, Codex smí zavést Alembic pouze po dependency review a ADR.
- Před Phase 17 musí existovat test migrace ze staršího schématu na aktuální.

Editable migration files:

- `src/coinbase_freqtrade_guarded_bot/tax_layer/migrations/`
- `src/coinbase_freqtrade_guarded_bot/storage/schema_version.py`
- `scripts/migrate_tax_db.py`
- `tests/test_tax_migrations.py`
- `docs/DB_SCHEMA_POLICY.md`

### Storage policy

MVP storage pravidlo:

- audit trail: append-only JSONL jako primární auditní stopa;
- tax ledger: SQLite jako lokální strukturované úložiště, pokud JSONL nestačí pro dotazy/exporty;
- SQLModel je povolený kandidát pro typované SQLite modely, ale pouze po dependency review a ADR;
- plný ORM není povinný pro MVRS;
- žádné síťové DB ani cloud DB v MVP bez explicitního ADR.

### Exporty

- CSV;
- XLSX;
- Parquet;
- JSONL;
- roční přehled;
- podklad pro účetního/daňového poradce.

### Acceptance criteria

- [ ] Ledger ukládá všechny potřebné údaje.
- [ ] FIFO kalkulátor má ručně ověřený test.
- [ ] Exporty fungují bez secretů.
- [ ] Dokumentace obsahuje disclaimer.
- [ ] `cz_tax_rules.md` má datum posledního ověření.
- [ ] SQLite schema versioning/migration policy existuje.
- [ ] Test migrace nebo reset policy pro disposable test DB existuje.
- [ ] LOG aktualizován.

---

## Phase 13 — Enterprise UI MVP

**Agent:** `ui-agent`

### Cíl

Vytvořit interní enterprise-style dashboard pro monitoring, audit a daňovou evidenci.

### MVP stack

- Streamlit.
- Lokální přístup.
- Žádný live trade button.
- Čtení z lokálních reportů, audit logů, DB.

### Pozdější enterprise stack

- FastAPI backend.
- PostgreSQL.
- React/Next.js frontend.
- Prometheus/Grafana monitoring.
- Auth za VPN.
- Žádné veřejně vystavené UI.

### Editable files

- `ui/README.md`
- `ui/streamlit_app.py`
- `ui/pages/*.py`
- `docs/UI_SPEC.md`
- `docs/adr/ADR-004-ui-stack.md`
- `docs/skills/ui_patterns.md`
- `LOG.md`

### Obrazovky

1. Overview.
2. Backtests.
3. Dry-run status.
4. Audit log.
5. Tax ledger.
6. Risk/Kill-switch.
7. Research.
8. System health.

### Zásady

- UI není gambling terminál.
- UI nesmí mít live order tlačítko.
- Každé číslo musí být dohledatelné do audit logu nebo DB.
- Rizikové stavy musí být vizuálně zřetelné.
- Kill-switch status musí být vždy viditelný.

### Acceptance criteria

- [ ] UI běží lokálně.
- [ ] Nepotřebuje API key.
- [ ] Neobsahuje live trade tlačítko.
- [ ] Zobrazuje kill-switch stav.
- [ ] Zobrazuje audit log.
- [ ] Zobrazuje tax ledger.
- [ ] LOG aktualizován.

---

## Phase 14 — Research update loop

**Agent:** `research-agent`

### Cíl

Umožnit řízený research bez neřízeného přebírání kódu.

### Editable files

- `scripts/research_update.py`
- `docs/RESEARCH_POLICY.md`
- `reports/research/`
- `docs/skills/*.md`
- `LOG.md`

### Povinné oblasti

- Coinbase API změny.
- Freqtrade issues.
- CCXT issues.
- Reddit zkušenosti.
- GitLab mirror/projekty.
- Dependency licence.
- Security advisories.
- ML/trading research.
- UI patterns.
- Daňové pravidlo před exportem.

### Acceptance criteria

- [ ] Každý research má report.
- [ ] Research nepřebírá kód bez licence.
- [ ] Výstup je doporučení, ne automatická implementace.
- [ ] LOG aktualizován.

---

## Phase 15 — ML / FreqAI research track

**Agent:** `strategy-agent` + `quant-research-agent`

### Cíl

Ověřit, zda ML/FreqAI přináší stabilní edge nad baseline.

### Důležité pravidlo

ML může běžet jako research paralelně, ale nesmí být blíž live režimu než baseline strategie. ML má přísnější validaci.

### Editable files

- `user_data/strategies/CoinbaseFreqAIResearchV1.py`
- `user_data/config/config.freqai.json`
- `docker-compose.freqai.yml`
- `docs/ML_RESEARCH_NOTES.md`
- `docs/skills/freqai_practices.md`
- `docs/skills/backtest_validation.md`
- `reports/backtests/`
- `LOG.md`

### Model pořadí

1. Buy-and-hold baseline.
2. Trend-following baseline.
3. Momentum/volatility baseline.
4. Logistic regression.
5. Random forest.
6. LightGBM/XGBoost.
7. FreqAI built-in models.
8. Regime detection.
9. Deep learning pouze experimentálně.
10. Reinforcement learning pouze budoucí experiment, ne MVP.

### Feature groups

- returns;
- momentum;
- volatility;
- volume;
- distance from moving average;
- drawdown state;
- regime features;
- cross-pair BTC/ETH features;
- market regime labels;
- sentiment pouze jako doplněk, ne primární vstup.

### Feature and leakage rules

- ML features nesmí používat budoucí data.
- Label horizon musí být explicitně definovaný.
- Feature/label alignment musí mít unit test.
- Raw close/open/high/low ceny se nesmí použít jako přímý vstup bez Algorithm Review.
- Preferovat returns/log-returns/normalizované vzdálenosti/volatility features.
- Stacionaritu posuzovat p-hodnotou a kritickými hodnotami, nikoliv jednou pevnou hranicí.
- FreqAI Dissimilarity Index / outlier filtering je povolený research kandidát, ne povinný MVP gate.

### Validace ML

- time-based split;
- walk-forward;
- purged gap mezi train/test, pokud label horizon překrývá data;
- out-of-sample held-out;
- feature importance;
- calibration;
- confusion matrix;
- PnL po nákladech;
- max drawdown;
- comparison vs baseline;
- random strategy comparison;
- Monte Carlo trade order resampling.

### Acceptance criteria

- [ ] ML nepřechází do live.
- [ ] Feature importance report existuje.
- [ ] Purged/walk-forward validace existuje.
- [ ] Feature/label alignment test existuje.
- [ ] Pokud je použit FreqAI DI/outlier filtering, má Algorithm Review a porovnání s baseline bez DI.
- [ ] ML porovnáno s baseline.
- [ ] Každý použitý ML/trading algoritmus má Algorithm Review.
- [ ] Pokud ML nepřidá robustní edge, zůstává research-only.
- [ ] LOG aktualizován.

---

## Phase 16 — Crypto trader knowledge base

**Agent:** `knowledge-agent` + `research-agent`

### Cíl

Vytvořit znalostní bázi veřejně dostupných poznatků od úspěšných crypto traderů, investorů a systematických obchodníků. Tato znalostní báze má pomáhat při tvorbě checklistů, risk pravidel, režimových filtrů a interpretaci výsledků. Nesmí sloužit jako přímý signál typu „kopíruj obchod tradera X“.

### Důležité omezení

Znalostní báze není zdroj automatických obchodních pokynů. Codex nesmí:

- slepě kopírovat obchody známých traderů;
- používat neověřené PnL screenshoty jako důkaz kvality;
- přebírat signály z placených skupin, Telegramu nebo neověřitelných zdrojů;
- scrapeovat obsah za paywallem bez oprávnění;
- zaměnit popularitu na sociálních sítích za obchodní kompetenci;
- zapojit znalostní bázi přímo do live exekuce.

### Editable files

- `docs/TRADER_KNOWLEDGE_BASE.md`
- `docs/skills/crypto_trader_knowledge.md`
- `knowledge_base/crypto_traders/`
- `knowledge_base/strategy_patterns/`
- `knowledge_base/risk_playbooks/`
- `reports/research/YYYY-MM-DD_crypto_trader_knowledge.md`
- `LOG.md`

### Research required

Codex musí vyhledávat a hodnotit pouze veřejně dostupné a ověřitelné zdroje:

- rozhovory;
- knihy;
- veřejné blogy;
- podcasty;
- post-mortem analýzy;
- veřejné trading deníky;
- GitHub/research projekty;
- diskuse na Redditu pouze jako slabý zkušenostní signál;
- akademické/quant materiály k risku a behaviorálním selháním.

### Hodnocení zdrojů

Každý záznam musí mít:

- jméno nebo alias;
- typ tradera/investora;
- zdroj;
- datum zdroje;
- ověřitelnost;
- hlavní principy;
- risk management principy;
- čemu se vyhýbá;
- zda je přístup relevantní pro spot BTC/ETH 4h/1d;
- zda je přístup systematizovatelný;
- riziko survivorship bias;
- riziko marketingového zkreslení;
- závěr: použít jako checklist / nepoužít / pouze inspirace.

### Výstupy znalostní báze

Znalostní báze má generovat pouze pomocné artefakty:

```text
knowledge_base/strategy_patterns/*.md
knowledge_base/risk_playbooks/*.md
knowledge_base/crypto_traders/*.md
```

Příklady užitečných artefaktů:

- checklist pro nevstupování po euforické pumpě;
- checklist pro práci s drawdownem;
- seznam známých chyb retail traderů;
- zásady snižování pozice při růstu volatility;
- pravidla pro režimový filtr;
- varování proti overtradingu;
- post-mortem šablona pro ztrátové série.

### Napojení na projekt

Povoleno:

- použít znalostní bázi pro návrh risk checklistů;
- použít znalostní bázi pro generování hypotéz k backtestu;
- použít znalostní bázi pro vysvětlení obchodů v reportu;
- použít znalostní bázi pro auditní komentáře.

Zakázáno:

- přímé použití jako buy/sell signál;
- přímá live exekuce;
- kopírování discretionary trade calls;
- změna risk limitů bez backtestu a acceptance kritérií.

### Acceptance criteria

- [ ] `TRADER_KNOWLEDGE_BASE.md` existuje.
- [ ] `crypto_trader_knowledge.md` existuje.
- [ ] Každý trader/princip má zdroj a hodnocení ověřitelnosti.
- [ ] Znalostní báze má minimálně jeden risk checklist.
- [ ] Znalostní báze nemá žádnou přímou live execution vazbu.
- [ ] Codex explicitně označí survivorship/marketing bias.
- [ ] LOG aktualizován.

---

## Phase 17 — Live pilot readiness checklist

**Agent:** `guard-agent` + `sre-agent`

### Cíl

Zabránit předčasnému live obchodování.

### Editable files

- `docs/LIVE_TRADING_CHECKLIST.md`
- `docs/PHASE_GATE.md`
- `LOG.md`

### Podmínky pro live pilot

- [ ] Data Parity Gate PASS.
- [ ] Baseline strategy PASS nebo jasně označená RESEARCH_ONLY.
- [ ] Backtest reporty existují.
- [ ] Walk-forward validace existuje.
- [ ] Out-of-sample validace existuje.
- [ ] Dry-run běžel dohodnutou dobu.
- [ ] Fault injection PASS.
- [ ] Guard layer PASS.
- [ ] Kill-switch PASS.
- [ ] Coinbase preview PASS.
- [ ] Reconciliation skeleton PASS.
- [ ] Tax ledger PASS.
- [ ] Audit logy kompletní.
- [ ] `pytest` PASS.
- [ ] `pytest --cov=src --cov-branch --cov-fail-under=85` PASS.
- [ ] Kritické coverage gates pro Guard/Tax/DataParity/Reconciliation/Metrics PASS nebo explicitní BLOCKER.
- [ ] `ruff check .` PASS nebo explicitní schválený waiver.
- [ ] Import smoke test PASS.
- [ ] No-secrets smoke test PASS.
- [ ] Document Completeness Check PASS: fáze 00–18 jsou přítomné, žádná sekce nekončí uříznutou větou, všechny odkazy na soubory odpovídají package layoutu.
- [ ] API key s IP allowlistem připraven, pokud se projekt dostane do live pilotu.
- [ ] Minimální oprávnění.
- [ ] Jedno portfolio.
- [ ] Malý kapitál definovaný uživatelem.
- [ ] Max akceptovatelná ztráta definovaná uživatelem.
- [ ] `ALLOW_LIVE_TRADING=false` stále default.
- [ ] Uživatel explicitně potvrzuje, že chápe riziko.

### Acceptance criteria

- [ ] Checklist existuje.
- [ ] Všechny položky mají PASS/FAIL.
- [ ] FAIL položky blokují live pilot.
- [ ] LOG aktualizován.

---

## Phase 18 — Limited live pilot only after explicit user approval

**Agent:** `guard-agent` + `sre-agent`

### Cíl

Teprve po splnění Phase 17 a explicitním souhlasu uživatele připravit velmi omezený pilot.

### Důležité

Codex nesmí tuto fázi zahájit bez výslovného pokynu uživatele.

### Podmínky

- `ALLOW_LIVE_TRADING=true` nastavuje uživatel samostatným commitem.
- Kapitál je malý a omezený.
- Spot only.
- BTC/ETH only.
- Long only.
- Žádná páka.
- Denní loss limit.
- Portfolio drawdown stop.
- Kill-switch.
- Reconciliation.
- Tax ledger.
- Manual approval.

### První live režim

První live režim není plně automatický:

```text
bot navrhne
→ preview
→ risk
→ report
→ uživatel ručně potvrdí
→ případně se obchod zadá ručně nebo samostatně schválenou exekuční vrstvou
```

### Acceptance criteria

- [ ] Žádný automatický live order bez samostatného schválení.
- [ ] Každý live krok auditován.
- [ ] Reconciliation po každém fillu.
- [ ] Tax ledger po každém fillu.
- [ ] Kill-switch testován.
- [ ] LOG aktualizován.

---

# 15. Master prompt pro každou novou Codex session

Vlož na začátek každé nové Codex session:

```text
Jsi senior Python engineer, kvantitativní analytik, bezpečnostně orientovaný architekt a DevOps inženýr.

Pracuješ na projektu coinbase_freqtrade_guarded_bot podle dokumentu CODEX_MASTER_PLAN.md v rootu repozitáře.

Před jakoukoliv akcí:
1. Přečti CODEX_MASTER_PLAN.md celý.
2. Přečti AGENTS.md.
3. Přečti `PROJECT_STATE.md`, pokud existuje.
4. Přečti z `LOG.md` minimálně STATUS SUMMARY, OPEN QUESTIONS, PHASE TRACKER, DECISION REGISTER, DEPENDENCY REGISTER a poslední checkpoint; archiv otevírej jen při potřebě historického detailu.
5. Urči aktuální fázi podle PHASE TRACKER a STATUS SUMMARY.
6. Pokud není jasné, kde pokračovat, zastav se a polož otázku.

Tvrdé limity:
- Žádný live trading v MVP.
- Žádné reálné API keys, secrets, seed fráze ani privátní klíče.
- Žádné futures, žádná páka, žádné shorty.
- Pouze spot, long-only, BTC/ETH v první verzi.
- Coinbase sandbox nepoužívat jako validační prostředí strategie.
- Žádné tvrzení o garantovaném zisku.
- Při nejistotě fail-closed.
- Pokud narazíš na live trading, secret nebo obchodní rozhodnutí uživatele, zastav se.

Pracovní postup:
- Pracuj autonomně přes fáze, dokud nevznikne hard-stop podle CODEX_MASTER_PLAN.md.
- Pracuj pouze v aktuálním scope.
- Dodržuj `docs/CODING_STANDARDS.md` a package layout pod `src/coinbase_freqtrade_guarded_bot/`.
- Před změnou vypiš call-flow.
- Vypiš editable/read-only scope.
- Každý shell příkaz označ execution contextem `[HOST_POWERSHELL]`, `[LOCAL_VENV]`, `[DOCKER_APP]` nebo `[DOCKER_FREQTRADE]`.
- Přečti relevantní soubory celé.
- Pokud je technická nejistota, použij research protokol z CODEX_MASTER_PLAN.md.
- Nové poznatky ukládej do docs/skills/*.md a reports/research/.
- Každou změnu testuj.
- Průběžně aktualizuj LOG.md po checkpointech, ne až na konci.
- Po PASS aktuálního malého slice automaticky pokračuj dalším bezpečným slice, pokud nevznikl hard-stop a neblíží se usage limit.
- Pokud se blíží usage limit, zapiš `QUOTA_SAFE_CHECKPOINT`, aktualizuj `PROJECT_STATE.md`, navrhni commit a vypiš resume instructions.
- Pokud vznikne hard-stop, zapiš WAITING_FOR_USER nebo BLOCKED do LOG.md a zastav se.
- Výstup dávej jako summary + files changed + tests run + PASS/FAIL + next step.
```

---

# 16. Prompt pro implementaci aktuální fáze

```text
Implementuj aktuální fázi podle CODEX_MASTER_PLAN.md.

Postup:
1. Přečti CODEX_MASTER_PLAN.md a AGENTS.md.
2. Přečti `PROJECT_STATE.md`, pokud existuje, a z `LOG.md` minimálně STATUS SUMMARY, OPEN QUESTIONS, PHASE TRACKER, DECISION REGISTER, DEPENDENCY REGISTER a poslední checkpoint.
3. Urči aktuální fázi.
4. Vypiš editable/read-only scope.
5. Přečti relevantní soubory celé.
6. Vypiš call-flow.
7. Pokud je potřeba research, proveď research protocol a výstup ulož do reports/research/.
8. Implementuj jen aktuální fázi.
9. Přidej nebo uprav testy.
10. Spusť testy.
11. Aktualizuj LOG.md a PROJECT_STATE.md.
12. Vyhodnoť acceptance criteria.
13. Pokud PASS a nevznikl hard-stop, pokračuj další fází.
14. Pokud vznikl hard-stop, vrať WAITING_FOR_USER/BLOCKED summary.

Zastav se, pokud:
- potřebuješ rozhodnutí uživatele;
- potřebuješ API key/secret;
- hrozí live trading;
- acceptance criteria nelze splnit;
- testy selhávají a příčina není jasná.
```

---

# 17. Prompt pro repair loop

```text
Aktuální fáze selhala. Proveď repair loop pouze v rámci scope aktuální fáze.

Postup:
1. Přečti failure log.
2. Urči root cause.
3. Pokud je příčina jasná, proveď minimální opravu.
4. Spusť relevantní testy.
5. Aktualizuj LOG.md.
6. Pokud chyba trvá nebo není jasná, zastav se a napiš BLOCKER report.

Neupravuj soubory mimo scope aktuální fáze.
Nepřidávej nové dependency bez dependency review.
```

---

# 18. Prompt pro research

```text
Proveď cílený research pro aktuální technický problém.

Povinně zkontroluj:
- oficiální dokumentaci;
- GitHub issues;
- GitLab, pokud relevantní;
- Reddit jako zkušenostní signál;
- licence knihoven;
- bezpečnostní rizika;
- uživatelské recenze;
- pro kvantitativní/statistické otázky relevantní quant/academic zdroje.

Výstup ulož do:
reports/research/YYYY-MM-DD_<topic>.md

Zjištění zapiš také do příslušného:
docs/skills/*.md

Report musí obsahovat:
- otázku;
- zdroje;
- shrnutí;
- rizika;
- doporučení;
- co neimplementovat;
- dopad na projekt.
```

---

# 19. První praktické kroky pro uživatele

```powershell
mkdir D:\2026\CryptoBot
cd D:\2026\CryptoBot
mkdir coinbase_freqtrade_guarded_bot
cd coinbase_freqtrade_guarded_bot
git init
```

Ulož tento dokument jako:

```text
CODEX_MASTER_PLAN.md
```

Pak založ minimální složky:

```powershell
ni README.md
ni .gitignore
ni .env.example
ni AGENTS.md
ni LOG.md
ni PROJECT_STATE.md
ni pyproject.toml
ni Makefile
mkdir docs
mkdir docs\adr
mkdir docs\skills
mkdir reports
mkdir reports\research
mkdir reports\data_parity
mkdir reports\backtests
mkdir reports\dryrun
mkdir reports\audits
mkdir reports\tax
mkdir tests
mkdir src
mkdir src\coinbase_freqtrade_guarded_bot
mkdir src\coinbase_freqtrade_guarded_bot\config
mkdir src\coinbase_freqtrade_guarded_bot\network
mkdir src\coinbase_freqtrade_guarded_bot\storage
mkdir src\coinbase_freqtrade_guarded_bot\data_layer
mkdir src\coinbase_freqtrade_guarded_bot\guard_layer
mkdir src\coinbase_freqtrade_guarded_bot\tax_layer
mkdir src\coinbase_freqtrade_guarded_bot\tax_layer\migrations
mkdir src\coinbase_freqtrade_guarded_bot\reporting
mkdir src\coinbase_freqtrade_guarded_bot\research
mkdir src\coinbase_freqtrade_guarded_bot\ui_support
mkdir src\coinbase_freqtrade_guarded_bot\utils
mkdir scripts
ni scripts\dev.ps1
mkdir user_data
mkdir user_data\config
mkdir user_data\strategies
mkdir ui
mkdir ui\pages
```

Ověř:

```powershell
tree /F
git status
```

Výstup pošli ke kontrole před spuštěním Codexu.

---

## 20. Operator discipline and survival policy

Cílem projektu není rychle vydělat, ale přežít dostatečně dlouho na to, aby bylo možné testovat hypotézy.

Pravidla:

- žádná strategie není považována za stabilní jen proto, že měla dobrý backtest;
- drawdown není chyba systému, pokud je v očekávaném rozsahu, ale musí být měřen a reportován;
- uživatel nesmí ručně obcházet kill-switch kvůli emocím nebo snaze „dohnat ztrátu“;
- po sérii ztrát se nemění strategie bez Algorithm Review a nového backtestu;
- před jakoukoliv změnou risk limitů musí vzniknout Decision Register záznam;
- každý post-mortem větší ztrátové série se zapisuje do `knowledge_base/risk_playbooks/`.

Mantra projektu:

```text
Nejdřív přežít.
Potom měřit.
Potom zlepšovat.
Až nakonec uvažovat o live pilotu.
```

---

## 21. Trvalý disclaimer

Tento text vložit do README a každého reportu:

> Tento projekt je nástroj pro výzkum a auditovatelné testování obchodních strategií, ne investiční poradenství ani příslib zisku. Historický backtest a dry-run výsledky nejsou zárukou budoucích výsledků. Obchodování s kryptoměnami je rizikové a může vést ke ztrátě části nebo celého vloženého kapitálu. Daňové informace v tomto projektu jsou technický podklad pro evidenci, ne daňové poradenství. Pro finální daňové přiznání je nutné ověřit aktuální pravidla a konzultovat daňového poradce.

---

## 22. Kritéria, kdy projekt nepouštět dál

Nepokračovat do live pilotu, pokud:

- Data Parity Gate selže.
- Backtest nemá out-of-sample validaci.
- Strategie funguje jen v jednom bull období.
- Strategie selže po realistických fees/slippage.
- Dry-run je nestabilní.
- Fault injection selže.
- Audit log má díry.
- Kill-switch nefunguje.
- Reconciliation neblokuje unknown status.
- Tax ledger neexportuje kompletní údaje.
- UI nebo monitoring skrývá rizikové stavy.
- API klíč nemá IP allowlist.
- Uživatel nemá definovaný kapitál a max akceptovatelnou ztrátu.
- Codex nebo uživatel nerozumí tomu, proč strategie obchoduje.

---

## 23. Shrnutí finálního rozhodnutí

Finální architektura:

```text
Freqtrade = research/backtest/dry-run engine
Coinbase Advanced SDK/order preview = validační guardrail
guard_layer = risk, audit, kill-switch, fault handling
tax_layer = evidence/export
ui = auditní enterprise dashboard
ML/FreqAI = oddělený research track, ne live shortcut
trader knowledge base = pomocná znalostní vrstva pro checklisty a hypotézy, ne buy/sell signály
package/coding standards = vlastní Python kód je instalovatelný, typovaný a testovatelný balíček, ne sada ad-hoc skriptů
MVRS = první dokončovací milník do Phase 08 s minimálním Guard Core už ve Phase 05b
operator discipline = přežít, měřit, zlepšovat; ne obcházet kill-switch kvůli emocím
execution context = každý příkaz má jasné prostředí: host, lokální venv, Docker app nebo Docker Freqtrade
schema/network/coverage gates = SQLite schema versioning, bounded retry/backoff, pytest-cov quality gates
final hardening = Docker package import policy, PROJECT_STATE template, pytest-socket offline tests, MVRS scope freeze, Windows-first dev.ps1
plus-safe operation = bounded slices, QUOTA_SAFE_CHECKPOINT, PROJECT_STATE resume, Git/diff persistence, no important work only in chat
```

Finální princip:

```text
Nejdřív ověřit data.
Pak ověřit baseline.
Pak ověřit stabilitu.
Pak auditovat risk.
Pak evidovat daně.
Pak teprve uvažovat o pilotu.
```
