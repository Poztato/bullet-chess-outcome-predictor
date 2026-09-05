# Repository recovery audit

Audit date: 5 September 2026.

## Scope and sources

Compared the supplied Chessica directory, the original Word document, and all 15 commits in `Poztato/bullet-chess-outcome-predictor`. The starting GitHub commit was `f2fedf70995e1db73952f630af71e980b3781d44`.

The starting directory contained 67 files and no root Git repository. GitHub's latest tree contained 35 files. Eight additional paths had been deleted or relocated in history. [`recovery-manifest.json`](recovery-manifest.json) records all 110 source entries with SHA-256 hashes and their retained locations.

## Reconciliation

| Item | Comparison | Decision |
| --- | --- | --- |
| Final dataset | Local and GitHub copies are byte-for-byte identical | One canonical file at `data/processed/final_dataset.csv` |
| Saved model | Local and GitHub copies are byte-for-byte identical | One canonical artifact at `models/chessica_random_forest.pkl` |
| Stockfish Python script | Local bytes match the original Git blob; Windows checkout conversion initially obscured the match | Consolidate under `archive/data-cleaning-code/`; the original local copy also remains in the backup |
| Notebooks | Local version adds a correlation cell and an unfinished `scatter_matrix()` call; shared saved metric and feature importances match | Preserve both originals in `archive/notebooks/`; adapt the local version into `notebooks/chessica.ipynb` |
| Notebook checkpoints | One exact local notebook duplicate; one empty notebook | Deduplicate the first in the public tree; keep all originals in the local backup |
| Four intermediate CSVs and historical scripts | Present on GitHub but absent from the original local directory | Restore into `data/interim/` and `archive/` |
| Compiled dataset | Deleted in commit `07c4a69` | Recover 8,948 rows as `data/interim/compiled_dataset_before_filtering.csv`, preserving its earlier state |
| Deleted utilities | `GetLocation.py` contains a mouse-position helper; ELO `DupeRemover.py` is empty | Preserve in `archive/recovered-from-history/`; five relocated plotting scripts already exist elsewhere and are deduplicated |
| Word notes and artwork | Present only locally | Preserve under `docs/history/` and `assets/` |
| Session pipeline and model converter | Present only locally | Preserve unchanged under `archive/extension-prototypes/` |
| Downloaded extension bundles | Third-party references, duplicated build assets, incomplete provenance | Preserve originals locally and document their locations in `archive/reference-extensions/README.md` |
| Personal test-subject list | Contains personal annotations about named accounts | Preserve locally in the ignored backup; omit its contents from the public repository |

The adapted notebook changes only input/output locations, adds recovery context, and removes the unfinished argument-free plotting call. Historical training code and its stored results remain available in both exact originals. Future notebook exports go into `models/generated/` rather than overwriting the recovered model.

## Model findings

The notebook records `0.7677004095962551` accuracy, approximately 76.77%. The artifact loads with scikit-learn 1.6.1 and contains 100 trees, five input features, and classes ordered `Draw`, `Lose`, `Win`. Its inspected feature importances match those stored in the notebook.

Five input examples produced finite probabilities summing to one. This is an inference smoke check, not a new accuracy evaluation. The notebook has no fixed `random_state`, retained test split, or environment lockfile. The exact original held-out score cannot be independently reconstructed.

### The streak correction still uses the current outcome

The Word document correctly identifies that the first model's approximately 97% accuracy came from post-result streak information. Its proposed correction, implemented in `archive/data-cleaning-code/Final Dataset/StreakCorrection.py`, moves each post-result streak one unit toward zero.

This is not the same as shifting the previous game's streak forward. For example, after three wins, a fourth win becomes `3`, while a loss becomes `0`. The input for the same pre-game situation therefore changes according to the result being predicted.

The recovered dataset confirms the problem: all 2,071 rows with positive streak values are wins, and all 1,969 rows with negative streak values are losses. This invalidates interpreting the stored 76.77% as established performance on live, outcome-independent features. The baseline is retained unchanged, and model tuning remains outside this cleanup. Correct feature timing is an integration prerequisite even when reusing the same classifier design.

### Completed-game punishment is unavailable during a game

The model uses one `avg_pr` value for a completed game. A live extension only has a partial history. Punishment also requires the opponent's reply, so it cannot be finalized immediately after every player move. A running average needs an explicit pending state and should be tested against the training distribution.

