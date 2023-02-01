import os
import numpy as np

def readLines(fileName: str) -> list:
    file = open(os.path.join(os.path.dirname(__file__), fileName), "r")
    lines = file.read().splitlines()
    file.close()
    return lines

def manhatanDistance(p: tuple, q: tuple) -> int:
    return abs(p[0] - q[0]) + abs(p[1] - q[1])

# It is a slow solution ~ 30s
def part1() -> int:
    lines = readLines("inputs/input15.txt")
    sensorsReport = []
    # min and max range in x axis where sensors can show that there cannot be a present beacon
    x_minRange = 10000000
    x_maxRange = 0
    for line in lines:
        sensor, beacon = line.split(": ")
        xTmp, yTmp = sensor[10:].split(", ")
        sensor_x = int(xTmp[2:])
        sensor_y = int(yTmp[2:])
        xTmp, yTmp = beacon[21:].split(", ")
        beacon_x = int(xTmp[2:])
        beacon_y = int(yTmp[2:])

        sensor = {
            "sensor_pos": (sensor_x, sensor_y),
            "closest_beacon": (beacon_x, beacon_y),
            "manh_dist": manhatanDistance((sensor_x, sensor_y), (beacon_x, beacon_y))
        }
        sensorsReport.append(sensor)

        if sensor_x - sensor["manh_dist"] < x_minRange:
            x_minRange = sensor_x - sensor["manh_dist"]
        if sensor_x + sensor["manh_dist"] > x_maxRange:
            x_maxRange = sensor_x + sensor["manh_dist"]

    numOfPos = 0  # number of positions where a beacon cannot be present
    y = 2000000
    for x in range(x_minRange, x_maxRange):
        for sensor in sensorsReport:
            if (manhatanDistance((x, y), sensor["sensor_pos"]) <= sensor["manh_dist"] and
                    sensor["closest_beacon"] != (x, y)):
                numOfPos = numOfPos + 1
                break  # So I don't count the same position multiple times

    return numOfPos

def printScanScreen(scan: list) -> None:
    for i, line in enumerate(scan):
        print(str(i).ljust(len(str(len(scan)))), end=" ")
        for dot in line:
            print(dot.decode("utf-8"), end="")
        print()

# It kills the procces on the real input
# Probably out of memory
def part2bad() -> int:
    lines = readLines("inputs/tmp.txt")
    screen = np.chararray((20, 20), itemsize=1)
    screen[:] = b"."

    for line in lines:
        sensor, beacon = line.split(": ")
        xTmp, yTmp = sensor[10:].split(", ")
        sensor_x = int(xTmp[2:])
        sensor_y = int(yTmp[2:])
        xTmp, yTmp = beacon[21:].split(", ")
        beacon_x = int(xTmp[2:])
        beacon_y = int(yTmp[2:])

        manh_dist = manhatanDistance(
            (sensor_x, sensor_y), (beacon_x, beacon_y))
        for i in range(0, manh_dist + 1):
            y1 = sensor_y + i
            y2 = sensor_y - i
            for x in range(-(manh_dist - i) + sensor_x, manh_dist - i + 1 + sensor_x):
                if 0 <= x < len(screen[0]) and 0 <= y1 < len(screen):
                    screen[y1, x] = "#"
                if 0 <= x < len(screen[0]) and 0 <= y2 < len(screen):
                    screen[y2, x] = "#"

    pos = np.where(screen == b".")

    return 4000000 * pos[1][0] + pos[0][0]

# Prohibited
def part2():
    lines = readLines("inputs/input15.txt")
    pairs_temp = [tuple(map(lambda item: tuple(map(lambda x: int(x[2:]), item.replace(
        ",", "").split()[-2:])), line.split(": "))) for line in lines]
    pairs = [(sensor, beacon, abs(sensor[0] - beacon[0]) +
              abs(sensor[1] - beacon[1])) for sensor, beacon in pairs_temp]
    target_ys = 20 if pairs[0] == ((2, 18), (-2, 15)) else 4000000

    for target_y in range(target_ys + 1):
        x_ranges = []
        for sensor, _, distance in pairs:
            diff_x = distance - abs(target_y - sensor[1])
            if diff_x >= 0:
                x_ranges.append((sensor[0] - diff_x, sensor[0] + diff_x))

        x_ranges.sort()

        coverage = x_ranges[0]
        for i in range(1, len(x_ranges)):
            if x_ranges[i][0] <= coverage[1]:
                coverage = (coverage[0], max(coverage[1], x_ranges[i][1]))
            else:
                # print("position:", (coverage[1] + 1, target_y))
                return (coverage[1] + 1) * 4000000 + target_y

def main():
    numOfPos = part1()
    print("Number of positions where a beacon cannot be present in a row:")
    print(numOfPos)

    tuningFrequency = part2()
    print("Tuning frequency:")
    print(tuningFrequency)

if __name__ == "__main__":
    main()
