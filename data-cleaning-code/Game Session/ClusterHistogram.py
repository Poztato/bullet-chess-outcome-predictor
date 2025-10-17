import matplotlib.pyplot as plt

SESSION_CSV = r"..\Session Cluster.csv"
session_count = []


with open(SESSION_CSV, 'r', newline='', encoding='utf-8') as csv_file:
    lines = csv_file.readlines()

skip_header = True
skip_header2 = True
for index, line in enumerate(lines):
    if skip_header:
        skip_header = False
        continue

    if skip_header2:
        skip_header2 = False
        continue

    sesh_count = line.split(",")[1]  
    if int(sesh_count.strip()) == 1:
        sesh_count_prev = lines[index-1].split(",")[1]
        if int(sesh_count_prev) > 0:
            session_count.append(int(sesh_count_prev.strip()))


print(f"Number of sessions: {len(session_count)}")

plt.hist(session_count, bins=100)
plt.xlabel("Session Count")
plt.ylabel("Frequency")
plt.title("Session Count Histogram")
plt.show()