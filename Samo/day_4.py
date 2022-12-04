import os

def readLines(fileName: str) -> list:
    file = open(os.path.join(os.path.dirname(__file__), fileName), "r")
    data = file.read().splitlines()
    file.close()
    return data

def part1() -> int:
    lines = readLines("inputs/input4.txt")
    numOfFullyContains = 0
    for line in lines:
        firstAssignment, secondAssignment = line.split(",", 2)
        firstFrom, firstTo = [int(x) for x in firstAssignment.split("-", 2)]
        secondFrom, secondTo = [int(x) for x in secondAssignment.split("-", 2)]

        if (secondFrom <= firstFrom and firstTo <= secondTo
            or firstFrom <= secondFrom and secondTo <= firstTo):
            numOfFullyContains += 1

    return numOfFullyContains

def part2() -> int:
    lines = readLines("inputs/input4.txt")
    numOfOverlaps = 0
    for line in lines:
        firstAssignment, secondAssignment = line.split(",", 2)
        firstFrom, firstTo = [int(x) for x in firstAssignment.split("-", 2)]
        secondFrom, secondTo = [int(x) for x in secondAssignment.split("-", 2)]

        if (firstFrom <= secondFrom <= firstTo
            or firstFrom <= secondTo <= firstTo
            or secondFrom <= firstFrom <= secondTo
            or secondFrom <= firstTo <= secondTo):
            numOfOverlaps += 1

    return numOfOverlaps

def main():
    numOfFullyContains = part1()
    print("One of the assignments fully contains the other:")
    print(numOfFullyContains)
    numOfOverlaps = part2()
    print("Number of overlaps:")
    print(numOfOverlaps)

if __name__ == "__main__":
    main()
