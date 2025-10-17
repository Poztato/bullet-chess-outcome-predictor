import csv

FINAL_CSV = r"..\Final Dataset.csv"
game_list = [f"ID{x:04d}" for x in range(1, 9001)]


with open(FINAL_CSV, 'r', newline='', encoding='utf-8') as read_csv:
    final_reader = csv.DictReader(read_csv)

    for line in final_reader:
        try:
            game_list.remove(line['game_id'])

        except:
            print(f"Failed for {line['game_id']}")

print(game_list)