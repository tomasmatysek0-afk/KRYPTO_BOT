# CODEX_MASTER_PLAN_V2_10_NUMBERED_FINAL — coinbase_freqtrade_guarded_bot

> **Document purpose:** final merged master plan for Codex GPT-5.5 for the `coinbase_freqtrade_guarded_bot` project.  
> **How to use:** save this file in the repository root as `CODEX_MASTER_PLAN.md` or `CODEX_MASTER_PLAN_V2_FINAL.md` and reference it in every new Codex session.  
> **Primary mode:** safe, auditable, restartable development in phases.  
> **Primary goal:** research, backtesting, dry-run, and controlled strategy validation for Coinbase spot BTC/ETH.  
> **Codex autonomous mode:** Codex should continue from phase to phase without ongoing user confirmation until it reaches a hard-stop state defined in this document.  
> **Application mode:** custom Python code must be developed as an installable package with unified coding standards, CLI entry points, and a testable architecture, not as a loose set of scripts.  
> **Method validation:** predictive and computational methods must be causal, tested against a baseline, free of lookahead bias/data leakage, and verified for suitability for time series.  
> **Completion priority:** the first milestone is the Minimum Viable Research System (MVRS): data parity, baseline strategy, minimal guard core, backtest report, and dry-run. Enterprise UI, ML/FreqAI, advanced tax export, and trader knowledge base are subsequent hardening/research layers, not blockers for MVRS.  
> **Execution determinism:** every shell command must clearly state its execution context: host PowerShell, local `.venv`, Docker app, or Docker Freqtrade.  
> **Import determinism:** Freqtrade strategies in Docker must have safe and tested imports of custom package code without `sys.path.append` hacks.  
> **Quota safety:** the project must be restartable even if Codex/ChatGPT limits are exhausted; no work may exist only in the conversation without being written to files, the LOG, and ideally Git.  
> **Reproducibility and context:** the project must use locked runtime dependencies and an active working context summary so it can be safely restarted even after long development without overloading the context window.  
> **Non-goal:** guarantee of profit, fast live trading, fully autonomous trading with money without human supervision, or hardware selection/purchase.

---

## 0. Basic principle of the project

This project is intended to create a **safe, auditable, and testable research/dry-run system** for cryptocurrency spot trading through Coinbase.

The project must not be built as an “AI money machine”. It must be built as a technical system:

```text
data
→ data validation
→ baseline strategy
→ backtest
→ robust statistical validation
→ dry-run
→ guard layer
→ audit
→ tax ledger
→ manual approval
→ only later, a limited live pilot
```

Every strategy result must be evaluated after accounting for:

- fees,
- slippage,
- data quality,
- out-of-sample results,
- walk-forward stability,
- drawdown,
- operational risks,
- API errors,
- tax records,
- auditability.

Every algorithm, method, model, or computational procedure must undergo verification of correctness and current validity. Codex must not use an algorithm merely because it is common or known from memory. It must verify:

- whether the method is mathematically and programmatically implemented correctly;
- whether it is suitable for the given data type and trading mode;
- whether newer or more robust methods exist;
- what assumptions and weaknesses the method has;
- whether it is prone to lookahead bias, data leakage, or overfitting;
- whether there is a benchmark against a simpler baseline method;
- whether the result is reproducible on out-of-sample data;
- whether features and labels are correctly aligned in time;
- whether each predictive feature uses only information available at the moment of decision;
- whether chronological splitting or walk-forward/time-series split is used, not random k-fold splitting without a time axis;
- whether any stationarity tests are evaluated using p-values and critical values, not by one hard-coded test-statistic threshold.

Every new Python module must follow the unified coding standards of the project. Codex must not create one-off scripts or non-importable modules where application logic is supposed to be created. The project’s custom code must be importable, typed, testable, and executable through CLI entry points.

---

## 1. Hard security contract

Codex must not violate these rules under any circumstances.

### 1.1 Forbidden in MVP

1. No live trading with real money.
2. No real Coinbase API keys in the repository, code, log, documentation, or responses.
3. No seed phrases, private keys, session cookies, key exports, or secrets.
4. No futures.
5. No leverage.
6. No shorting.
7. No options, perpetuals, margin, lending, or staking in the trading engine.
8. No altcoins in the first version.
9. No adoption of someone else’s strategy based only on Reddit, Telegram, YouTube, or a marketing article.
10. No third-party “arbitrage bot”, smart contract bot, or unverified code executed locally.
11. No live order path until the live pilot criteria are met.
12. No claim of guaranteed profit.
13. No change to a security rule without a separate user decision and an entry in `LOG.md`.

### 1.2 Mandatory in MVP

1. Spot only.
2. Long only.
3. BTC and ETH only.
4. One quote currency consistently: USD or USDC according to the user’s decision.
5. Main timeframe: 4h.
6. Trend filter: 1d.
7. Mode: backtest + dry-run / simulation.
8. Coinbase sandbox is not considered a strategy validation environment.
9. Every trade proposal has an audit record.
10. Every relevant module has tests.
11. Every phase has acceptance criteria.
12. Every phase ends with an entry in `LOG.md`.
13. If something is unclear, Codex stops and asks a question.
14. If the system does not know what happened, it must fail closed.
15. If audit is not possible, trading is not possible.
16. If the kill-switch is active, trading is not possible.
17. If there is an unreconciled order, no further trade is possible.

---

## 2. Codex operating mode

Codex works in **supervised-autonomous execution** mode.

This means:

```text
Codex automatically continues through all phases
if acceptance criteria are met
and no hard-stop state has occurred.
```

Codex must not wait for confirmation after every phase. Instead, after every phase it:

1. writes the result to `LOG.md`;
2. updates `PHASE TRACKER`;
3. creates a brief phase summary;
4. automatically continues to the next phase if no hard-stop has occurred.

### 2.1 Autonomous loop

```text
AUTONOMOUS LOOP:
  1. Read CODEX_MASTER_PLAN.md.
  2. Read AGENTS.md.
  3. Read LOG.md.
  4. Determine the current phase.
  5. Read relevant files in full.
  6. Print call-flow, editable/read-only scope, and execution context for commands.
  7. If research is needed, run the RESEARCH PROTOCOL.
  8. Implement only files in the current scope.
  9. Add/update tests.
 10. Run relevant tests.
 11. If tests fail and the cause is clear, repair within scope; maximum 3 auto-remediation iterations for the same error type. If the 2nd iteration fails on the same error, Codex must run the RESEARCH PROTOCOL before the 3rd attempt to verify the current syntax/API of the given library. If the 2nd iteration fails on the same error, Codex must run the RESEARCH PROTOCOL before the 3rd attempt and verify the current syntax/API of the given library in the official documentation or release notes.
 12. Continuously write LOG checkpoints.
 13. Evaluate acceptance criteria.
 14. If PASS and no hard-stop occurred, continue to the next phase.
 15. If a hard-stop occurred, write the state to LOG.md and stop.
```

### 2.2 Continuous logging for token limits and resuming

Codex must log continuously, not only at the end of a long phase.

Mandatory LOG checkpoint:

- at the beginning of every phase;
- after every significant file change;
- after every research report;
- after every test run;
- before longer refactoring;
- before running a long backtest;
- after completing a long backtest;
- at every blocker;
- before ending a response.

The checkpoint must be brief, but must allow resuming after token exhaustion:

```markdown
### CHECKPOINT — YYYY-MM-DD HH:MM — Phase XX
State:
Done:
In progress:
Files changed since last checkpoint:
Git diff summary:
Execution context used for commands:
Tests:
Identified risks:
Next safe step:
```

### 2.3 Hard-stop states

Codex must stop only in the following cases:

| Hard-stop | What Codex must do |
|---|---|
| It needs an API key, secret, private key, seed, Coinbase login, or authentication file | Write it to `OPEN QUESTIONS`, explain exactly what it needs, why, and in what safe format. Do not ask for a secret to be pasted into chat if a local `.env` can be used. |
| It needs connection to an account, Coinbase, broker, Gmail, repository, or other external system | Write the requirement to `OPEN QUESTIONS`, stop, and wait. |
| It is supposed to set `ALLOW_LIVE_TRADING=true` or open Phase 18 | Stop. Requires explicit user decision and a separate commit. |
| It is supposed to create or submit a live order | Stop. Forbidden in MVP. |
| Data is unavailable even after a safe fallback | Write a blocker report. |
| Data Parity Gate fails and it is not possible to automatically switch to a safe fallback | Write a blocker report and a question. |
| A new dependency’s license is unclear or risky | Write a dependency blocker and a question. |
| A tax/legal rule cannot be safely verified | Write it as a working assumption or stop if it would affect computation. |
| Codex is expected to make a trading/policy decision that changes the user’s risk | Stop. |
| Before MVRS completion Codex wants to shift the work focus to UI/ML/knowledge base/advanced tax export | Write scope drift to LOG.md and return to MVRS. |
| Tests repeatedly fail and the root cause is unclear | Write a blocker report. |
| The same error type fails after 3 auto-remediation iterations | Write a blocker report and stop. |
| Codex does not know whether a command should run in host `.venv`, Docker app, or Docker Freqtrade container | Write an execution-context blocker, do not guess, and stop. |
| Codex is approaching a usage limit or sees a limit warning | Stop expanding scope, write `QUOTA_SAFE_CHECKPOINT`, update `PROJECT_STATE.md`, suggest commit/resume instructions. |

### 2.4 What is NOT a hard-stop

Codex must not ask unnecessarily in these cases:

| Situation | Autonomous handling |
|---|---|
| A small helper file is missing | Create it according to the plan and write it to LOG.md |
| A test failed due to a clear implementation error | Fix it in the repair loop |
| Freqtrade/CCXT Coinbase data fails parity, but Coinbase API data is available | Switch the design to Coinbase API as authoritative data source and create an ADR |
| Research finds a better library with an obviously suitable license and activity | Perform dependency review, write it to the register, and continue |
| The strategy does not beat the baseline | Mark as RESEARCH_ONLY/FAIL, do not run live, continue with reporting and infrastructure-safety work |
| ML does not add robust edge | Mark ML as RESEARCH_ONLY and continue |
| An optional phase blocks MVRS | Mark as POST_MVRS and continue core phases |
| Codex limit interrupts work after a safe checkpoint | After limit reset, continue from `PROJECT_STATE.md`, `LOG.md`, and the latest Git/diff state |
| UI MVP can be done without API keys | Implement only read-only UI over local data |
| A tax rule is not legally definitive | Write it as a working assumption to verify; do not issue tax advice |

### 2.5 Auto-remediation rules

Codex should prefer a safe fallback over stopping.

| Problem | Safe fallback |
|---|---|
| Freqtrade/CCXT Coinbase has a data problem | Coinbase Advanced API downloader as authoritative data source, Freqtrade only as engine |
| 4h data is missing | Deterministically aggregate from closed 1h candles |
| Preview API returns an error | Reject the intent, audit it, continue without live execution |
| Audit writer fails | Activate kill-switch |
| Reconciliation unknown | Block the next intent |
| ML model fails | Return to baseline strategy |
| Dependency is not necessary | Do not add dependency; use standard library or the already existing stack |
| UI dependency is unnecessarily heavy | Use a simpler read-only Streamlit/local report approach |
| SQLite schema drift in MVP/test/dry-run DB | If the DB is marked disposable/replayable, create a backup copy, write it to LOG.md, delete and recreate the DB. If the DB contains valuable dry-run/live data, stop or perform an approved migration. |

