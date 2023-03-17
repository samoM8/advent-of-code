import os
from collections import deque


def read_lines(file_name: str) -> list:
    with open(os.path.join(os.path.dirname(__file__), file_name), "r") as file:
        lines = file.read().splitlines()
    return lines


def move_blizzards(up_blizzards, down_blizzards, left_blizzards, right_blizzards, y_len, x_len):
    """
    Simulate blizzard movement across the map.
    Function returns new sets of blizzards' positions.
    """
    new_up_tmp_blizzards = set()
    for up in up_blizzards:
        if up[0] == 0:
            new_up_tmp_blizzards.add((y_len - 1, up[1]))
        else:
            new_up_tmp_blizzards.add((up[0] - 1, up[1]))
    up_blizzards = new_up_tmp_blizzards

    new_down_tmp_blizzards = set()
    for down in down_blizzards:
        if down[0] == y_len - 1:
            new_down_tmp_blizzards.add((0, down[1]))
        else:
            new_down_tmp_blizzards.add((down[0] + 1, down[1]))
    down_blizzards = new_down_tmp_blizzards

    new_left_tmp_blizzards = set()
    for left in left_blizzards:
        if left[1] == 0:
            new_left_tmp_blizzards.add((left[0], x_len - 1))
        else:
            new_left_tmp_blizzards.add((left[0], left[1] - 1))
    left_blizzards = new_left_tmp_blizzards

    new_right_tmp_blizzards = set()
    for right in right_blizzards:
        if right[1] == x_len - 1:
            new_right_tmp_blizzards.add((right[0], 0))
        else:
            new_right_tmp_blizzards.add((right[0], right[1] + 1))
    right_blizzards = new_right_tmp_blizzards

    return up_blizzards, down_blizzards, left_blizzards, right_blizzards


def path_to_goal(start, end, y_len, x_len, up_blizzards, down_blizzards, left_blizzards, right_blizzards):
    """
    Some type of breadth first search\n
    We go from start to the end through the maze of blizzards and also we need to consider movement of blizzards.\n
    Functions returns the fewest number of minutes to reach the goal.
    """

    vertices = deque()
    vertices.append((start, 1))
    previous_time = 0
    while vertices:
        vertex = vertices.popleft()
        pos = vertex[0]

        # Blizzard movement if we already did all moves in a single minute
        if previous_time < vertex[1]:
            previous_time = vertex[1]

            up_blizzards, down_blizzards, left_blizzards, right_blizzards = move_blizzards(
                up_blizzards, down_blizzards, left_blizzards, right_blizzards, y_len, x_len)

        # Move position
        for move in [(0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_pos = (pos[0] + move[0], pos[1] + move[1])

            # We found the end position so we return time spent on path.
            if next_pos == end:
                return vertex[1], up_blizzards, down_blizzards, left_blizzards, right_blizzards

            # Position is out of bounds (exception is start position).
            if (next_pos[0] < 0 or next_pos[0] >= y_len or
                    next_pos[1] < 0 or next_pos[1] >= x_len) and next_pos != start:
                continue

            # We can move to this position because there are no blizzards.
            # We do not move to the position if the same position is already in queue
            # Example ((1, 2), 3) -> ((2, 2), 4) gives us the same next position as
            #         ((3, 2), 3) -> ((2, 2), 4) so we do not add it twice
            if next_pos not in up_blizzards and next_pos not in down_blizzards and \
                    next_pos not in left_blizzards and next_pos not in right_blizzards and \
                    ((next_pos, vertex[1] + 1) not in vertices):
                vertices.append((next_pos, vertex[1] + 1))

    # No path found
    return -1


def part1() -> int:
    lines = read_lines("inputs/input24.txt")

    start = (-1, lines.pop(0).index(".") - 1)
    end = (len(lines) - 1, lines.pop(len(lines) - 1).index(".") - 1)

    y_len = len(lines)
    x_len = len(lines[0]) - 2

    # Get blizzard indices and put them in set.
    # We subtract 1 from x because we will cut off the wall.
    up_blizzards = set()
    down_blizzards = set()
    left_blizzards = set()
    right_blizzards = set()
    for y, line in enumerate(lines):
        for x, blizz in enumerate(line):
            if blizz == "^":
                up_blizzards.add((y, x-1))
            elif blizz == "v":
                down_blizzards.add((y, x-1))
            elif blizz == "<":
                left_blizzards.add((y, x-1))
            elif blizz == ">":
                right_blizzards.add((y, x-1))

    fewest_minutes_to_goal = path_to_goal(
        start, end, y_len, x_len, up_blizzards, down_blizzards, left_blizzards, right_blizzards)[0]

    return fewest_minutes_to_goal


def part2() -> int:
    lines = read_lines("inputs/input24.txt")

    start = (-1, lines.pop(0).index(".") - 1)
    end = (len(lines) - 1, lines.pop(len(lines) - 1).index(".") - 1)

    y_len = len(lines)
    x_len = len(lines[0]) - 2

    up_blizzards = set()
    down_blizzards = set()
    left_blizzards = set()
    right_blizzards = set()
    for y, line in enumerate(lines):
        for x, blizz in enumerate(line):
            if blizz == "^":
                up_blizzards.add((y, x-1))
            elif blizz == "v":
                down_blizzards.add((y, x-1))
            elif blizz == "<":
                left_blizzards.add((y, x-1))
            elif blizz == ">":
                right_blizzards.add((y, x-1))

    min_to_goal, up_blizzards, down_blizzards, left_blizzards, right_blizzards = path_to_goal(
        start, end, y_len, x_len, up_blizzards, down_blizzards, left_blizzards, right_blizzards
    )

    min_back_to_start, up_blizzards, down_blizzards, left_blizzards, right_blizzards = path_to_goal(
        end, start, y_len, x_len, up_blizzards, down_blizzards, left_blizzards, right_blizzards
    )

    min_to_goal_again, up_blizzards, down_blizzards, left_blizzards, right_blizzards = path_to_goal(
        start, end, y_len, x_len, up_blizzards, down_blizzards, left_blizzards, right_blizzards
    )

    return min_to_goal + min_back_to_start + min_to_goal_again


def main():
    print("Fewest number of minutes to reach the goal:")
    print(part1())

    print("Fewest number of minutes to reach the goal, go back to start and reach the goal again:")
    print(part2())


if __name__ == "__main__":
    main()
