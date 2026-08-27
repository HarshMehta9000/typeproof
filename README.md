# Typeproof

**Live Vercel app:** [typeproof-workbench.vercel.app](https://typeproof-workbench.vercel.app)

## About

Typeproof turns untrusted model output into data your app can trust. It reads text, builds a typed object, checks every field with Pydantic, records failures, and retries only the broken part. The demo uses ten honest fixtures, SQLite storage, and an in-memory test fallback so each step can be inspected, tested, and explained. It stays easy to use.

## Main ideas

- **Typed output:** Pydantic checks dates, required fields, types, confidence, and extra fields.
- **Safe repair:** a failed result is recorded, then only the broken part is retried.
- **Clear records:** the app shows the source, result, error, retry, and final status together.
- **Honest demo:** ten local fixtures are labeled as simulated. The app does not invent model results.
- **Simple first view:** the landing page has two steps. The full workbench is still one click away.

## Live demo

Open [Typeproof on Vercel](https://typeproof-workbench.vercel.app). Choose an example, run it, and inspect the typed `NewsEntity` result.

## How it works

1. Choose a source fixture.
2. Run the extraction.
3. Check the typed result.
4. If a field fails, review the error and retry.
5. Open Advanced workbench for the schema, retry ledger, modes, constraints, schema changes, and review tools.

## Labels

- **Deterministic demo:** the result comes from a local fixture. It is not a live model test.
- **Pydantic v2:** the output is checked against a typed Python model.
- **Needs repair:** a field failed validation. The result is not accepted.
- **Repair accepted:** a retry passed the typed contract.
- **Schema valid:** every displayed field passed validation.
- **SQLite fallback ready:** the backend supports SQLite and an in-memory SQLite test path.
- **OpenAI-compatible adapter idle:** a compatible provider can be connected later. The demo runs without a key.

## Ten source fixtures

| Fixture | Style | Format | Result |
| --- | --- | --- | --- |
| `board_appointment_01` | wire brief | plain text | invalid date, repaired |
| `market_exit_02` | analyst note | plain text | valid direct path |
| `partnership_03` | press release | quoted release | invalid date, repaired |
| `funding_04` | wire story | plain text | valid direct path |
| `docket_05` | court docket | structured lines | missing organization, repaired |
| `transcript_06` | earnings transcript | speaker turns | confidence issue, repaired |
| `bulletin_07` | regulatory bulletin | bulletin | extra field, repaired |
| `email_08` | internal email | email | valid direct path |
| `interview_09` | radio transcript | quoted transcript | source span issue, repaired |
| `webhook_10` | event webhook | JSON envelope | valid direct path |

## Example inputs

### Wire brief

```text
Aster Labs appointed Maya Chen as chief operating officer on 2024-13-40 after the board approved its expansion plan.
```

The invalid date is shown, recorded, and repaired to `2024-02-14`.

### Earnings transcript

```text
Q: What changed this quarter?
A - Jonah Lee: We consolidated the Atlas division on 2024-04-22 and moved the product team to Chicago.
Q: Are you confident?
A: Yes, very.
```

The confidence issue is shown and repaired by the fixture flow.

### JSON webhook

```json
{"event":"leadership_change","org":"Vela Robotics","person":"Ari Kim","effective_date":"2024-08-19","action":"joined"}
```

This valid example passes in one attempt.

## GIF walkthroughs

### 1. Full simulation

![Full Typeproof simulation](typeproof-gifs/00-full-typeproof-simulation.gif)

### 2. Seeded validation playback

![Seeded validation playback](typeproof-gifs/01-seeded-validation-playback.gif)

### 3. Malformed output repair

![Malformed output repair](typeproof-gifs/02-malformed-output-repair.gif)

### 4. Schema tree inspection

![Schema tree inspection](typeproof-gifs/03-schema-tree-inspection.gif)

### 5. Failure observatory filtering

![Failure observatory filtering](typeproof-gifs/04-failure-observatory-filter.gif)

### 6. Function calling and JSON mode

![Function calling and JSON mode](typeproof-gifs/05-function-vs-json-mode.gif)

### 7. Constraint revalidation

![Constraint revalidation](typeproof-gifs/06-constraint-revalidation.gif)

### 8. Schema evolution and adjudication

![Schema evolution and adjudication](typeproof-gifs/07-evolution-and-adjudication.gif)

### 9. Architecture and local run

![Architecture and local run](typeproof-gifs/08-architecture-local-run.gif)

### 10. Fixture library selector

![Fixture library selector](typeproof-gifs/09-fixture-library-selector.gif)

### 11. Repair and valid fixture path

![Repair and valid fixture path](typeproof-gifs/10-repair-and-valid-fixture-path.gif)

### 12. Contract and audit improvements

![Contract and audit improvements](typeproof-gifs/11-contract-and-audit-improvements.gif)

## Stack

- Next.js and React
- TypeScript
- FastAPI and Pydantic v2
- SQLite
- In-memory SQLite for tests
- OpenAI-compatible provider boundary
- ESLint and pytest

## Run locally

```bash
npm install
npm run dev
```

The app runs at `http://localhost:3000` by default.

To run the backend reference implementation:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
PYTHONPATH=backend uvicorn typeproof.api:app --reload
```

## Tests

```bash
npm run build
npm run lint
PYTHONPATH=backend .venv/bin/pytest -q backend/tests
```

## Notes

- The ten fixtures are local, deterministic, and labeled as simulated.
- Their failures are intentional and visible.
- The demo needs no API key.
- The GIFs show the actual product flow.

## Author

Harsh Mehta
