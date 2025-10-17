from datetime import datetime
from datetime import timedelta
import os


GAME_DIRECTORY = r"..\Individual Games"
SESSION_CSV = r"..\Session Cluster.csv"
DATE_HEADER = "[Date "
TIME_HEADER = "[EndTime "
TIME_THRESHOLD = timedelta(minutes = 15)

allGames = os.listdir(GAME_DIRECTORY)
currentSession = []
dupeList = [f"ID{x}.txt" for x in range(8702, 8801, 2)]

# Remove duplicated files
for file in dupeList:
    allGames.remove(file)


def getDatetimeElements(individualGame):
    with open(f"{GAME_DIRECTORY}\\{individualGame}", 'r', encoding='utf-8') as game:
        lines = game.readlines()

        for line in lines:
            if line.startswith(DATE_HEADER):
                currentDate = line.split("\"")[1]

            elif line.startswith(TIME_HEADER):
                currentTime = line.split("\"")[1].split(" ")[0]
                break
        
        return f"{currentDate} {currentTime}"

isFirstGame = True
writeHeader = True
isIndividualGame = False
for gameIndex, individualGame in enumerate(allGames):

    currentDateTime = datetime.strptime(getDatetimeElements(individualGame), "%Y.%m.%d %H:%M:%S")
    
    gameIndex -= 1
    if gameIndex < 0:   # Skip first file
        continue

    previousDateTime = datetime.strptime(getDatetimeElements(allGames[gameIndex]), "%Y.%m.%d %H:%M:%S")

    timeDifference = currentDateTime - previousDateTime

    if timeDifference <= TIME_THRESHOLD:        # If its the same session
        if isFirstGame:
            currentSession.append(allGames[gameIndex])      # Appends previous date time
            isFirstGame = False
        
        isIndividualGame = False     # Not individual because there are at least two games
        currentSession.append(individualGame)               # Appends current date time

    else:
        if writeHeader:
            with open(SESSION_CSV, 'w', newline='', encoding='utf-8') as csv_file:
                csv_file.write("game_id,sesh_count\n")
            writeHeader = False

        if isIndividualGame:
            with open(SESSION_CSV, 'a', newline='', encoding='utf-8') as csv_file:
                sessionGame = allGames[gameIndex].split(".")[0]
                csv_file.write(f"{sessionGame},1\n")

        else:
            for sessionIndex, sessionGame in enumerate(currentSession):
                with open(SESSION_CSV, 'a', newline='', encoding='utf-8') as csv_file:
                    sessionGame = sessionGame.split(".")[0]
                    csv_file.write(f"{sessionGame},{sessionIndex+1}\n")
                    print(f"Writing {sessionGame}")
        
        isFirstGame = True          # Reset session settings
        currentSession = []
        isIndividualGame = True     # Assumes that the next game is individual

# Flush out the final list 
for sessionIndex, sessionGame in enumerate(currentSession):
    with open(SESSION_CSV, 'a', newline='', encoding='utf-8') as csv_file:
        sessionGame = sessionGame.split(".")[0]
        csv_file.write(f"{sessionGame},{sessionIndex+1}\n")
        print(f"Writing {sessionGame}")