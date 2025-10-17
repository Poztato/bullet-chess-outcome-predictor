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
dupe_list = [f"ID{x}.txt" for x in range(8702, 8801, 2)]

# Remove duplicated games
for file in dupe_list:
    all_games.remove(file)


for game in all_games:
    with open(f"{GAME_DIRECTORY}\\{game}", "r", encoding="utf-8") as txt_file:
        lines = txt_file.readlines()
    
    if lines[IS_WHITE_INDEX].startswith(IS_WHITE):
        current_game_elo = lines[WHITE_ELO].split("\"")[1]
    
    else:
        current_game_elo = lines[BLACK_ELO].split("\"")[1]

    elo_dict[game.split(".")[0]] = current_game_elo


with open(SESSION_CSV, 'r', newline='', encoding='utf-8') as csv_file:
    session_lines = csv_file.readlines() 


game_keys = elo_dict.keys()
game_keys = list(game_keys)

write_list = []
skip_header = True
for line in session_lines:  
    if skip_header:
        skip_header = False
        continue

    elements = line.split(",")
    if elements[1].strip() == "1":
        first_game_elo = int(elo_dict[elements[0]])
        # Finds the index of current Game ID, finds and extracts the previous Game ID
        prev_game_elo = elo_dict[game_keys[max(0, game_keys.index(elements[0]) - 1)]]
        
        current_line_diff = first_game_elo - int(prev_game_elo)
        current_session_elo = int(prev_game_elo)

        write_list.append(f"1,{str(current_line_diff)}\n")
    else:
        current_line_diff = int(elo_dict[elements[0]]) - current_session_elo
        write_list.append(f"{elements[1].strip()},{str(current_line_diff)}\n")


with open(GAME_RATINGS, 'w', newline='', encoding='utf-8') as write_csv:
    write_csv.write("game_id,sesh_cnt,elo_diff\n")

with open(GAME_RATINGS, 'a', newline='', encoding='utf-8') as write_csv:
    for index, elo_diff in enumerate(write_list):
        write_csv.write(f"{game_keys[index]},{elo_diff}")
