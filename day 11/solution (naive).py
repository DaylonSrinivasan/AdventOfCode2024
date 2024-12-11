# solves part 1, but too slow for part 2

input = "92 0 286041 8034 34394 795 8 2051489"

def parse(input):
    return [int(val) for val in input.split(" ")]

def blink(stones):
    i = 0
    while i < len(stones):
        val = stones[i]
        if val == 0:
            stones[i] = 1
        elif len(str(val)) % 2 == 0:
            strVal = str(val)
            left = int(strVal[0:int(len(strVal) / 2)])
            right = int(strVal[int(len(strVal) / 2):])
            stones[i] = left
            stones.insert(i + 1, right)
            i += 1
        else:
            stones[i] *= 2024
        i += 1
    
def solution(stones):
    for _ in range(25):
        blink(stones)
    return len(stones)

def main():
    print(solution(parse(input)))
    
main()