import csv

FINAL_CSV = r"..\Final Dataset.csv"
FINAL_CSV2 = r"..\Final Dataset2.csv"
headers = ['game_id', 'is_white', 'avg_pr', 'sesh_cnt', 'elo_diff', 'streak', 'result']

with open(FINAL_CSV, 'r', newline='') as read_csv:
    final_reader = csv.DictReader(read_csv)

    data = list(final_reader)

    for line in data:
        streak = int(line['streak'])
        if streak > 0:
            streak -= 1
        else:
            streak += 1
        line['streak'] = streak

    with open(FINAL_CSV2, 'w', newline='') as write_csv:
        final_writer = csv.DictWriter(write_csv, fieldnames=headers, delimiter=',')
        final_writer.writeheader()

        final_writer.writerows(data)