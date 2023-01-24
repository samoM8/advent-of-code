import os
import numpy as np

def readLines(fileName: str) -> list:
    file = open(os.path.join(os.path.dirname(__file__), fileName), "r")
    data = file.read().splitlines()
    file.close()
    return data

def part1() -> int:
    lines = readLines("inputs/input10.txt")

    cycle = 1
    X = 1
    sumOfSignals = 0
    for line in lines:
        # noop just adds one cicle
        if line[:4] == "noop":
            if (cycle - 20) % 40 == 0:
                sumOfSignals += cycle * X
            cycle = cycle + 1
        # addx is two cycles and it change X
        elif line[:4] == "addx": 
            if (cycle - 20) % 40 == 0:
                sumOfSignals += cycle * X
            cycle = cycle + 1
            if (cycle - 20) % 40 == 0:
                sumOfSignals += cycle * X

            X = X + int(line[5:])
            cycle = cycle + 1

    return sumOfSignals

def part2() -> int:
    lines = readLines("inputs/input10.txt")

    cycle = 1
    X = 1 # middle of sprite position
    crt = np.chararray((240), itemsize=1)
    crt[:] = "."

    for line in lines:
        position = cycle - 1
        if abs(position % 40 - X) <= 1:
            crt[position] = "#"
        
        cycle = cycle + 1
        position = cycle - 1

        if line[:4] == "addx":
            if abs(position % 40 - X) <= 1:
                crt[position] = "#"
            
            X = X + int(line[5:])
            cycle = cycle + 1
    
    print("CRT screen:")
    for i in range(0, 240, 40):
        for j in range(40):
            print(crt[i + j].decode("utf-8"), end="")
        print()

def main():
    sumOfSignals = part1()
    print("Sum of signal strengths:")
    print(sumOfSignals)

    part2()

if __name__ == "__main__":
    main()
