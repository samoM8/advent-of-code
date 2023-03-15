import os
from collections import deque


def read_lines(file_name: str) -> list:
    with open(os.path.join(os.path.dirname(__file__), file_name), "r") as file:
        lines = file.read().splitlines()
    return lines


def eight_directions_empty(elf_pos: tuple, elf_positions: set) -> bool:
    """
    Returns True if all elements neighbor elements are not in elf_positions
    Otherwise returns False
    """
    for dir in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, 1), (1, -1), (-1, -1)]:
        if (elf_pos[0] + dir[0], elf_pos[1] + dir[1]) in elf_positions:
            return False
    return True


def check_positions(to_check: list, elf_positions: set) -> bool:
    """
    Returns True if all elements in to_check are not in elf_positions
    Otherwise returns False
    """
    for pos in to_check:
        if pos in elf_positions:
            return False
    return True


def part1() -> int:
    lines = read_lines("inputs/input23.txt")

    # Directions of movement (north, south, west, east)
    # and also the positions we have to check to make a move.
    directions = deque([
        [(-1, 0), (-1, 1), (-1, -1)],
        [(1, 0), (1, 1), (1, -1)],
        [(0, -1), (1, -1), (-1, -1)],
        [(0, 1), (1, 1), (-1, 1)]
    ])

    # Initial elf positions
    elf_positions = set()
    for i, line in enumerate(lines):
        for j, position in enumerate(line):
            if position == "#":
                elf_positions.add((i, j))

    # Simulate moves for 10 rounds
    for i in range(10):
        prev_new_pos = {}
        new_prev_pos = {}
        for elf_pos in elf_positions:
            if eight_directions_empty(elf_pos, elf_positions):
                # This elf does not move because he has no neighbors
                continue

            for check in directions:
                check_pos = [(elf_pos[0] + dir[0], elf_pos[1] + dir[1])
                             for dir in check]  # positions to check
                new_pos = check_pos[0]

                # If elf can propose a move
                if check_positions(check_pos, elf_positions):
                    # Check if any other elf wants to move in this position
                    if new_pos in new_prev_pos:
                        # We found the other elf so we remove his move to new position
                        if new_prev_pos[new_pos] in prev_new_pos:
                            del prev_new_pos[new_prev_pos[new_pos]]
                    else:
                        # Position is empty, elf can make a move
                        prev_new_pos[elf_pos] = new_pos
                        new_prev_pos[new_pos] = elf_pos

                    break

        for prev_pos in prev_new_pos:
            elf_positions.remove(prev_pos)
            elf_positions.add(prev_new_pos[prev_pos])

        directions.rotate(-1)

    max_y = max(elf_positions, key=lambda i: i[0])[0]
    min_y = min(elf_positions, key=lambda i: i[0])[0]
    max_x = max(elf_positions, key=lambda i: i[1])[1]
    min_x = min(elf_positions, key=lambda i: i[1])[1]

    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(elf_positions)


def part2() -> int:
    lines = read_lines("inputs/input23.txt")

    # Directions of movement (north, south, west, east)
    # and also the positions we have to check to make a move
    directions = deque([
        [(-1, 0), (-1, 1), (-1, -1)],
        [(1, 0), (1, 1), (1, -1)],
        [(0, -1), (1, -1), (-1, -1)],
        [(0, 1), (1, 1), (-1, 1)]
    ])

    # Initial elf positions
    elf_positions = set()
    for i, line in enumerate(lines):
        for j, position in enumerate(line):
            if position == "#":
                elf_positions.add((i, j))

    rounds = 1
    # Loop while at least one move is made
    while True:
        prev_new_pos = {}
        new_prev_pos = {}
        for elf_pos in elf_positions:
            if eight_directions_empty(elf_pos, elf_positions):
                # This elf does not move because he has no neighbors
                continue

            for check in directions:
                check_pos = [(elf_pos[0] + dir[0], elf_pos[1] + dir[1])
                             for dir in check]  # positions to check
                new_pos = check_pos[0]

                # If elf can propose a move
                if check_positions(check_pos, elf_positions):
                    # Check if any other elf wants to move in this position
                    if new_pos in new_prev_pos:
                        # We found the other elf so we remove his move to new position
                        if new_prev_pos[new_pos] in prev_new_pos:
                            del prev_new_pos[new_prev_pos[new_pos]]
                    else:
                        # Position is empty, elf can make a move
                        prev_new_pos[elf_pos] = new_pos
                        new_prev_pos[new_pos] = elf_pos

                    break

        for prev_pos in prev_new_pos:
            elf_positions.remove(prev_pos)
            elf_positions.add(prev_new_pos[prev_pos])

        directions.rotate(-1)

        # No moves were made because all elves have zero neighbors
        if not prev_new_pos:
            break
        rounds = rounds + 1

    return rounds


def main():
    print("Empty ground tiles the rectangle contain:")
    print(part1())

    print("Round when no elf moves:")
    print(part2())


if __name__ == "__main__":
    main()
