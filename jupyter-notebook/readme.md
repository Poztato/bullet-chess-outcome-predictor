# 🧠 Model Notebook & Exported Artifact

### Overview

This directory contains the **Jupyter notebook** used to train the classification model and the **exported `.pkl` artifact**.

---

## 📁 Contents

* **Chessica.ipynb** — Notebook implementing the full workflow
* **chessica_random_forest.pkl** — Serialized `RandomForestClassifier` model (`joblib.dump`)

---

## ⚙️ Workflow Summary

The notebook performs the following steps:

1. **Load** the engineered dataset
2. **Preprocess** minimally & run **EDA**
3. **Train** a `RandomForestClassifier`
4. **Evaluate** model accuracy
5. **Inspect** feature importances
6. **Visualize** the confusion matrix

---

## 🧩 Data Schema

### Original Columns

| Column     | Description                                             |
| ---------- | ------------------------------------------------------- |
| `game_id`  | Unique game ID *(dropped before training)*              |
| `is_white` | `1` if player is White, `0` if Black                    |
| `avg_pr`   | Average Punishment Rating per game                      |
| `sesh_cnt` | Game’s position within a session *(≤15 min clustering)* |
| `elo_diff` | ELO change vs. session start                            |
| `streak`   | Win/Loss streak before current game                     |
| `result`   | Numeric outcome *(1.0 = Win, 0.0 = Lose, 0.5 = Draw)*   |

---

### Target Mapping

| Original | Mapped Label |
| -------- | ------------ |
| `0.0`    | Lose         |
| `1.0`    | Win          |
| `0.5`    | Draw         |

---

### Final Training Features

`is_white`, `avg_pr`, `sesh_cnt`, `elo_diff`, `streak`

**Target:** `result ∈ {"Win", "Lose", "Draw"}`

---

## 📦 Dependencies

* Python 3.9+
* pandas
* scikit-learn
* joblib
* matplotlib
* seaborn

---

## 🧪 Reproducibility Notes

* `train_test_split` without `random_state` → different splits per run
  → **Set a fixed seed** to stabilize metrics
* **Feature order** must match `model.feature_names_in_` when predicting
* **Class balance** in dataset:

  * Win: 4189
  * Lose: 4074
  * Draw: 279
