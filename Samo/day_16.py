import os
import copy
from collections import deque
from itertools import combinations


def read_lines(file_name: str) -> list:
    with open(os.path.join(os.path.dirname(__file__), file_name), "r") as file:
        lines = file.read().splitlines()
    return lines


def calculate_move_times(g: dict) -> dict:
    """
    Functions that calculates shortest paths between all of the nodes.
    We run BFS for all of the nodes and so we get all the shortest paths.\n
    Returns dictionary of shortest times between all pair nodes.
    """
    move_times = {}
    for v in g.keys():
        move_times_for_one = {}

        visited = set()
        visited.add(v)
        q = deque()
        q.append((v, 0))
        while q:
            valve, time = q.popleft()

            move_times_for_one[(v, valve)] = time

            for next_valve in g[valve]["neighbor_valves"]:
                if next_valve not in visited:
                    visited.add(next_valve)
                    q.append((next_valve, time + 1))

        move_times.update(move_times_for_one)

    return move_times


def part1() -> int:
    lines = read_lines("inputs/input16.txt")

    # Graph with all valves, their pressure flow rates and neighbor valves
    g = {}
    useful_valves = set()  # valves which have a flow rate higher than 0
    for line in lines:
        valve_and_rate, leads_to = line.split("; ")
        valve = valve_and_rate[6:8]
        flow_rate = int(valve_and_rate[23:])
        neighbor_valves = list(map(lambda x: x[-2:], leads_to.split(", ")))

        g[valve] = {
            "flow_rate": flow_rate,
            "neighbor_valves": neighbor_valves,
        }
        if flow_rate > 0:
            useful_valves.add(valve)

    move_times = calculate_move_times(g)
    max_pressure = 0

    # BFS with just the useful_valves, which have flow rate more than zero
    q = deque()
    # [valve, time_left, closed_valves_to_be_used, current_pressure]
    q.append(["AA", 30, copy.deepcopy(useful_valves), 0])
    while q:
        valve, time, closed_valves, pressure = q.popleft()

        if pressure > max_pressure:
            max_pressure = pressure

        if not closed_valves:  # If there are no more closed valves
            continue

        for next in closed_valves:
            # We subtract movement to valve and opening of the valve
            new_time = time - move_times[(valve, next)] - 1
            if new_time > 0:
                new_pressure = pressure + g[next]["flow_rate"] * new_time
                new_closed = copy.deepcopy(closed_valves)
                new_closed.remove(next)

                # Could speed up a bit by not adding solutins which can't reach max_pressure

                q.append([next, new_time, new_closed, new_pressure])

    return max_pressure


def part2() -> int:
    lines = read_lines("inputs/input16.txt")

    # Graph with all valves, their pressure flow rates and neighbor valves
    g = {}
    useful_valves = set()  # valves which have a flow rate higher than 0
    for line in lines:
        valve_and_rate, leads_to = line.split("; ")
        valve = valve_and_rate[6:8]
        flow_rate = int(valve_and_rate[23:])
        neighbor_valves = list(map(lambda x: x[-2:], leads_to.split(", ")))

        g[valve] = {
            "flow_rate": flow_rate,
            "neighbor_valves": neighbor_valves,
        }
        if flow_rate > 0:
            useful_valves.add(valve)

    move_times = calculate_move_times(g)
    max_pressure = 0

    # BFS with just the useful_valves, which have flow rate more than zero
    q = deque()
    # [[(valve, time), (valve, time)] closed_valves_to_be_used, current_pressure]
    q.append([[("AA", 26), ("AA", 26)], copy.deepcopy(useful_valves), 0])
    while q:
        positions, closed_valves, pressure = q.popleft()
        # We use only one valve and time in loop
        valve, time = positions.pop(0)

        if pressure > max_pressure:
            max_pressure = pressure

        if not closed_valves:  # If there are no more closed valves
            continue

        for next in closed_valves:
            # We subtract movement to valve and opening of the valve
            new_time = time - move_times[(valve, next)] - 1
            if new_time > 0:
                new_pressure = pressure + g[next]["flow_rate"] * new_time
                new_closed = copy.deepcopy(closed_valves)
                new_closed.remove(next)

                # We don't add solutions which cannot reach max_pressure
                remaining_pressure = sum(
                    [new_time * g[v]["flow_rate"] for v in closed_valves])
                if new_pressure + remaining_pressure < max_pressure:
                    continue

                q.append([positions + [(next, new_time)],
                         new_closed, new_pressure])

    return max_pressure


def part2_too_slow() -> int:
    lines = read_lines("inputs/tmp.txt")

    # Graph with all valves, their pressure flow rates and neighbor valves
    g = {}
    useful_valves = set()  # valves which have a flow rate higher than 0
    for line in lines:
        valve_and_rate, leads_to = line.split("; ")
        valve = valve_and_rate[6:8]
        flow_rate = int(valve_and_rate[23:])
        neighbor_valves = list(map(lambda x: x[-2:], leads_to.split(", ")))

        g[valve] = {
            "flow_rate": flow_rate,
            "neighbor_valves": neighbor_valves,
        }
        if flow_rate > 0:
            useful_valves.add(valve)

    move_times = calculate_move_times(g)
    max_pressure = 0

    # BFS with just the useful_valves, which have flow rate more than zero
    q = deque()
    # [me_valve, me_time_left, elephant_valve, elephant_time_left, closed_valves_to_be_used, current_pressure]
    q.append(["AA", 26, "AA", 26, copy.deepcopy(useful_valves), 0])
    while q:
        valve_1, time_1, valve_2, time_2, closed_valves, pressure = q.popleft()

        if pressure > max_pressure:
            max_pressure = pressure

        if not closed_valves:  # If there are no more closed valves
            continue

        # Try all Variation without Repetition
        # [A, B, C] --combinations-> [AB, AC, BC] --switch places-> [AB, AC, BC, BA, CA, CB]
        for n1, n2 in combinations(closed_valves, 2):
            # We subtract movement to valve and opening of the valve to get new time
            new_time_1 = time_1 - move_times[(valve_1, n1)] - 1
            new_time_2 = time_2 - move_times[(valve_2, n2)] - 1

            if new_time_1 > 0 or new_time_2 > 0:
                new_pressure = pressure
                new_closed = copy.deepcopy(closed_valves)

                if new_time_1 > 0:
                    new_pressure += g[n1]["flow_rate"] * new_time_1
                    new_closed.remove(n1)
                if new_time_2 > 0:
                    new_pressure += g[n2]["flow_rate"] * new_time_2
                    new_closed.remove(n2)

                q.append([n1, new_time_1, n2, new_time_2,
                         new_closed, new_pressure])

            tmp = n1
            n1 = n2
            n2 = tmp

            new_time_1 = time_1 - move_times[(valve_1, n1)] - 1
            new_time_2 = time_2 - move_times[(valve_2, n2)] - 1

            if new_time_1 > 0 or new_time_2 > 0:
                new_pressure = pressure
                new_closed = copy.deepcopy(closed_valves)

                if new_time_1 > 0:
                    new_pressure += g[n1]["flow_rate"] * new_time_1
                    new_closed.remove(n1)
                if new_time_2 > 0:
                    new_pressure += g[n2]["flow_rate"] * new_time_2
                    new_closed.remove(n2)

                q.append([n1, new_time_1, n2, new_time_2,
                         new_closed, new_pressure])

    return max_pressure


def main():
    print("The most pressure released in 30 minutes:")
    print(part1())

    print("The most pressure released in 26 minutes with the help of one elephant:")
    print(part2())


if __name__ == "__main__":
    main()
