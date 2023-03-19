import os


def read_lines(file_name: str) -> list:
    with open(os.path.join(os.path.dirname(__file__), file_name), "r") as file:
        lines = file.read().splitlines()
    return lines


def convert_snafu_to_decimal(snafu_num: str) -> int:
    decimal_num = 0
    power = len(snafu_num) - 1
    for snafu_digit in snafu_num:
        if snafu_digit == "=":
            decimal_num = decimal_num + pow(5, power) * -2
        elif snafu_digit == "-":
            decimal_num = decimal_num + pow(5, power) * -1
        else:  # Snafu digit is 0, 1 or 2
            decimal_num = decimal_num + pow(5, power) * int(snafu_digit)

        power -= 1

    return decimal_num


def convert_decimal_to_snafu(decimal_num: int) -> str:
    snafu_num = ""
    while decimal_num > 0:
        remainder = decimal_num % 5

        if remainder == 3:
            snafu_num = str("=") + snafu_num
            decimal_num += 5
        elif remainder == 4:
            snafu_num = str("-") + snafu_num
            decimal_num += 5
        else:  # Remainder is 0, 1 or 2
            snafu_num = str(remainder) + snafu_num

        decimal_num //= 5

    return snafu_num


def part1() -> int:
    lines = read_lines("inputs/input25.txt")

    sum = 0
    for snafu_num in lines:
        sum += convert_snafu_to_decimal(snafu_num)

    return convert_decimal_to_snafu(sum)


def main():
    print("SNAFU number supplied to Bob's console:")
    print(part1())


if __name__ == "__main__":
    main()
