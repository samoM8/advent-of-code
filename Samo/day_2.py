
import os


def readLines(fileName: str):
    return [line[0:3] for line in open(os.path.join(os.path.dirname(__file__), fileName), "r")]

def part1() -> int:
    lines = readLines("inputs/input2.txt")
    totalScore = 0
    for line in lines:
        # Get the difference between opponents and my 'letter' hand
        # and than I can calculate who won based on the difference.
        res = ord(line[0]) - ord(line[2])
        myHand = ord(line[2]) - 87

        totalScore += myHand
        if (res == -23): # draw
            totalScore += 3
        elif (res == -21 or res == -24): # win
            totalScore += 6
        # else lose
        
    return totalScore

def part2() -> int:
    lines = readLines("inputs/input2.txt")
    totalScore = 0
    for line in lines:
        # Get the opponents hand and type of strategy and then
        # I can calculate based on the difference which hand I
        # need to win.
        opponentsHand = line[0]
        strategy = line[2]
        
        if strategy == "X": # lose
            if opponentsHand == "A":
                totalScore += 3
            else:
                totalScore += (ord(opponentsHand) - 65)
        elif strategy == "Y": # draw
            totalScore += 3
            totalScore += (ord(opponentsHand) - 64)
        else: # win
            totalScore += 6
            if opponentsHand == "C":
                totalScore += 1
            else:
                totalScore += (ord(opponentsHand) - 63)


    return totalScore

def main():
    score = part1()
    print("Score with prediction strategy:")
    print(score)
    score2 = part2()
    print("Score with ultimate strategy:")
    print(score2)
    

if __name__ == "__main__":
    main()
