import os
import re
import numpy as np
from collections import deque


def read_lines(file_name: str) -> list:
    with open(os.path.join(os.path.dirname(__file__), file_name), "r") as file:
        lines = file.read().splitlines()
    return lines


def able_to_build(cost: tuple, ores: np.array) -> bool:
    for i in range(len(cost)):
        if cost[i] > ores[i]:
            return False
    return True


def calculate_quality_level_too_slow(blueprint: str, time: int) -> list:
    """
    First try of solving part1 puzzle but it is slower than the other solution.
    Still solves the part1 in couple of minutes.
    Some of the optimisation methods used in the function calculate_geodes_opened
    were also used in this function
    """
    id, instuctions = blueprint.split(": ")
    ore, clay, obsidian, geode = instuctions.split(". ")

    # Robot costs
    ore_cost = (int(re.findall("\d+", ore)[0]), 0, 0, 0)
    clay_cost = (int(re.findall("\d+", clay)[0]), 0, 0, 0)
    tmp = [int(i) for i in re.findall("\d+", obsidian)]
    obsidian_cost = (tmp[0], tmp[1], 0, 0)
    tmp = [int(i) for i in re.findall("\d+", geode)]
    geode_cost = (tmp[0], 0, tmp[1], 0)

    robot_costs = [ore_cost, clay_cost, obsidian_cost, geode_cost]

    # Maximum number of material we need to build a robot
    # Geodes are not used for building robots so we set it to infinity
    max_material_used_for_robot = [
        max([i[0] for i in robot_costs]),
        max([i[1] for i in robot_costs]),
        max([i[2] for i in robot_costs]),
        float("inf")]

    max_geodes = 0
    q = deque()
    # [Num of robots, Num of current ores, Time left]
    q.append([np.array([1, 0, 0, 0]), np.array([0, 0, 0, 0]), time])
    seen = set()
    while q:
        robots, ores, time = q.popleft()
        new_ores = np.add(robots, ores)  # Element wise numpy sum

        if (tuple(robots), tuple(ores)) in seen:
            continue
        seen.add((tuple(robots), tuple(ores)))

        if ores[-1] > max_geodes:
            max_geodes = ores[-1]

        if time == 0:
            continue

        for i in range(4):  # 4 robot costs
            cost = robot_costs[i]
            if (i == 3 and time <= 1) or (time <= 2 and i < 3):
                continue
            # For any resource R that's not geode: if you already have X robots creating resource R,
            # and no robot requires more than X of resource R to build, then you never need to build
            # another robot mining R anymore. This rule is correct since you can only build one robot
            # every minute. This rule prevents a lot of useless branching: it especially prevents you
            # from building ore robots when the time is almost up (which is a pretty useless thing to do).
            if robots[i] < max_material_used_for_robot[i] and able_to_build(cost, ores):
                new_robots = np.copy(robots)
                new_robots[i] += 1
                q.append((new_robots, np.subtract(new_ores, cost), time-1))

        # We didn't build any robots this round
        q.append(([np.copy(robots), np.copy(new_ores), time-1]))

    return max_geodes, int(id[10:])


