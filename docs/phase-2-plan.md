# Phase two: live outcome probabilities

The immediate objective is a browser extension that observes game moves and updates Chessica outcome probabilities. Improving the classifier algorithm is deferred. The user reports receiving Chess.com confirmation for this project; that statement is project context, not a browser compatibility test.

## First deliverable: an isolated engine harness

Implement a minimal Manifest V3 extension that starts a locally packaged Stockfish build, completes the UCI readiness handshake, and evaluates a fixed FEN. Keep the harness independent of Chess.com until worker startup, resource loading, and message handling are verified.

Use an extension-owned offscreen document to host the engine Worker, with messages routed through the service worker. Chrome's offscreen API provides a hidden extension document and a `WORKERS` reason. This is a candidate architecture to test, not evidence that the existing bundles will work unchanged. [Chrome offscreen API](https://developer.chrome.com/docs/extensions/reference/api/offscreen)

Declare an extension CSP that permits packaged WebAssembly, including `script-src 'self' 'wasm-unsafe-eval'`. The default extension policy disables WASM. Keep engine code and its resources packaged in the extension. [Chrome extension CSP](https://developer.chrome.com/docs/extensions/reference/manifest/content-security-policy)

Start with a single-threaded engine build to limit dependencies on threading and cross-origin isolation while diagnosing startup. Record its source revision, license, file hashes, and build instructions. Capture actual worker errors and test the harness before changing website integration.

## Connect the model without changing its predictions

Replace the archived converter with an exporter that reads actual feature/class order and retains floating-point values and thresholds. Implement browser inference and compare its full three-class probability vectors with scikit-learn on representative inputs, mixed leaves, and threshold boundaries. Include scikit-learn's float32 input conversion in the parity checks.

The interface must decide how to represent draws: show all three outcomes or clearly define any conditional win/loss calculation. The existing forest is a three-class model. Raw forest probabilities should not be described as calibrated until calibration is measured.

## Define inputs that exist at prediction time

| Feature | Required behavior |
| --- | --- |
| `is_white` | Use the actual player identity and color |
| `avg_pr` | Define a running aggregate and a pending state until the opponent replies; match the intended evaluation cap and player perspective |
| `sesh_cnt` | Count the current game from completed prior games using the documented session boundary |
| `elo_diff` | Choose and document the rating baseline, accounting for the historical code/notes discrepancy |
| `streak` | Derive from completed prior games only; shifting outcomes chronologically is required, moving a current-game streak toward zero is insufficient |

Keep the recovered baseline intact while developing the mechanics. Any results using provisional feature semantics are integration demonstrations, not validated live prediction performance. Later evaluation can retain the random forest design while fixing feature timing and using a reproducible chronological holdout.

## Integrate move capture and session state

Build an adapter that supplies legal move history or a complete validated FEN. Piece positions alone do not recover castling rights, en passant, or active turn. Test both colors, castling, en passant, promotion, game restarts, and board replacement during site navigation.

Serialize UCI searches, attach a game/position identifier to requests, and discard stale responses. Preserve session state across extension service worker restarts and retrieve sufficient completed-game history across month boundaries. Record engine latency before deciding depth and update frequency for bullet games.

## Completion evidence

1. A reproducible packaged engine starts and evaluates fixed positions in the target browser.
2. JavaScript inference agrees with the original model's probabilities within a documented tolerance.
3. Move and session fixtures prove inputs use only information available at each prediction point.
4. Browser automation covers engine startup, move updates, navigation, stale responses, and probability rendering.
5. A separate site integration run records browser version, target page, errors, and observed behavior.

The cleanup supplies the baseline artifacts and audit for this work. It does not implement or claim a tested CSP workaround.
