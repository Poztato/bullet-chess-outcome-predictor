import matplotlib.pyplot as plt

FILE_READ = r"..\Move Evaluations.csv"
FILE_WRITE = r"..\Average PR.csv"
# FILE_READ = r"U:\Move Evaluations.csv"

PR = 2
GAME_ID = 0
MOVE = 1

with open(FILE_READ, 'r', newline='', encoding='utf-8') as csv_file:
    lines = csv_file.readlines()

highRating = []
moveNumber = []
gameCounter = set()


flag = True
counter = 1
for row in lines:
    if flag:
        flag = False
        continue        # Skip header

    elements = row.split(",")

    if int(elements[PR]) >= 100 and int(elements[PR]) <= 2000:
        gameCounter.add(elements[GAME_ID])
        highRating.append(int(elements[PR].strip()))
        moveNumber.append(int(elements[MOVE].strip()))
        counter += 1


print("Number of games: "+ str(len(gameCounter)))
print(f"Number of times: {counter}\n")

def ScatterPlot(highRating, moveNumber):
    plt.scatter(highRating, moveNumber)
    plt.xlabel("Punishment Rating")
    plt.ylabel("Move Number")
    plt.title("PR Plot")
    plt.grid(True)
    plt.show()

def Histogram(highRating):
    plt.hist(highRating, bins=100)
    plt.xlabel("Punishment Rating")
    plt.ylabel("Frequency")
    plt.title("PR Histogram")
    plt.show()

userChoice = input("1. Histogram\n2. Scatterplot\nEnter Number: ")
if userChoice == "1":
    Histogram(highRating)

elif userChoice == "2":
    ScatterPlot(highRating, moveNumber)
