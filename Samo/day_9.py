import os
import re
import numpy as np

def readLines(fileName: str) -> list:
    file = open(os.path.join(os.path.dirname(__file__), fileName), "r")
    lines = file.read().splitlines()
    file.close()
    return lines


def part1() -> int:
    moves = readLines("inputs/input9.txt")
    positions = set()
    xHead = 0; yHead = 0
    xTail = 0; yTail = 0
    positions.add((xTail, yTail)) # add starting position

    for move in moves:
        direction = move[0]
        step = int(re.findall(r"\d+", move)[0])
        
        if direction == "R":
            xHead += step
            if abs(yHead - yTail) <= 1 and abs(xHead - xTail) <= 1:
                # no need to move tail
                continue

            # diagonal movement
            if yHead != yTail:
                xTail += 1
                yTail += (yHead - yTail)
                positions.add((xTail, yTail))

            # horizontal movement
            for _ in range(xHead - xTail - 1):
                xTail += 1
                positions.add((xTail, yTail))
                
        elif direction == "L":
            xHead -= step
            if abs(yHead - yTail) <= 1 and abs(xHead - xTail) <= 1:
                # no need to move tail
                continue

            # diagonal movement
            if yHead != yTail:
                xTail -= 1
                yTail += (yHead - yTail)
                positions.add((xTail, yTail)) 

            # horizontal movement
            for _ in range(xTail - xHead - 1):
                xTail -= 1
                positions.add((xTail, yTail))

        elif direction == "U":
            yHead += step
            if abs(yHead - yTail) <= 1 and abs(xHead - xTail) <= 1:
                # no need to move tail
                continue
            
            # diagonal movement
            if xHead != xTail:
                yTail += 1
                xTail += (xHead - xTail)
                positions.add((xTail, yTail))

            # vertical movement
            for _ in range(yHead - yTail - 1):
                yTail += 1
                positions.add((xTail, yTail))

        elif direction == "D":
            yHead -= step
            if abs(yHead - yTail) <= 1 and abs(xHead - xTail) <= 1:
                # no need to move tail
                continue
            
            # diagonal movement
            if xHead != xTail:
                yTail -= 1
                xTail += (xHead - xTail)
                positions.add((xTail, yTail))

            # vertical movement
            for _ in range(yTail - yHead - 1):
                yTail -= 1
                positions.add((xTail, yTail))

    return len(positions)



def part2() -> int:
    moves = readLines("inputs/input9.txt")
    positions = set()
    rope = [(0, 0) for _ in range(10)]
    positions.add(rope[-1]) # add starting position

    directions = {"R": [1, 0], "L" : [-1, 0], "U" : [0, 1], "D" : [0, -1]}
    for move in moves:
        moveDir, n = move.split(" ")

        # do number of steps specified
        for _ in range(int(n)):
            rope[0] = (rope[0][0] + directions[moveDir][0], rope[0][1] + directions[moveDir][1])

            for i in range(1, len(rope)):
                # difference between two neighbor knots
                xMove = rope[i-1][0] - rope[i][0]
                yMove = rope[i-1][1] - rope[i][1]
                
                # move a knot
                dx, dy = 0, 0
                if abs(xMove) == 2 or abs(yMove) == 2:
                    dx = 0 if xMove == 0 else 1 if xMove > 0 else -1
                    dy = 0 if yMove == 0 else 1 if yMove > 0 else -1
                if dx or dy:
                    rope[i] = (rope[i][0] + dx, rope[i][1] + dy)

            positions.add(rope[-1])

    return len(positions)

def main():
    numOfPositioins = part1()
    print("Number of positions that the tail of the rope visits:")
    print(numOfPositioins)

    numOfPositioins2 = part2()
    print("Number of positions that the long tail of the rope visits:")
    print(numOfPositioins2)

if __name__ == "__main__":
    main()