### 2.6 User questions — format

If Codex stops, it must not ask a vague question. It must state:

```markdown
## WAITING_FOR_USER — Phase XX

### I need
...

### Why I need it
...

### Architectural impact
...

### Solution options
- Option A:
  - Advantages:
  - Risks:
- Option B:
  - Advantages:
  - Risks:

### Safe way to provide it
...

### What not to send in chat
...

### What I will do after it is provided
...

### Entry in LOG.md
- [ ] question written to OPEN QUESTIONS
```

---

## 3. Plus-safe usage, quota and persistence policy

This project is designed to be usable even on a personal ChatGPT Plus plan. The Plus plan is not intended for unlimited long autonomous runs without interruption; therefore work must be divided into small, restartable blocks.

### 3.1 Basic principle

No important work may exist only in chat.

Every significant step must be saved at least into:

1. project files;
2. `LOG.md`;
3. `PROJECT_STATE.md`;
4. ideally a Git commit or at least a clean `git diff --stat` record.

If a limit is exhausted, a session crashes, the computer restarts, or the service is interrupted, the next session must be able to continue from the repository without reconstructing state from memory.

### 3.2 Plus-safe execution mode

Codex must not plan a long “do the whole project at once” run on the Plus plan.

Instead, it works in bounded slices:

```text
one slice = one small phase, subphase, or one clear acceptance block
```

Recommended size of one slice:

- 1–5 files;
- one clear call-flow;
- one test set;
- one LOG checkpoint;
- one PROJECT_STATE update;
- one suggested commit.

Forbidden:

- merging several large phases into one run;
- starting a long refactor without a previous checkpoint;
- holding a large diff without LOG/PROJECT_STATE entry;
- continuing to the next large block if a usage limit is approaching;
- leaving an in-progress project only in the model response.

### 3.3 Quota-aware checkpoint

Codex must create a quota-safe checkpoint:

- before every long test;
- before every backtest;
- before every refactoring;
- after every larger file change;
- on any limit warning;
- before ending a response.

Format:

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

Codex should suggest a commit after every completed slice.

A commit may be made only if:

- the working tree contains no secrets;
- tests for the given slice passed or the exception is explicitly recorded;
- `LOG.md` and `PROJECT_STATE.md` are updated;
- the commit message is short and phase-labeled.

Recommended format:

```text
phase-00b: add package skeleton and CLI baseline
phase-05b: add minimal guard core
phase-03b: add data parity gate
```

If Codex does not perform the commit, it must at least write:

```powershell
# [HOST_POWERSHELL]
git status
git diff --stat
```

to `LOG.md`.

### 3.5 Usage-limit hard-stop

If Codex sees a limit banner, usage warning, or has reason to expect that the limit will run out during the current work, it must:

1. stop expanding scope;
2. finish or safely discard the small step currently in progress;
3. write `QUOTA_SAFE_CHECKPOINT`;
4. update `PROJECT_STATE.md`;
5. suggest a commit or save the diff;
6. print exact resume instructions.

Codex must not start a new phase when approaching a limit.

### 3.6 Model-tiering policy

For the Plus plan:

| Task type | Recommendation |
|---|---|
| architecture, security, guard layer, tax, reconciliation | use the strongest available reasoning/coding mode |
| routine import fixes, formatting, small tests | use a cheaper/smaller available model if Codex UI/CLI allows selection |
| long research | split into small research reports |
| large refactors | first plan + checkpoint, then implementation in blocks |
| UI cosmetics | POST_MVRS, low priority |

### 3.7 No-project-loss guarantee

The project is considered safely restartable only if these exist:

- `CODEX_MASTER_PLAN.md`;
- `AGENTS.md`;
- `LOG.md`;
- `PROJECT_STATE.md`;
- current project files on disk;
- `git status` known in the latest checkpoint;
- latest safe next command.

If any of these points are missing, Codex must first restore restartability before further implementation.

---

## 4. LOG.md as the single source of truth

`LOG.md` is an append-only work diary. Codex must update it at every phase and every blocker.

### 4.1 LOG.md structure

```markdown
# PROJECT LOG — coinbase_freqtrade_guarded_bot

## STATUS SUMMARY
Current phase: <number and name>
Active agent: <agent name>
Last update: <YYYY-MM-DD HH:MM>
State: TODO | IN_PROGRESS | WAITING_FOR_USER | BLOCKED | DONE
Current branch:
Current commit:
Note:

## OPEN QUESTIONS
- [ ] <date> <phase> — <question for user> (waiting for answer)
- [x] <date> <phase> — <question> → ANSWER: <answer> <answer date>

## PHASE TRACKER
| Phase | Name | State | Completion date | Note |
|---|---|---|---|---|
| 00 | Repository bootstrap | TODO | — | — |
| 01 | Development environment | TODO | — | — |

## DEPENDENCY REGISTER
| Package | Version | License | Reason | Added in phase | Review date | Security status | Lock status |
|---|---|---|---|---|---|---|---|

## DECISION REGISTER
| ADR | Decision | Date | State |
|---|---|---|---|

## ENTRIES

### YYYY-MM-DD HH:MM — Phase XX — <agent>
**Action:**  
**Files read:**  
**Files modified:**  
**Commands run:**  
**Tests:**  
**Research:**  
**Decision:**  
**Result:** DONE / PARTIAL / BLOCKED / WAITING_FOR_USER  
**Next step:**  
```

### 4.2 Entry rules

- `STATUS SUMMARY` is always updated.
- History is not rewritten, only appended.
- Every blocker has a precise reason.
- Every question for the user goes into `OPEN QUESTIONS`.
- Every user answer is written next to the question.
- Every new package goes into `DEPENDENCY REGISTER`.
- Every architectural decision goes into `DECISION REGISTER` and `docs/adr/`.

### 4.3 Context compaction and log archive policy

`LOG.md` must remain usable as working context for Codex. Chronological history must not grow uncontrollably so that it pushes the main instructions out of the context window. At the same time, the audit trail must not be lost.

Therefore:

- `STATUS SUMMARY`, `OPEN QUESTIONS`, `PHASE TRACKER`, `DECISION REGISTER`, and `DEPENDENCY REGISTER` always remain in the main `LOG.md`.
- Detailed `ENTRIES` for the current and previous 3 phases remain in the main `LOG.md`.
- Older detailed records must not be destructively deleted. They are moved to an archive file in `logs/archive/`, for example `logs/archive/LOG_ENTRIES_PHASE_00_03.md`.
- A brief summary of archived phases remains in the main `LOG.md` in the `ARCHIVED SUMMARY` section.
- Every archive file must record a SHA-256 hash and the phase range it contains.
- Before starting a new session, Codex must primarily read `STATUS SUMMARY`, `OPEN QUESTIONS`, `PHASE TRACKER`, `DECISION REGISTER`, `DEPENDENCY REGISTER`, and the latest checkpoint. It opens the archive only if the current task requires historical detail.
- Once the main `LOG.md` exceeds approximately 800 lines or the `ENTRIES` section contains more than 3 completed phases, Codex creates or updates the archive.

Recommended file for quick resumption:

```text
PROJECT_STATE.md
```

`PROJECT_STATE.md` is a short working summary: current phase, last PASS/FAIL, open questions, latest decisions, next safe step. It does not replace `LOG.md`; it only reduces context load.

---

## 5. AGENTS.md — Codex working roles

Codex creates and maintains the file `AGENTS.md`.

### 5.1 Mandatory contents of `AGENTS.md`

