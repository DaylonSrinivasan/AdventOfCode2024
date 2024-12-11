# solves part 1 faster, but still too slow for part 2

from __future__ import annotations

input = "92 0 286041 8034 34394 795 8 2051489"

import dataclasses

@dataclasses.dataclass
class Node:
    val: int
    next: Node | None


def parse(input):
    values = input.split(" ")
    curr = None
    head = None
    for val in values:
        n = Node(int(val), None)
        if head == None:
            head = n
        else:
            curr.next = n
        curr = n
    return head


def blink(stones):
    curr = stones
    while curr:
        val = curr.val
        if val == 0:
            curr.val = 1
        elif len(str(val)) % 2 == 0:
            strVal = str(val)
            length = len(strVal)
            left = int(strVal[0:int(length / 2)])
            right = int(strVal[int(length / 2):])
            curr.val = left
            curr.next = Node(right, curr.next)
            curr = curr.next
        else:
            curr.val *= 2024
        curr = curr.next
    
def solution(stones):
    # solves part 1 faster, but not part 2
    for i in range(25):
        print(i)
        blink(stones)
    i = 0
    curr = stones
    while curr:
        i += 1
        curr = curr.next
    return i


def main():
    print(solution(parse(input)))
    
main()