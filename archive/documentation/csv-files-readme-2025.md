# 📂 Dataset Files

### **1. `Average PR.csv`**
- **Purpose:** Stores the first derived variable: **Average Punishment Rating per Game**.
- **Columns:**
  - `game_id` – Unique identifier for each game.
  - `avg_pr` – Average Punishment Rating (PR) for moves with PR > 100.
  - `is_white` – 1 if the player is White, 0 if Black.
  - `result` – Game outcome (1 = Win, 0 = Loss, 0.5 = Draw).
- **Why:** Captures how often and how severely mistakes were punished, reflecting emotional stress.

---

### **2. `Session Cluster.csv`**
- **Purpose:** Groups games into sessions based on time proximity (≤15 minutes apart).
- **Columns:**
  - `game_id` – Unique identifier.
  - `sesh_cnt` – Session count (1, 2, 3… for order in session).
- **Why:** Models fatigue and momentum effects during extended play.

---

### **3. `Game Ratings.csv`**
- **Purpose:** Tracks rating changes within each session.
- **Columns:**
  - `game_id` – Unique identifier.
  - `sesh_cnt` – Session count.
  - `elo_diff` – Difference in ELO compared to session start.
- **Why:** Reflects emotional impact of rating gains/losses.

---

### **4. `Streak Record.csv`**
- **Purpose:** Records consecutive wins/losses before the current game.
- **Columns:**
  - `game_id` – Unique identifier.
  - `streak` – Positive for win streaks, negative for loss streaks.
- **Why:** Captures psychological pressure from ongoing streaks.

---

### **5. `Final Dataset.csv`**
- **Purpose:** Consolidates all engineered features for model training.
- **Columns:**
  - `game_id` – Unique identifier.
  - `is_white` – Player color (1 = White, 0 = Black).
  - `avg_pr` – Average Punishment Rating.
  - `sesh_cnt` – Session count.
  - `elo_diff` – ELO difference from session start.
  - `streak` – Win/Loss streak before current game.
  - `result` – Target variable (Win/Lose/Draw).
- **Why:** Serves as the complete dataset for predictive modeling.
