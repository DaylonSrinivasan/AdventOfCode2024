# solves part 1 and part 2

input = "92 0 286041 8034 34394 795 8 2051489"

def parse(input):
    return [int(c) for c in input.split(" ")]

class Solution:
    def __init__(self):
        # map from {(value, blinksRemaining): number of stones it produces}
        self._cache = {}

    def solve(self, values, numBlinks):
        total = 0
        for value in values:
            total += self._calculateNumStonesProduced(value, numBlinks)
        return total

    def _calculateNumStonesProduced(self, value, numBlinks):
        key = (value, numBlinks)
        if key in self._cache:
            return self._cache[key]

        if numBlinks == 0:
            self._cache[key] = 1
        elif value == 0:
            self._cache[key] = self._calculateNumStonesProduced(1, numBlinks - 1)
        elif len(str(value)) % 2 == 0:
            strVal = str(value)
            length = len(strVal)
            left = int(strVal[0:int(length / 2)])
            right = int(strVal[int(length / 2):])
            self._cache[key] = self._calculateNumStonesProduced(left, numBlinks - 1) + self._calculateNumStonesProduced(right, numBlinks - 1)
        else:
            self._cache[key] = self._calculateNumStonesProduced(value * 2024, numBlinks - 1)
        return self._cache[key]

def main():
    solution = Solution()
    numBlinks = 75
    print(solution.solve(parse(input), numBlinks))
    print(len(solution._cache))

main()        
        