def calculate_geodes_opened(blueprint: str, time: int) -> list:
    """
    Solution examines the search space with BFS algorithm, but we had to do
    some optimisations to improve the speed of solution.
    For optimisations we try to narrow the search space as much as possible.
    \n\n

    Optimizations(some optimizations were found on reddit - 
    https://www.reddit.com/r/adventofcode/comments/zpy5rm/2022_day_19_what_are_your_insights_and/):
    1. For any resource R that's not geode: if you already have X robots creating resource R,
    and no robot requires more than X of resource R to build, then you never need to build
    another robot mining R anymore. This rule is correct since you can only build one robot
    every minute. This rule prevents a lot of useless branching: it especially prevents you
    from building ore robots when the time is almost up (which is a pretty useless thing to do).

    2. (optimized 1.) Note that we can do a bit better: For any resource R that's not geode: 
    if you already have X robots creating resource R, a current stock of Y for that resource, 
    T minutes left, and no robot requires more than Z of resource R to build, and X * T+Y >= T * Z, 
    then you never need to build another robot mining R anymore.
    Build robot if:
    ore_robot * time + ore < time * max_ore_needed

    3. We store the states we have already seen in a set so we do not examines 
    same solutions multiple times.

    4. Nothing you build in the last minute will provide more resources and nothing
    you build in the 2nd-to-last minute will help us build more geode bots, so we
    stop expanding our search space at the end.

    5. Crediting the geodes the moment the geode bot was created (ie. a geode bot created
    with five minutes left was immediate +5 score), which meant I no longer had to track
    the count of geode bots at all and let me collapse some states together.
    """
    id, instuctions = blueprint.split(": ")
    ore, clay, obsidian, geode = instuctions.split(". ")

    # Robot costs
    # ore_r_ore means that for ore robot we need that much ore which is stored in this variable
    # clay_r_ore mean that for building a clay robot we need so much ore as stored in int
    ore_r_ore = int(re.findall("\d+", ore)[0])
    clay_r_ore = int(re.findall("\d+", clay)[0])
    obs_r_ore, obs_r_clay = [int(i) for i in re.findall("\d+", obsidian)]
    geode_r_ore, geode_r_obs = [int(i) for i in re.findall("\d+", geode)]

    max_ore_needed = max(ore_r_ore, clay_r_ore, obs_r_ore, geode_r_ore)
    max_clay_needed = obs_r_clay
    max_obs_needed = geode_r_obs

    max_geodes_mined = 0

    # BFS
    q = deque()
    # (ore robot, clay robot, obsidian robot, ore, clay, obsidian, geode, time)
    q.append((1, 0, 0, 0, 0, 0, 0, time))
    seen = set()
    while q:
        ore_r, clay_r, obs_r, ore, clay, obs, geode, time = q.popleft()

        max_geodes_mined = max(max_geodes_mined, geode)

        if time <= 0:
            continue

        if (ore_r, clay_r, obs_r, ore, clay, obs, geode) in seen:
            continue
        seen.add((ore_r, clay_r, obs_r, ore, clay, obs, geode))

        new_ore = ore + ore_r
        new_clay = clay + clay_r
        new_obs = obs + obs_r

        # Ore robot
        if ore_r * time + ore < max_ore_needed * time and ore >= ore_r_ore and time > 2:
            q.append((ore_r + 1, clay_r, obs_r,
                      new_ore - ore_r_ore, new_clay, new_obs, geode,
                      time - 1))

        # Clay robot
        if clay_r * time + clay < max_clay_needed * time and ore >= clay_r_ore and time > 2:
            q.append((ore_r, clay_r + 1, obs_r,
                      new_ore - clay_r_ore, new_clay, new_obs, geode,
                      time - 1))

        # Obsidian robot
        if obs_r * time + obs < max_obs_needed * time and ore >= obs_r_ore and clay >= obs_r_clay and time > 2:
            q.append((ore_r, clay_r, obs_r + 1,
                     new_ore - obs_r_ore, new_clay - obs_r_clay, new_obs, geode,
                     time - 1))

        # Geode robot
        if ore >= geode_r_ore and obs >= geode_r_obs and time > 1:
            q.append((ore_r, clay_r, obs_r,
                     new_ore - geode_r_ore, new_clay, new_obs - geode_r_obs, geode + time - 1,
                     time - 1))

        # No robot built
        q.append((ore_r, clay_r, obs_r,
                  new_ore, new_clay, new_obs, geode, time - 1))

    return max_geodes_mined, int(id[10:])


def part1() -> int:
    blueprints = read_lines("inputs/input19.txt")

    sum_of_quality_levels = 0
    for blueprint in blueprints:
        max_geodes, id = calculate_geodes_opened(blueprint, 24)
        sum_of_quality_levels += max_geodes * id

    return sum_of_quality_levels


def part2() -> int:
    blueprints = read_lines("inputs/input19.txt")

    b = min(3, len(blueprints))

    prod = 1
    for i in range(b):
        p, _ = calculate_geodes_opened(blueprints[i], 32)
        # print(p)
        prod *= p

    return prod


def main():
    print("Sum of quality level of all blueprints:")
    print(part1())

    print("Multipication of max geodes opened with first 3 blueprints:")
    print(part2())


if __name__ == "__main__":
    main()
