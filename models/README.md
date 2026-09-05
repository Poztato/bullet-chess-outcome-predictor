# Recovered baseline

`chessica_random_forest.pkl` is the original 19,450,833-byte joblib artifact. The local and GitHub copies were identical and have been consolidated without modifying the model.

[`baseline-metadata.json`](baseline-metadata.json) records its SHA-256, 100-tree random forest structure, feature order, class order, feature importances, and five inference examples. Inspection used scikit-learn 1.6.1, matching the version string embedded in the artifact. This verifies that the model loads, not its predictive validity.

Feature order: `is_white`, `avg_pr`, `sesh_cnt`, `elo_diff`, `streak`.

Class order: `Draw`, `Lose`, `Win`. A future interface must account for draw probability when displaying win/loss percentages.

The notebook's stored accuracy is `0.7677004095962551`. The original test indices and random seed are unavailable. Its saved feature importances match this model's inspected importances, but the accuracy cannot be independently recreated for the original held-out split.

Read the [audit](../docs/recovery-audit.md) for feature leakage and live input limitations. New model outputs belong in ignored `models/generated/` so the historical baseline remains reproducible as an artifact.
