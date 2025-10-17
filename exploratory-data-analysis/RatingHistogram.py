import matplotlib.pyplot as plt

RATING_CSV = r"..\Game Ratings.csv"

with open(RATING_CSV, 'r', newline='', encoding='utf-8') as csv_file:
    lines = csv_file.readlines()

all_rating_diff = []

skip_header = True
for line in lines:
    if skip_header:
        skip_header = False
        continue

    elements = line.split(",")

    elo = int(elements[2].strip())

    if True:
        all_rating_diff.append(elo)

print(f"---All Sessions---")
print(f"Highest rating change : {max(all_rating_diff)}")
print(f"Lowest rating change  : {min(all_rating_diff)}")
print(f"Average rating change : {sum(all_rating_diff) / len(all_rating_diff)}")


session_end_rating = []

skip_header = True
skip_second = True
for index, line in enumerate(lines):
    if skip_header:
        skip_header = False
        continue

    if skip_second:
        skip_second = False
        continue

    elements = line.split(",")
    session = elements[1]
    if session == "1":
        last_end_rating_line = lines[index-1]
        last_end_rating_element = last_end_rating_line.split(",")[2].strip()
        session_end_rating.append(int(last_end_rating_element))

print(f"\n---Session End---")
print(f"Highest rating change : {max(session_end_rating)}")
print(f"Lowest rating change  : {min(session_end_rating)}")
print(f"Average rating change : {sum(session_end_rating) / len(session_end_rating)}")



def showHistogram(some_list):
    plt.hist(some_list, bins=100)
    plt.xlabel("Rating Change")
    plt.ylabel("Frequency")
    plt.title("Rating Change Histogram")
    plt.show()

# showHistogram(session_end_rating)

counter = 0
for i in all_rating_diff:
    if i == 1:
        counter += 1
    
print(f"\nNumber of 0 values: {counter}")