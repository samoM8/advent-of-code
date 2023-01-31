import os
import numpy as np

def readLines(fileName: str) -> list:
    file = open(os.path.join(os.path.dirname(__file__), fileName), "r")
    lines = file.read().splitlines()
    file.close()
    return lines

def printScanScreen(scan: list) -> None:
    for i, line in enumerate(scan):
        print(str(i).ljust(len(str(len(scan)))), end=" ")
        for dot in line:
            print(dot.decode("utf-8"), end="")
        print()

def pathToArrayOfArrays(lines: list) -> list:
    """
    Packs all paths in array of arrays with integers.
    Return minimal x coordinate, minimal y coordinate,
    maximal x coordinate and array of arrays - rock paths.
    """
    rockPathsTmp = [x.split(" -> ") for x in lines]

    rockPaths = []
    minX = 1000
    maxX = 0
    maxY = 0
    i = 0
    for path in rockPathsTmp:
        rockPaths.append([])
        for coordinates in path:
            x, y = coordinates.split(",")
            x = int(x); y = int(y)
            rockPaths[i].append((x, y))

            if x < minX: minX = x
            if x > maxX: maxX = x
            if y > maxY: maxY = y

        i = i + 1
    
    return minX, maxX, maxY, rockPaths

def generateScanScreen(rockPaths: list, ySize:int, xSize:int) -> np.array:
    """
    Generate Scan Screen based on rock paths in a list.
    Returns 2d numpy array of characters with rocks as '#'.
    """
    scan = np.chararray((ySize, xSize), itemsize=1)
    scan[:] = "."
    # Draw rock paths on scan screen
    for rockPath in rockPaths:
        i = 0
        while i < len(rockPath) - 1:
            coord_1 = rockPath[i]
            coord_2 = rockPath[i+1]

            yLow = min(coord_1[1], coord_2[1])
            yHigh = max(coord_1[1], coord_2[1])
            xLow = min(coord_1[0], coord_2[0])
            xHigh = max(coord_1[0], coord_2[0])

            scan[yLow:yHigh+1, xLow:xHigh+1] = "#"
            i = i + 1
    
    return scan

def part1() -> int:
    lines = readLines("inputs/input14.txt")
    
    # Pack all paths in array of arrays with integers
    minX, maxX, maxY, rockPaths = pathToArrayOfArrays(lines)

    # Transfer the coordination system to (0, 0)
    for rockPath in rockPaths:
        i = 0
        for x, y in rockPath:
            rockPath[i] = (x - minX, y)
            i = i + 1
    
    # Generate scan screen
    xSize = maxX - minX + 1
    scan = generateScanScreen(rockPaths, maxY + 1, xSize)

    # printScanScreen(scan)

    # Sand falling simulation until all units of sand come to rest
    pouringSand = (500 - minX, 0)
    numOfSandResting = 0
    flowingIntoAbyss = False
    while not flowingIntoAbyss:
        x = pouringSand[0]
        y = pouringSand[1]
        while y < len(scan) and 0 <= x and x < len(scan[0]):            
            if scan[y+1, x] == b".": # fall down
                y = y + 1
            elif scan[y+1, x-1] == b".": # down and left
                x = x - 1
                y = y + 1
            elif scan[y+1, x+1] == b".": # down and right
                x = x + 1
                y = y + 1
            else: # nowhere to fall
                scan[y, x] = b"o"
                numOfSandResting = numOfSandResting + 1
                break
            
            # if we get to the edge the sand will fall down into the abyss
            if y == len(scan)-1 or x == -1 or x == len(scan[0])-1:
                flowingIntoAbyss = True
                # printScanScreen(scan)
                break

    return numOfSandResting

def part2() -> int:
    lines = readLines("inputs/input14.txt")
    
    # Pack all paths in array of arrays with integers
    minX, maxX, maxY, rockPaths = pathToArrayOfArrays(lines)

    # Transfer the coordination system to (0, maxY + 5)
    for rockPath in rockPaths:
        i = 0
        for x, y in rockPath:
            rockPath[i] = (x - minX + maxY + 5, y)
            i = i + 1
    
    # Generate scan screen
    xSize = maxX - minX + 1 + 2 * maxY + 2 * 5
    scan = generateScanScreen(rockPaths, maxY + 1 + 2, xSize)
    # Add bottom row of rocks
    scan[-1, :] = "#"
    
    # printScanScreen(scan)

    # Sand falling simulation until all units of sand come to rest
    pouringSand = (500 - minX + maxY + 5, 0)

    numOfSandResting = 0
    while scan[pouringSand[1], pouringSand[0]] != b"o":
        x = pouringSand[0]
        y = pouringSand[1]
        while y < len(scan) and 0 <= x and x < len(scan[0]):            
            if scan[y+1, x] == b".": # fall down
                y = y + 1
            elif scan[y+1, x-1] == b".": # down and left
                x = x - 1
                y = y + 1
            elif scan[y+1, x+1] == b".": # down and right
                x = x + 1
                y = y + 1
            else: # nowhere to fall
                scan[y, x] = b"o"
                numOfSandResting = numOfSandResting + 1
                break

    # printScanScreen(scan)

    return numOfSandResting

def main():
    unitsOfSand = part1()
    print("Units of sand that has come to rest before flowing into abyss below:")
    print(unitsOfSand)

    unitsOfSand2 = part2()
    print("Units of sand that has come to rest before blocking source:")
    print(unitsOfSand2)

if __name__ == "__main__":
    main()