```markdown
# AGENTS.md

## Role
You are a senior Python engineer, quantitative analyst, security-oriented architect, and DevOps engineer.

## Project
coinbase_freqtrade_guarded_bot is a research/dry-run crypto trading system for Coinbase.

## Hard limits
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

### 5.2 Agents

| Agent | Active phases | Responsibility |
|---|---|---|
| `architect-agent` | 00, 02, 04 | structure, ADR, documentation, scope |
| `sre-agent` | 01, 02, 08, 08b | Docker, operations, monitoring, execution context, command catalog |
| `data-agent` | 03, 03b, 04 | data, Coinbase/CCXT validation, data quality |
| `strategy-agent` | 05, 15 | strategies, Freqtrade, FreqAI research |
| `quant-research-agent` | 06, 07, 15 | backtesting, validation, overfitting, metrics |
| `guard-agent` | 09, 10, 10b, 11, 17, 18 | risk, audit, kill-switch, preview, reconciliation |
| `tax-agent` | 12 | tax records, exports, FIFO/ledger |
| `ui-agent` | 13 | enterprise dashboard, audit UI |
| `research-agent` | 14 | research update loop, dependency review |
| `knowledge-agent` | 16 | knowledge base of successful crypto traders, trading playbooks, risk checklists |

---

## 6. Project skills

Codex creates the folder:

```text
docs/skills/
```

Skill files are the cumulative knowledge base of the project. They are not logs. Every new finding is written with a date and source.

### 6.1 Mandatory skill files

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

### 6.2 Minimum structure of a skill file

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

## 7. Research protocol

Codex must not guess technical facts. If there is uncertainty, it uses the research protocol.

### 7.1 Source priority

| Question type | Primary sources |
|---|---|
| Coinbase API | Coinbase official docs, coinbase-advanced-py GitHub, StackOverflow |
| Freqtrade | Freqtrade docs, Freqtrade GitHub issues |
| CCXT | CCXT docs, CCXT GitHub issues |
| Hummingbot/Jesse/OctoBot comparison | official docs, GitHub issues, community experience |
| ML/trading validation | FreqAI docs, sklearn, LightGBM/XGBoost docs, López de Prado, Ernest Chan, QuantConnect |
| UI | FreqUI, Streamlit, FastAPI, React dashboard patterns |
| Tax | current Czech legal/tax sources, expert articles, tax advisor; Codex must not claim a definitive legal conclusion without verification |
| Algorithm validation | official library documentation, academic sources, benchmark implementations, GitHub issues, quant literature |
| Crypto trader knowledge | public interviews, verifiable sources, books, blogs, podcasts, public post-mortems; do not adopt signals without validation |

### 7.2 GitHub / Reddit / GitLab rules

- GitHub issue = evidence of a real problem or workaround, not necessarily a general rule.
- Reddit = experiential signal, not an authoritative source.
- GitLab = secondary source; often a mirror, but verify if relevant.
- Official documentation = primary source for API and config.
- Academic/quant source = primary source for method validation.
- Reviews and stars are not proof of profitability.
- A strategy is not adopted just because someone praises it.

### 7.2a MIT-first active search policy

When searching for a new library, framework, reference implementation, or algorithmic solution, Codex must actively prefer open and compatible licenses already during the research phase, not only after choosing a dependency.

Preference order:

1. Python standard library or a simple custom implementation, if safe and auditable.
2. Official library/API client of the given service.
3. Actively maintained projects with MIT / Apache-2.0 / BSD license.
4. GPL projects only after a conscious decision and entry of impact into LOG.md / ADR.
5. Do not use unmaintained, unclearly licensed, or marketing-suspicious projects.

When comparing candidates, Codex evaluates:

- license;
- commit activity;
- age of latest release;
- number and age of open issues;
- security advisories;
- documentation quality;
- test coverage, if discoverable;
- community usage;
- GitHub stars only as a weak popularity signal;
- compatibility with Python/Docker stack of the project;
- possibility of replacing the dependency with simpler custom code.

MIT-first research output must be written to `reports/research/` and summarized in `docs/skills/dependency_review.md`.

### 7.3 Research output

Every research report is saved to:

```text
reports/research/YYYY-MM-DD_<topic>.md
```

The report must contain:

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

Codex must not add a dependency without review.

### 8.1 Before adding a dependency Codex must write

- package name;
- version;
- license;
- reason for use;
- alternatives;
- security risks;
- project activity;
- impact on Docker image;
- whether the package is runtime-only or dev-only;
- entry in `LOG.md`;
- entry in `DEPENDENCY REGISTER`;
- method of pinning / locking the runtime environment.

### 8.1a Dependency pinning and lock policy

Distinguish two dependency layers:

1. **Project metadata in `pyproject.toml`** — reasonable compatible ranges may be used here for library metadata. Do not use unnecessarily hard exact pins in package metadata if it would hinder installation or testing.
2. **Reproducible runtime environment** — exact versions of all direct and transitive dependencies must be locked here.

Mandatory files for reproducibility:

```text
requirements.lock
requirements-dev.lock
constraints.txt
```

Rules:

- Runtime and dev environments must have exact pins in the format `package==X.Y.Z` in lock/requirements files.
- Loose specifications such as `package>=X` must not be used in a lock file.
- A compatible range `package~=X.Y` is allowed only in the abstract `pyproject.toml` layer, not as the final runtime lock.
- Before updating a dependency, Codex must create a research/dependency review entry and run relevant tests.
- If the tool supports hash checking or lock files, prefer it for automated environments.
- Codex must write to `DEPENDENCY REGISTER` whether the dependency is pinned in the lock file and when it was last verified.

Recommended procedure:

```bash
python -m pip install -e .
python -m pip freeze > requirements.lock
python -m pip check
```

If `pip-tools` or another locking tool is introduced, it must pass dependency review.


### 8.1b Bootstrap minimal dependency policy

Phase 00b must not add an unnecessary stack.

Allowed bootstrap/dev stack:

- `hatchling` or `setuptools`;
- `pytest`;
- `pytest-cov`;
- `pytest-socket`;
- `ruff`;
- `pydantic` / `pydantic-settings`, if config/domain models already exist;
- `mypy` or `pyright` only as a quality gate if it does not delay MVRS.

Deferred dependencies:

- `tenacity`: add only when implementing network resilience in Phase 03b/08b;
- `SQLModel`: add only if JSONL/SQLite is insufficient and an ADR exists;
- `Alembic`: add only after introducing SQLModel/SQLAlchemy migrations;
- `LightGBM`, `XGBoost`, FreqAI extras: only Phase 15;
- UI extras: only Phase 13.

Every deferred dependency must have an explicit reason in LOG.md explaining why it is now truly needed.

### 8.2 Preferred licenses

Prefer:

- MIT,
- Apache-2.0,
- BSD.

Acceptable with awareness of impacts:

- GPLv3, if it is a framework such as Freqtrade and the project remains internal.

Unclear licenses = stop and ask.

---

## 9. Algorithm validation policy

When designing or modifying an algorithm, Codex must verify that the method is correct, suitable, and that there is no obviously better current approach.

### 9.1 What counts as an algorithm

- trading strategy;
- indicator;
- feature engineering;
- risk calculation;
- position sizing;
- stop-loss / take-profit logic;
- backtest metric;
- walk-forward validation;
- Monte Carlo simulation;
- ML model;
- FreqAI model;
- tax/FIFO calculation;
- reconciliation rule;
- data aggregation rule.

### 9.1a Causal feature and time-series validation policy

Codex must enforce data causality in all trading/ML functions.

Mandatory:

- no function may access future candles;
- all predictive features must be available at the moment of decision;
- labels may use future movement only as a training target and must be separate from features;
- tests must verify that the feature matrix does not contain columns created from the future;
- random `KFold` splitting without a time axis is forbidden for ML validation;
- use chronological split, walk-forward, `TimeSeriesSplit`, or purged/gap split according to label type;
- indicators based on OHLCV must use only closed candles;
- if aggregating 1h → 4h, aggregation must be deterministic and must not include an unclosed candle;
- missing OHLCV candles must not be blindly interpolated; either fill from an authoritative lower timeframe, or Data Quality Gate returns WARN/FAIL.

Stationarity:

- raw prices must not be used as direct input into regression/ML models without Algorithm Review;
- prefer returns, logarithmic returns, normalized distance from trend, or other causal transforms;
- ADF test is an allowed tool, but not the only gate;
- do not use a single hard-coded test statistic threshold such as `ADF < -3.4`; evaluate the p-value and critical values from the used implementation;
- fractional differencing is a research-only candidate, not a mandatory step for MVP.

### 9.2 Mandatory Algorithm Review

Before using a new algorithm, Codex must create or update:

```text
docs/skills/algorithm_review.md
```

and, depending on significance, also:

```text
reports/research/YYYY-MM-DD_algorithm_<topic>.md
```

The review must contain:

- algorithm/method name;
- purpose;
- inputs and outputs;
- mathematical description or pseudocode;
- assumptions;
- known weaknesses;
- possible better alternatives;
- reason for selection;
- correctness tests;
- benchmark against baseline;
- out-of-sample verification if it is a trading/ML method;
- link to sources.

### 9.3 Mandatory comparison with baseline

No sophisticated algorithm may be accepted unless it is compared against a simpler baseline.

Examples:

| Area | Baseline |
|---|---|
| Trading strategy | buy-and-hold, simple trend-following |
| ML model | logistic regression / simple tree |
| Feature set | returns + volatility + volume |
| Risk sizing | fixed fractional risk |
| Backtest validation | simple out-of-sample split |
| Tax calculation | manually verified FIFO example |

### 9.4 Stop rule

Codex stops if:

- the method looks sophisticated, but it is unclear why it should work;
- the method improves the backtest, but worsens out-of-sample results;
- the method has a data leakage risk;
- the method is adopted without a clear license;
- the method requires live data or live trading;
- there is a conflict between sources and Codex does not know what is correct.

---

## 10. Coding standards and package architecture

This section is binding for all phases. Codex must not produce a vibecoded mixture of scripts. Custom application logic must be structured as an installable Python package.

### 10.1 Python coding standards

Mandatory rules:

- Python 3.11+.
- Every module has a module docstring describing the module purpose.
- Every public function/method/class has type hints.
- Every public function/method/class has a concise docstring.
- Internal helper functions have type hints; docstring only if the logic is not obvious.
- Domain models must not be loose `dict`/`tuple`; use `dataclasses` or Pydantic models.
- One class/module = one responsibility.
- No “god files” with unrelated logic.
- No magic constants; use named constants or config.
- No `print()` in business logic; use structured logger.
- No broad `except Exception` without justification and audit entry.
- Model errors using domain exceptions.
- IO layer and business logic must be separated.
- Computation functions should be deterministic and testable without network.
- All code that changes decision logic requires a test.
- Critical functions in Guard, Reconciliation, Data Parity, Backtest Metrics, and Tax/FIFO layers must have deterministic unit tests including edge cases.

### 10.2 Modeling rules

| Area | Recommended approach |
|---|---|
| Env/config validation | Pydantic / pydantic-settings |
| Domain immutable objects | `@dataclass(frozen=True)` or Pydantic frozen model |
| API request/response schema | Pydantic model |
| Audit event | Pydantic/dataclass + explicit JSON serializer |
| Computation functions | pure functions with types |
| Risk/reconciliation decision | explicit result object, not a bool without a reason |
| Tax ledger entry | dataclass/Pydantic model with validation |

### 10.3 Package layout

Custom application code should be under `src/coinbase_freqtrade_guarded_bot/`.

Recommended layout:

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

Freqtrade runtime folder `user_data/` remains outside the package because it is a Freqtrade convention. Strategies in `user_data/strategies/` may import helper validated functions from the package.

### 10.4 pyproject.toml and CLI

The project must have a working `pyproject.toml`.

Recommended default stack for the custom application layer:

- build backend: `hatchling` by default; `setuptools` is an acceptable alternative after ADR;
- formatting/linting: `ruff`;
- tests: `pytest`;
- typing: `mypy` or `pyright` as a quality gate depending on phase;
- config/schema validation: `pydantic` v2 and optionally `pydantic-settings`;
- MVP storage: append-only JSONL + SQLite; SQLModel only after dependency review and ADR if JSONL/SQLite is insufficient.

Mandatory:

```bash
pip install -e .
python -m coinbase_freqtrade_guarded_bot --help
pytest
ruff check .
```

Recommended depending on phase:

```bash
mypy src
```

Mandatory CLI entry points no later than Phase 00b/07:

```toml
[project.scripts]
cbot-data-parity = "coinbase_freqtrade_guarded_bot.cli:data_parity"
cbot-backtest-report = "coinbase_freqtrade_guarded_bot.cli:backtest_report"
cbot-dryrun-healthcheck = "coinbase_freqtrade_guarded_bot.cli:dryrun_healthcheck"
cbot-tax-export = "coinbase_freqtrade_guarded_bot.cli:tax_export"
```

CLI must not have a live execution command in MVP.

### 10.5 Quality gates

Codex must maintain at least:

- `pytest`;
- `ruff check .`;
- import smoke test;
- no-secrets grep/smoke test;
- offline unit-test gate through `pytest-socket --disable-socket`.

Network sanity gate:

- Unit tests should disable sockets by default via `pytest-socket`.
- Tests that need network must be explicitly marked as integration tests and must not run in the default unit-test command.
- Coinbase/API SDK calls in unit tests must be mocked.
- Exceptions for localhost/Unix socket are allowed only with a comment and test marker.

Coverage policy:

- Phase 00b introduces `pytest-cov` as a dev dependency after dependency review.
- From Phase 05b, `pytest --cov=src --cov-branch --cov-fail-under=85` must run if enough non-trivial application code already exists.
- In Phase 05b–07, the mandatory fallback is `critical paths only`: test primarily Guard Core, Data Parity, and Backtest Metrics edge cases, even if global coverage is not yet representative.
- Critical layers `guard_layer`, `data_layer/data_parity`, `tax_layer`, `reconciliation`, and `research/metrics` must target 95%+ branch coverage before Phase 17.
- If per-module coverage cannot be enforced directly by pytest-cov, Codex creates `scripts/check_critical_coverage.py`, which reads coverage JSON and verifies critical thresholds.
- A trivial test without edge cases must not satisfy acceptance criteria for a critical phase.

Mypy/pyright is recommended; if it would slow down bootstrap, Codex may mark it as a later quality gate, but must write that to LOG.md.

### 10.5a Document completeness check

Phase 00b must verify that all new governing sections have corresponding documents and skills.

Minimum check:

| Section | Document | Skill |
|---|---|---|
| Coding standards | `docs/CODING_STANDARDS.md` | `docs/skills/coding_standards.md` |
| Packaging | `docs/PACKAGING.md` | `docs/skills/packaging_app_architecture.md` |
| Execution context | `docs/EXECUTION_CONTEXT.md` | `docs/skills/execution_context.md` |
| Network resilience | `docs/NETWORK_RESILIENCE.md` | `docs/skills/network_resilience.md` |
| DB schema policy | `docs/DB_SCHEMA_POLICY.md` | `docs/skills/db_schema_migrations.md` |
| Test quality gates | `docs/TEST_QUALITY_GATES.md` | `docs/skills/test_quality_gates.md` |
| Codex usage policy | `docs/CODEX_USAGE_POLICY.md` | `docs/skills/codex_usage_budget.md` |

Codex must write the check result to `LOG.md` and `PROJECT_STATE.md`.

### 10.6 Forbidden coding patterns

- ad-hoc `sys.path.append(...)`;
- imports dependent on the current working directory;
- unvalidated global variables for config;
- direct `.env` reading inside business logic;
- silent failure without audit entry;
- `dict` as a substitute for domain model;
- live/execution side effect in import-time code;
- network call in a unit test without mock;
- trading decision in the UI layer.

---

## 11. Execution context and command policy

Codex must not guess where a command should run. Every command in a response, LOG, RUNBOOK, or prompt must be marked with one of these contexts:

| Context | Use |
|---|---|
| `[HOST_POWERSHELL]` | Git repository operations, folders, Docker commands on Windows host |
| `[LOCAL_VENV]` | local Python package, pytest, ruff, mypy, CLI app commands |
| `[DOCKER_APP]` | app container, if a separate container exists for the custom Python application |
| `[DOCKER_FREQTRADE]` | Freqtrade CLI, Freqtrade config validation, Freqtrade backtest/dry-run commands |

### 11.1 Canonical command catalog

Phase 00b must create at least one of these tools:

- `Makefile`, if make is available;
- `scripts/dev.ps1` as Windows-first fallback;
- `docs/RUNBOOK.md` with a command catalog.

Preferred examples:

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

Freqtrade strategies in `user_data/strategies/` may import only validated helper functions and models from the package `coinbase_freqtrade_guarded_bot`.

Forbidden:

- `sys.path.append(...)`;
- copying source files to `user_data/strategies/`;
- duplicate definitions of `OrderIntent`, `RiskDecision`, `settings`, or guard models in the strategy;
- import-time side effects.

Allowed dev/MVRS method:

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

Allowed later production-like method:

```text
custom Freqtrade image
→ install package wheel / regular install
→ no editable bind mount
```

Acceptance:

- Phase 02 must include Docker import smoke test:
  `python -c "import coinbase_freqtrade_guarded_bot"`.
- Strategy import test must verify that `user_data/strategies/CoinbaseTrendGuardV1.py` can import the package without `sys.path.append`.
- If import in Docker fails, Codex must not solve the issue with a hack; it must fix compose/PYTHONPATH or package install.

### 11.3 Environment ownership

| Artifact | Environment owner |
|---|---|
| `src/coinbase_freqtrade_guarded_bot/` | local `.venv` / app container |
| `tests/` | local `.venv` / CI |
| `user_data/` | Freqtrade container |
| `docker-compose.yml` | host Docker |
| `reports/` | shared output, generated by CLI or containers |
| `.env` | local host, never commit |

### 11.4 Stop rule

If Codex does not know where a command should run, it must not continue by guessing. It must:

1. write an execution-context blocker to `LOG.md`;
2. state possible contexts;
3. suggest a safe default;
4. stop if the wrong context could change environment, data, or installations.

---

## 11A. NO_DOCKER_LOCAL_MODE and Docker portability policy

`NO_DOCKER_LOCAL_MODE` is an approved local development mode for a workstation where Docker Desktop, Docker Compose, and WSL2 are unavailable and administrator rights are not available.

### 11A.1 Local limitation

The current local environment has these confirmed constraints:

- Docker Desktop is unavailable locally.
- Docker Compose is unavailable locally.
- WSL2 is unavailable locally.
- Administrator privileges are not available for installing or repairing these tools.
- `winget` cannot install Docker because the `winget` source fails with `0x8a15000f : Data required by the source is missing`.
- `winget source reset --force` requires administrator privileges and must not be attempted by Codex in this mode.

Codex must not stop only because Docker/WSL are missing while `NO_DOCKER_LOCAL_MODE` is active. Codex must also not ask the user again to install Docker/WSL during this mode.

### 11A.2 Decision

Local development continues without Docker. Docker remains part of the target architecture and must not be removed, bypassed, or treated as obsolete.

Local work may continue on:

- Python package structure;
- CLI;
- local pytest, ruff, pytest-cov, and pytest-socket checks;
- guard layer;
- audit writer;
- kill-switch;
- risk limits;
- data parity logic with mocked/offline data;
- tax ledger;
- SQLite schema policy;
- reports;
- documentation;
- offline tests.

The following work is postponed until a Docker-capable environment is available:

- Docker Compose validation;
- Freqtrade container execution;
- Docker import smoke tests;
- Freqtrade dry-run runtime;
- any command requiring administrator rights;
- any command requiring credentials or secrets.

### 11A.3 Acceptance criteria status

Docker-dependent acceptance criteria must be marked `DEFERRED_DOCKER_REQUIRED`.

This means:

- the criterion is not considered passed;
- the criterion is not considered failed solely because Docker is unavailable locally;
- the criterion remains mandatory before live-pilot readiness;
- the criterion must be revalidated on a future Docker-capable machine.

Known deferred criteria include:

- Docker Compose config validation;
- Freqtrade container start;
- Freqtrade container package import smoke tests;
- Docker-based strategy import smoke tests;
- Docker/Freqtrade backtest execution;
- Docker/Freqtrade dry-run execution.

### 11A.4 Portability requirements

All local work must remain portable to Docker and to another workstation.

Required:

- use relative repository paths in application logic and configuration examples;
- keep application logic under `src/coinbase_freqtrade_guarded_bot/`;
- keep Docker-related files maintainable even when not locally validated;
- keep Freqtrade-facing imports compatible with the package import policy;
- keep tests runnable in the local virtual environment without network access by default;
- keep generated reports and runtime data out of Git unless explicitly intended.

Forbidden:

- Windows-only hardcoded paths in application logic;
- application code that depends on the current developer's user profile path;
- replacing Docker/Freqtrade architecture with a local-only architecture;
- marking Docker runtime validation as passed without actually running it;
- using secrets, real API keys, or live trading to compensate for missing Docker validation.

### 11A.5 Future Docker handoff checklist

When a Docker-capable environment is available, Codex must run a bounded Docker revalidation slice before any Docker-dependent phase can be considered complete:

- verify `[HOST_POWERSHELL] docker --version`;
- verify `[HOST_POWERSHELL] docker compose version`;
- verify `[HOST_POWERSHELL] wsl --status` on Windows if WSL2 is the Docker backend;
- run `[HOST_POWERSHELL] docker compose config`;
- run `[DOCKER_FREQTRADE] docker compose run --rm freqtrade --help`;
- run the Docker package import smoke test;
- run the Freqtrade strategy import smoke test without `sys.path.append`;
- verify `dry_run=true` in Freqtrade config;
- verify there are no real API keys or secrets in Docker config;
- update `LOG.md`, `PROJECT_STATE.md`, and the relevant phase tracker rows with PASS or remaining blockers.

---

## 12. Network I/O, rate limiting and retry policy

All network operations against Coinbase, CCXT, Freqtrade API, or external sources must be separated from business logic.

### 12.1 Mandatory rules

- Every HTTP/API call must have an explicit timeout.
- Every retry must have an upper attempt limit and total deadline.
- HTTP 429 must respect `Retry-After` if available.
- HTTP 5xx/503 and temporary network errors use exponential backoff with jitter.
- 401/403 is not retried indefinitely; it is an auth/policy problem and leads to fail-closed / WAITING_FOR_USER depending on phase.
- Network calls must not run in import-time code.
- Unit tests must not perform real network calls.
- Long data downloads run through CLI/worker and write checkpoints.
- Kill-switch and audit must not wait for long network downloads in the same thread/process.

### 12.2 Sync vs async policy

MVRS default is a synchronous client with timeouts, retry/backoff, and bounded concurrency. Async I/O is not mandatory for MVP.

Async (`asyncio`, `aiohttp`, async SDK) is allowed only if:

- an ADR exists;
- there is a clear reason why a synchronous bounded client is insufficient;
- there are tests for cancellation, timeout, and retry;
- kill-switch is not blocked by waiting on network;
- complexity does not move the project outside MVRS.

### 12.3 Tenacity/backoff dependency policy

`tenacity` is an allowed candidate for the retry/backoff layer because it supports stop conditions, wait strategies, exponential backoff, jitter, and retry for coroutines. Still, it must pass dependency review and pinning policy.

### 12.4 Acceptance

The network layer must have tests for:

- 429 + Retry-After;
- 503 + retry;
- timeout;
- auth 401 without infinite retry;
- bounded retry count;
- audit record of retry/fail;
- fail-closed after deadline exceeded.

---

## 13. Target architecture

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

# 14. Phase plan

Codex may autonomously move to the next phase if the current phase’s acceptance criteria are met, the result is written to `LOG.md`, and no hard-stop state has occurred.

---

## Phase 00 — Repository bootstrap, scope, AGENTS, LOG, docs/skills

**Agent:** `architect-agent`

### Goal

Create a safe project skeleton, work rules, LOG, agents, and skills.

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

### Tasks

1. Create the basic project structure.
2. Create `LOG.md` according to the format in this document.
3. Create `AGENTS.md`.
4. Create skill files.
5. Create `.env.example` with placeholders only.
6. Create `.gitignore` for secrets, logs, DB, cache, exports, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`, `.mypy_cache/`, `.venv/`, large `reports/*.csv`, `reports/*.parquet`, `reports/*.jsonl`, and local runtime artifacts.
7. Add disclaimer to README.
8. Write that MVP does not support live trading.

