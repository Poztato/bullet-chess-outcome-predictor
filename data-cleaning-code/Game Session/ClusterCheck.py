SESSION_CSV = r"..\Session Cluster.csv"
all_games = [f"ID{x:04d}" for x in range(1, 9001)]

with open(SESSION_CSV, 'r', newline='', encoding='utf-8') as csv_file:
    lines = csv_file.readlines()

for line in lines:
    game_id = line.split(",")[0]
    
    try:
        all_games.remove(game_id)
    
    except:
        print(game_id)

print(all_games)