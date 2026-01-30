from collections import defaultdict
from itertools import combinations
import time

NUMBERS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
NUMBERS_2_STRENGTHS = {
    'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2
}
SUITS = ['S', 'H', 'C', 'D']


def find_best_combination(cards):
    # cards格式：["2H", "3H", "4D", "5S", "KD", "KC", "AS"]
    # 遍历所有7选5的可能组合，找出其中最大者
    assert len(cards) == 7, "Invalid cards input"
    assert all(len(x) == 2 for x in cards), "Invalid cards input"
    assert all(x[0] in NUMBERS for x in cards), "Invalid cards input"
    assert all(x[1] in SUITS for x in cards), "Invalid cards input"
    cards = sorted(cards, key=lambda x: NUMBERS_2_STRENGTHS[x[0]])  # 根据数字大小排序

    best_result = None
    combs = list(combinations(cards, 5))
    for comb in combs:
        current_result = get_5_cards_strength(comb)  # 牌力
        if best_result is None or compare_strength(current_result, best_result) > 0:
            best_result = current_result  # 记录最高牌力
    
    return best_result


def get_5_cards_strength(comb):
    # comb格式：["2H", "3H", "4D", "5S", "KD"]，已经从小到大排序
    # 返回组合牌力
    if is_straight_flush(comb):
        return {"level": 9, "label": "straight flush", "cards": comb}
    elif is_four_of_a_kind(comb):
        return {"level": 8, "label": "four of a kind", "cards": comb}
    elif is_full_house(comb):
        return {"level": 7, "label": "full house", "cards": comb}
    elif is_flush(comb):
        return {"level": 6, "label": "flush", "cards": comb}
    elif is_straight(comb):
        return {"level": 5, "label": "straight", "cards": comb}
    elif is_three_of_a_kind(comb):
        return {"level": 4, "label": "three of a kind", "cards": comb}
    elif is_two_pairs(comb):
        return {"level": 3, "label": "two pairs", "cards": comb}
    elif is_one_pair(comb):
        return {"level": 2, "label": "one pair", "cards": comb}
    else:
        return {"level": 1, "label": "high card", "cards": comb}


def compare_strength(card_a, card_b):
    # 比较两手牌的大小，a大返回1，b大返回-1，等大返回0
    if card_a["level"] > card_b["level"]:
        return 1
    elif card_a["level"] < card_b["level"]:
        return -1
    else:
        # 等级相同，需要提取比较特征（Comparison Key）
        key_a = get_comparison_key(card_a)
        key_b = get_comparison_key(card_b)
        
        if key_a > key_b:
            return 1
        elif key_a < key_b:
            return -1
        else:
            return 0


def get_comparison_key(card_info):
    # 根据牌型等级生成可直接比较的元组
    level = card_info["level"]
    cards = card_info["cards"]
    strengths = [NUMBERS_2_STRENGTHS[c[0]] for c in cards] # 这里的 cards 已按 strength 从小到大排序
    
    # 顺子和同花顺的特殊处理：A2345 是最小的顺子（5-high）
    if level == 5 or level == 9:
        if strengths[4] == 14 and strengths[0] == 2:
            return (5,)
        return (strengths[4],)  # 顺子的最高牌
        
    # 其他牌型：统计频率并按 (频率, 点数) 降序排序
    # 这种方式适用于：四条、葫芦、同花、三条、两对、一对、高牌
    counts = defaultdict(int)
    for s in strengths:
        counts[s] += 1
    
    # 排序规则：先看出现的次数（如三带二中的3），再看点数大小
    # items 格式：[(频率, 点数), ...]
    items = [(count, strength) for strength, count in counts.items()]
    # 按频率降序，频率相同时按点数降序
    items.sort(key=lambda x: (x[0], x[1]), reverse=True)
    
    # 返回纯点数组成的元组用于比较
    return tuple(item[1] for item in items)


def is_straight_flush(cards):
    if is_flush(cards) and is_straight(cards):
        return True
    else:
        return False


def is_four_of_a_kind(cards):
    num_counts = defaultdict(int)
    for card in cards:
        num_counts[card[0]] += 1
    if 4 in num_counts.values():
        return True
    else:
        return False


def is_full_house(cards):
    num_counts = defaultdict(int)
    for card in cards:
        num_counts[card[0]] += 1
    if 3 in num_counts.values() and 2 in num_counts.values():
        return True
    else:
        return False


def is_flush(cards):
    suit_counts = defaultdict(int)
    for card in cards:
        suit_counts[card[1]] += 1
    if 5 in suit_counts.values():
        return True
    else:
        return False


def is_straight(cards):
    if NUMBERS_2_STRENGTHS[cards[0][0]] + 4 == NUMBERS_2_STRENGTHS[cards[4][0]] or \
        (
            NUMBERS_2_STRENGTHS[cards[0][0]] + 3 == NUMBERS_2_STRENGTHS[cards[3][0]] and \
            cards[4][0] == 'A' and \
            cards[0][0] == '2'
        ):
        return True  # 考虑A2345的情况
    else:
        return False


def is_three_of_a_kind(cards):
    num_counts = defaultdict(int)
    for card in cards:
        num_counts[card[0]] += 1
    if 3 in num_counts.values():
        return True
    else:
        return False


def is_two_pairs(cards):
    num_counts = defaultdict(int)
    for card in cards:
        num_counts[card[0]] += 1
    if 2 in num_counts.values() and len(num_counts) == 3:
        return True
    else:
        return False


def is_one_pair(cards):
    num_counts = defaultdict(int)
    for card in cards:
        num_counts[card[0]] += 1
    if 2 in num_counts.values() and len(num_counts) == 4:
        return True
    else:
        return False


if __name__ == "__main__":
    cards = ["TS", "JS", "JH", "TH", "4H", "5S", "6S"]
    start_time = time.time()
    result = find_best_combination(cards)
    end_time = time.time()
    print(result)
    print(f"Time taken: {end_time - start_time} seconds")
    
