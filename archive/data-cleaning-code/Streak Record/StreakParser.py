import csv

FILE_WRITE = r"..\Streak Record.csv"
FILE_READ = r"..\Average PR.csv"

result_dict = {}
streak_counter = 0
streak_dict = {}
current_streak = "0.0"


with open(FILE_READ, "r", newline="", encoding="utf-8") as read_file:
    lines = csv.DictReader(read_file)

    for line in lines:
        result_dict[line["game_id"]] = line["result"]


for game_id, result in result_dict.items():
    if current_streak == result:
        if current_streak == "1.0":
            streak_counter += 1
        
        elif current_streak == "0.0":
            streak_counter -= 1

        else:
            current_streak = 1

    else:
        if result == "1.0":
            current_streak = result
            streak_counter = 1

        elif result == "0.0":
            current_streak = result
            streak_counter = -1

        else:
            current_streak = "0.5"
            streak_counter = 1

    streak_dict[game_id] = streak_counter


fieldnames = ["game_id", "streak"]
with open(FILE_WRITE, "w", newline="", encoding="utf-8") as file_write:
    csv_writer = csv.DictWriter(file_write, fieldnames=fieldnames, delimiter=",")
    csv_writer.writeheader()

    for game_id, streak in streak_dict.items():
        print(f"Writing {game_id}")
        csv_writer.writerow({"game_id": game_id, "streak": streak})