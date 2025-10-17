import csv

white_wins = 0
black_wins = 0
draws = 0
total_games = 0

with open(r"..\Average PR.csv", "r", newline="", encoding="utf-8") as read_csv:
    reader = csv.reader(read_csv)
    next(reader)

    for fields in reader:
        if len(fields) < 4:
            continue

        print(fields[0])

        is_white = fields[2].strip()
        result = fields[3].strip()

        total_games += 1

        if result == "0.5":
            draws += 1
        elif is_white == "1":
            if result == "1.0":
                white_wins += 1
            else:
                black_wins += 1
        else:
            if result == "1.0":
                black_wins += 1
            else:
                white_wins += 1

print(f"\nWhite Wins: {white_wins}")
print(f"\tWinrate -> {white_wins / total_games:.2%}")
print(f"\nBlack Wins: {black_wins}")
print(f"\tWinrate -> {black_wins / total_games:.2%}")
print(f"\nDraws: {draws}")
