import os
from collections import deque
from math import lcm

class Monkey:
    def __init__(self, items: list, opSign: str, opNum: str, 
                 testDivider: int, testTrue: int, testFalse: int) -> None:
        self.items = deque(items)
        self.inspectedItems = 0
        self.opSign = opSign
        self.opNum = opNum
        self.testDivider = testDivider
        self.testTrue = testTrue
        self.testFalse = testFalse

    def inspected(self):
        self.inspectedItems = self.inspectedItems + 1

    # adds a new item to the end
    def addItem(self, item: int):
        self.items.append(item)

    # returns the first item
    def getItem(self) -> int:
        return self.items.popleft()

    def hasItems(self) -> bool:
        if self.items:
            return True
        return False

    # returns item with worry level increased based on operation
    def inspecting(self, item: int) -> int:
        if self.opNum.isnumeric():
            opNum = int(self.opNum)
        else:
            opNum = item
        
        if self.opSign == "+":
            return item + opNum
        elif self.opSign == "*":
            return item * opNum
        else:
            print("Error: unavailable operator")
            exit(1)
    
    # return item with worry level divided by 3    
    def boredWithItem(self, item: int) -> int:
        return item // 3
    
    # returns number to which monkey we have to throw
    def testItem(self, item: int):
        if item % self.testDivider == 0:
            return self.testTrue
        else:
            return self.testFalse

    def decreaseNumberSize(self, item:int, lcm: int) -> int:
        return item % lcm

def readLines(fileName: str) -> list:
    file = open(os.path.join(os.path.dirname(__file__), fileName), "r")
    data = file.read().split("\n\n")
    file.close()
    return data

# generate monkeys with starting items, operations and tests
def generateMonkeys(allActions: list) -> list:
    monkeys = []
    for oneAction in allActions:
        _, itemsLine, operationLine, testDivLine, testTrueLine, testFalseLine = oneAction.splitlines()
        items = [int(x) for x in itemsLine[18:].split(", ")]
        opSign = operationLine[23]
        opNum = operationLine[25:]
        testDivider = int(testDivLine[21:])
        testTrue = int(testTrueLine[29:])
        testFalse = int(testFalseLine[29:])
        monkeys.append(Monkey(items, opSign, opNum, testDivider, testTrue, testFalse))

    return monkeys

def part1() -> int:
    allActions = readLines("inputs/input11.txt")
    monkeys = generateMonkeys(allActions)

    # 20 rounds of monkeys throwing items around
    for _ in range(20):
        for monkey in monkeys:
            while monkey.hasItems():
                item = monkey.getItem()
                item = monkey.boredWithItem(monkey.inspecting(item))
                monkey.inspected()
                monkeyToGive = monkey.testItem(item)
                monkeys[monkeyToGive].addItem(item)

    monkeysSorted = sorted(monkeys, key=lambda x: x.inspectedItems, reverse=True)

    return monkeysSorted[0].inspectedItems * monkeysSorted[1].inspectedItems

def part2() -> int:
    allActions = readLines("inputs/input11.txt")
    monkeys = generateMonkeys(allActions)

    # calculate least common multiple of monkey dividers to
    # mitigate worry level growth
    lcmOfDividers = lcm(*[x.testDivider for x in monkeys])
    # 20 rounds of monkeys throwing items around
    for _ in range(10000):
        for monkey in monkeys:
            while monkey.hasItems():
                item = monkey.getItem()
                item = monkey.inspecting(item)
                monkey.inspected()
                item = monkey.decreaseNumberSize(item, lcmOfDividers)
                monkeyToGive = monkey.testItem(item)
                monkeys[monkeyToGive].addItem(item)

    monkeysSorted = sorted(monkeys, key=lambda x: x.inspectedItems, reverse=True)

    return monkeysSorted[0].inspectedItems * monkeysSorted[1].inspectedItems

def main():
    monkeyBusiness = part1()
    print("Monkey business after 20 rounds:")
    print(monkeyBusiness)

    monkeyBusiness2 = part2()
    print("Monkey business after 10000 rounds:")
    print(monkeyBusiness2)

if __name__ == "__main__":
    main()
