# #main.py
import gymnasium as gym
import numpy as np
from dqn_agent import DQNAgent
import pygame
import time
from datetime import datetime
import torch
import os
from game import Character  # Characterクラスをインポート
from game import GROUND_Y  # GROUND_Yもインポート
from config import BATTLES_PER_EPISODE  # 対戦回数をインポート
import csv
from config import *  # configの全ての設定をインポート

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

# 学習ループ
for episode in range(EPISODES):
    start_time = time.time()  # エピソードの開始時間を記録
    total_player_reward = 0
    total_enemy_reward = 0
    total_steps = 0  # 合計ステップ数を初期化
    for battle in range(BATTLES_PER_EPISODE):
        state, _ = env.reset()
        done = False
        step_count = 0
        while not done and step_count < MAX_STEPS:
            # ランダムな行動を選択
            if np.random.rand() < agent.epsilon:
                player_action = env.action_space.sample()
                enemy_action = env.action_space.sample()
            else:
                player_action = agent.act(state, is_player=True)
                enemy_action = agent.act(state, is_player=False)  # 敵の行動も決定

            action = (player_action, enemy_action)  # タプルにする
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            agent.remember(state, action, reward, next_state, done)
            agent.learn(is_player=True)  # プレイヤーの学習
            agent.learn(is_player=False)  # 敵の学習
            state = next_state
            total_player_reward += reward[0]  # プレイヤーの報酬を合計する
            total_enemy_reward += reward[1]  # 敵の報酬を合計する
            step_count += 1
            total_steps += 1  # ステップ数をカウント

            # ターゲットネットワークを定期的に更新
            if step_count % agent.update_target_every == 0:
                agent.update_target_network()

            # ゲーム画面を描画
            if RENDER:
                env.render()

            # 報酬が発生した時にログを記録
            if reward != 0:
                # print(f"Episode {episode+1}, Step: {step_count}, Action: {action}, Reward: {reward}, Total Player Reward: {total_player_reward}, Total Enemy Reward: {total_enemy_reward}")
                pass

    # 探索率を減少させる
    agent.epsilon = max(agent.epsilon_min, agent.epsilon * agent.epsilon_decay)

    # エピソードの終了時間を計算して表示
    elapsed_time = time.time() - start_time
    print(f"Episode {episode+1}: Total Player Reward: {total_player_reward}, Total Enemy Reward: {total_enemy_reward}, Elapsed Time: {elapsed_time:.2f} seconds, Steps: {total_steps/1000:.1f}/{MAX_STEPS*BATTLES_PER_EPISODE/1000}K steps")

# 学習が終了した後にモデルを保存
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
player_model_path = os.path.join('agent-status', f'player_q_network_{timestamp}.pth')
enemy_model_path = os.path.join('agent-status', f'enemy_q_network_{timestamp}.pth')
config_path = os.path.join('agent-status', f'config_{timestamp}.csv')

torch.save(agent.player_q_network.state_dict(), player_model_path)
torch.save(agent.enemy_q_network.state_dict(), enemy_model_path)

# config設定をCSV形式で保存
config_data = {key: value for key, value in globals().items() if key.isupper()}

with open(config_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for key, value in config_data.items():
        writer.writerow([key, value])

env.close()