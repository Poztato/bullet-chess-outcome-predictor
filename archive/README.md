# Historical source archive

These files preserve the original research and extension attempts. They are evidence for reconstruction, not a working build pipeline. Original paths, assumptions, incomplete code, and historical wording are retained.

| Directory | Contents |
| --- | --- |
| `data-cleaning-code/` | Original GitHub collection, cleaning, feature engineering, and Stockfish scripts |
| `exploratory-data-analysis/` | Historical plotting scripts; the PDF is now under `reports/eda/` |
| `notebooks/` | Both distinct original notebooks, retained byte-for-byte |
| `extension-prototypes/` | Local Python session pipeline and random forest JSON converter |
| `documentation/` | Original GitHub README files |
| `recovered-from-history/` | Deleted utility files recovered from earlier commits |
| `reference-extensions/` | Provenance and local locations of downloaded extension bundles |

Many scripts assume the original working directory and missing PGN files. Some execute file writes or desktop automation at import time. Their locations were changed during cleanup; their behavior was not repaired. See the [audit](../docs/recovery-audit.md) before reusing them.
