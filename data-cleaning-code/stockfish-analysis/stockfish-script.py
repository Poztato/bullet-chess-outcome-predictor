import os
import csv
import chess.pgn
import chess.engine
from multiprocessing import Pool, cpu_count

# ─── CONFIGURATION ─────────────────────────────────────────────────────────────
INDIVIDUAL_DIR = "/media/poztato/secondary/Individual Games"
CSV_PATH       = "/media/poztato/secondary/Move Evaluations.csv"
ENGINE_PATH    = "/usr/games/stockfish"
USERNAME       = "IgniteZeus"
DEPTH          = 16
CTP_THRESHOLD  = 100    # centipawns above which a loss can be punished
MATE_CAP       = 1000   # clamp any mate score to ±1000
# ────────────────────────────────────────────────────────────────────────────────

def convert_score(pov_score, mate_cap=MATE_CAP):
    mate_in = pov_score.mate()
    if mate_in is not None:
        return mate_cap if mate_in > 0 else -mate_cap
    return pov_score.score(mate_score=mate_cap)

def analyze_game(fn):
    game_id = os.path.splitext(fn)[0]
    print(f"→ Starting {game_id}", flush=True)

    results = []
    path = os.path.join(INDIVIDUAL_DIR, fn)
    with open(path, 'r', encoding='utf-8') as f:
        game = chess.pgn.read_game(f)
    if not game:
        return results

    # Determine which colour I am
    w = game.headers.get("White", "")
    b = game.headers.get("Black", "")
    if USERNAME.lower() == w.lower():
        you = chess.WHITE
    elif USERNAME.lower() == b.lower():
        you = chess.BLACK
    else:
        return results

    engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)
    engine.configure({"Threads": 1})

    moves = list(game.mainline_moves())
    board = game.board()
    user_move_idx = 0
    i = 0

    while i < len(moves):
        mv = moves[i]

        # eval before move
        info_before = engine.analyse(board, chess.engine.Limit(depth=DEPTH))
        eval_before = convert_score(info_before["score"].white())

        board.push(mv)

        # eval after move
        info_after = engine.analyse(board, chess.engine.Limit(depth=DEPTH))
        eval_after = convert_score(info_after["score"].white())

        side_before = not board.turn  # the side that just moved

        if side_before == you:
            user_move_idx += 1
            ctp_loss = abs(eval_after - eval_before)

            # always evaluate the opponent's reply if it exists
            if (i + 1) < len(moves):
                board.push(moves[i+1])
                info_reply = engine.analyse(board, chess.engine.Limit(depth=DEPTH))
                eval_reply = convert_score(info_reply["score"].white())
                board.pop()
            else:
                eval_reply = None

            # Punishment Rating
            if ctp_loss > CTP_THRESHOLD and eval_reply is not None:
                PR = max(0, eval_before - eval_reply)
            else:
                PR = 0

            print(
                f"   • {game_id} move {user_move_idx} "
                f"eval_before={eval_before} eval_after={eval_after} "
                f"ctp_loss={ctp_loss} PR={PR}",
                flush=True
            )

            # fill both eval columns:
            if side_before == chess.WHITE:
                white_eval = eval_after
                black_eval = eval_reply if eval_reply is not None else ""
            else:
                black_eval = eval_after
                white_eval = eval_reply if eval_reply is not None else ""

            results.append([
                game_id,
                user_move_idx,
                white_eval,
                black_eval,
                ctp_loss,
                PR
            ])
        else:
            print(
                f"   • Game: {game_id} "
                f"eval_before={eval_before} eval_after={eval_after}",
                flush=True
            )

        i += 1

    engine.quit()
    return results

def main():
    files = [
        fn for fn in sorted(os.listdir(INDIVIDUAL_DIR))
        if fn.lower().startswith("id") and fn.lower().endswith(".txt")
    ]

    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as out:
        writer = csv.writer(out)
        writer.writerow([
            "Game ID",
            "move",
            "white_eval",
            "black_eval",
            "ctp_loss",
            "PR"
        ])

        with Pool(processes=cpu_count()) as pool:
            for game_results in pool.imap(analyze_game, files):
                writer.writerows(game_results)
                out.flush()

if __name__ == "__main__":
    main()
