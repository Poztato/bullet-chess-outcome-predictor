EVENT = f'[Event "Live Chess"]\n'
COMPILED_GAMES = "..\\Compiled_Games.txt"

line_count = 0
counter = 0

with open(COMPILED_GAMES, 'r', encoding='utf-8') as games:
    all_lines = games.readlines()

for i in all_lines:
    line_count += 1
    if i == EVENT:
        counter += 1

print("Number of games:", counter)
print("Number of lines:", line_count)