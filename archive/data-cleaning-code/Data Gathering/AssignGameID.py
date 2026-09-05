import os

COMPILED_GAMES = "Compiled_Games.txt"
INDIVIDUAL_GAMES = "..\\Individual Games"
os.makedirs(INDIVIDUAL_GAMES, exist_ok=True)

EVENT = '[Event "Live Chess"]'
SITE = '[Site "Chess.com"]'
ROUND = '[Round "-"]'
TIME = '[TimeControl "60"]'

# Rows to delete (not currently used)
unwanted_rows = [EVENT, SITE, ROUND, TIME]
written_files = set()

def extract_datetime_from_pgn(game_start_index, all_lines):
    # Search for [Date "..."] and [EndTime "..."] within the next 15 lines
    date_str, time_str = None, None
    for j in range(game_start_index, min(game_start_index + 15, len(all_lines))):
        if all_lines[j].startswith('[Date'):
            date_str = all_lines[j].split('"')[1]
        elif all_lines[j].startswith('[EndTime'):
            time_str = all_lines[j].split('"')[1].split(' ')[0]
        if date_str and time_str:
            break

    if not date_str or not time_str:
        raise ValueError(f"Missing Date or EndTime at index {game_start_index}")

    date_fmt = date_str.replace('.', '-')       # e.g., 2025-06-29
    time_fmt = time_str.replace(':', '-')       # e.g., 9-38-21
    return f"{date_fmt}_{time_fmt}"


with open(COMPILED_GAMES, 'r', encoding="utf-8") as all_games:
    all_lines = [line.rstrip("\n") for line in all_games]

current_lines = []
for i, line in enumerate(all_lines):
    if line == EVENT and current_lines:
        # Save current game
        dateTime = extract_datetime_from_pgn(i, all_lines)
        out_path = os.path.join(INDIVIDUAL_GAMES, f"{dateTime}.txt")
        with open(out_path, "w", encoding="utf-8") as out_file:
            for current in current_lines:
                if current in unwanted_rows:
                    continue
                else:
                    out_file.write(current + "\n")
        current_lines = []

    current_lines.append(line)

# Write last game if needed
if current_lines:
    dateTime = extract_datetime_from_pgn(i, all_lines)
    out_path = os.path.join(INDIVIDUAL_GAMES, f"{dateTime}.txt")
    if out_path in written_files:
        print(f"Collision: {dateTime} at line {i}")

    with open(out_path, "w", encoding="utf-8") as out_file:
        for current in current_lines:
            if current in unwanted_rows:
                continue
            else:
                out_file.write(current + "\n")

    written_files.add(out_path)
