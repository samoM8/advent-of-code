import os

def readLines(fileName: str) -> list:
    return [line.rstrip("\n") for line in open(os.path.join(os.path.dirname(__file__), fileName), "r")]

RUCKSACK_ITEMS = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def part1() -> int:
    lines = readLines("inputs/input3.txt")
    sumOfPrioritioes = 0
    for line in lines:
        firstHalf, secondHalf = line[: len(line) // 2], line[len(line) // 2 :]
        firstSet = set(firstHalf)
        secondSet = set(secondHalf)

        inBothSets = firstSet & secondSet
        sumOfPrioritioes += RUCKSACK_ITEMS.rfind(next(iter(inBothSets)))
        
    return sumOfPrioritioes

def part2() -> int:
    lines = readLines("inputs/input3.txt")
    sumOfPrioritioes = 0
    for i in range(0, len(lines), 3):
        set1 = set(lines[i])
        set2 = set(lines[i+1])
        set3 = set(lines[i+2])

        inAllSets = set1 & set2 & set3
        sumOfPrioritioes += RUCKSACK_ITEMS.rfind(next(iter(inAllSets)))
        
    return sumOfPrioritioes

def main():
    sumOfPriorities = part1()
    print("Sum of priorities:")
    print(sumOfPriorities)
    sumOfPriorities2 = part2()
    print("Sum of priorities for groups:")
    print(sumOfPriorities2)

if __name__ == "__main__":
    main()
