from typing import Generator, List
from itertools import starmap, cycle
from operator import sub

def read_line(file_name: str) -> Generator[str, None, None]:
    with open(file_name, 'r') as file:
        for line in file:
            yield line.strip('\n')
            
def parse_ints(line: str) -> List[int]:
    return [int(n) for n in line.split(' ')]

def difference(numbers: List[int]):
    return list(starmap(sub, zip(numbers[1:], numbers)))         

def part1():
    res = 0
    for line in read_line("input.txt"):
        ints = parse_ints(line)
        diff = difference(ints)
        s = ints[len(ints)- 1]
        while not all(d == 0 for d in diff):
            s += diff[len(diff) - 1]
            diff = difference(diff)
        res += s
    print(res)

def part2():
    res = 0
    for line in read_line("input.txt"):
        ints = parse_ints(line)
        diff = difference(ints)
        res += ints[0]
        sign = cycle([-1, 1])
        while not all(d == 0 for d in diff):
            res += next(sign) * diff[0]
            diff = difference(diff)
    print(res)
part1() 
part2()