### Acceptance criteria

- [ ] `LOG.md` exists.
- [ ] `AGENTS.md` exists.
- [ ] `docs/skills/` exists.
- [ ] `.env.example` contains no secrets.
- [ ] `.gitignore` excludes `.env`, DB, logs, exports, secrets, cache folders, `.venv/`, large CSV/Parquet/JSONL reports, and runtime artifacts.
- [ ] README contains risk disclaimer.
- [ ] RISK_POLICY contains the ban on live trading, leverage, futures, shorts, and secrets.
- [ ] Coinbase sandbox is marked unsuitable for strategy validation.
- [ ] Phase written to `LOG.md`.

---

## Phase 00b — Coding standards, package skeleton, pyproject, CLI baseline

**Agent:** `architect-agent`

### Goal

Ensure the project is created as an installable Python application with a unified code style, not as a collection of scripts.

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

### Tasks

1. Create `src/coinbase_freqtrade_guarded_bot/`.
2. Create minimal `pyproject.toml`.
3. Set package metadata including `[project.urls]`.
4. Configure `pytest`.
5. Configure `ruff`.
6. Configure `pytest-cov` and coverage command.
7. Configure `pytest-socket` with default `--disable-socket`.
8. Prepare optional `mypy`/typing gate.
9. Create minimal CLI with `--help`.
10. Create Windows-first command catalog in `scripts/dev.ps1`; `Makefile` is secondary convenience.
11. Mark every command with execution context.
12. Verify local editable install through `python -m pip install --upgrade pip` and `python -m pip install -e .`.
13. Create `docs/CODEX_USAGE_POLICY.md` and write Plus-safe slice workflow.
14. Verify that `PROJECT_STATE.md` contains quota-safe resume fields.
8. Create import smoke test.
9. Add coding standards to `docs/CODING_STANDARDS.md`.
10. Add packaging rules to `docs/PACKAGING.md`.
11. Update `AGENTS.md` so application logic belongs in `src/`.

