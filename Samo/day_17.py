import os
import numpy as np
from itertools import cycle


def read_jet_pattern(file_name: str) -> list:
    file = open(os.path.join(os.path.dirname(__file__), file_name), "r")
    jet_pattern = file.read()
    file.close()
    return jet_pattern


def check_rock_sides(next_pos: tuple, rock_shape: list, rock_tower: np.array) -> bool:
    """
    Checks the whole rock shape if there is any conflict with next movement.\n
    Returns True if rock can move to next_pos or false if it can't.
    """
    for rock_unit in rock_shape:
        new_y = next_pos[0] + rock_unit[0]
        new_x = next_pos[1] + rock_unit[1]

        # Out of bounds
        if new_y >= len(rock_tower) or new_y < 0:
            return False
        if new_x >= len(rock_tower[0]) or new_x < 0:
            return False

        # The is already a rock in this position
        if rock_tower[new_y, new_x] == b"#":
            return False

    return True


def part1() -> int:
    jet_pattern = list(read_jet_pattern("inputs/input17.txt"))
    rock_tower = np.chararray((2022 * 4, 7), itemsize=1)
    rock_tower[:] = b"."

    # Rock shapes
    rock0 = [(0, 0), (0, 1), (0, 2), (0, 3)]
    rock1 = [(0, 1), (-1, 0), (-1, 1), (-1, 2), (-2, 1)]
    rock2 = [(0, 0), (0, 1), (0, 2), (-1, 2), (-2, 2)]
    rock3 = [(0, 0), (-1, 0), (-2, 0), (-3, 0)]
    rock4 = [(0, 0), (0, 1), (-1, 0), (-1, 1)]

    rocks_cycle = cycle([rock0, rock1, rock2, rock3, rock4])
    rock_heights = cycle([1, 3, 3, 4, 2])
    jet_cycle = cycle(jet_pattern)
    tower_ix = len(rock_tower) - 1

    # Simulate all 2022 rocks falling
    for _ in range(2022):
        pos_ix = (tower_ix - 3, 2)
        rock_shape = next(rocks_cycle)

        while True:
            # Simulate jet move (left/right)
            next_x_pos = pos_ix[1] - \
                1 if next(jet_cycle) == "<" else pos_ix[1] + 1
            can_move = check_rock_sides(
                (pos_ix[0], next_x_pos), rock_shape, rock_tower)

            # Move left or right
            if can_move:
                pos_ix = (pos_ix[0], next_x_pos)
            # Else don't make a left/right move

            # Simulate falling
            can_move = check_rock_sides(
                (pos_ix[0] + 1, pos_ix[1]), rock_shape, rock_tower)

            if can_move:
                # Falls one unit down
                pos_ix = (pos_ix[0] + 1, pos_ix[1])
            else:
                # Rock stops falling
                break

        # Draw rock on rock_tower
        for x in rock_shape:
            rock_tower[pos_ix[0] + x[0], pos_ix[1] + x[1]] = b"#"

        # Update the tower index so it points to
        # the tallest rock
        next_height = next(rock_heights)
        if pos_ix[0] - next_height <= tower_ix:
            tower_ix = pos_ix[0] - next_height

    return len(rock_tower) - 1 - tower_ix


def part2() -> int:
    # We use jet index, rock type and the last 100 rows of rock tower to
    # store a state. When the state repeats, we can calculate the difference
    # of rocks fallen and the difference in height. Than we can calculate how
    # many times can this state repeat, so we do not have to simulate a lot of
    # falling rocks. We simulate what we have left and we add this calculated
    # height at the end.

    jet_pattern = list(read_jet_pattern("inputs/input17.txt"))
    rock_tower = np.chararray((1000000, 7), itemsize=1)
    rock_tower[:] = b"."

    # Rock shapes
    rock0 = [(0, 0), (0, 1), (0, 2), (0, 3)]
    rock1 = [(0, 1), (-1, 0), (-1, 1), (-1, 2), (-2, 1)]
    rock2 = [(0, 0), (0, 1), (0, 2), (-1, 2), (-2, 2)]
    rock3 = [(0, 0), (-1, 0), (-2, 0), (-3, 0)]
    rock4 = [(0, 0), (0, 1), (-1, 0), (-1, 1)]

    rocks = [rock0, rock1, rock2, rock3, rock4]
    rock_heights = [1, 3, 3, 4, 2]
    jet_ix = 0
    tower_ix = len(rock_tower) - 1
    states = {}

    # Simulate all 1000000000000 rocks falling
    pattern_found = False
    i = 0
    while i < 1000000000000:
        pos_ix = (tower_ix - 3, 2)
        rock_shape = rocks[i % 5]

        while True:
            # Simulate jet move (left/right)
            next_x_pos = pos_ix[1] - 1 if jet_pattern[jet_ix %
                                                      len(jet_pattern)] == "<" else pos_ix[1] + 1
            jet_ix = jet_ix + 1
            can_move = check_rock_sides(
                (pos_ix[0], next_x_pos), rock_shape, rock_tower)

            # Move left or right
            if can_move:
                pos_ix = (pos_ix[0], next_x_pos)
            # Else don't make a left/right move

            # Simulate falling
            can_move = check_rock_sides(
                (pos_ix[0] + 1, pos_ix[1]), rock_shape, rock_tower)

            if can_move:
                # Falls one unit down
                pos_ix = (pos_ix[0] + 1, pos_ix[1])
            else:
                # Rock stops falling
                break

        # Draw rock on rock_tower
        for x in rock_shape:
            rock_tower[pos_ix[0] + x[0], pos_ix[1] + x[1]] = b"#"

        # Update the tower index so it points to
        # the tallest rock
        next_height = rock_heights[i % 5]
        if pos_ix[0] - next_height <= tower_ix:
            tower_ix = pos_ix[0] - next_height

        # Generate a state
        pattern = (
            jet_ix % len(jet_pattern),                      # jet index
            i % 5,                                          # type of rock
            rock_tower[tower_ix:tower_ix+100, :].tobytes()  # upper 100 layers
        )

        # We found the same pattern. We have to calculate what is the height
        # difference and how many rocks have fallen betweeen those two same patterns.
        # Then we can calculate added height and skip many of the same repetitions.
        if not pattern_found and pattern in states:
            pattern_found = True
            height_diff = states[pattern][0] - tower_ix
            rocks_ix_diff = i - states[pattern][1]
            rocks_left = 1000000000000 - i
            # (rocks_left // rocks_ix_diff) ... number of patterns we can skip
            rocks_skip = (rocks_left // rocks_ix_diff) * rocks_ix_diff
            height_skip = (rocks_left // rocks_ix_diff) * height_diff
            i = i + rocks_skip

        # Store state in the dictionary
        states[pattern] = (tower_ix, i)

        i += 1

    # We add the height we skipped by calculating height of repeting pattern
    return len(rock_tower) - 1 - tower_ix + height_skip


def main():
    height_of_tower = part1()
    print("The height of the tower of 2022 rocks in units:")
    print(height_of_tower)

    height_of_tower_2 = part2()
    print("The height of the tower of 1000000000000 rocks in units:")
    print(height_of_tower_2)


if __name__ == "__main__":
    main()
