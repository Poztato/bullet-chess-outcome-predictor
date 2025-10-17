import matplotlib.pyplot as plt
import csv

STREAK_CSV = r"..\Streak Record.csv"
streak_list = []

with open(STREAK_CSV, 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)

    for line in reader:
        streak_list.append(int(line["streak"]))


plt.hist(streak_list, bins=20)
plt.xlabel("Win/Loss counter")
plt.ylabel("Frequency")
plt.title("Win/Lost Streak Histogram")
plt.show()