### Acceptance criteria

- [ ] `pip install -e .` works.
- [ ] `[LOCAL_VENV] python -m pip install --upgrade pip` succeeds.
- [ ] `[LOCAL_VENV] python -m pip install -e .` succeeds.
- [ ] `python -m coinbase_freqtrade_guarded_bot --help` works.
- [ ] Minimal CLI exists without live execution commands.
- [ ] `pytest` passes at least import/CLI smoke tests.
- [ ] `pytest-cov` is configured.
- [ ] `pytest-socket` is configured with default socket ban for unit tests.
- [ ] `scripts/dev.ps1` exists as the primary Windows-first entry point.
- [ ] Command catalog exists and distinguishes `[HOST_POWERSHELL]`, `[LOCAL_VENV]`, `[DOCKER_APP]`, `[DOCKER_FREQTRADE]`.
- [ ] `ruff check .` passes or is documented as TODO with reason.
- [ ] `docs/CODING_STANDARDS.md` exists.
- [ ] `docs/PACKAGING.md` exists.
- [ ] Document Completeness Check PASS for coding/packaging/execution/network/db/test/usage docs and skills.
- [ ] `docs/CODEX_USAGE_POLICY.md` exists.
- [ ] `PROJECT_STATE.md` contains quota-safe resume fields.
- [ ] Phase 00b can end with a safe `QUOTA_SAFE_CHECKPOINT`.
- [ ] `requirements.lock`, `requirements-dev.lock`, or documented locking procedure exists.
- [ ] Document contains complete phases 00–18; Codex performs Document Completeness Check and writes result to LOG.md.
- [ ] `AGENTS.md` contains code style rules.
- [ ] Application logic is directed to `src/coinbase_freqtrade_guarded_bot/`.
- [ ] Phase written to `LOG.md`.

---

## Phase 01 — Development environment

**Agent:** `sre-agent`

### Goal

Verify the local environment.

### Check commands

```bash
docker --version
docker compose version
git --version
python --version
```

On Windows also:

```powershell
wsl --status
```

### Tasks

1. Verify available tools.
2. If something is missing, write exact commands for the user to `LOG.md`.
3. Verify that `.env` is not tracked by Git.
4. Recommend development mode: local PC.
5. Write that production 24/7 mode will be handled later in an infrastructure phase.

### Acceptance criteria

- [ ] Tool versions written to `LOG.md`.
- [ ] `git status` does not show `.env`.
- [ ] If a tool is missing, state `WAITING_FOR_USER`.
- [ ] No secrets.

---

## Phase 02 — Freqtrade Docker skeleton

**Agent:** `architect-agent` + `sre-agent`

### Goal

Run Freqtrade in Docker in safe dry-run/backtest mode.

### Editable files

- `docker-compose.yml`
- `user_data/config/config.dryrun.json`
- `user_data/config/config.backtest.json`
- `user_data/config/pairlist.json`
- `docs/RUNBOOK.md`
- `tests/test_no_live_execution.py`

### Requirements

- `dry_run` must be true.
- No API keys.
- No live order.
- WebUI only locally.
- UI must not be exposed publicly to the internet.
- Containers must not expose unencrypted ports to the external network; local ports only through explicit localhost binding.
- Config must not contain futures/leverage/short.
- `src/` must be available inside the Freqtrade container through a safe path:
  - MVRS/dev: bind mount `./src:/freqtrade/src:ro` + `PYTHONPATH=/freqtrade/src`;
  - later: custom image with regular package install.
- Solving imports through `sys.path.append` is forbidden.

### Check commands

```bash
docker compose pull
docker compose run --rm freqtrade --help
docker compose config
```

### Acceptance criteria

- [ ] Docker compose config is valid.
- [ ] Freqtrade container has access to package code through mount/PYTHONPATH or package install.
- [ ] Docker import smoke test `python -c "import coinbase_freqtrade_guarded_bot"` PASS.
- [ ] Strategies do not contain `sys.path.append`.
- [ ] Freqtrade container can be started.
- [ ] `dry_run=true`.
- [ ] Test verifies that live mode is not allowed.
- [ ] No real API keys.
- [ ] Phase written to LOG.md.

---

## Phase 03 — Coinbase/Freqtrade capability check

**Agent:** `data-agent`

### Goal

Verify current Coinbase support in Freqtrade/CCXT.

### Editable files

- `docs/RUNBOOK.md`
- `docs/DATA_SOURCE_POLICY.md`
- `docs/skills/freqtrade_coinbase_ccxt.md`
- `reports/research/YYYY-MM-DD_coinbase_freqtrade_capability.md`
- `LOG.md`

### Research required

Codex must verify:

- current Freqtrade docs;
- current CCXT Coinbase support;
- Freqtrade issues around Coinbase support;
- Coinbase product/pair naming;
- known OHLCV problems;
- known fetch limit problems;
- known timestamp and volume problems.

### Check commands

```bash
docker compose run --rm freqtrade list-exchanges
docker compose run --rm freqtrade list-pairs --exchange coinbase
docker compose run --rm freqtrade --version
```

### Decision tree

| Result | State | Next step |
|---|---|---|
| Coinbase works in Freqtrade and pairs/data look OK | PASS | continue to Phase 03b — Data Parity Gate |
| Coinbase sees pairs, but data does not match | PARTIAL | use Freqtrade as engine, download data through Coinbase Advanced API and convert to Freqtrade format |
| Coinbase does not work at all | BLOCKED | stop, write OPEN QUESTION, propose alternatives, and wait for user decision |
| Coinbase works only with different pair naming | WARN | document mapping `BTC/USD` vs `BTC-USD` |
| data has limited history | WARN/BLOCKED | decide whether the range is sufficient for backtest and out-of-sample validation |


### Acceptance criteria

- [ ] Research report exists.
- [ ] `docs/skills/freqtrade_coinbase_ccxt.md` updated.
- [ ] It is clear whether Freqtrade sees Coinbase.
- [ ] It is clear which pairs are available.
- [ ] If unclear, Codex stops.
- [ ] Decision written to LOG.md.

---

## Phase 03b — Data Parity Gate

**Agent:** `data-agent`

### Goal

Verify that data from Freqtrade/CCXT matches data from Coinbase Advanced API.

Without this gate, the backtest is not sufficiently trustworthy.

### Editable files

- `src/coinbase_freqtrade_guarded_bot/guard_layer/data_parity.py`
- `src/coinbase_freqtrade_guarded_bot/network/http_client.py`
- `scripts/compare_coinbase_data_sources.py`
- `tests/test_data_parity.py`
- `docs/DATA_SOURCE_POLICY.md`
- `reports/data_parity/.gitkeep`
- `LOG.md`

### Requirements

- Compare only closed candles.
- Convert all timestamps to UTC.
- Support BTC/USD and ETH/USD.
- Support 1h and 1d.
- If 4h is not native through Coinbase API, aggregate 1h → 4h deterministically from closed 1h candles.
- Compare:
  - timestamp,
  - open,
  - high,
  - low,
  - close,
  - volume.
- Generate markdown report.
- Missing candles must not be interpolated from surrounding values; only filling from an authoritative lower timeframe is allowed, otherwise FAIL/WARN.

### Tolerance

| Field | Rule |
|---|---|
| timestamp | exact match after alignment |
| OHLC | only configurable rounding tolerance; no fixed universal value without ADR |
| volume | WARN/FAIL tolerance mode according to config |
| missing candle | FAIL |
| shifted candle | FAIL |
| unclosed current candle | ignore |

### Acceptance criteria

- [ ] Data parity report exists.
- [ ] Tests use mock data.
- [ ] Network layer has timeout/retry/backoff tests for 429/503/timeout.
- [ ] Missing candles = FAIL.
- [ ] Shifted timestamps = FAIL.
- [ ] OHLC difference above tolerance = FAIL.
- [ ] If gate fails, Codex stops and asks the user.
- [ ] Result written to LOG.md.

---

## Phase 04 — Data source decision ADR

**Agent:** `architect-agent` + `data-agent`

### Goal

Decide the authoritative data source.

### Editable files

- `docs/adr/ADR-002-data-source-policy.md`
- `docs/DATA_SOURCE_POLICY.md`
- `LOG.md`

### Options

1. Freqtrade/CCXT data is OK and used for backtest.
2. Freqtrade/CCXT data is not OK; data is downloaded through Coinbase Advanced API and converted into Freqtrade format.
3. Hybrid: Freqtrade engine, Coinbase API as validation source.

### Acceptance criteria

- [ ] ADR exists.
- [ ] Decision has a date.
- [ ] Decision has a reason.
- [ ] Decision states risks.
- [ ] Decision states what happens on data failure.
- [ ] LOG updated.

---

## Phase 05 — Baseline strategy V1

**Agent:** `strategy-agent`

### Goal

Create a simple, readable, and auditable baseline strategy without ML.

### Editable files

- `user_data/strategies/CoinbaseTrendGuardV1.py`
- `docs/ARCHITECTURE.md`
- `docs/RUNBOOK.md`
- `tests/test_strategy_sanity.py`
- `LOG.md`

### Strategy

- Long-only.
- Spot.
- BTC/ETH.
- Main timeframe: 4h.
- Informative timeframe: 1d.
- Trend filter.
- Momentum filter.
- Volume filter.
- Volatility guard.
- Protection against overextended candle.
- `enter_tag`.
- `exit_reason`.

### Forbidden

- ML.
- FreqAI.
- Hyperopt.
- Futures.
- Leverage.
- Short.
- Too many parameters.
- Magic constants without comment.

### Acceptance criteria

- [ ] Strategy can be loaded by Freqtrade.
- [ ] `can_short = False`.
- [ ] No leverage.
- [ ] Every entry has `enter_tag`.
- [ ] Volatility/volume guard exists.
- [ ] Sanity test PASS.
- [ ] No optimization on historical result.
- [ ] Used indicators and rules have a brief Algorithm Review.
- [ ] LOG updated.

---

## Phase 05b — Minimal Guard Core before backtest/dry-run expansion

**Agent:** `guard-agent` + `architect-agent`

### Goal

Create a minimal safety core before the project starts generating larger numbers of signals and dry-run events.

This phase is not the full Phase 09 Guard Layer. It is a minimal, simple, and testable layer for MVRS.

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

### Minimum scope

- `OrderIntent` domain model.
- `RiskDecision` domain model.
- JSONL append-only audit writer.
- File-based kill-switch through file `KILL_SWITCH`.
- Env/config flag for halt state.
- Basic risk limits:
  - max stake per intent;
  - max open intents/positions;
  - no live execution;
  - no leverage/futures/short.
- Rejected intent is also written to audit.

### Forbidden

- Coinbase live order.
- Coinbase preview integration.
- Reconciliation against exchange.
- Complex ORM.
- UI toggle as primary mechanism.

### Acceptance criteria

- [ ] `OrderIntent` and `RiskDecision` are typed domain models.
- [ ] Audit writer writes append-only JSONL.
- [ ] Active `KILL_SWITCH` file blocks intent.
- [ ] `ALLOW_LIVE_TRADING=false` blocks live execution path.
- [ ] Rejected intent is audited.
- [ ] Unit tests PASS.
- [ ] Phase 08 dry-run will use minimal guard core.
- [ ] LOG updated.

