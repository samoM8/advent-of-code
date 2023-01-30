import os
import json
from functools import cmp_to_key

def readLines(fileName: str) -> list:
    file = open(os.path.join(os.path.dirname(__file__), fileName), "r")
    lines = file.read()
    file.close()
    return lines

def compareItems(item1, item2) -> int:
    """
    Compares two items with recursion.
    Item can be integers or all kind of nester arrays. \n
    Returns -1, 0, 1 if item1 is before, equal to, after item2.
    """
    if type(item1) == int and type(item2) == int: # compare integers
        if item1 < item2:
            return -1
        elif item1 > item2:
            return 1
        else:
            return 0
    elif type(item1) == list and type(item2) == list: # recuresively compare items in list
        ix1 = 0
        ix2 = 0

        while ix1 < len(item1) and ix2 < len(item2):
            result = compareItems(item1[ix1], item2[ix2])
            if result == -1 or result == 1:
                return result

            ix1 = ix1 + 1; ix2 = ix2 + 1
        
        # We ran out of items in both arrays
        if ix1 == len(item1) and ix2 == len(item2): return 0
        # We ran out of items in the first arrays
        if ix1 == len(item1): return -1
        # We ran out of items in the second arrays
        if ix2 == len(item2): return 1

    elif type(item1) == int: # convert integer to list with 1 item
        item1 = [item1]
        return compareItems(item1, item2)
    elif type(item2) == int: # convert integer to list with 1 item
        item2 = [item2]
        return compareItems(item1, item2)
    else:
        raise Exception("Impossible combination of pair items.")

def part1() -> int:
    pairs = readLines("inputs/input13.txt").split("\n\n")
    indexOfPair = 1
    sumOfIndices = 0
    
    # Loop through all pairs and compare if two packets are in right order
    for pair in pairs:
        tmp1, tmp2 = pair.split("\n")
        packet1 = json.loads(tmp1)
        packet2 = json.loads(tmp2)

        if compareItems(packet1, packet2) < 0:
            sumOfIndices = sumOfIndices + indexOfPair

        indexOfPair = indexOfPair + 1

    return sumOfIndices

def part2() -> int:
    divPacket1 = json.loads("[[2]]")
    divPacket2 = json.loads("[[6]]")
    packetStrings = readLines("inputs/input13.txt").replace("\n\n", "\n").splitlines()
    packets = []
    for pStr in packetStrings:
        packets.append(json.loads(pStr))
    packets.append(divPacket1)
    packets.append(divPacket2)

    # Sort the packets with our compare function
    sortedPackets = sorted(packets, key=cmp_to_key(compareItems))

    # Return divider key by multiplying indices of divider packets
    return (sortedPackets.index(divPacket1) + 1) * (sortedPackets.index(divPacket2) + 1)

def main():
    sumOfIndices = part1()
    print("Sum of indices of pairs of packets in the right order:")
    print(sumOfIndices)

    decoderKey = part2()
    print("Decoder key for disress signal:")
    print(decoderKey)

if __name__ == "__main__":
    main()
