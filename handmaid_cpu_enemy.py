# handmaid_cpu_enemy.py
import random

def rule_based_action(state):
    """
    ルールベースの行動を決定する関数。
    state: 環境の状態
    return: 行動 (0: 何もしない, 1: 左移動, 2: 右移動, 3: ジャンプ, 4: パンチ, 5: キック, 6: 上攻撃)
    """
    player_x, player_y, enemy_x, enemy_y, player_hp, enemy_hp, player_is_jumping, enemy_is_jumping, player_action, enemy_action = state

    # # 敵が近い場合はパンチ、遠い場合は近づく(最適化されてて強すぎ)
    # if abs(player_x - enemy_x) <80:
    #     return 4  # パンチ
    # elif player_x < enemy_x:
    #     return 1  # 左移動
    # else:
    #     return 2  # 右移動
    
    
    
    # # 適切な行動をしない確率
    # random_action_prob = 0.7
    # if random.random() < random_action_prob:
    #     return 0  # 何もしない

    # # 敵が近い場合は何かしらの行動、遠い場合は近づく
    # if abs(player_x - enemy_x) < 90:
    #     return random.choice([3, 5]) #近づいてなんかする
    # elif player_x < enemy_x:
    #     return 1  # 左移動
    # else:
    #     return 2  # 右移動
    
    
    # copilot作のちょうどいいcpu
    random_action_prob = 0.7
    if random.random() < random_action_prob:
        return 0  # 何もしない

    # 敵が近い場合は攻撃、遠い場合は近づく
    if abs(player_x - enemy_x) < 80:
        return random.choice([4, 5, 6])  # パンチ、キック、上攻撃
    elif player_x < enemy_x:
        return 1  # 左移動
    else:
        return 2  # 右移動

    # ジャンプの追加
    if not enemy_is_jumping and random.random() < 0.1:
        return 3  # ジャンプ