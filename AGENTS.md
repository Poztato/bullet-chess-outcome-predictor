# Repository instructions

- Avoid em dashes. Use commas, colons, parentheses, or regular hyphens.
- The current priority is the browser extension and live feature integration. Do not tune or retrain the baseline unless the task asks for it.
- Read `docs/recovery-audit.md` before changing feature semantics or using historical metrics.
- Preserve `data/processed/final_dataset.csv`, `models/chessica_random_forest.pkl`, and files mapped as exact originals in `docs/recovery-manifest.json`. Put new generated models in `models/generated/`.
- Treat `archive/` as historical evidence. Copy useful code into an active module before changing it.
- Keep `.local-backup/` and `.recovery/` out of commits. They contain original files, personal notes, and third-party downloads.
- Run `python scripts/verify_repository.py` for repository changes. Run relevant behavioral checks for implementation changes. Do not execute archived automation or data rewriting scripts as a validation shortcut.
- Distinguish stored notebook outputs, model smoke checks, browser tests, and live site verification in reports.
