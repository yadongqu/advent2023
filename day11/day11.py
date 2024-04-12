from typing import NamedTuple, List, Tuple
from itertools import combinations
from functools import reduce
from operator import add
from math import copysign
class Point(NamedTuple):
    x :int
    y :int

def get_neighbors(bound: Tuple[int, int], cur: Point) -> List[Point]:
    neighbors = []
    if cur.x > 0:
        neighbors.append(Point(cur.x-1, cur.y))
    if cur.x < bound[0] - 1:
        neighbors.append(Point(cur.x+ 1, cur.y))
    if cur.y > 0:
        neighbors.append(Point(cur.x, cur.y - 1))
    if cur.y < bound[1] - 1:
        neighbors.append(Point(cur.x, cur.y + 1))
    return neighbors


def distance(start: Point, end: Point) -> int:
    x_distance = abs(end.x - start.x)
    y_distance = abs(end.y - start.y)
    return x_distance + y_distance

def calculate_path(start: Point, end: Point, empty_rows: List[int], empty_cols: List[int], multiplier: int = 2) -> int:
    dis = distance(start, end)
    empties = 0
    for x in range(start.x, end.x, int(copysign(1, end.x - start.x))):
        if x in empty_cols:
            empties += 1
    for y in range(start.y, end.y, int(copysign(1, end.y - start.y))):
        if y in empty_rows:
            empties += 1
    return dis + empties * (multiplier - 1)
            

def parse_map(content: str) -> Tuple[List[Point], List[int], List[int]]:
    maze = [[ch for ch in line] for line in content.split('\n')]
    empty_rows = [i for i in range(len(maze)) if "#" not in maze[i]]
    transposed = list(map(list, zip(*maze)))
    empty_cols = [i for i in range(len(transposed)) if "#" not in transposed[i]]
    height = len(maze)
    width = len(maze[0])
    galaxies = [Point(j, i) for j in range(width) for i in range(height) if maze[i][j] != '.']
    return (galaxies, empty_cols, empty_rows)
    
def part1():
    file = open("input.txt")
    content = file.read()
    (galaxies, empty_cols, empty_rows) = parse_map(content)
    path = reduce(add, [calculate_path(galaxies[0], galaxies[1], empty_rows=empty_rows, empty_cols=empty_cols) for galaxies in combinations(galaxies, 2)])

    print(path)
    
def part2():
    file = open("input.txt")
    content = file.read()
    (galaxies, empty_cols, empty_rows) = parse_map(content)
    path = reduce(add, [calculate_path(galaxies[0], galaxies[1], empty_rows=empty_rows, empty_cols=empty_cols, multiplier=1000000) for galaxies in combinations(galaxies, 2)])

    print(path)
    
part1()
part2()