---

## Phase 06 — Advanced backtest validation

**Agent:** `quant-research-agent`

### Goal

Validate the baseline strategy robustly, not just by one nice-looking backtest.

### Editable files

- `scripts/run_backtest_report.py`
- `docs/RUNBOOK.md`
- `docs/skills/backtest_validation.md`
- `reports/backtests/.gitkeep`
- `LOG.md`

### Mandatory scenarios

| Scenario | Description |
|---|---|
| Base fee | conservative maker/taker model |
| Worst fee | roundtrip worst-case |
| Slippage low | low slippage |
| Slippage medium | medium slippage |
| Slippage high | high slippage |
| Bull | rising period |
| Bear | falling period |
| Sideways | sideways period |
| Crash | extreme volatility |
| Full period | entire period |
| Out-of-sample | locked final segment |

### Metrics

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

### Advanced validation

Codex must implement or at least document and prepare:

1. Walk-forward analysis.
2. Out-of-sample held-out test.
3. Random strategy sanity test.
4. Monte Carlo resampling of trade order.
5. Sensitivity analysis on fee/slippage.
6. Research on deflated Sharpe ratio if multiple variants were tested.
7. Lookahead bias check.
8. Check for excessive parameter sensitivity.

### Acceptance criteria

- [ ] Backtest report exists.
- [ ] Walk-forward report exists.
- [ ] Out-of-sample segment is written in LOG.md.
- [ ] Random strategy comparison exists.
- [ ] Monte Carlo report exists and contains real numerical outputs: number of simulations, 5/50/95 percentile CAGR, 5/50/95 percentile max drawdown, worst simulated drawdown, probability of drawdown above limit, and probability of negative result after costs.
- [ ] Walk-forward report exists and contains real numerical outputs: number of windows, train/test window length, result of every test window, number of profitable/loss windows, aggregated profit, aggregated drawdown, and PASS/FAIL conclusion.
- [ ] Fee/slippage sensitivity exists and contains a numeric scenario table.
- [ ] Report contains disclaimer.
- [ ] If strategy beats baseline only in one bull period, result = FAIL.
- [ ] If strategy does not beat buy-and-hold or baseline after costs, result = FAIL or RESEARCH_ONLY.
- [ ] LOG updated.

---

## Phase 07 — Report layer

**Agent:** `quant-research-agent` + `sre-agent`

### Goal

Automate report generation.

### Editable files

- `scripts/run_backtest_report.py`
- `reports/backtests/.gitkeep`
- `docs/RUNBOOK.md`
- `LOG.md`

### Outputs

```text
reports/backtests/YYYY-MM-DD_strategy_summary.md
reports/backtests/YYYY-MM-DD_trades.csv
reports/backtests/YYYY-MM-DD_metrics.json
reports/backtests/YYYY-MM-DD_drawdown.csv
reports/backtests/YYYY-MM-DD_walkforward.json
reports/backtests/YYYY-MM-DD_montecarlo.json
```

### Report must contain

- strategy name;
- config version;
- data source decision;
- pairs;
- timeframe;
- fee model;
- slippage model;
- number of trades;
- max drawdown;
- buy-and-hold comparison;
- walk-forward;
- Monte Carlo;
- best/worst trade;
- monthly results;
- `enter_tag` aggregation;
- PASS/FAIL conclusion;
- disclaimer.

### Acceptance criteria

- [ ] Script runs without API key.
- [ ] Script does not run live trading.
- [ ] Outputs exist.
- [ ] Report is readable.
- [ ] LOG updated.

---

## Phase 08 — Dry-run / paper trading

**Agent:** `sre-agent`

### Goal

Run the bot without real money and verify operational stability.

### Editable files

- `scripts/run_dryrun_healthcheck.py`
- `docs/RUNBOOK.md`
- `reports/dryrun/.gitkeep`
- `LOG.md`

### Monitored items

- container uptime;
- restart behavior;
- log errors;
- DB status;
- number of signals;
- signal path through minimal Guard Core;
- open dry-run positions;
- backtest vs dry-run difference;
- `enter_tag`/`exit_reason`;
- absence of live order path;
- log rotation;
- basic database backup/restore smoke test.

### Acceptance criteria

- [ ] Dry-run can be started.
- [ ] Healthcheck report exists.
- [ ] Mode is without real money.
- [ ] Restart test performed.
- [ ] No live execution path.
- [ ] Dry-run signals pass through Minimal Guard Core from Phase 05b.
- [ ] Log rotation is configured or documented.
- [ ] Backup/restore smoke test of local DB is performed or documented as TODO with reason.
- [ ] LOG updated.

---

## Phase 08b — Fault Injection

**Priority:** POST_MVRS safety hardening. Must not block MVRS completion, but must be done before live readiness.

**Agent:** `sre-agent` + `guard-agent`

### Goal

Verify behavior during infrastructure and API faults.

### Editable files

- `src/coinbase_freqtrade_guarded_bot/guard_layer/fault_injection.py`
- `tests/test_fault_injection.py`
- `docs/RUNBOOK.md`
- `docs/RISK_POLICY.md`
- `LOG.md`

### Scenarios

| Scenario | Expected behavior |
|---|---|
| API timeout | fail-closed |
| 401 Unauthorized | fail-closed + incident |
| 429 rate limit | respect Retry-After, backoff + no order |
| stale price | no order |
| missing price | no order |
| invalid symbol | fail-closed |
| preview failure | trade rejected |
| audit writer failure | trade rejected |
| kill-switch read failure | system halted |
| unknown order status | block next order |
| DB unavailable | fail-closed |
| duplicate event | deduplication or incident |

### Acceptance criteria

- [ ] Tests exist.
- [ ] All scenarios fail closed.
- [ ] Retry/backoff has bounded attempt count and does not exceed defined deadline.
- [ ] Incident is written to audit if audit works.
- [ ] If audit does not work, the system stops trading.
- [ ] LOG updated.

---

## Phase 09 — Guard layer: OrderIntent, risk, audit, persistent kill-switch

**Agent:** `guard-agent`

### Goal

Extend the minimal Guard Core from Phase 05b into a full security layer that separates trading signal from trade intent and execution.

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

The kill-switch must be activatable in at least three simple ways:

1. by creating a local file `KILL_SWITCH`;
2. by env/config flag;
3. later by read-only UI indication and a separate manual toggle workflow if the UI remains safely separated from the execution layer.

The simplest file-based mechanism is mandatory because it must work even without UI and network.

### Kill-switch types

- `manual_halt`;
- `daily_loss_halt`;
- `weekly_loss_halt`;
- `drawdown_halt`;
- `api_error_halt`;
- `audit_failure_halt`;
- `reconciliation_halt`;
- `data_quality_halt`.

### Requirements

- Kill-switch must be persistent.
- Kill-switch must survive restart.
- Kill-switch reset must be audited.
- If kill-switch state cannot be read, the system behaves as halted.
- If auditing is impossible, trading must not be allowed.
- Every intent, even rejected, is stored.

### Acceptance criteria

- [ ] Active kill-switch blocks intent.
- [ ] Kill-switch survives restart.
- [ ] Audit failure blocks trading.
- [ ] `ALLOW_LIVE_TRADING=false` blocks live order.
- [ ] Rejected intent is recorded.
- [ ] Tests PASS.
- [ ] LOG updated.

---

## Phase 10 — Coinbase order preview wrapper

**Agent:** `guard-agent`

### Goal

Add Coinbase Advanced SDK/order preview layer without live orders.

### Editable files

- `src/coinbase_freqtrade_guarded_bot/guard_layer/coinbase_preview.py`
- `tests/test_coinbase_preview.py`
- `docs/COINBASE_SECURITY.md`
- `docs/adr/ADR-001-coinbase-key-type.md`
- `docs/skills/coinbase_auth.md`
- `LOG.md`

### Allowed

- load env placeholders;
- validate config;
- prepare preview request;
- use mock client in tests;
- save preview response to audit;
- evaluate fee/slippage limit.

### Forbidden

- `create_order`;
- `cancel_order`;
- `withdraw`;
- `transfer`;
- market order without explicit later approval;
- live execution.

### Auth/JWT

Codex must:

- verify current Coinbase documentation;
- verify SDK README/issues;
- document ECDSA vs Ed25519 decision;
- prefer official SDK;
- avoid manual JWT signing unless necessary;
- put no secret into repository.

### Acceptance criteria

- [ ] Preview wrapper has no live order method or explicitly blocks it.
- [ ] Preview failure = fail-closed.
- [ ] Fee/slippage above limit = reject.
- [ ] Mock tests PASS.
- [ ] ADR exists.
- [ ] LOG updated.

---

## Phase 10b — Reconciliation skeleton

**Agent:** `guard-agent`

### Goal

Prepare order/fill reconciliation before live mode.

### Editable files

- `src/coinbase_freqtrade_guarded_bot/guard_layer/reconciliation.py`
- `tests/test_reconciliation.py`
- `docs/RECONCILIATION.md`
- `docs/ARCHITECTURE.md`
- `docs/skills/reconciliation.md`
- `LOG.md`

### Models

- `OrderIntent`;
- `PreviewResult`;
- `ExecutionRequest`;
- `ExecutionResult`;
- `FillEvent`;
- `ReconciliationReport`.

### Checks

| Field | Check |
|---|---|
| symbol | must match |
| side | must match |
| size | must not exceed intent |
| price | within tolerance |
| fee | within limit |
| slippage | within limit |
| client_order_id | must match |
| status | must not be unknown |
| partial fill | must be marked |
| duplicate fill | must be detected |
| missing fill | block next order |

### Acceptance criteria

- [ ] Unreconciled order blocks new intent.
- [ ] Mismatch = FAIL.
- [ ] Unknown status = FAIL.
- [ ] Mock tests PASS.
- [ ] LOG updated.

---

## Phase 11 — Manual approval mode

**Agent:** `guard-agent` + `sre-agent`

### Goal

Create a workflow where the bot proposes and a human decides.

### Workflow

```text
strategy
→ signal
→ OrderIntent
→ risk engine
→ kill-switch check
→ Coinbase preview
→ report
→ user manually decides
→ possible manual entry in Coinbase UI
```

### Editable files

- `docs/RUNBOOK.md`
- `docs/LIVE_TRADING_CHECKLIST.md`
- `reports/audits/.gitkeep`
- `LOG.md`

### Forbidden

- API live create order.
- Automatic order submit.
- Hidden enablement of live mode.

### Acceptance criteria

- [ ] Proposed trade report is readable.
- [ ] Report contains signal reason.
- [ ] Report contains risk.
- [ ] Report contains preview fee/slippage.
- [ ] No automatic live execution.
- [ ] LOG updated.

---

## Phase 12 — Tax ledger

**Agent:** `tax-agent`

### Goal

Ensure technical trade records for tax purposes.

### Important limitation

Codex must not provide final tax advice. It must create a technical basis and state that rules must be verified before tax filing.

### Initial working assumptions — always verify before live tax export

The following points are an initial working framework for ledger design, not definitive tax advice. Codex must write them during implementation to `docs/skills/cz_tax_rules.md` with date, sources, and verification status.

Working assumptions for record design:

