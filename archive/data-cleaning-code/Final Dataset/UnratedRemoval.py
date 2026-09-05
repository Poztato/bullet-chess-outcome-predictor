import csv

COMPILED_CSV = r"..\Compiled Dataset.csv"
FINAL_CSV = r"..\Final Dataset.csv"
headers = ['game_id', 'is_white', 'avg_pr', 'sesh_cnt', 'elo_diff', 'streak', 'result']

unrated1 = [f"ID{x}" for x in range(2721, 2740)]
unrated2 = [f"ID{x}" for x in range(3112, 3123)]
unrated3 = [f"ID{x}" for x in range(5732, 5739)]
unrated4 = [f"ID{x}" for x in range(5908, 5929)]
unrated5 = [f"ID{x}" for x in range(6881, 7229)]

unrated_games = unrated1 + unrated2 + unrated3 + unrated4 + unrated5


with open(COMPILED_CSV, 'r', newline='', encoding='utf-8') as csv_read:
    final_reader = csv.DictReader(csv_read)

    with open(FINAL_CSV, 'w', newline='', encoding='utf-8') as csv_write:
        final_writer = csv.DictWriter(csv_write, fieldnames=headers, delimiter=',')
        final_writer.writeheader()

        for line in final_reader:
            if line['game_id'] not in unrated_games:
                final_writer.writerow(line)