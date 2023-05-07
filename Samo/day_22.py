import os
import numpy as np
import re
from dataclasses import dataclass
from typing import Optional


def readLines(file_name: str) -> list:
    with open(os.path.join(os.path.dirname(__file__), file_name), "r") as file:
        board, moves = file.read().split("\n\n")
    return board, moves


def printBoard(b: np.array) -> None:
    for line in b:
        for dot in line:
            print(dot, end="")
        print()


MOVES = {
    0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)
}


def part1() -> int:
    board_str, moves = readLines("inputs/input22.txt")
    board_lines = board_str.split("\n")

    max_len = len(max(board_lines, key=len))  # Length of board in x direction
    board = np.empty((len(board_lines), max_len), dtype=str)
    board[:] = " "

    # Initiate the board
    for ix, board_line in enumerate(board_lines):
        board[ix, 0:len(board_line)] = list(board_line)

    steps = re.split(r"L|R", moves)
    turns = re.split(r"\d+", moves)
    turns.pop(0)

    facing = 0
    pos = np.array([0, board_lines[0].index(".")])

    for num, turn in zip(steps, turns):
        # Move in steps
        for _ in range(int(num)):
            next_step = pos + MOVES[facing]
            # We skip empty space if there are any
            while True:
                # Check if we are out of bounds and move to other side
                if next_step[0] < 0:
                    next_step[0] = len(board) - 1
                elif next_step[0] >= len(board):
                    next_step[0] = 0
                elif next_step[1] < 0:
                    next_step[1] = len(board[0]) - 1
                elif next_step[1] >= len(board[0]):
                    next_step[1] = 0

                if board[next_step[0], next_step[1]] == "#" or \
                        board[next_step[0], next_step[1]] == ".":
                    break

                next_step = next_step + MOVES[facing]

            # If there is a wall we can not make the step so we stop
            if board[next_step[0], next_step[1]] == "#":
                break
            # If there is empty path we make a step and continue
            if board[next_step[0], next_step[1]] == ".":
                pos = next_step

        # Turn clockwise if R or counterclockwise if L
        if turn == "R":
            facing = (facing + 1) % 4
        elif turn == "L":
            facing = (facing - 1) % 4

    return 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + facing


@dataclass
class Tile:
    x: int
    y: int
    wall: bool

    # tuple { neighbor, facing direction }
    left: Optional[tuple["Tile", int]] = None
    right: Optional[tuple["Tile", int]] = None
    up: Optional[tuple["Tile", int]] = None
    down: Optional[tuple["Tile", int]] = None

    def get_neighbor(self, facing: int) -> Optional[tuple["Tile", int]]:
        if facing == 0:
            return self.right
        elif facing == 1:
            return self.down
        elif facing == 2:
            return self.left
        else:
            return self.up

def part2() -> int:
    board, moves = readLines("inputs/input22.txt")

    tiles: dict[tuple[int, int], Tile] = {}
    current_tile = None
    facing = 0

    # Set up tiles
    for y, line in enumerate(board.splitlines()):
        for x, ch in enumerate(line):
            if ch == " ":
                continue

            tile = Tile(x + 1, y + 1, ch == "#")

            tiles[(x + 1, y + 1)] = tile
            if current_tile is None:
                current_tile = tile

    # Set up neighbors for all tiles
    for tile in tiles.values():
        if (tile.x - 1, tile.y) in tiles:
            tile.left = tiles[(tile.x - 1, tile.y)], -1
        else:
            # if tile.y in range(1, 5):
            #     tile.left = tiles[(8 - tile.y + 4, 5)], 1
            # elif tile.y in range(5, 9):
            #     tile.left = tiles[(16 - tile.y + 5, 12)], 3
            # else:
            #     tile.left = tiles[(8 - tile.y + 9, 8)], 3
            if tile.y in range(1, 51):
                tile.left = tiles[(1, 51 - tile.y + 100)], 0
            elif tile.y in range(51, 101):
                tile.left = tiles[(tile.y - 50, 101)], 1
            elif tile.y in range(101, 151):
                tile.left = tiles[(51, 151 - tile.y)], 0
            else:
                tile.left = tiles[(tile.y - 100, 1)], 1

        if (tile.x + 1, tile.y) in tiles:
            tile.right = tiles[(tile.x + 1, tile.y)], -1
        else:
            # if tile.y in range(1, 5):
            #     tile.right = tiles[(16, 5 - tile.y + 8)], 2
            # elif tile.y in range(5, 9):
            #     tile.right = tiles[(8 - tile.y + 13, 9)], 1
            # else:
            #     tile.right = tiles[(12, 13 - tile.y)], 2
            if tile.y in range(1, 51):
                tile.right = tiles[(100, 51 - tile.y + 100)], 2
            elif tile.y in range(51, 101):
                tile.right = tiles[(tile.y + 50, 50)], 3
            elif tile.y in range(101, 151):
                tile.right = tiles[(150, 151 - tile.y)], 2
            else:
                tile.right = tiles[(tile.y - 100, 150)], 3

        if (tile.x, tile.y - 1) in tiles:
            tile.up = tiles[(tile.x, tile.y - 1)], -1
        else:
            # if tile.x in range(1, 5):
            #     tile.up = tiles[(5 - tile.x + 8, 1)], 1
            # elif tile.x in range(5, 9):
            #     tile.up = tiles[(9, tile.x - 4)], 0
            # elif tile.x in range(9, 13):
            #     tile.up = tiles[(tile.x - 8, 5)], 1
            # else:
            #     tile.up = tiles[(12, 17 - tile.x + 4)], 2
            if tile.x in range(1, 51):
                tile.up = tiles[(51, tile.x + 50)], 0
            elif tile.x in range(51, 101):
                tile.up = tiles[(1, tile.x + 100)], 0
            else:
                tile.up = tiles[(tile.x - 100, 200)], -1

        if (tile.x, tile.y + 1) in tiles:
            tile.down = tiles[(tile.x, tile.y + 1)], -1
        else:
            # if tile.x in range(1, 5):
            #     tile.down = tiles[(5 - tile.x + 8, 12)], 3
            # elif tile.x in range(5, 9):
            #     tile.down = tiles[(9, 9 - tile.x + 8)], 0
            # elif tile.x in range(9, 13):
            #     tile.down = tiles[(13 - tile.x, 8)], 3
            # else:
            #     tile.down = tiles[(1, 17 - tile.x + 4)], 0
            if tile.x in range(1, 51):
                tile.down = tiles[(tile.x + 100, 1)], -1
            elif tile.x in range(51, 101):
                tile.down = tiles[(50, tile.x + 100)], 2
            else:
                tile.down = tiles[(100, tile.x - 50)], 2

    # Simulate all the moves
    for command in re.findall(r"(\d+|[A-Z])", moves.strip()):
        if command.isdigit():
            for _ in range(int(command)):
                neighbor = current_tile.get_neighbor(facing)
                if neighbor is None:
                    break

                next_tile, next_facing = neighbor
                if next_tile.wall:
                    break

                current_tile = next_tile
                if next_facing > -1:
                    facing = next_facing
        elif command == "R":
            facing = (facing + 1) % 4
        else:
            facing = (facing - 1) % 4

    return current_tile.y * 1000 + current_tile.x * 4 + facing

def main():
    print("Final password part 1:")
    print(part1())

    print("Final password part 2:")
    print(part2())


if __name__ == "__main__":
    main()