- use FIFO as the primary method of matching buys and sells unless the user confirms another rule after consulting a tax advisor;
- record the 3-year time test as a flag on the tax lot;
- record the CZK 100,000 annual value test as an informational flag;
- record 15% / 23% rates only as a verified parameter, not a hardcoded legal conclusion;
- for an active 4h/1d trading bot, assume most positions will close within days to weeks, so the time test is probably not the main scenario;
- for active trading, assume the value test can be exhausted quickly, therefore the ledger must primarily calculate taxable profit;
- never use exemption as default, only as an explicitly verified flag;
- final tax export must contain a disclaimer and should serve as input for an accountant/tax advisor.


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

### Record fields

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

Tax/audit data must not be silently damaged by a schema change.

MVP rules:

- SQLite database must contain `schema_version` or equivalent metadata.
- Every schema change has a migration note in `docs/DB_SCHEMA_POLICY.md`.
- Destructive DB reset is allowed only for disposable/replayable test or MVRS dry-run data and must be written to LOG.md.
- Before destructive reset of an existing SQLite DB, a `.bak` copy is created if the file exists.
- Once the DB contains valuable dry-run/live data, backup is mandatory before migration.
- Append-only audit JSONL is not migrated destructively; new schema is handled by a new event type or export to a new version.
- If the project moves to SQLModel/SQLAlchemy, Codex may introduce Alembic only after dependency review and ADR.
- Before Phase 17, a test migration from an older schema to the current one must exist.

Editable migration files:

- `src/coinbase_freqtrade_guarded_bot/tax_layer/migrations/`
- `src/coinbase_freqtrade_guarded_bot/storage/schema_version.py`
- `scripts/migrate_tax_db.py`
- `tests/test_tax_migrations.py`
- `docs/DB_SCHEMA_POLICY.md`

### Storage policy

MVP storage rule:

- audit trail: append-only JSONL as primary audit trail;
- tax ledger: SQLite as local structured storage if JSONL is insufficient for queries/exports;
- SQLModel is an allowed candidate for typed SQLite models, but only after dependency review and ADR;
- full ORM is not mandatory for MVRS;
- no network DB or cloud DB in MVP without explicit ADR.

### Exports

- CSV;
- XLSX;
- Parquet;
- JSONL;
- annual overview;
- input for accountant/tax advisor.

### Acceptance criteria

- [ ] Ledger stores all required data.
- [ ] FIFO calculator has a manually verified test.
- [ ] Exports work without secrets.
- [ ] Documentation contains disclaimer.
- [ ] `cz_tax_rules.md` has last verification date.
- [ ] SQLite schema versioning/migration policy exists.
- [ ] Migration test or reset policy for disposable test DB exists.
- [ ] LOG updated.

---

## Phase 13 — Enterprise UI MVP

**Agent:** `ui-agent`

### Goal

Create an internal enterprise-style dashboard for monitoring, audit, and tax records.

### MVP stack

- Streamlit.
- Local access.
- No live trade button.
- Read from local reports, audit logs, DB.

### Later enterprise stack

- FastAPI backend.
- PostgreSQL.
- React/Next.js frontend.
- Prometheus/Grafana monitoring.
- Auth behind VPN.
- No publicly exposed UI.

### Editable files

- `ui/README.md`
- `ui/streamlit_app.py`
- `ui/pages/*.py`
- `docs/UI_SPEC.md`
- `docs/adr/ADR-004-ui-stack.md`
- `docs/skills/ui_patterns.md`
- `LOG.md`

### Screens

1. Overview.
2. Backtests.
3. Dry-run status.
4. Audit log.
5. Tax ledger.
6. Risk/Kill-switch.
7. Research.
8. System health.

### Principles

- UI is not a gambling terminal.
- UI must not have a live order button.
- Every number must be traceable to audit log or DB.
- Risk states must be visually clear.
- Kill-switch status must always be visible.

### Acceptance criteria

- [ ] UI runs locally.
- [ ] Does not require API key.
- [ ] Contains no live trade button.
- [ ] Shows kill-switch state.
- [ ] Shows audit log.
- [ ] Shows tax ledger.
- [ ] LOG updated.

---

## Phase 14 — Research update loop

**Agent:** `research-agent`

### Goal

Enable controlled research without uncontrolled code adoption.

### Editable files

- `scripts/research_update.py`
- `docs/RESEARCH_POLICY.md`
- `reports/research/`
- `docs/skills/*.md`
- `LOG.md`

### Mandatory areas

- Coinbase API changes.
- Freqtrade issues.
- CCXT issues.
- Reddit experience.
- GitLab mirror/projects.
- Dependency license.
- Security advisories.
- ML/trading research.
- UI patterns.
- Tax rule before export.

### Acceptance criteria

- [ ] Every research item has a report.
- [ ] Research does not adopt code without license.
- [ ] Output is a recommendation, not automatic implementation.
- [ ] LOG updated.

---

## Phase 15 — ML / FreqAI research track

**Agent:** `strategy-agent` + `quant-research-agent`

### Goal

Verify whether ML/FreqAI provides stable edge over baseline.

### Important rule

ML may run as parallel research, but must not be closer to live mode than the baseline strategy. ML has stricter validation.

### Editable files

- `user_data/strategies/CoinbaseFreqAIResearchV1.py`
- `user_data/config/config.freqai.json`
- `docker-compose.freqai.yml`
- `docs/ML_RESEARCH_NOTES.md`
- `docs/skills/freqai_practices.md`
- `docs/skills/backtest_validation.md`
- `reports/backtests/`
- `LOG.md`

### Model order

1. Buy-and-hold baseline.
2. Trend-following baseline.
3. Momentum/volatility baseline.
4. Logistic regression.
5. Random forest.
6. LightGBM/XGBoost.
7. FreqAI built-in models.
8. Regime detection.
9. Deep learning only experimentally.
10. Reinforcement learning only future experiment, not MVP.

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
- sentiment only as supplement, not primary input.

### Feature and leakage rules

- ML features must not use future data.
- Label horizon must be explicitly defined.
- Feature/label alignment must have a unit test.
- Raw close/open/high/low prices must not be used as direct input without Algorithm Review.
- Prefer returns/log-returns/normalized distances/volatility features.
- Evaluate stationarity by p-value and critical values, not one fixed threshold.
- FreqAI Dissimilarity Index / outlier filtering is an allowed research candidate, not mandatory MVP gate.

### ML validation

- time-based split;
- walk-forward;
- purged gap between train/test if label horizon overlaps data;
- out-of-sample held-out;
- feature importance;
- calibration;
- confusion matrix;
- PnL after costs;
- max drawdown;
- comparison vs baseline;
- random strategy comparison;
- Monte Carlo trade order resampling.

### Acceptance criteria

- [ ] ML does not move to live.
- [ ] Feature importance report exists.
- [ ] Purged/walk-forward validation exists.
- [ ] Feature/label alignment test exists.
- [ ] If FreqAI DI/outlier filtering is used, it has Algorithm Review and comparison with baseline without DI.
- [ ] ML compared with baseline.
- [ ] Every used ML/trading algorithm has Algorithm Review.
- [ ] If ML does not add robust edge, it remains research-only.
- [ ] LOG updated.

---

## Phase 16 — Crypto trader knowledge base

**Agent:** `knowledge-agent` + `research-agent`

### Goal

Create a knowledge base of publicly available insights from successful crypto traders, investors, and systematic traders. This knowledge base should help create checklists, risk rules, regime filters, and result interpretation. It must not serve as a direct signal such as “copy trader X’s trade”.

### Important limitation

The knowledge base is not a source of automatic trading instructions. Codex must not:

- blindly copy trades from known traders;
- use unverified PnL screenshots as evidence of quality;
- adopt signals from paid groups, Telegram, or unverifiable sources;
- scrape content behind a paywall without authorization;
- mistake social media popularity for trading competence;
- connect the knowledge base directly to live execution.

### Editable files

- `docs/TRADER_KNOWLEDGE_BASE.md`
- `docs/skills/crypto_trader_knowledge.md`
- `knowledge_base/crypto_traders/`
- `knowledge_base/strategy_patterns/`
- `knowledge_base/risk_playbooks/`
- `reports/research/YYYY-MM-DD_crypto_trader_knowledge.md`
- `LOG.md`

### Research required

Codex must search and evaluate only publicly available and verifiable sources:

- interviews;
- books;
- public blogs;
- podcasts;
- post-mortem analyses;
- public trading journals;
- GitHub/research projects;
- Reddit discussions only as weak experiential signal;
- academic/quant materials on risk and behavioral failures.

### Source evaluation

Every record must have:

- name or alias;
- trader/investor type;
- source;
- source date;
- verifiability;
- main principles;
- risk management principles;
- what they avoid;
- whether the approach is relevant for spot BTC/ETH 4h/1d;
- whether the approach can be systematized;
- survivorship bias risk;
- marketing distortion risk;
- conclusion: use as checklist / do not use / inspiration only.

### Knowledge base outputs

The knowledge base should generate only supporting artifacts:

```text
knowledge_base/strategy_patterns/*.md
knowledge_base/risk_playbooks/*.md
knowledge_base/crypto_traders/*.md
```

Examples of useful artifacts:

- checklist for not entering after an euphoric pump;
- checklist for working with drawdown;
- list of known retail trader mistakes;
- principles for reducing position when volatility increases;
- rules for regime filter;
- warning against overtrading;
- post-mortem template for losing streaks.

### Connection to the project

Allowed:

- use the knowledge base to design risk checklists;
- use the knowledge base to generate hypotheses for backtests;
- use the knowledge base to explain trades in reports;
- use the knowledge base for audit comments.

Forbidden:

- direct use as buy/sell signal;
- direct live execution;
- copying discretionary trade calls;
- changing risk limits without backtest and acceptance criteria.

### Acceptance criteria

- [ ] `TRADER_KNOWLEDGE_BASE.md` exists.
- [ ] `crypto_trader_knowledge.md` exists.
- [ ] Every trader/princip has a source and verifiability evaluation.
- [ ] Knowledge base has at least one risk checklist.
- [ ] Knowledge base has no direct live execution link.
- [ ] Codex explicitly marks survivorship/marketing bias.
- [ ] LOG updated.

---

## POST_MVRS — Personal Trading Briefing / Operator Discipline Layer

**Agent:** `knowledge-agent` + `guard-agent` + `research-agent`

**Priority:** POST_MVRS. This feature must not block MVRS, local no-Docker development, or the core guard/audit/data work.

### Purpose

Create a short personal trading briefing before the operator opens charts. The briefing is a risk and discipline layer, not a signal engine.

It should help:

- reduce impulsive trading;
- relate market information to predefined trading rules;
- summarize what changed since the prior review;
- highlight no-trade conditions;
- keep the operator aligned with documented risk limits.

### Future briefing content

The briefing may eventually include:

- what happened overnight;
- BTC and ETH state;
- watchlist movers;
- relevant news or macro events;
- key levels;
- sentiment or volatility regime;
- today's personal trading rules;
- impulse-risk warning;
- today's allowed plan;
- no-trade conditions.

### Constraints

- Read-only.
- No live trading.
- No automatic order generation.
- No direct buy/sell signal generation.
- No hallucinated news, levels, or market data.
- All factual market/news data must be sourced or generated from validated local data.
- If data quality is insufficient, the briefing must say so.
- The briefing must be short, ideally one page or readable in two minutes.
- The feature is POST_MVRS and must not block current local development.

### Acceptance criteria

