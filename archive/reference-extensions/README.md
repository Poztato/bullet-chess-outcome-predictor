# Downloaded extension references

The local folder contained two third-party extension bundles. Their original bytes remain in the ignored `.local-backup/originals/` directory on the recovery machine. Their per-file hashes and locations are recorded in `docs/recovery-manifest.json`; these downloads are not part of the published Chessica application.

| Original folder | Identified provenance | Finding |
| --- | --- | --- |
| `chess-move-analyzer-main/` | Its README points to [kenhendricks00/chess-move-analyzer](https://github.com/kenhendricks00/chess-move-analyzer); bundled license names Kenneth Hendricks and MIT | Chrome manifest is V2. `platform/chrome` duplicates `src` assets and code. Bundled engine files identify GPLv3 separately. Exact source revision/build provenance is not recorded. |
| `Extension/ChessMint/` | Compiled JavaScript and source maps naming `src/*.ts` | Original TypeScript is absent, maps have no embedded source, and no license or upstream revision was supplied. It loads engine paths from a page global named `Config`. |

The loose `Extension/stockfish.js` and `Extension/stockfish.wasm.js` are exact duplicates of files in the downloaded analyzer. An actual `stockfish.wasm` exists inside that analyzer, though none accompanies the loose pair.

These bundles implement move hints or automation features, and neither connects to the Chessica model. Preserve their notices if using them later. Select and document a reproducible engine distribution when implementing the new extension.
