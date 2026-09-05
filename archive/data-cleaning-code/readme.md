# 📂 Directory Overview

This repository contains **pure Python algorithms** used to clean raw chess data and derive variables for the final `.csv` files. Each directory represents a specific feature engineering step, implemented without data analytics libraries to practice algorithm writing skills.

---

## **Directories**
- **`average-pr/`**  
  Scripts for calculating **Average Punishment Rating (PR)** per game after Stockfish evaluation.

- **`game-session/`**  
  Algorithms to group games into sessions based on time proximity (≤15 minutes apart).

- **`elo-difference/`**  
  Scripts to compute **ELO gain/loss per session**, reflecting rating swings.

- **`streak-record/`**  
  Tracks consecutive wins/losses before the current game to capture psychological streak effects.

- **`final-dataset/`**  
  Combines all derived variables into `FinalDataset.csv` for model training.

- **`stockfish-analysis/`**  
  **Exception:** Contains the script used to analyze ~9,000 raw `.PGN` games downloaded from Chess.com using Stockfish for move evaluations.

---
