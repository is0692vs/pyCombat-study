# #main.py
import gymnasium as gym
import numpy as np
from dqn_agent import DQNAgent
import pygame
import time
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

# 学習ループ
for episode in range(1000):
    state, _ = env.reset()
    done = False
    total_reward = 0
    step_count = 0
    while not done:
        # ランダムな行動を選択
        if np.random.rand() < agent.epsilon:
            player_action = env.action_space.sample()
            enemy_action = env.action_space.sample()
        else:
            player_action = agent.act(state)
            enemy_action = agent.act(state)  # 敵の行動も決定

        # ジャンプを封じる
        if player_action == 2:
            player_action = 0
        if enemy_action == 2:
            enemy_action = 0

        action = (player_action, enemy_action)  # タプルにする
        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        agent.remember(state, action, reward, next_state, done)
        agent.learn()
        state = next_state
        total_reward += reward
        step_count += 1

        # ターゲットネットワークを定期的に更新
        if episode % agent.update_target_every == 0:
            agent.update_target_network()

        # ゲーム画面を描画
        env.render()

        # エージェントの行動をログに記録
        print(f"Episode {episode+1}, Step: {step_count}, Action: {action}, Reward: {reward}")

    print(f"Episode {episode+1}: Total Reward: {total_reward}")

env.close()