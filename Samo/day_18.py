import os
import numpy as np
from collections import deque


def readLines(fileName: str) -> list:
    file = open(os.path.join(os.path.dirname(__file__), fileName), "r")
    lines = file.read().splitlines()
    file.close()
    return lines


def part1() -> int:
    lines = readLines("inputs/input18.txt")
    coordinates = []
    for line in lines:
        coordinates.append(np.array([int(x) for x in line.split(",")]))

    all_sides = len(coordinates) * 6
    connected_sides = 0

    for i in range(len(coordinates)):
        for j in range(i+1, len(coordinates)):
            sum_of_diff = sum(abs(coordinates[i] - coordinates[j]))
            if sum_of_diff == 1:
                connected_sides += 1

    return all_sides - 2 * connected_sides


def part1_faster():
    data = readLines("inputs/input18.txt")
    droplets = set([tuple(map(int, line.split(","))) for line in data])
    sides = 0
    neighbors = [(-1, 0, 0), (1, 0, 0), (0, -1, 0),
                 (0, 1, 0), (0, 0, -1), (0, 0, 1)]

    for x, y, z in droplets:
        neighbor_droplets = [(x + dx, y + dy, z + dz)
                             for dx, dy, dz in neighbors]
        sides += len([1 for nd in neighbor_droplets if nd not in droplets])

    return sides


def part2() -> int:
    lines = readLines("inputs/input18.txt")
    coordinates = set([tuple(map(int, line.split(","))) for line in lines])
    neighbors = [(-1, 0, 0), (1, 0, 0), (0, -1, 0),
                 (0, 1, 0), (0, 0, -1), (0, 0, 1)]

    max_x = max(list(zip(*coordinates))[0])
    max_y = max(list(zip(*coordinates))[1])
    max_z = max(list(zip(*coordinates))[2])

    # make a cube bigger than dropplets so we can go around them
    cube = np.zeros((max_x + 2, max_y + 2, max_z + 2))
    for x, y, z in coordinates:
        cube[x, y, z] = 1

    # BFS and set all reachable indices to 2
    # We get a 3D array which has values
    # 0 - not reachable by water or steam
    # 1 - lava droplets
    # 2 - reachable by water or steam
    queue = deque()
    queue.append((0, 0, 0))
    while queue:
        x, y, z = queue.popleft()
        cube[x, y, z] = 2
        for dx, dy, dz in neighbors:
            x_n, y_n, z_n = x + dx, y + dy, z + dz
            if 0 <= x_n < max_x + 2 and 0 <= y_n < max_y + 2 and \
                    0 <= z_n < max_z + 2 and cube[x_n, y_n, z_n] == 0:
                # If I set value 2 here, we reduce a lot of repetitions
                # so we don't put same indices in the queue again
                cube[x_n, y_n, z_n] = 2
                queue.append((x_n, y_n, z_n))

    # Loop through all lava droplet coordinates and check if neighbors are set to 2 in cube.
    # If they are 2 then add them to sides counter.
    sides = 0
    for x, y, z in coordinates:
        neighbor_coordinates = [(x + dx, y + dy, z + dz)
                                for dx, dy, dz in neighbors]
        sides += len([1 for nd in neighbor_coordinates if cube[nd] == 2])

    return sides


def main():
    surface_area = part1()
    print("Surface area of scanned lava droplet:")
    print(surface_area)

    surface_area = part2()
    print("Surface area of scanned lava droplet which are reachable by air:")
    print(surface_area)


if __name__ == "__main__":
    main()
