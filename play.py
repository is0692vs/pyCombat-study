import gymnasium as gym
import numpy as np
import torch
from dqn_agent import DQNAgent
import pygame
import time
from datetime import datetime
import os
from game import Character  # Characterクラスをインポート
from game import GROUND_Y  # GROUND_Yもインポート

# pygameの初期化
pygame.init()
pygame.font.init()

# 環境の登録
gym.register(
    id='FightingGame-v0',
    entry_point='gym_fighting_game_env:GymFightingGameEnv',
)

# 環境が完全に登録されるのを少し待つ
time.sleep(1)

# 環境の初期化
env = gym.make('FightingGame-v0')

# state_sizeとaction_sizeを取得
state_size = env.observation_space.shape[0]
action_size = env.action_space.n

# DQNAgentのインスタンスを作成
agent = DQNAgent(state_size, action_size)

# 学習済みモデルのロード関数
def load_model(agent, player_model_path, enemy_model_path):
    agent.player_q_network.load_state_dict(torch.load(player_model_path))
    agent.enemy_q_network.load_state_dict(torch.load(enemy_model_path))
    agent.update_target_network()

# 学習済みモデルのロード
player_model_path = 'player-agent/player_q_network_20241116_134239.pth'  # 実際のファイルパス
enemy_model_path = 'enemy-agent/enemy_q_network_20241116_134239.pth'  # 実際のファイルパス
load_model(agent, player_model_path, enemy_model_path)

# 探索率を低く設定
agent.epsilon = 0.01

# プレイループ
state, _ = env.reset()
done = False
total_player_reward = 0
total_enemy_reward = 0
step_count = 0
while not done:
    # エージェントの行動を決定
    player_action = agent.act(state, is_player=True)
    enemy_action = agent.act(state, is_player=False)  # 敵の行動も決定

    action = (player_action, enemy_action)  # タプルにする
    next_state, (player_reward, enemy_reward), terminated, truncated, _ = env.step(action)
    done = terminated or truncated
    state = next_state
    total_player_reward += player_reward
    total_enemy_reward += enemy_reward
    step_count += 1

    # ゲーム画面を描画
    env.render(total_player_reward, total_enemy_reward)

    # 報酬が発生した時にログを記録
    if player_reward != 0 or enemy_reward != 0:
        # print(f"Step: {step_count}, Action: {action}, Player Reward: {player_reward}, Enemy Reward: {enemy_reward}, Total Player Reward: {total_player_reward}, Total Enemy Reward: {total_enemy_reward}")
        pass
env.close()