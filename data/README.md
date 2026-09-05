# Recovered data

| File | Data rows | Meaning |
| --- | ---: | --- |
| `processed/final_dataset.csv` | 8,542 | Exact shared local/GitHub training dataset |
| `interim/average_pr.csv` | 8,949 | Historical per-game punishment averages |
| `interim/game_ratings.csv` | 8,950 | Historical session count and rating differences |
| `interim/session_cluster.csv` | 8,950 | Historical session assignments |
| `interim/streak_record.csv` | 8,948 | Historical streak values before the attempted correction |
| `interim/compiled_dataset_before_filtering.csv` | 8,948 | Deleted intermediate compilation recovered from Git history |

The final dataset has 8,542 unique game IDs: 4,189 wins, 4,074 losses, and 279 draws. The intermediate counts differ and should not be assumed to represent the same population.

## Final dataset fields

| Column | Stored meaning and limitations |
| --- | --- |
| `game_id` | Historical identifier, excluded from model inputs |
| `is_white` | Target player is White (`1`) or Black (`0`) |
| `avg_pr` | Completed-game punishment average, intended to include values above 100 centipawns; not an observed live feature |
| `sesh_cnt` | Position within a session using a 15-minute game-end gap |
| `elo_diff` | Rating difference using the historical parser's pre-session-game baseline; this differs from the first-game baseline described in the Word notes |
| `streak` | Post-result streak moved one unit toward zero; still depends on the current result |
| `result` | `1.0` = Win, `0.0` = Lose, `0.5` = Draw |

The raw PGN downloads, individual game files, and move-level evaluation CSV are absent from the supplied folder and all recorded Git filenames. They are needed to reconstruct the original feature pipeline. Future downloads and regenerated datasets belong in ignored `raw/` and `generated/` folders.
