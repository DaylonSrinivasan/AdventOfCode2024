input = """...........V..................b.g.................
..................................g...............
.............................c....................
............T........Z.......P....................
.x........................VP......................
..........................PH......................
.................H.....Z.......g.R................
......f............T.V....b......A................
......................P...........................
.......f..................A.............R.........
........x..............T.......l..H.....A.c.......
..k..x..............Z.............................
........5....S...............0.A..................
.............N....L...............................
.f............................T........s.....N....
..................l..........bH.......tc.R..N.....
......Z...6......n......l...k.N...0...............
...........g....S......l.r.................t..s...
..L................b.......K..t...................
................5....n........0.............c.....
.....L......n............................E........
.k.......L................m.....................Es
..............St.....5....Rm......................
............6..5...................3...0..........
...........k.................W........3...........
................n......K...E....2S..........3.....
....................................E....Q........
..........M.....x...............K.................
..h.............................1.................
.6............z..............4...e.........WY....y
........f............a.......Y..y...s.............
...h............r.............v....m..............
.....h.................v....m.....Y.Q.....W3......
.........................Yq....Q.................7
.........6..............7.................9.......
...................X..........y..q.....2..........
............r..............q.....y...........7.8..
..B..............M....4............9..............
...1.......M...X.......CGzp...4..B...2..K.........
.....................z...v....Q.....8...........9.
B.......X.F....rM...v...............2...8..D......
h1..............................7..D.....8....d...
...............F.....................9D....4....d.
..........a......p............F.........W.D......d
.........................G..C...........q.........
...B..................................C...........
.........w..........z....p.....................e..
.a............G....w........p........F........e...
........a...w.....................................
........w...............XC.......G................"""
import dataclasses
from collections import defaultdict
# Create 2d matrix
def parse(input):
    lines = input.split("\n")
    return [list(line) for line in lines]

@dataclasses.dataclass(frozen=True)
class location:
    r: int
    c: int

def gcd(bigger, smaller):
    while smaller:
        bigger, smaller = smaller, bigger % smaller
    return abs(bigger)

def getAntennas(matrix):
    # {character: [locations]}
    antennas = defaultdict(list)
    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            character = matrix[r][c]
            if character.isalnum():
                antennas[character].append(location(r, c))

    return antennas

def getAntinodes(antennas, matrix):
    # {locations}
    antinodes = set()
    for _, locations in antennas.items():
        for location1_index in range(len(locations)):
            for location2_index in range(location1_index + 1, len(locations)):
                location1 = locations[location1_index]
                location2 = locations[location2_index]
                if location1 == location2:
                    continue

                # points on same row -> add the whole row
                if location1.r == location2.r:
                    antinodes.update([location(location1.r, i) for i in range(len(matrix[0]))])
                
                # points on same column -> add the whole column
                elif location1.c == location2.c:
                    antinodes.update([location(i, location1.c) for i in range(len(matrix))])
                
                # points on diff row / column
                # To get all points on the line identified by two different points,
                # we can start at one point and add the minimum rDiff / cDiff in both
                # directions.
                #
                # minimum rDiff / cDiff can be calculated by getting the diffs
                # between the two points, and dividing each diff by their greatest
                # common divisor.
                else:
                    # First, get the minimum rDiff and cDiff
                    rDiff = location2.r - location1.r
                    cDiff = location2.c - location1.c
                    divisor = gcd(max(abs(rDiff), abs(cDiff)), min(abs(rDiff), abs(cDiff)))
                    rDiff = rDiff / divisor
                    cDiff = cDiff / divisor

                    # Then, expand from location1 to the boundary in one direction
                    r, c = location1.r, location1.c
                    while(r >= 0 and r < len(matrix) and c >= 0 and c < len(matrix[0])):
                        antinodes.add(location(r, c))
                        r += rDiff
                        c += cDiff
                    # Finally expand from location1 to the boundary in the other direction
                    r, c = location1.r, location1.c
                    while(r >= 0 and r < len(matrix) and c >= 0 and c < len(matrix[0])):
                        antinodes.add(location(r, c))
                        r -= rDiff
                        c -= cDiff
    return antinodes

def solution(matrix):
    # {character: [locations]}
    antennas = getAntennas(matrix)

    # {locations}
    antinodes = getAntinodes(antennas, matrix)
    return len(antinodes)
    
    
def main():
    print(solution(parse(input)))
    
main()