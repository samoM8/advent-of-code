import os
import re
from collections import deque

def readLines(fileName: str) -> list:
    file = open(os.path.join(os.path.dirname(__file__), fileName), "r")
    startCrateArrangement, moves = file.read().split("\n\n")
    file.close()
    return startCrateArrangement.splitlines(), moves.splitlines()

def part1():
    startCrateArrangement, moves = readLines("inputs/input5.txt")
    # find the last number, which is the number of crates
    numOfCrates = int(re.findall(r"\d+", startCrateArrangement[len(startCrateArrangement)-1])[-1])
    startCrateArrangement.pop() # remove the last row

    currentCrateArrangement = []
    # prepare list of stacks
    for i in range(numOfCrates):
        currentCrateArrangement.append(deque())

    # put crates in list of stacks
    for row in reversed(startCrateArrangement):
        for i in range(numOfCrates):
            crate = row[4 * i + 1]
            if crate.isalpha():
                currentCrateArrangement[i].append(crate)

    # do all the moves of the crates CrateMover 9000
    # can only move 1 crate at once
    for row in moves:
        numOfMovedCrates, moveFrom, moveTo = [int(num) for num in re.findall(r"\d+", row)]
        for i in range(numOfMovedCrates):
            crate = currentCrateArrangement[moveFrom-1].pop()
            currentCrateArrangement[moveTo-1].append(crate)

    upperCrates = []
    # get the upper crates from all the stacks
    for i in range(numOfCrates):
        upperCrates.append(currentCrateArrangement[i].pop())
    return "".join(upperCrates)

def part2():
    startCrateArrangement, moves = readLines("inputs/input5.txt")
    # find the last number, which is the number of crates
    numOfCrates = int(re.findall(r"\d+", startCrateArrangement[len(startCrateArrangement)-1])[-1])
    startCrateArrangement.pop() # remove the last row

    currentCrateArrangement = []
    # prepare list of lists
    for i in range(numOfCrates):
        currentCrateArrangement.append([])

    # put crates in list of lists
    for row in reversed(startCrateArrangement):
        for i in range(numOfCrates):
            crate = row[4 * i + 1]
            if crate.isalpha():
                currentCrateArrangement[i].append(crate)

    # do all the moves of the crates with CrateMover 9001
    # can move multiple crates at once
    for row in moves:
        numOfMovedCrates, moveFrom, moveTo = [int(num) for num in re.findall(r"\d+", row)]
        crates = currentCrateArrangement[moveFrom-1][-numOfMovedCrates:]
        del currentCrateArrangement[moveFrom-1][-numOfMovedCrates:]
        currentCrateArrangement[moveTo-1].extend(crates)

    upperCrates = []
    # get the upper crates from all the stacks
    for i in range(numOfCrates):
        upperCrates.append(currentCrateArrangement[i].pop())
    return "".join(upperCrates)

def main():
    upperCrates = part1()
    print("Upper creates after all the moves with CrateMover 9000:")
    print(upperCrates)

    upperCrates2 = part2()
    print("Upper creates after all the moves with CrateMover 9001:")
    print(upperCrates2)

if __name__ == "__main__":
    main()