The legacy averaging script omits the final row of each game when collecting punishment values. Its expected five-column move input also differs from the six-column output of the recovered Stockfish script. These are further reasons not to claim the saved dataset can be rebuilt by running the available files in sequence.

## Missing or incomplete material

| Material | Evidence and effect |
| --- | --- |
| Raw downloaded games and `Compiled_Games.txt` | Referenced by the notes and collection scripts; absent locally and from all recorded Git paths |
| `Individual Games` directory | Referenced by rating/session scripts and the Stockfish analyzer; absent |
| `Move Evaluations.csv` | Referenced by PR aggregation and EDA; absent |
| Final V4 Stockfish implementation | Notes describe both mate and ordinary evaluations capped at 1,000 and a different output schema. The recovered script only caps mate scores, uses White perspective for both player colors, and writes the earlier six-column format |
| Separate `Chess Scraper` project and exported `model.json` | Converter points to `../Chess Scraper/model.json`; neither is in the supplied folder, its sibling directory listing, or Git history |
| Notebook export named `Chessica.pkl` | Stored notebook export output uses this name, but the supplied artifact is `chessica_random_forest.pkl`; a rename is plausible but its provenance was not logged |
| Original training split and environment record | No seed, split indices, lockfile, calibration report, or independently reproducible metric record |
| Original ChessMint TypeScript | Source maps reference four `src/*.ts` files but contain no source text; source files are absent |
| Working Chessica extension integration | No manifest plus move capture, PR calculation, model inference, session persistence, and probability display connected together |
| Browser failure evidence | No saved CSP error logs, browser version, minimal failing case, or Playwright tests to identify the exact old failure |

These findings concern the supplied directory and repository history. They do not establish that the files are absent from other drives, old machines, or cloud storage.

## Existing extension attempts

The downloaded Chess Move Analyzer's Chrome manifest uses Manifest V2 and a persistent background page. Current Chrome no longer supports MV2. Its background script already attempts an extension-owned Worker, so a website CSP restriction alone does not explain every failure in this bundle. [Chrome's MV2 timeline](https://developer.chrome.com/docs/extensions/develop/migrate/mv2-deprecation-timeline)

Its board-to-FEN function hardcodes castling rights, en passant, halfmove count, and move number, and derives the active turn from the selected player color. Its engine message handler is replaced for each request without a queue. These are state and concurrency defects to avoid carrying into phase two.

ChessMint injects its main script into the page and reads engine paths from `Config.threadedEnginePaths.stockfish`. This couples it to undocumented site globals and page execution restrictions. It contains no Chessica model inference. Neither downloaded bundle is the requested probability-only application.

The converter casts every tree value to `int` and rounds thresholds to six decimals. Inspection found 257,987 fractional values and 284 mixed-class leaves in the saved forest. Integer conversion would turn those mixed leaf distributions into zero vectors. Scikit-learn 1.6 documents tree values as class proportions. An eventual exporter must preserve values and verify probability parity. [Scikit-learn tree structure documentation](https://scikit-learn.org/1.6/auto_examples/tree/plot_unveil_tree_structure.html)

The standalone `final_pipeline.py` fetches only the latest month and the most recent completed session. Month-boundary history can be incomplete, streak calculation resets to the fetched subset, and its reported statistics describe an already finished game. It needs explicit next-game/live semantics before integration.

## Preservation and verification

All original local files are retained under ignored `.local-backup/originals/`. The downloaded repository and a Git bundle of its pre-cleanup history are retained in ignored `.recovery/`. GitHub originals were restored from Git blobs to preserve their recorded bytes without Windows checkout conversion. `.gitattributes` keeps those bytes stable across platforms. No history rewrite is part of this migration.

The repository check verifies every tracked original mapping against its hash, validates the canonical dataset, and parses Python and notebook source without executing archived code. An optional `--include-local-backups` check covers the local-only files on the recovery machine. Exact original copies, including duplicate files, remain locally available.

The existing model was loaded and smoke checked without retraining. No engine was launched, no data pipeline was rerun, and no extension behavior on Chess.com was tested during cleanup. The extension plan is a proposed implementation path, not a demonstrated fix for the old browser failure.
