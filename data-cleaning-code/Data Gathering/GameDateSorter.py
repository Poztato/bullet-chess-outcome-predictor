import os

DIRECTORY = "..\\Chess Games"
COMPILED_GAMES = "..\\Compiled Games\\Compiled Games.txt"

files = os.listdir(DIRECTORY)

with open(COMPILED_GAMES, 'w') as full_games:
    for file in files:
        file_path = os.path.join(DIRECTORY, file)
        with open(file_path, 'r') as games:
            lines = games.readlines()
            full_games.writelines(lines)
            full_games.write('\n')
