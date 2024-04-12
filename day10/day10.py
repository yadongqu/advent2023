from typing import List, Tuple, Optional, Dict
from enum import Enum
from typing import NamedTuple

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

pipe_to_direction = {
    '|': (Direction.NORTH, Direction.SOUTH),
    '-': (Direction.EAST, Direction.WEST),
    'L': (Direction.NORTH, Direction.EAST),
    'J': (Direction.NORTH, Direction.WEST),
    '7': (Direction.SOUTH, Direction.WEST),
    'F': (Direction.SOUTH, Direction.EAST),
    'S': (Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST)
}

direction_to_pipe = {
    item[1]: item[0] for item in pipe_to_direction.items()
}

pair_direction = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
}

def read_file(file_name: str) -> str:
    file = open(file_name, 'r')
    return file.read()

def parse_maze(content: str) -> List[List[str]]:
    return  [[ch for ch in line] for line in content.split("\n")]

def find_start(maze: List[List[str]]) -> Tuple[int, int]:
    return [(i, j) for i in range(len(maze)) for j in range(len(maze[i])) if maze[i][j] == 'S']


def get_possible_next_pos(maze: List[List[str]], pos: Tuple[int,int]) -> Dict[Direction, Tuple[int, int]]:
    (row, col) = pos
    direction = pipe_to_direction.get(maze[row][col])
    res = {}
    if Direction.NORTH in direction:
        if row > 0:
            north = (row - 1, col)
            if Direction.SOUTH in pipe_to_direction.get(maze[north[0]][north[1]]):
                res[Direction.NORTH] = north
    if Direction.EAST in direction:
        if col < len(maze[0]) - 1:
            east = (row, col + 1)
            if Direction.WEST in pipe_to_direction.get(maze[east[0]][east[1]]):
                res[Direction.EAST] = east
    if Direction.SOUTH in direction:
        if row < len(maze) - 1:
            south = (row + 1, col)
            if Direction.NORTH in pipe_to_direction.get(maze[south[0]][south[1]]):
                res[Direction.SOUTH] = south
    if Direction.WEST in direction:
        if col > 0:
            west = (row, col - 1)
            if Direction.EAST in pipe_to_direction.get(maze[west[0]][west[1]]):
                res[Direction.WEST] = west
    return res
    

def get_next(maze: List[List[str]], pos: Tuple[int, int], origin: Direction) -> Tuple[Direction, Tuple[int, int]]:
    neighbors = get_possible_next_pos(maze, pos)
    directions = list(neighbors.keys())
    # if it is not posssible to reach from the origin direction or there is only 1 direction possible in current position
    # that means we have reached a dead end, there is no possible path.
    if origin not in directions or len(directions) == 1:
        return None
    else:
        # we need to remove the origin direction, the remaning direction will be our next direction.
        # as each pipe only have at most two possible directions, we are certain we only have one avaiable in 
        # the remaing
        directions.remove(origin)
        return (directions[0], neighbors[directions[0]])
        

def walk_maze(maze: List[List[str]], start: Tuple[int, int]):
    possible_pos = get_possible_next_pos(maze, start)
    assert(len(possible_pos) == 2)
    # since it is a loop, it doesn't matter which path we took. 
    # we just choose the first one here.
    (next_direction, next_position) = list(possible_pos.items())[0]
    path = [start, next_position]
    walkable = True
    while True:
        res = get_next(maze, next_position, pair_direction[next_direction])
        if res == None:
            walkable = False
            break
        (next_direction, next_position) = res
        if next_position == start:
            break
        path.append(next_position)
        
    if walkable:
        print(len(path)/2)
    
    
        # print((len(path)+1)/2)
        

content = read_file("input.txt")
maze = parse_maze(content)
start = find_start(maze)[0]
walk_maze(maze, start)
