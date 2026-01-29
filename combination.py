from collections import defaultdict

NUMBERS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
NUMBERS_2_STRENGTHS = {
    'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2
}
STRENGTHS_2_NUMBERS = {v: k for k, v in NUMBERS_2_STRENGTHS.items()}
SUITS = ['S', 'H', 'C', 'D']

# 给定五张公共牌和两张手牌，找到七张牌中可能的最大组合
def find_best_combination(cards):
    # cards格式：["2H", "3H", "4D", "5S", "KD", "KC", "AS"]
    # 按照以下顺序逐个检查，直到高牌为止
    # L9：同花顺
    # L8：四条
    # L7：葫芦
    # L6：同花
    # L5：顺子
    # L4：三条
    # L3：两对
    # L2：一对
    # L1：高牌
    assert len(cards) == 7, "Invalid cards input"
    assert all(len(x) == 2 for x in cards), "Invalid cards input"
    assert all(x[0] in NUMBERS for x in cards), "Invalid cards input"
    assert all(x[1] in SUITS for x in cards), "Invalid cards input"
    cards = sorted(cards, key=lambda x: NUMBERS_2_STRENGTHS[x[0]])
    cards_num_indexed, cards_suit_indexed = defaultdict(list), defaultdict(list)
    for card in cards:
        num, suit = card[0], card[1]
        cards_num_indexed[num].append(suit)
        cards_suit_indexed[suit].append(num)
    
    result = find_straight_flush(cards_num_indexed, cards_suit_indexed)
    if result["found"]:
        return {
            "level": 9,
            "cards": result["cards"],
            "top_card": result["top_card"],
            "message": "Straight Flush with Top Card " + result["top_card"][0]
        }
    
    result = find_four_of_a_kind(cards_num_indexed, cards_suit_indexed)
    if result["found"]:
        return {
            "level": 8,
            "cards": result["cards"],
            "four_of_a_kind_card": result["four_of_a_kind_card"],
            "kicker_card": result["kicker_card"],
            "message": "Four of " + result["four_of_a_kind_card"][0]
        }
    
    result = find_full_house(cards_num_indexed, cards_suit_indexed)
    if result["found"]:
        return {
            "level": 7,
            "cards": result["cards"],
            "three_of_a_kind_card": result["three_of_a_kind_card"],
            "two_of_a_kind_card": result["two_of_a_kind_card"],
            "message": "Full House with " + result["three_of_a_kind_card"][0] + " over " + result["two_of_a_kind_card"][0]
        }
    
    result = find_flush(cards_num_indexed, cards_suit_indexed)
    if result["found"]:
        return {
            "level": 6,
            "cards": result["cards"],
            "top_card": result["top_card"],
            "message": "Flush with Top Card " + result["top_card"][0]
        }
    
    result = find_straight(cards_num_indexed, cards_suit_indexed)
    if result["found"]:
        return {
            "level": 5,
            "cards": result["cards"],
            "top_card": result["top_card"],
            "message": "Straight with Top Card " + result["top_card"][0]
        }
    
    result = find_three_of_a_kind(cards_num_indexed, cards_suit_indexed)
    if result["found"]:
        return {
            "level": 4,
            "cards": result["cards"],
            "three_of_a_kind_card": result["three_of_a_kind_card"],
            "kicker_cards": result["kicker_cards"],
            "message": "Three of " + result["three_of_a_kind_card"][0]
        }

    result = find_two_pairs(cards_num_indexed, cards_suit_indexed)
    if result["found"]:
        return {
            "level": 3,
            "cards": result["cards"],
            "two_pairs_cards": result["two_pairs_cards"],
            "kicker_cards": result["kicker_cards"],
            "message": "Two Pairs of " + result["two_pairs_cards"][0] + " and " + result["two_pairs_cards"][1]
        }
    
    result = find_one_pair(cards_num_indexed, cards_suit_indexed)
    if result["found"]:
        return {
            "level": 2,
            "cards": result["cards"],
            "one_pair_card": result["one_pair_card"],
            "kicker_cards": result["kicker_cards"],
            "message": "One Pair of " + result["one_pair_card"][0]
        }
    
    return {
        "level": 1,
        "cards": cards,
        "top_card": cards[-1],
        "kicker_cards": result["kicker_cards"],
        "message": "High Card with Top Card " + result["top_card"][0]
    }

def find_straight_flush(cards_num_indexed, cards_suit_indexed):
    for suit in cards_suit_indexed:
        if len(cards_suit_indexed[suit]) >= 5:
            cards_suited = cards_suit_indexed[suit]  # 可能有顺子的花色
            for num in cards_suited:
                # 特殊处理：'A'可以作为1或14
                if num == 'A':
                    if all(STRENGTHS_2_NUMBERS[1 + i] in cards_suited for i in range(1, 5)):
                        return {
                            "found": True,
                            "cards": ['A' + suit, '2' + suit, '3' + suit, '4' + suit, '5' + suit],
                            "top_card": '5' + suit
                        }
                strength = NUMBERS_2_STRENGTHS[num]
                if strength + 4 <= NUMBERS_2_STRENGTHS['A']:  # 可能有同花顺，但需要检查是否连续
                    if all(STRENGTHS_2_NUMBERS[strength + i] in cards_suited for i in range(5)):
                        return {
                            "found": True,
                            "cards": [STRENGTHS_2_NUMBERS[strength + i] + suit for i in range(5)],
                            "top_card": STRENGTHS_2_NUMBERS[strength + 4] + suit
                        }
    return {
        "found": False,
        "cards": [],
        "top_card": ""
    }


def find_four_of_a_kind(cards_num_indexed, cards_suit_indexed):
    pass


def find_full_house(cards_num_indexed, cards_suit_indexed):
    pass


def find_flush(cards_num_indexed, cards_suit_indexed):
    pass


def find_straight(cards_num_indexed, cards_suit_indexed):
    pass


def find_three_of_a_kind(cards_num_indexed, cards_suit_indexed):
    pass


def find_two_pairs(cards_num_indexed, cards_suit_indexed):
    pass


def find_one_pair(cards_num_indexed, cards_suit_indexed):
    pass


if __name__ == "__main__":
    cards = [
        "2H", "3H", "4H", "5H", "6D", "AC", "AH"
    ]
    cards_num_indexed, cards_suit_indexed = defaultdict(list), defaultdict(list)
    for card in cards:
        num, suit = card[0], card[1]
        cards_num_indexed[num].append(suit)
        cards_suit_indexed[suit].append(num)
    print(find_straight_flush(cards_num_indexed, cards_suit_indexed))
