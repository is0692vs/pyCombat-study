# handmaid_cpu_enemy.py
import random
from config import CHARACTER_HP

def enemy_rule_based_action(state):
    """
    ルールベースの行動を決定する関数。
    state: 環境の状態
    return: 行動 (0: 何もしない, 1: 左移動, 2: 右移動, 3: ジャンプ, 4: パンチ, 5: キック, 6: 上攻撃)
    """
    relative_x, relative_y, player_hp, enemy_hp, player_is_jumping, enemy_is_jumping, player_is_down, enemy_is_down, player_action, enemy_action = state

    # 敵が近い場合はパンチ、遠い場合は近づく(最適化されてて強すぎ)
    if abs(relative_x) <80:
        return random.choice([4,4,5,5,6])  # 攻撃
    elif relative_x < 0:
        return 1  # 左移動
    else:
        return 2  # 右移動
    
    
    
    # # 適切な行動をしない確率
    # random_action_prob = 0.9
    # if random.random() < random_action_prob:
    #     return 0  # 何もしない

    # # 敵が近い場合は何かしらの行動、遠い場合は近づく
    # if abs(relative_x) < 90:
    #     return random.choice([3, 4, 5, 6, 4, 5, 6, 4, 5, 6, 4, 5, 6, 4, 5, 6, 4, 5, 6, 4, 5, 6]) #近づいてなんかする
    # elif relative_x < 0:
    #     return 1  # 左移動
    # else:
    #     return 2  # 右移動
    
    
    # # 適切な行動をしない確率
    # random_action_prob = 0.5
    # if random.random() < random_action_prob:
    #     return 0  # 何もしない

    # # 体力が減るたびに逃げる行動の確率を増やす
    # escape_prob = (1 - (enemy_hp / CHARACTER_HP)) * 0.1  # 体力が減るほど逃げる確率が増える
    # if random.random() < escape_prob:
    #     if relative_x < 0:
    #         return 2  # 右移動
    #     else:
    #         return 1  # 左移動

    # # プレイヤーのHPが低い場合、手加減する確率を増やす
    # mercy_prob = (1 - (player_hp / CHARACTER_HP)) * 0.1  # プレイヤーの体力が減るほど手加減する確率が増える
    # if random.random() < mercy_prob:
    #     return 0  # 何もしない

    # # 敵が近い場合は攻撃、遠い場合は近づく
    # if abs(relative_x) < 80:
    #     return random.choice([4,5 ]) #近づいてなんかする
    # elif relative_x < 0:
    #     return 1  # 左移動
    # else:
    #     return 2  # 右移動



def player_rule_based_action(state):
    """
    ルールベースの行動を決定する関数。
    state: 環境の状態
    return: 行動 (0: 何もしない, 1: 左移動, 2: 右移動, 3: ジャンプ, 4: パンチ, 5: キック, 6: 上攻撃)
    """
    relative_x, relative_y, player_hp, enemy_hp, player_is_jumping, enemy_is_jumping, player_is_down, enemy_is_down, player_action, enemy_action = state

    # 適切な行動をしない確率
    random_action_prob = 0.8
    if random.random() < random_action_prob:
        return 0  # 何もしない

    # 体力が減るたびに逃げる行動の確率を増やす
    escape_prob = (1 - (enemy_hp / CHARACTER_HP)) * 0.3  # 体力が減るほど逃げる確率が増える
    if random.random() < escape_prob:
        if relative_x < 0:
            return 1  # 左移動

        else:
            return 2  # 右移動

    # プレイヤーのHPが低い場合、手加減する確率を増やす
    mercy_prob = (1 - (player_hp / CHARACTER_HP)) * 0.3  # プレイヤーの体力が減るほど手加減する確率が増える
    if random.random() < mercy_prob:
        return 0  # 何もしない

    # 敵が近い場合は攻撃、遠い場合は近づく
    if abs(relative_x) < 80:
        return 3
        # return random.choice([4,5 ]) #近づいてなんかする
    elif relative_x < 0:
        return 2  # 右移動
    else:
        return 1  # 左移動