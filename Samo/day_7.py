from collections import deque
import os

def readLines(fileName: str) -> list:
    file = open(os.path.join(os.path.dirname(__file__), fileName), "r")
    lines = file.read().splitlines()
    file.close()
    return lines

def part1() -> int:
    lines = readLines("inputs/input7.txt")
    queue = deque()
    sum = 0

    i = 0
    while i < len(lines):
        instr = lines[i]

        # if we move
        if instr.split()[1] == "cd":
            # when we move backwards we check if current dir size is 
            # less or equal to 10000 we add it to our sum of sizes
            if instr.split()[2] == "..":
                dirSize = queue.pop()["size"]
                if dirSize <= 100000:
                    sum += dirSize
            else: # when we move inside a dir
                queue.append({"dirName": instr.split()[2], "size": 0})

            i = i + 1
        # if we list items we must count all file sizes and
        # add it to all directories we are currenlty in
        elif instr.split()[1] == "ls":
            i = i + 1
            while i < len(lines) and lines[i][0] != "$":
                one, *_ = lines[i].split()
                if one.isnumeric():
                    size = int(one)
                    for dir in queue:
                        dir["size"] += size

                i = i + 1

    # I can also check the sizes left in queue...

    return sum


def part2() -> int:
    lines = readLines("inputs/input7.txt")
    queue = deque()
    dirsWithSizes = {}

    i = 0
    while i < len(lines):
        instr = lines[i]

        # if we move
        if instr.split()[1] == "cd":
            # we save the dir into dictionary
            if instr.split()[2] == "..":
                dir = queue.pop()
                dirsWithSizes[dir["dirName"]] = dir["size"]
            else: # when we move inside a dir
                queue.append({"dirName": instr.split()[2], "size": 0})

            i = i + 1
        # if we list items we must count all file sizes and
        # add it to all directories we are currenlty in
        elif instr.split()[1] == "ls":
            i = i + 1
            while i < len(lines) and lines[i][0] != "$":
                one, *_ = lines[i].split()
                if one.isnumeric():
                    size = int(one)
                    for dir in queue:
                        dir["size"] += size

                i = i + 1

    # I can also check the sizes left in queue
    for dir in queue:
        dirsWithSizes[dir["dirName"]] = dir["size"]

    # we need 30 000 000 for update
    unusedSpace = 70000000 - dirsWithSizes["/"]
    needToDelete = 30000000 - unusedSpace
    
    lowestSize = 30000000
    for dirName in dirsWithSizes:
        if dirsWithSizes[dirName] >= needToDelete and dirsWithSizes[dirName] < lowestSize:
            lowestSize = dirsWithSizes[dirName]

    return lowestSize


def main():
    sumOfSizes = part1()
    print("Sum of total sizes in directories which have a size lower than 100000:")
    print(sumOfSizes)

    dirSizeToDelete = part2()
    print("Size of directory we need to delete:")
    print(dirSizeToDelete)


if __name__ == "__main__":
    main()
