from functools import reduce
from typing import Tuple, List, Dict
from collections import Counter
def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def least_common_mulitple(numbers: List[int]) -> int:
    res = dict()
    frequencies = [Counter(prime_factors(n)) for n in numbers]
    for frequency in frequencies:
        items = frequency.items()
        for item in items:
            if item[0] in res.keys():
                res[item[0]] = max(item[1], res[item[0]])
            else:
                res[item[0]] = item[1]
    
    return reduce(lambda s, value: s * value[0] ** value[1],  res.items(), 1)            

def read_file(file_name: str) -> str:
    file = open(file_name, 'r')
    return file.read()

def parse(data: str) -> Tuple[List[int], Dict[str, List[str]]]:
    [instructions, directions] = data.split("\n\n")
    instructions = [0 if ch == 'L' else 1 for ch in instructions.strip()]
    directions = {value[0].strip(): [des.strip() for des in value[1].strip(' ()').split(',')] for value in [d.split("=") for d in directions.strip().splitlines()]}
    return (instructions, directions)

def part1():
    content = read_file("input.txt")
    (instructions, directions) = parse(content)
    step = 1
    index = 0;
    current_key = 'AAA'
    while True:
        index = index % len(instructions)
        ins = instructions[index]
        current_key = directions[current_key][ins]
        if current_key == 'ZZZ':
            break
        index += 1
        step += 1

def part2():
    content = read_file("input.txt")
    (instructions, directions) = parse(content)
    current_keys = [key for key in directions.keys() if key.endswith('A')]
    steps = []
    for current_key in current_keys:
        index = 0
        step = 1
        while True:
            index = index % len(instructions)
            ins = instructions[index]
            current_key = directions[current_key][ins]
            if current_key.endswith('Z'):
                steps.append(step)
                break
            index += 1
            step += 1
    result = least_common_mulitple(steps)
    print(result)
        
    
# part1()
part2()
