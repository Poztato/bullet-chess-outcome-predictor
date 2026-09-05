import os

GAME_DIRECTORY = r"..\Individual Games"
SESSION_CSV = r"..\Session Cluster.csv"
GAME_RATINGS = r"..\Game Ratings.csv"

IS_WHITE = r'[White "IgniteZeus"]'
IS_WHITE_INDEX = 2
WHITE_ELO = 5
BLACK_ELO = 6

elo_dict = {}   # {GameID: ELO}
all_games = os.listdir(GAME_DIRECTORY)

for game in all_games:
    with open(f"{GAME_DIRECTORY}\\{game}", "r", encoding="utf-8") as txt_file:
        lines = txt_file.readlines()
    
    if lines[IS_WHITE_INDEX].startswith(IS_WHITE):
        current_game_elo = lines[WHITE_ELO].split("\"")[1]
    
    else:
        current_game_elo = lines[BLACK_ELO].split("\"")[1]

    elo_dict[game.split(".")[0]] = current_game_elo
    print(f"Reading {game}")


with open(SESSION_CSV, 'r', newline='', encoding='utf-8') as csv_file:
    csv_lines = csv_file.readlines()


write_list = []
skip_header = True
for line in csv_lines:
    if skip_header:
        skip_header = False
        continue

    elements = line.split(",")
    if elements[1].strip() == "1":
        current_session_elo = int(elo_dict[elements[0]])
        write_list.append("1,0\n")
    else:
        current_line_diff = current_session_elo - int(elo_dict[elements[0]])
        write_list.append(f"{elements[1].strip()},{str(current_line_diff)}\n")

game_keys = elo_dict.keys()
game_keys = list(game_keys)
with open(GAME_RATINGS, 'w', newline='', encoding='utf-8') as write_csv:
    write_csv.write("game_id,sesh_cnt,elo_diff\n")

with open(GAME_RATINGS, 'a', newline='', encoding='utf-8') as write_csv:
    for index, elo_diff in enumerate(write_list):
        write_csv.write(f"{game_keys[index]},{elo_diff}")
