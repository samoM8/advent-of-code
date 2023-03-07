import os
from collections import deque


def readLines(fileName: str) -> list:
    with open(os.path.join(os.path.dirname(__file__), fileName), "r") as file:
        lines = file.read().splitlines()
    return lines


def part1() -> int:
    lines = readLines("inputs/input21.txt")

    monkey_nums = {}  # Number monkey yelled
    monkey_operations = deque()  # Operation which have not been calculated yet
    for line in lines:
        if len(line) == 17:
            monkey_operations.append(line)
        else:
            name, num = line.split(": ")
            monkey_nums[name] = int(num)

    while monkey_operations:
        operation = monkey_operations.popleft()
        monkey_res, math = operation.split(": ")
        monkey_1, operator, monkey_2 = math.split(" ")

        # Monkey can't calculate his number yet because it depens on monkeys
        # which haven't yelled their number.
        if monkey_1 not in monkey_nums or monkey_2 not in monkey_nums:
            monkey_operations.append(operation)
            continue

        # Calculate which number monkey yelled
        if operator == "+":
            monkey_nums[monkey_res] = monkey_nums[monkey_1] + \
                monkey_nums[monkey_2]
        elif operator == "-":
            monkey_nums[monkey_res] = monkey_nums[monkey_1] - \
                monkey_nums[monkey_2]
        elif operator == "*":
            monkey_nums[monkey_res] = monkey_nums[monkey_1] * \
                monkey_nums[monkey_2]
        elif operator == "/":
            monkey_nums[monkey_res] = monkey_nums[monkey_1] // \
                monkey_nums[monkey_2]

    return monkey_nums["root"]


def part2() -> int:
    lines = readLines("inputs/input21.txt")

    monkey_nums = {}  # Number monkey yelled
    monkey_operations = deque()  # Operation which have not been calculated yet
    for line in lines:
        # Store childs of root
        if line[:4] == "root":
            _, root_math = line.split(": ")
            child_1, _, child_2 = root_math.split(" ")

        if len(line) == 17:
            monkey_operations.append(line)
        else:
            if line[:4] == "humn":  # Skip this monkey's number
                continue
            name, num = line.split(": ")
            monkey_nums[name] = int(num)

    # While no child of root yelled a number.
    # Same as part1 but I stop calculation when I have 1 child of root.
    while child_1 not in monkey_nums and child_2 not in monkey_nums:
        operation = monkey_operations.popleft()
        monkey_res, math = operation.split(": ")
        monkey_1, operator, monkey_2 = math.split(" ")

        # Monkey can't calculate his number yet because it depens on monkeys
        # which haven't yelled their number.
        if monkey_1 not in monkey_nums or monkey_2 not in monkey_nums:
            monkey_operations.append(operation)
            continue

        # Calculate which number monkey yelled
        if operator == "+":
            monkey_nums[monkey_res] = monkey_nums[monkey_1] + \
                monkey_nums[monkey_2]
        elif operator == "-":
            monkey_nums[monkey_res] = monkey_nums[monkey_1] - \
                monkey_nums[monkey_2]
        elif operator == "*":
            monkey_nums[monkey_res] = monkey_nums[monkey_1] * \
                monkey_nums[monkey_2]
        elif operator == "/":
            monkey_nums[monkey_res] = monkey_nums[monkey_1] // \
                monkey_nums[monkey_2]

    # Set the child to the same as other child because at root
    # the childs must have the same number.
    if child_1 in monkey_nums:
        monkey_nums[child_2] = monkey_nums[child_1]
    else:
        monkey_nums[child_1] = monkey_nums[child_2]

    # Do another calculation loop until we have the monkey humn's number.
    # Here there is also on option that we have the result and one of the
    # terms of math equation, so we have to calculate the other term.
    while "humn" not in monkey_nums:
        operation = monkey_operations.popleft()
        monkey_res, math = operation.split(": ")
        monkey_1, operator, monkey_2 = math.split(" ")

        if monkey_res in monkey_nums and monkey_1 in monkey_nums:
            # We have result and term 1 and we calculate term 2
            if operator == "+":
                monkey_nums[monkey_2] = monkey_nums[monkey_res] - \
                    monkey_nums[monkey_1]
            elif operator == "-":
                monkey_nums[monkey_2] = monkey_nums[monkey_1] - \
                    monkey_nums[monkey_res]
            elif operator == "*":
                monkey_nums[monkey_2] = monkey_nums[monkey_res] // \
                    monkey_nums[monkey_1]
            elif operator == "/":
                monkey_nums[monkey_2] = monkey_nums[monkey_1] // \
                    monkey_nums[monkey_res]
        elif monkey_res in monkey_nums and monkey_2 in monkey_nums:
            # We have result and term 2 and we calculate term 1
            if operator == "+":
                monkey_nums[monkey_1] = monkey_nums[monkey_res] - \
                    monkey_nums[monkey_2]
            elif operator == "-":
                monkey_nums[monkey_1] = monkey_nums[monkey_res] + \
                    monkey_nums[monkey_2]
            elif operator == "*":
                monkey_nums[monkey_1] = monkey_nums[monkey_res] // \
                    monkey_nums[monkey_2]
            elif operator == "/":
                monkey_nums[monkey_1] = monkey_nums[monkey_res] * \
                    monkey_nums[monkey_2]
        elif monkey_1 in monkey_nums and monkey_2 in monkey_nums:
            # We have term 1 and term 2 and we calculate result
            if operator == "+":
                monkey_nums[monkey_res] = monkey_nums[monkey_1] + \
                    monkey_nums[monkey_2]
            elif operator == "-":
                monkey_nums[monkey_res] = monkey_nums[monkey_1] - \
                    monkey_nums[monkey_2]
            elif operator == "*":
                monkey_nums[monkey_res] = monkey_nums[monkey_1] * \
                    monkey_nums[monkey_2]
            elif operator == "/":
                monkey_nums[monkey_res] = monkey_nums[monkey_1] // \
                    monkey_nums[monkey_2]
        else:  # Else just check the next operation
            monkey_operations.append(operation)
            continue

    return monkey_nums["humn"]


def main():
    print("Root monkey yells:")
    print(part1())

    print("Number I yell to pass root's equality test:")
    print(part2())


if __name__ == "__main__":
    main()
