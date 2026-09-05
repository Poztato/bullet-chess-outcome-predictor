import csv

PR_CSV = r"..\Average PR.csv"
RATING_CSV = r"..\Game Ratings.csv"
STREAK_CSV = r"..\Streak Record.csv"
COMPILED_CSV = r"..\Compiled Dataset.csv"

pr_dict = {}
colour_dict = {}
result_dict = {}
session_dict = {}
rating_dict = {}
streak_dict = {}


with open(PR_CSV, 'r', newline='', encoding='utf-8') as read_csv:
        pr_reader = csv.DictReader(read_csv)
        for line in pr_reader:
            pr_dict[line['game_id']] = line['avg_pr'].strip()
            colour_dict[line['game_id']] = line['is_white'].strip()
            result_dict[line['game_id']] = line['result'].strip()


with open(RATING_CSV, 'r', newline='', encoding='utf-8') as read_csv:
        rating_reader = csv.DictReader(read_csv)
        for line in rating_reader:
            session_dict[line['game_id']] = line['sesh_cnt'].strip()
            rating_dict[line['game_id']] = line['elo_diff'].strip()


with open(STREAK_CSV, 'r', newline='', encoding='utf-8') as read_csv:
        streak_reader = csv.DictReader(read_csv)
        for line in streak_reader:
              streak_dict[line['game_id']] = line['streak'].strip()


headers = ['game_id', 'is_white', 'avg_pr', 'sesh_cnt', 'elo_diff', 'streak', 'result']
with open(COMPILED_CSV, 'w', newline='') as write_csv:
       final_writer = csv.DictWriter(write_csv, fieldnames=headers, delimiter=',')
       final_writer.writeheader()

       for game_id, result in result_dict.items():
             final_writer.writerow({'game_id': game_id, 'is_white': colour_dict[game_id],
                                    'avg_pr': pr_dict[game_id], 'sesh_cnt': session_dict[game_id],
                                    'elo_diff': rating_dict[game_id], 'streak': streak_dict[game_id],
                                    'result': result})
             