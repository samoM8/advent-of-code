import os
import numpy as np

def readLines(fileName: str) -> list:
    file = open(os.path.join(os.path.dirname(__file__), fileName), "r")
    lines = file.read().splitlines()
    file.close()
    return lines

def visibleLeft(trees: np.array, x: int, y: int) -> bool:
    """Check if all the trees on the left are smaller than current one"""
    return True if np.max(trees[x, 0:y]) < trees[x, y] else False

def visibleRight(trees: np.array, x: int, y: int) -> bool:
    """Check if all the trees on the right are smaller than current one"""
    return True if np.max(trees[x, y+1:len(trees[x])]) < trees[x, y] else False

def visibleTop(trees: np.array, x: int, y: int) -> bool:
    """Check if all the trees on the top are smaller than current one"""
    return True if np.max(trees[0:x, y]) < trees[x, y] else False

def visibleBottom(trees: np.array, x: int, y: int) -> bool:
    """Check if all the trees of the bottom are smaller than current one"""
    return True if np.max(trees[x+1:len(trees), y]) < trees[x, y] else False

def part1() -> int:
    lines = readLines("inputs/input8.txt")
    # put tree heights in 2D numpy array (list of lists)
    trees = np.zeros((len(lines), len(lines[0])), dtype=np.int32)
    for i, line in enumerate(lines):
        trees[i, :] = [*line]
    
    numOfVisibleTrees = 2 * len(trees) + 2 * len(trees[0]) - 4
    for i in range(1, len(trees)-1):
        for j in range(1, len(trees[i])-1):
            if visibleLeft(trees, i, j) or visibleRight(trees, i, j) or \
               visibleTop(trees, i, j) or visibleBottom(trees, i, j):
                numOfVisibleTrees += 1

    return numOfVisibleTrees


def scenicScore(trees: np.array, x: int, y: int) -> int:
    """
    Calculates the scenic score of a tree with coordinates (x, y).
    Scenic score is multiplied distances in all directions 
    (left, right, top, bottom
    """
    xyTreeHight = trees[x, y]

    leftScenicScore = 0
    for treeHeight in np.flip(trees[x, 0:y]):
        leftScenicScore += 1
        if treeHeight >= xyTreeHight:
            break

    rightScenicScore = 0
    for treeHeight in trees[x, y+1:len(trees[x])]:
        rightScenicScore += 1
        if treeHeight >= xyTreeHight:
            break

    topScenicScore = 0
    for treeHeight in np.flip(trees[0:x, y]):
        topScenicScore += 1
        if treeHeight >= xyTreeHight:
            break

    bottomScenicScore = 0
    for treeHeight in trees[x+1:len(trees), y]:
        bottomScenicScore += 1
        if treeHeight >= xyTreeHight:
            break

    return leftScenicScore * rightScenicScore * topScenicScore * bottomScenicScore

def part2() -> int:
    lines = readLines("inputs/input8.txt")
    # put tree heights in 2D numpy array (list of lists)
    trees = np.zeros((len(lines), len(lines[0])), dtype=np.int32)
    for i, line in enumerate(lines):
        trees[i, :] = [*line]
    
    maxScenicScore = 0
    # I don't have to loop through all trees because on the edges
    # at least one distance is zero so the scenic score is zero
    for i in range(1, len(trees)-1):
        for j in range(1, len(trees[i])-1):
            currentScenicScore = scenicScore(trees, i, j)
            if currentScenicScore > maxScenicScore:
                maxScenicScore = currentScenicScore

    return maxScenicScore

def main():
    numOfVisibleTrees = part1()
    print("Number of visible trees:")
    print(numOfVisibleTrees)

    maxScenicScore = part2()
    print("Highest scenic score possible for any tree:")
    print(maxScenicScore)

if __name__ == "__main__":
    main()
