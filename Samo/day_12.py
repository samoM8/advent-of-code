import os
import numpy as np
from collections import deque

def readLines(fileName: str) -> list:
    file = open(os.path.join(os.path.dirname(__file__), fileName), "r")
    data = file.read().splitlines()
    file.close()
    return data

def findNeighbors(node: dict, heightMap: np.array) -> list:
    """
    Find neighbors of positions.
    Neighbors are left, right, up, down and must be inside bounds.
    Neighbor must only be 1 elevation level higher which is stored in nextElevation
    """
    height = len(heightMap)
    width = len(heightMap[0])
    pos = node["pos"]
    nextIx = ELEVATIONS.index(node["elevation"]) + 1 # next elevation index

    # This is needed because E has the same elevation level as z
    # and i did not know that before so it is just a quick fix.
    # Should be changed so the solution is prettier...
    if nextIx == 26:
        nextIx = nextIx + 1

    neighbors = []
    if (pos[0] - 1 >= 0 and 
        ELEVATIONS.index(heightMap[(pos[0] - 1, pos[1])]) <= nextIx): # upper neighbor
        neighbors.append((pos[0] - 1, pos[1]))
    if (pos[1] + 1 < width and
        ELEVATIONS.index(heightMap[(pos[0], pos[1] + 1)]) <= nextIx): # right neighbor
        neighbors.append((pos[0], pos[1] + 1))
    if (pos[0] + 1 < height and 
        ELEVATIONS.index(heightMap[(pos[0] + 1, pos[1])]) <= nextIx): # down neighbor
        neighbors.append((pos[0] + 1, pos[1]))
    if (pos[1] - 1 >= 0 and 
        ELEVATIONS.index(heightMap[(pos[0], pos[1] - 1)]) <= nextIx): # left neighbor
        neighbors.append((pos[0], pos[1] - 1))

    return neighbors

ELEVATIONS = "SabcdefghijklmnopqrstuvwxyzE"

def part1() -> int:
    lines = readLines("inputs/input12.txt")
    heightMap = np.array([list(x) for x in lines], np.str_)
    visitedMap = np.zeros((len(heightMap), len(heightMap[0])), np.uint8)

    startArr = np.where(heightMap == "S")
    endArr = np.where(heightMap == "E")
    start = (startArr[0][0], startArr[1][0])
    end = (endArr[0][0], endArr[1][0])

    # Solving with Breaths First Search
    # Could use a hevristic which would speed up the solution
    # Something like distance to end or just A* algorithm
    positions = deque()
    # positions.append({"pos": start, "steps": 0, "elevation": "S", "path": [start]})
    positions.append({"pos": start, "steps": 0, "elevation": "S"})
    visitedMap[start] = 1
    while positions:
        currNode = positions.popleft()
        nextStep = currNode["steps"] + 1 # add one step

        neighbors = findNeighbors(currNode, heightMap)
        for neighbor in neighbors:
            # if we found end we return number of steps
            if neighbor == end:
                ################
                # testmap = np.zeros((len(heightMap), len(heightMap[0])), np.uint32)
                # i = 1
                # for node in currNode["path"]:
                #     testmap[node] = i
                #     i = i + 1
                # f = open("ttt.txt", "w")
                # for i in range(len(testmap)):
                #     for j in range(len(testmap[i])):
                #         f.write(str(testmap[i, j]).ljust(4))
                #     f.write("\n")
                # f.close()
                ################
                return nextStep
            # we check if node has not yet been visited and add it to queue
            elif visitedMap[neighbor] == 0:
                visitedMap[neighbor] = 1
                # positions.append({"pos": neighbor, "steps": nextStep, "elevation": heightMap[neighbor], "path": currNode["path"] + [neighbor]})
                positions.append({"pos": neighbor, "steps": nextStep, "elevation": heightMap[neighbor]})

    # we did not find end
    return -1

def part2() -> int:
    lines = readLines("inputs/input12.txt")
    heightMap = np.array([list(x) for x in lines], np.str_)

    startArr = np.where(heightMap == "a")
    endArr = np.where(heightMap == "E")
    end = (endArr[0][0], endArr[1][0])

    lowestSteps = 1000000
    # Check for all starting positions
    # It would be better if i went from end and finished when i
    # move to the first elevations 'a', this would be faster
    for i in range(len(startArr[0])):
        visitedMap = np.zeros((len(heightMap), len(heightMap[0])), np.uint8)
        start = (startArr[0][i], startArr[1][i])
        positions = deque()
        positions.append({"pos": start, "steps": 0, "elevation": "a"})
        visitedMap[start] = 1
        while positions:
            currNode = positions.popleft()
            nextStep = currNode["steps"] + 1 # add one step

            neighbors = findNeighbors(currNode, heightMap)
            for neighbor in neighbors:
                # if we found end we return number of steps
                if neighbor == end:
                    if nextStep < lowestSteps: lowestSteps = nextStep
                    positions.clear() # for termination of while loop
                    break
                # we check if node has not yet been visited and add it to queue
                elif visitedMap[neighbor] == 0:
                    visitedMap[neighbor] = 1
                    positions.append({"pos": neighbor, "steps": nextStep, "elevation": heightMap[neighbor]})

    return lowestSteps

def main():
    numOfSteps = part1()
    print("Fewest steps from current position to final position:")
    print(numOfSteps)

    numOfSteps2 = part2()
    print("Fewest steps from all positions with elevation level 'a' to final position:")
    print(numOfSteps2)

if __name__ == "__main__":
    main()
