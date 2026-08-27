# Typeproof

> Recruiter summary: AI systems reliability, Pydantic validation, bounded retry design, failure observability, schema evolution, auditability, deterministic testing, and a polished Next.js product surface.

**Vercel landing page:** [typeproof-workbench.vercel.app](https://typeproof-workbench.vercel.app)

**Private GitHub repository:** [HarshMehta9000/typeproof](https://github.com/HarshMehta9000/typeproof)

Typeproof is a Pydantic-first JSON extraction workbench. It treats model output as untrusted input, validates it against a typed contract, records failures, repairs only the invalid structure, and returns an object only after the schema passes.

## Why this project signals engineering strength

- **Typed AI boundary:** Pydantic v2 validates dates, required fields, types, confidence bounds, and extra-field policy.
- **Bounded repair loop:** invalid output becomes a recorded attempt, then a targeted retry. The UI shows failed, repairing, and accepted states.
- **Operational visibility:** retry ledger, failure observatory, provider mode comparison, constraint revalidation, schema evolution, and adjudication are visible product surfaces.
- **Honest demo design:** ten fixtures are deterministic and labeled as simulated. Deliberate failures are visible instead of hidden behind made-up model claims.
- **Production-minded fallback:** SQLite is the durable storage path, with in-memory SQLite for tests and local fallback behavior.
- **Usable product direction:** the default landing view is a simple two-step flow. The full schema and debugging workbench remains one click away.

## Live demo

The published Vercel URL is listed at the top of this README.

## Product flow

1. Choose a source fixture from the library.
2. Run deterministic extraction.
3. Inspect the typed `NewsEntity` result.
4. If validation fails, review the exact field and bounded repair attempt.
5. Open Advanced workbench for schema fields, retries, modes, constraints, evolution, and adjudication.

## Labels and what they mean

- **Deterministic demo:** the UI uses a local fixture provider. It does not claim live model quality, latency, or token measurements.
- **Pydantic v2:** the output contract is expressed as a typed Python model and checked before success.
- **Needs repair:** the candidate object failed a visible constraint and is not presented as accepted.
- **Repair accepted:** the bounded retry produced a candidate that satisfies the typed contract.
- **Schema valid:** every displayed field passed validation and can move to the next application step.
- **SQLite fallback ready:** durable SQLite is supported by the backend reference implementation, with in-memory SQLite for tests.
- **OpenAI-compatible adapter idle:** the provider boundary is ready for a compatible model adapter, while the demo stays local and keyless.

## Fixture library

All ten examples are selectable and update the source, output, status, issue, and retry behavior together.

| Fixture | Style | Format | Behavior |
| --- | --- | --- | --- |
| `board_appointment_01` | wire brief | plain text | invalid calendar date, repaired |
| `market_exit_02` | analyst note | plain text | valid direct path |
| `partnership_03` | press release | quoted release | invalid calendar date, repaired |
| `funding_04` | wire story | plain text | valid direct path |
| `docket_05` | court docket | structured lines | missing organization, repaired |
| `transcript_06` | earnings transcript | speaker turns | confidence type issue, repaired |
| `bulletin_07` | regulatory bulletin | bulletin | extra field, repaired |
| `email_08` | internal email | email | valid direct path |
| `interview_09` | radio transcript | quoted transcript | source span issue, repaired |
| `webhook_10` | event webhook | JSON envelope | valid direct path |

## Example inputs

### Wire brief with an invalid date

```text
Aster Labs appointed Maya Chen as chief operating officer on 2024-13-40 after the board approved its expansion plan.
```

Expected behavior: the date is blocked, persisted as a validation failure, then repaired to `2024-02-14` on the next attempt.

### Earnings transcript with a confidence issue

```text
Q: What changed this quarter?
A - Jonah Lee: We consolidated the Atlas division on 2024-04-22 and moved the product team to Chicago.
Q: Are you confident?
A: Yes, very.
```

Expected behavior: the deterministic fixture marks `confidence` as the invalid path, then repairs the typed value.

### JSON webhook with a valid direct path

```json
{"event":"leadership_change","org":"Vela Robotics","person":"Ari Kim","effective_date":"2024-08-19","action":"joined"}
```

Expected behavior: the JSON envelope maps to a valid `NewsEntity` in one attempt.

## GIF walkthroughs

The GIFs are included in the repository so the product behavior is reviewable without opening the app.

![Full Typeproof simulation](typeproof-gifs/00-full-typeproof-simulation.gif)

- [Full Typeproof simulation](typeproof-gifs/00-full-typeproof-simulation.gif)
- [Seeded validation playback](typeproof-gifs/01-seeded-validation-playback.gif)
- [Malformed output repair](typeproof-gifs/02-malformed-output-repair.gif)
- [Schema tree inspection](typeproof-gifs/03-schema-tree-inspection.gif)
- [Failure observatory filtering](typeproof-gifs/04-failure-observatory-filter.gif)
- [Function calling versus JSON mode](typeproof-gifs/05-function-vs-json-mode.gif)
- [Constraint revalidation](typeproof-gifs/06-constraint-revalidation.gif)
- [Schema evolution and adjudication](typeproof-gifs/07-evolution-and-adjudication.gif)
- [Architecture and local run](typeproof-gifs/08-architecture-local-run.gif)
- [Fixture library selector](typeproof-gifs/09-fixture-library-selector.gif)
- [Repair and valid fixture path](typeproof-gifs/10-repair-and-valid-fixture-path.gif)
- [Contract and audit improvements](typeproof-gifs/11-contract-and-audit-improvements.gif)

## Stack

- Next.js and React for the interactive workbench
- TypeScript for the product surface
- FastAPI and Pydantic v2 for the backend reference implementation
- SQLite for durable attempt records
- In-memory SQLite fallback for tests
- OpenAI-compatible provider boundary
- ESLint, pytest, and deterministic fixtures for verification

## Run locally

```bash
npm install
npm run dev
```

The app opens at `http://localhost:3000` by default. The backend reference implementation can be run with:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
PYTHONPATH=backend uvicorn typeproof.api:app --reload
```

## Verification

```bash
npm run build
npm run lint
PYTHONPATH=backend .venv/bin/pytest -q backend/tests
```

## Integrity notes

- The ten source fixtures are labeled deterministic and simulated in the app.
- Fixture-specific failures are intentional and visible in the retry ledger.
- The local demo requires no API key.
- The backend reference implementation demonstrates bounded retries and persisted validation failures.
- The GIFs document the actual product flow and are not placeholder marketing assets.

## Contributor

- Harsh Mehta, sole author and maintainer
