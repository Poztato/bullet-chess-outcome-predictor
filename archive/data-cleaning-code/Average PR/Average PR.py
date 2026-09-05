FILE_READ = r"..\Move Evaluations.csv"
FILE_WRITE = r"..\Average PR.csv"

# File index
GAME_ID = 0
MOVE = 1
PR = 2
IS_WHITE = 3
RESULT = 4

punishmentList = []
counter = 0

with open(FILE_READ, 'r', newline='', encoding='utf-8') as csv_file:
    lines = csv_file.readlines()


def isSameGame(index, currentGame):
    try:
        elements = lines[index+1].split(",")
        nextGameID = elements[GAME_ID]
        if nextGameID == currentGame:
            return True
    
    except:
        return False
    
    return False

skipHeader = True
writeHeader = True
for index, line in enumerate(lines):
    individualElements = line.split(",")
    
    if skipHeader:
        skipHeader = False
        continue        # Skip header

    if isSameGame(int(index), individualElements[GAME_ID]):
        if int(individualElements[PR]) > 100:
            punishmentList.append(int(individualElements[PR]))

        continue

    else:
        if writeHeader:
            with open(FILE_WRITE, 'w', newline='', encoding='utf-8') as write_file:
                write_file.write(f"game_id,avg_pr,is_white,result\n")      
            writeHeader = False

        try:
            averagePR = sum(punishmentList) / len(punishmentList)
            averagePR = averagePR
        
        except:
            averagePR = 0

        with open(FILE_WRITE, 'a', newline='', encoding='utf-8') as write_file:
            write_file.write(f"{individualElements[GAME_ID]},{averagePR:.4f},\
                            {individualElements[IS_WHITE]},{individualElements[RESULT]}")
            
            counter += 1
        
        punishmentList = []

print(f"Number of games written: {counter}")