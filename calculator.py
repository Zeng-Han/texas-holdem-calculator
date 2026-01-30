import itertools
import math
from tqdm import tqdm
from combination import NUMBERS, SUITS, find_best_combination, compare_strength

def calculate_winning_rate(hand_a, hand_b, public_cards):
    # 1. 生成完整一副牌
    full_deck = [n + s for n in NUMBERS for s in SUITS]
    
    # 2. 移除已知手牌和公牌
    known_cards = set(hand_a + hand_b + public_cards)
    remaining_deck = [card for card in full_deck if card not in known_cards]
    
    # 3. 计算还需要补齐几张公牌
    cards_to_draw = 5 - len(public_cards)
    
    win_a = 0
    win_b = 0
    tie = 0
    total_scenarios = 0
    
    # 记录两手牌各自可能达到的最高牌型等级分布
    types_a = {i: 0 for i in range(1, 10)}
    types_b = {i: 0 for i in range(1, 10)}
    
    total_scenarios_count = 1
    # 4. 统计总场景数
    if cards_to_draw > 0:
        total_scenarios_count = math.comb(len(remaining_deck), cards_to_draw)
    
    possible_remaining_public = itertools.combinations(remaining_deck, cards_to_draw)
    
    # 5. 遍历所有可能的公牌组合
    for extra_public in tqdm(possible_remaining_public, total=total_scenarios_count, desc="计算中"):
        full_public = public_cards + list(extra_public)
        total_scenarios += 1
        
        # 为每手牌寻找最佳组合（7选5）
        best_a = find_best_combination(hand_a + full_public)
        best_b = find_best_combination(hand_b + full_public)
        
        # 统计牌型
        types_a[best_a["level"]] += 1
        types_b[best_b["level"]] += 1
        
        # 比较大小
        res = compare_strength(best_a, best_b)
        if res == 1:
            win_a += 1
        elif res == -1:
            win_b += 1
        else:
            tie += 1

    return {
        "win_a": win_a,
        "win_b": win_b,
        "tie": tie,
        "total": total_scenarios,
        "types_a": types_a,
        "types_b": types_b,
        "hand_a": hand_a,
        "hand_b": hand_b,
        "public_cards": public_cards
    }


if __name__ == "__main__":
    hand_a = ['AH', '9S']
    hand_b = ['JD', 'JH']
    public_cards = []
    
    result = calculate_winning_rate(hand_a, hand_b, public_cards)
    
    # 在函数外部处理打印输出
    labels = {
        9: "同花顺 (straight flush)",
        8: "四条 (four of a kind)",
        7: "葫芦 (full house)",
        6: "同花 (flush)",
        5: "顺子 (straight)",
        4: "三条 (three of a kind)",
        3: "两对 (two pairs)",
        2: "一对 (one pair)",
        1: "高牌 (high card)"
    }
    
    total = result["total"]
    print("\n" + "=" * 40)
    print(f"总计算场景数: {total}")
    print("-" * 40)
    print(f"玩家 A 手牌: {result['hand_a']}")
    print(f"玩家 B 手牌: {result['hand_b']}")
    print(f"当前公牌: {result['public_cards']}")
    print("-" * 40)
    print(f"玩家 A 胜率: {result['win_a'] / total * 100:.2f}% ({result['win_a']} 手)")
    print(f"玩家 B 胜率: {result['win_b'] / total * 100:.2f}% ({result['win_b']} 手)")
    print(f"平局率: {result['tie'] / total * 100:.2f}% ({result['tie']} 手)")
    print("-" * 40)
    
    print("玩家 A 牌型分布:")
    for lvl in range(9, 0, -1):
        if result["types_a"][lvl] > 0:
            print(f"  {labels[lvl]}: {result['types_a'][lvl] / total * 100:.2f}%")
            
    print("\n玩家 B 牌型分布:")
    for lvl in range(9, 0, -1):
        if result["types_b"][lvl] > 0:
            print(f"  {labels[lvl]}: {result['types_b'][lvl] / total * 100:.2f}%")
    print("=" * 40)
