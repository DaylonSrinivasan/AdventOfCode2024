# solves part 1 and part 2

input = "92 0 286041 8034 34394 795 8 2051489"

from functools import lru_cache

def parse(input):
    return [int(val) for val in input.split(" ")]

@lru_cache(maxsize=200000)
def calculateNumStonesProduced(value, numBlinks):
    if numBlinks == 0:
        return 1
    elif value == 0:
        return calculateNumStonesProduced(1, numBlinks - 1)
    elif len(str(value)) % 2 == 0:
        strVal = str(value)
        length = len(strVal)
        left = int(strVal[0:int(length / 2)])
        right = int(strVal[int(length / 2):])
        return calculateNumStonesProduced(left, numBlinks - 1) + calculateNumStonesProduced(right, numBlinks - 1)
    else:
        return calculateNumStonesProduced(value * 2024, numBlinks - 1)

def solution(values, numBlinks):
    total = 0
    for value in values:
        total += calculateNumStonesProduced(value, numBlinks)
    return total

def main():
    print(solution(parse(input), 75))
    
main()