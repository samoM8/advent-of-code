import os
import numpy as np
import re


def readLines(file_name: str) -> list:
    with open(os.path.join(os.path.dirname(__file__), file_name), "r") as file:
        board, moves = file.read().split("\n\n")
    return board, moves


def printBoard(b: np.array) -> None:
    for line in b:
        for dot in line:
            if dot:
                print(dot.decode("utf-8"), end="")
            else:
                print(" ", end="")
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


def part2() -> int:
    board_lines, moves = readLines("inputs/tmp.txt")

    return -1


def main():
    print("Final password:")
    print(part1())


if __name__ == "__main__":
    main()
