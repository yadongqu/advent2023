from typing import List, NamedTuple
from enum import Enum
from collections import Counter
from functools import reduce


Hand = NamedTuple("hand", [("cards", List[int]), ("type", int), ("bid", int)])

value_dict = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
}

value_dict_part_2 = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 1,
    "T": 10,
}

def string_to_cards(string: str, value_dict: dict) -> List[int]:
    return [ value_dict[ch] if ch in value_dict.keys() else int(ch) for ch in string]


# todo: this is a hack
def wildcard_to_card(cards: List[int]) -> int:
    cards = cards.copy()
    if 1 in cards:     
        counter = Counter(cards)
        most_common = counter.most_common(1)[0]
        if most_common[1] == 5:
            return cards
        else:
            if most_common[0] != 1:
                return [most_common[0] if i == 1 else i for i in cards]
            else:
                most_common = counter.most_common(2)[1][0]
                return [most_common if i == 1 else i for i in cards]
    else:
        return cards

    

def cards_to_handtype(cards: List[int]) -> int:
    counter = Counter(cards)
    items = counter.items()
    items = sorted(items, key=lambda x: x[1], reverse=True)
    first_occurences = items[0][1]
    if first_occurences == 5:
        return 6
    if first_occurences == 4:
        return 5
    if first_occurences == 3:
        second_occurences = items[1][1]
        if second_occurences == 2:
            return 4
        else:
            return 3
    if first_occurences == 2:
        second_occurences = items[1][1]
        if second_occurences == 2:
            return 2
        else:
            return 1
    return 0


def parse_hand(line : str, value_dict: dict, with_wild_card: bool = False) -> Hand:
    [card_str, bid_str] = line.split(" ")
    cards = string_to_cards(card_str, value_dict=value_dict)
    hand_type = cards_to_handtype(cards)
    if with_wild_card:
        wild_cards = wildcard_to_card(cards)
        hand_type = cards_to_handtype(wild_cards)
    bid = int(bid_str)
    return Hand(cards=cards, type=hand_type, bid=bid)


def part1():
    with open("input.txt", "r") as file:
        data = file.read()
        hands = [parse_hand(line, value_dict=value_dict) for line in data.splitlines()]
        hands = sorted(hands, key= lambda x : (x.type, x.cards))
        out = sum([ (i + 1) * hand.bid for i, hand in enumerate(hands)])
        print(out)
    
def part2():
    with open("input.txt", "r") as file:
        data = file.read()
        hands = [parse_hand(line, value_dict=value_dict_part_2, with_wild_card=True) for line in data.splitlines()]
        hands = sorted(hands, key= lambda x : (x.type, x.cards))
        print(hands)
        out = sum([ (i + 1) * hand.bid for i, hand in enumerate(hands)])
        print(out)

part1()
part2()
