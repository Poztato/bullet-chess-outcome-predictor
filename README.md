# Chessica

Chessica explores bullet chess outcomes using game performance and session history. The next phase is a browser extension that updates outcome probabilities as moves are played.

The recovered random forest notebook records **76.77% accuracy** on a random 80/20 split. This is a historical result, not a verified live prediction score. The saved model has 100 trees and three classes: `Draw`, `Lose`, and `Win`.

**Current priority:** build the extension and its feature pipeline. Model tuning is deferred. The existing dataset and model are preserved unchanged. The audit found outcome leakage in the historical streak feature and a difference between completed-game and live punishment ratings, both of which matter when connecting the model to live inputs.

Start with the [recovery audit](docs/recovery-audit.md) for what was found and what is missing, then the [phase two plan](docs/phase-2-plan.md) for the extension work. No working Chessica browser extension is included yet.

## Project layout

| Path | Purpose |
| --- | --- |
| [`data/`](data/README.md) | Final dataset, intermediate CSVs, and a dataset recovered from Git history |
| [`models/`](models/README.md) | Unchanged baseline model and inspected metadata |
| [`notebooks/chessica.ipynb`](notebooks/chessica.ipynb) | Working research notebook with corrected file paths |
| [`extension/`](extension/README.md) | Scope and entry point for the planned browser extension |
| [`docs/`](docs/recovery-audit.md) | Audit, migration inventory, roadmap, and original Word notes |
| [`reports/eda/`](reports/eda/) | Historical analysis figures in PDF form |
| [`archive/`](archive/README.md) | Original scripts, notebooks, README files, and extension prototypes |
| [`assets/`](assets/) | Original Chessica artwork |
| [`scripts/`](scripts/) | Repository checks and an optional model smoke check |

## Verify the recovered repository

From the repository root, run this dependency-free check with Python 3.10 or later:

```powershell
python scripts/verify_repository.py
```

It verifies preserved file hashes, dataset structure, notebook JSON and Python syntax. It does not train models, fetch games, or execute archived scripts. GitHub Actions runs the same check.

To inspect the saved model using the dependency versions verified during recovery:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-model.txt
.venv\Scripts\python.exe scripts/inspect_model.py
```

The optional smoke check loads the trusted project artifact and checks five saved input/output examples. It does not measure test accuracy. The pinned versions describe the recovery environment, not a recovered original training lockfile.

To use the research notebook, also install `jupyterlab`, `matplotlib`, and `seaborn` in that environment, then open `notebooks/chessica.ipynb`. Its existing outputs are historical. Running all cells trains a new model and writes to ignored `models/generated/`, preserving the baseline file.

## Continuing development

Use a branch for each scoped change, record its purpose and validation in the commit, and keep meaningful decisions in `docs/`. Run the repository check before committing. Add focused behavioral tests with the extension implementation.

The original Git history is preserved. The [recovery manifest](docs/recovery-manifest.json) maps every original file to its retained location, including local backup exceptions. The cleanup did not select a new project license or adopt the downloaded extensions as Chessica code.