- [ ] Feature remains POST_MVRS until MVRS is complete.
- [ ] No direct signal or execution path exists.
- [ ] All factual market/news data is sourced or produced from validated local data.
- [ ] Insufficient data quality produces a clear no-briefing or limited-briefing state.
- [ ] LOG updated if implementation starts in a future phase.

---

## Phase 17 — Live pilot readiness checklist

**Agent:** `guard-agent` + `sre-agent`

### Goal

Prevent premature live trading.

### Editable files

- `docs/LIVE_TRADING_CHECKLIST.md`
- `docs/PHASE_GATE.md`
- `LOG.md`

### Conditions for live pilot

- [ ] Data Parity Gate PASS.
- [ ] Baseline strategy PASS or clearly marked RESEARCH_ONLY.
- [ ] Backtest reports exist.
- [ ] Walk-forward validation exists.
- [ ] Out-of-sample validation exists.
- [ ] Dry-run ran for the agreed time.
- [ ] Fault injection PASS.
- [ ] Guard layer PASS.
- [ ] Kill-switch PASS.
- [ ] Coinbase preview PASS.
- [ ] Reconciliation skeleton PASS.
- [ ] Tax ledger PASS.
- [ ] Audit logs complete.
- [ ] `pytest` PASS.
- [ ] `pytest --cov=src --cov-branch --cov-fail-under=85` PASS.
- [ ] Critical coverage gates for Guard/Tax/DataParity/Reconciliation/Metrics PASS or explicit BLOCKER.
- [ ] `ruff check .` PASS or explicitly approved waiver.
- [ ] Import smoke test PASS.
- [ ] No-secrets smoke test PASS.
- [ ] Document Completeness Check PASS: phases 00–18 are present, no section ends with a truncated sentence, all file references match package layout.
- [ ] API key with IP allowlist prepared if the project reaches live pilot.
- [ ] Minimum permissions.
- [ ] One portfolio.
- [ ] Small capital defined by user.
- [ ] Maximum acceptable loss defined by user.
- [ ] `ALLOW_LIVE_TRADING=false` still default.
- [ ] User explicitly confirms understanding of risk.

### Acceptance criteria

- [ ] Checklist exists.
- [ ] All items have PASS/FAIL.
- [ ] FAIL items block live pilot.
- [ ] LOG updated.

---

## Phase 18 — Limited live pilot only after explicit user approval

**Agent:** `guard-agent` + `sre-agent`

### Goal

Only after Phase 17 is satisfied and the user gives explicit consent, prepare a very limited pilot.

### Important

Codex must not start this phase without explicit user instruction.

### Conditions

- `ALLOW_LIVE_TRADING=true` is set by the user in a separate commit.
- Capital is small and limited.
- Spot only.
- BTC/ETH only.
- Long only.
- No leverage.
- Daily loss limit.
- Portfolio drawdown stop.
- Kill-switch.
- Reconciliation.
- Tax ledger.
- Manual approval.

### First live mode

The first live mode is not fully automatic:

```text
bot proposes
→ preview
→ risk
→ report
→ user manually approves
→ possibly trade is entered manually or by a separately approved execution layer
```

### Acceptance criteria

- [ ] No automatic live order without separate approval.
- [ ] Every live step audited.
- [ ] Reconciliation after every fill.
- [ ] Tax ledger after every fill.
- [ ] Kill-switch tested.
- [ ] LOG updated.

---

# 15. Master prompt for every new Codex session

Place at the beginning of every new Codex session:

```text
You are a senior Python engineer, quantitative analyst, security-oriented architect, and DevOps engineer.

You are working on the coinbase_freqtrade_guarded_bot project according to CODEX_MASTER_PLAN.md in the repository root.

Before any action:
1. Read CODEX_MASTER_PLAN.md in full.
2. Read AGENTS.md.
3. Read `PROJECT_STATE.md`, if it exists.
4. From `LOG.md`, read at least STATUS SUMMARY, OPEN QUESTIONS, PHASE TRACKER, DECISION REGISTER, DEPENDENCY REGISTER, and the latest checkpoint; open the archive only if historical detail is needed.
5. Determine the current phase according to PHASE TRACKER and STATUS SUMMARY.
6. If it is not clear where to continue, stop and ask a question.

Hard limits:
- No live trading in MVP.
- No real API keys, secrets, seed phrases, or private keys.
- No futures, no leverage, no shorts.
- Only spot, long-only, BTC/ETH in the first version.
- Do not use Coinbase sandbox as a strategy validation environment.
- No claim of guaranteed profit.
- When uncertain, fail closed.
- If you encounter live trading, a secret, or a user trading decision, stop.

Workflow:
- Work autonomously through phases until a hard-stop occurs according to CODEX_MASTER_PLAN.md.
- Work only in the current scope.
- Follow `docs/CODING_STANDARDS.md` and package layout under `src/coinbase_freqtrade_guarded_bot/`.
- Before changing anything, print call-flow.
- Print editable/read-only scope.
- Mark every shell command with execution context `[HOST_POWERSHELL]`, `[LOCAL_VENV]`, `[DOCKER_APP]`, or `[DOCKER_FREQTRADE]`.
- Read relevant files in full.
- If there is technical uncertainty, use the research protocol from CODEX_MASTER_PLAN.md.
- Save new findings to docs/skills/*.md and reports/research/.
- Test every change.
- Continuously update LOG.md after checkpoints, not only at the end.
- After PASS of the current small slice, automatically continue to the next safe slice if no hard-stop occurs and no usage limit is approaching.
- If a usage limit is approaching, write `QUOTA_SAFE_CHECKPOINT`, update `PROJECT_STATE.md`, suggest a commit, and print resume instructions.
- If a hard-stop occurs, write WAITING_FOR_USER or BLOCKED to LOG.md and stop.
- Return output as summary + files changed + tests run + PASS/FAIL + next step.
```

---

# 16. Prompt for implementing the current phase

```text
Implement the current phase according to CODEX_MASTER_PLAN.md.

Procedure:
1. Read CODEX_MASTER_PLAN.md and AGENTS.md.
2. Read `PROJECT_STATE.md`, if it exists, and from `LOG.md` at least STATUS SUMMARY, OPEN QUESTIONS, PHASE TRACKER, DECISION REGISTER, DEPENDENCY REGISTER, and the latest checkpoint.
3. Determine the current phase.
4. Print editable/read-only scope.
5. Read relevant files in full.
6. Print call-flow.
7. If research is needed, perform the research protocol and save output to reports/research/.
8. Implement only the current phase.
9. Add or modify tests.
10. Run tests.
11. Update LOG.md and PROJECT_STATE.md.
12. Evaluate acceptance criteria.
13. If PASS and no hard-stop occurred, continue to the next phase.
14. If a hard-stop occurred, return WAITING_FOR_USER/BLOCKED summary.

Stop if:
- you need a user decision;
- you need an API key/secret;
- live trading is at risk;
- acceptance criteria cannot be met;
- tests fail and the cause is unclear.
```

---

# 17. Prompt for repair loop

```text
The current phase failed. Perform a repair loop only within the current phase scope.

Procedure:
1. Read the failure log.
2. Determine root cause.
3. If the cause is clear, make a minimal fix.
4. Run relevant tests.
5. Update LOG.md.
6. If the error persists or is unclear, stop and write a BLOCKER report.

Do not modify files outside the current phase scope.
Do not add new dependency without dependency review.
```

---

# 18. Prompt for research

```text
Perform targeted research for the current technical problem.

Mandatory checks:
- official documentation;
- GitHub issues;
- GitLab, if relevant;
- Reddit as experiential signal;
- library licenses;
- security risks;
- user reviews;
- for quantitative/statistical questions, relevant quant/academic sources.

Save output to:
reports/research/YYYY-MM-DD_<topic>.md

Also write findings to the relevant:
docs/skills/*.md

The report must contain:
- question;
- sources;
- summary;
- risks;
- recommendation;
- what not to implement;
- impact on the project.
```

---

# 19. First practical steps for the user

```powershell
mkdir D:\2026\CryptoBot
cd D:\2026\CryptoBot
mkdir coinbase_freqtrade_guarded_bot
cd coinbase_freqtrade_guarded_bot
git init
```

Save this document as:

```text
CODEX_MASTER_PLAN.md
```

Then create minimum folders:

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

Verify:

```powershell
tree /F
git status
```

Send the output for review before running Codex.

---

## 20. Operator discipline and survival policy

The goal of the project is not to make money quickly, but to survive long enough to test hypotheses.

Rules:

- no strategy is considered stable merely because it had a good backtest;
- drawdown is not a system error if it is within the expected range, but it must be measured and reported;
- the user must not manually bypass the kill-switch due to emotions or an attempt to “recover a loss”;
- after a losing streak, the strategy is not changed without Algorithm Review and a new backtest;
- before any risk limit change, a Decision Register entry must be created;
- every post-mortem of a larger losing streak is written to `knowledge_base/risk_playbooks/`.

Project mantra:

```text
Survive first.
Then measure.
Then improve.
Only then consider a live pilot.
```

---

## 21. Permanent disclaimer

Place this text into README and every report:

> This project is a tool for research and auditable testing of trading strategies, not investment advice or a promise of profit. Historical backtest and dry-run results are not a guarantee of future results. Cryptocurrency trading is risky and may lead to loss of part or all invested capital. Tax information in this project is a technical basis for recordkeeping, not tax advice. For final tax filing, current rules must be verified and a tax advisor should be consulted.

---

## 22. Criteria for not letting the project continue

Do not continue to live pilot if:

- Data Parity Gate fails.
- Backtest has no out-of-sample validation.
- Strategy works only in one bull period.
- Strategy fails under realistic fees/slippage.
- Dry-run is unstable.
- Fault injection fails.
- Audit log has gaps.
- Kill-switch does not work.
- Reconciliation does not block unknown status.
- Tax ledger does not export complete data.
- UI or monitoring hides risk states.
- API key has no IP allowlist.
- User has no defined capital and maximum acceptable loss.
- Codex or the user does not understand why the strategy trades.

---

## 23. Final decision summary

Final architecture:

```text
Freqtrade = research/backtest/dry-run engine
Coinbase Advanced SDK/order preview = validation guardrail
guard_layer = risk, audit, kill-switch, fault handling
tax_layer = records/export
ui = audit enterprise dashboard
ML/FreqAI = separate research track, not a live shortcut
trader knowledge base = supporting knowledge layer for checklists and hypotheses, not buy/sell signals
package/coding standards = custom Python code is an installable, typed, and testable package, not a set of ad-hoc scripts
MVRS = first completion milestone up to Phase 08 with Minimal Guard Core already in Phase 05b
operator discipline = survive, measure, improve; do not bypass kill-switch because of emotions
execution context = every command has a clear environment: host, local venv, Docker app, or Docker Freqtrade
schema/network/coverage gates = SQLite schema versioning, bounded retry/backoff, pytest-cov quality gates
final hardening = Docker package import policy, PROJECT_STATE template, pytest-socket offline tests, MVRS scope freeze, Windows-first dev.ps1
plus-safe operation = bounded slices, QUOTA_SAFE_CHECKPOINT, PROJECT_STATE resume, Git/diff persistence, no important work only in chat
```

Final principle:

```text
First verify data.
Then verify baseline.
Then verify stability.
Then audit risk.
Then record taxes.
Only then consider a pilot.
```
