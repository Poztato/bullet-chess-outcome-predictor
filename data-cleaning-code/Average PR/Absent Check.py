FILE = r"..\Average PR.csv"

gameCheck = []

for i in range(1, 9001):
    gameCheck.append(f"ID{i:04d}")

with open(FILE, 'r', newline='', encoding='utf-8') as read_file:
    lines = read_file.readlines()

skipHeader = True
for line in lines:
    if skipHeader:
        skipHeader = False
        continue

    individualElements = line.split(",")

    if individualElements[0] in gameCheck:
        gameCheck.remove(individualElements[0])

print(gameCheck)
    