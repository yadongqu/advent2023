from collections import namedtuple
from typing import List, Optional, Set

Mapping = namedtuple('Mapping', 'range, offset')

def parse_ints(ints_string: str) -> List[int]:
    return [int(i) for i in ints_string.strip().split(" ")]

def parse_seeds(seed_string: str) -> List[int]:
    _, seeds = seed_string.split(":")
    return parse_ints(seeds)

def parse_seeds_2(seed_string: str) -> List[range]:
    ints = parse_seeds(seed_string)
    result = []
    for i in range(0, len(ints), 2):
        result.append(range(ints[i], ints[i] + ints[i + 1]))
    return result

def parse_mapping(mapping: str) -> List:
   mappings = mapping.splitlines()[1:]
   return [Mapping(range(src, src + length), dest - src) for (dest, src, length) in map(parse_ints, mappings)]

def convert(seed: int, mappings: List[Mapping])->int:
    for mapping in mappings:
        if seed in mapping.range:
            return seed + mapping.offset
    return seed

def multi_convert(seed: int, mappings_lists: List[List[Mapping]]) -> int :
    for mappings in mappings_lists:
        seed = convert(seed, mappings)
    return seed

def find_intersect_mapping(r: range, mappings: List[Mapping]) -> Optional[Mapping]:
    for mapping in mappings:
        if mapping.range.start in r or r.start in mapping.range:
            return mapping
    return None

def convert_ranges(ranges: List[range], mappings: List[Mapping]) -> Set[range] :
    ranges = set(ranges)
    result = set()
    while ranges:
        r = ranges.pop()
        m = find_intersect_mapping(r, mappings)
        if m:
            start, stop = max(r.start, m.range.start), min(r.stop, m.range.stop)
            result.add(range(start + m.offset, stop + m.offset))
            if r.start < start:
                ranges.add(range(r.start, start))
            if stop < r.stop:
                ranges.add(range(stop, r.stop))
        else:
            result.add(r)
    return result

def multi_convert_ranges(ranges: List[range], mappings_lists: List[List[Mapping]]) :
    # num_seeds = sum(map(len, ranges))
    for mappings in mappings_lists:
        ranges = list(convert_ranges(ranges, mappings))
    return ranges

        

def part1():
    with open("input.txt", "r") as file:
        data = file.read()
        segments = data.split("\n\n")
        seeds = parse_seeds(segments[0])
        mappings = [parse_mapping(mapping) for mapping in segments[1:]]
        location = min(multi_convert(seed, mappings) for seed in seeds)
        print(location)

def part2():
    with open("input.txt", "r") as file:
        data = file.read()
        segments = data.split("\n\n")
        seeds = parse_seeds_2(segments[0])
        mappings = [parse_mapping(mapping) for mapping in segments[1:]]
        ranges = multi_convert_ranges(seeds, mappings)
        location = min(r.start for r in ranges)
        print(location)

part1()
part2()

