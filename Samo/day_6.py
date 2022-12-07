import os

def readLine(fileName: str) -> str:
    file = open(os.path.join(os.path.dirname(__file__), fileName), "r")
    signal = file.read()
    file.close()
    return signal

def part1() -> int:
    signal = readLine("inputs/input6.txt")
    for i in range(len(signal) - 3):
        # get four characters
        fourCharacterMarker = signal[i:i+4]
        # check if all the characters are different
        if len(fourCharacterMarker) == len(set(fourCharacterMarker)):
            return i + 4
    
    return -1

def part2() -> int:
    signal = readLine("inputs/input6.txt")
    for i in range(len(signal) - 13):
        # get fourteen characters
        fourteenCharacterMarker = signal[i:i+14]
        # check if all the characters are different
        if len(fourteenCharacterMarker) == len(set(fourteenCharacterMarker)):
            return i + 14
    
    return -1

def main():
    startOfPacketMarker = part1()
    print("Start-of-packet marker:")
    print(startOfPacketMarker)
    startOfMessageMarker = part2()
    print("Start-of-message marker:")
    print(startOfMessageMarker)

if __name__ == "__main__":
    main()
