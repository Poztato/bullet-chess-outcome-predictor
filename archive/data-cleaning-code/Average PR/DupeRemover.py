import csv

CSV_WRITE = r"..\Average PR.csv"
CSV_READ = r"..\Junk\Backups\Dupes\Average PR (Dupe).csv"

result_dict = {}
current_pr = None
dupe_list = []

with open(CSV_READ, "r", newline="", encoding="utf-8") as read_file:
    lines = csv.DictReader(read_file)

    for line in lines:
        result_dict[line["game_id"]] = line["avg_pr"]

    for game_id, avg_pr in result_dict.items():
        if current_pr == avg_pr:
            if game_id == "ID8799":
                continue

            if int(game_id.split("D")[1]) > 8700:
                dupe_list.append(game_id)    
        
        else:
            current_pr = avg_pr

    read_file.seek(0)
    lines = csv.DictReader(read_file)
    with open(CSV_WRITE, "w", newline="", encoding="utf-8") as write_file:
        fieldnames = ["game_id", "avg_pr", "is_white", "result"]
        csv_writer = csv.DictWriter(write_file, fieldnames=fieldnames, delimiter=",")

        csv_writer.writeheader()

        for line in lines:
            if line["game_id"] in dupe_list:
                continue

            else:
                csv_writer.writerow(line)


print(dupe_list)



