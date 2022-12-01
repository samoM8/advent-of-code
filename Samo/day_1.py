import os
import heapq

def readFile(fileName) -> str:
    f = open(os.path.join(os.path.dirname(__file__), fileName), "r")
    data = f.read()
    f.close()
    return data

def part1():
    data = readFile("inputs/input1_1.txt")
    caloriesPacks = data.split("\n\n")
    highestCalories = 0
    for caloriePack in caloriesPacks:
        currentCalories = sum([int(i) for i in caloriePack.split("\n")])
        
        if currentCalories > highestCalories:
            highestCalories = currentCalories

    return highestCalories

def part2():
    data = readFile("inputs/input1_1.txt")
    caloriesPacks = data.split("\n\n")
    
    caloriesSum = []
    for caloriePack in caloriesPacks:
        caloriesSum.append(sum([int(i) for i in caloriePack.split("\n")]))

    return sum(heapq.nlargest(3, caloriesSum))

def main():
    elfWithMostCalories = part1()
    print("Most calories that one elf has:")
    print(elfWithMostCalories)

    elfsWithMostCalories = part2()
    print("Highest sum of calories that 3 elf have:")
    print(elfsWithMostCalories)

if __name__ == "__main__":
    main()
