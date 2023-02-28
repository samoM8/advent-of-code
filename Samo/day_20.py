import os
import copy


def readLines(fileName: str) -> list:
    file = open(os.path.join(os.path.dirname(__file__), fileName), "r")
    lines = file.read().splitlines()
    file.close()
    return lines


def part1() -> int:
    lines = readLines("inputs/input20.txt")

    starting_sequence = list()
    starting_zero_ix = 0
    i = 0
    for line in lines:
        # We alse put index next to number so we get unique pairs
        starting_sequence.append((i, int(line)))
        if int(line) == 0:
            starting_zero_ix = i
        i += 1

    mixing = copy.deepcopy(starting_sequence)
    for pair in starting_sequence:
        # Get current number and index of number
        ix = mixing.index(pair)
        n = pair[1]

        # Calculate new index
        # We use (len-1) because we will remove number
        # from the list and then add it again
        new_ix = (ix + n) % (len(mixing) - 1)

        # Remove the number at current index
        mixing.pop(ix)
        # Add the number on new index
        mixing.insert(new_ix, pair)

    zero_ix = mixing.index((starting_zero_ix, 0))
    first_num = mixing[(zero_ix + 1000) % len(mixing)][1]
    second_num = mixing[(zero_ix + 2000) % len(mixing)][1]
    third_num = mixing[(zero_ix + 3000) % len(mixing)][1]

    return first_num + second_num + third_num


def part2() -> int:
    lines = readLines("inputs/input20.txt")

    starting_sequence = list()
    starting_zero_ix = 0
    i = 0
    for line in lines:
        # We alse put index next to number so we get unique pairs
        starting_sequence.append((i, int(line) * 811589153))
        if int(line) == 0:
            starting_zero_ix = i
        i += 1

    mixing = copy.deepcopy(starting_sequence)
    for _ in range(10):
        for pair in starting_sequence:
            # Get current number and index of number
            ix = mixing.index(pair)
            n = pair[1]

            # Calculate new index
            # We use (len-1) because we will remove number
            # from the list and then add it again
            new_ix = (ix + n) % (len(mixing) - 1)

            # Remove the number at current index
            mixing.pop(ix)
            # Add the number on new index
            mixing.insert(new_ix, pair)

    zero_ix = mixing.index((starting_zero_ix, 0))
    first_num = mixing[(zero_ix + 1000) % len(mixing)][1]
    second_num = mixing[(zero_ix + 2000) % len(mixing)][1]
    third_num = mixing[(zero_ix + 3000) % len(mixing)][1]

    return first_num + second_num + third_num


def main():
    print("Sum of the three numbers that form the grove coordinates:")
    print(part1())

    print("Sum of the three numbers that form the grove coordinates decrypted:")
    print(part2())


if __name__ == "__main__":
    main()
