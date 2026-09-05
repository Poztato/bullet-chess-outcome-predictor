# ♟️ Bullet Chess Outcome Prediction

## 📌 Overview
This project explores the link between **emotions and intuition in bullet chess**. The hypothesis: emotional state significantly impacts decision-making in fast-paced games. By engineering features that reflect psychological factors, we aim to predict blunders and game outcomes.

---

## 🔍 Methodology
- **Data Collection:** Downloaded ~9,000 bullet chess games from Chess.com archives.
- **Challenge:** Implemented **pure Python algorithms** for data cleaning and preprocessing **without pandas or data analytics libraries** to practise algorithmic thinking.
- **Move Analysis:** Leveraged **Stockfish** for centipawn loss and punishment rating calculations.
- **Feature Engineering:** Designed variables to capture emotional and performance trends.

---

## Key Variables & Why They Matter
1. **Punishment Rating (PR):**  
   Quantifies how severely a blunder was punished. High PR = emotional stress.
2. **Games Played per Session:**  
   Tracks fatigue or momentum effects during long sessions.
3. **ELO Loss/Gain per Session:**  
   Reflects emotional impact of rating swings.
4. **Streak Record:**  
   Captures psychological pressure from consecutive wins or losses.

These variables were chosen because they **mirror emotional triggers** that influence intuition in bullet chess.

---

## Modeling
- **Algorithm:** Random Forest Classifier.
- **Initial Accuracy:** ~77% base model.
- **Feature Importance:** Streak dominates, but PR and session metrics add context.

---

## Insights
- Bullet chess quality depends more on **intuition than calculation**.
- Emotional state strongly influences intuition.
- Streak and punishment dynamics are key predictors of performance.

---

## Future Work
- **Polish the base Random Forest model** using advanced statistical learning methods:
  - Gradient Boosting
  - XGBoost
  - Neural Networks
- Improve feature engineering to better capture **real-time emotional states**.
- Create a pipeline to automatically obtain features to enable real-time predictions. 

---

## 🛠 Tech Stack
- **Python** (pure algorithms for data handling)
- **Stockfish** (move evaluation)
- **Scikit-learn** (Random Forest modeling)
- **Matplotlib** (analysis & visualization)
- **Jupyter Notebook** (final dataset model training) 
