from functools import reduce
import math
import re
from typing import List, Optional, Tuple

# note we interpret range as [start, end] inclusive.
def calculate_range(time: int, distance: int) -> Optional[range]:
    half_a = time / 2
    half_a_squared = half_a * half_a
    right = half_a_squared - distance
    if right <= 0:
        return None
    root = math.sqrt(right)
    left = -root + half_a
    right = root + half_a
    if left.is_integer():
        left = int(left + 1.0)
    else:
        left = max(0, math.ceil(left))
    if right.is_integer():
        right = int(right - 1.0)
    else:
        right = math.floor(right)
    return range(left, right)


def parse_ints(ints_string: str) -> List[int]:
    return [int(n) for n in re.split(r' +', ints_string.strip())]

def parse_time_and_distance(file_name: str) -> Tuple[List, List]:
    with open(file_name, "r") as file:
        data = file.read()
        lines = data.splitlines()
        time = []
        distance = []
        for line in lines:
            name, numbers = line.split(":")
            if name.startswith("Time"):
                time = parse_ints(numbers)
            if name.startswith("Distance"):
                distance = parse_ints(numbers)
        return (time, distance)
    
def combine_ints_to_one(ints: List[int]) -> int:
    final_int = 0
    for i in reversed(ints):
        if final_int == 0:
            final_int = i
        else:
            final_int += i * (10 ** len(str(final_int)))
    return final_int

def part_1():
    (time, distance) = parse_time_and_distance("input.txt")
    res = []
    for i in range(0, len(time)):
        r = calculate_range(time[i], distance[i])
        n = r.stop - r.start + 1
        res.append(n)

    fin = reduce((lambda x, y: x * y), res)
    print(fin)

def part_2():
    (time, distance) = parse_time_and_distance("input.txt")
    final_time = combine_ints_to_one(time)
    final_distance = combine_ints_to_one(distance)
    r = calculate_range(final_time, final_distance)
    n = r.stop - r.start + 1
    print(n)
    
        
part_1()
part_2()