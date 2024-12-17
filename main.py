# main.pyで学習
import gymnasium as gym
import numpy as np
from dqn_agent import DQNAgent
import pygame
import time
from datetime import datetime
import torch
import os
from config import BATTLES_PER_EPISODE, INITIAL_PLAYER_REWARD, INITIAL_ENEMY_REWARD  # 対戦回数と初期報酬をインポート
import csv
from config import *  # configの全ての設定をインポート
import threading  # スレッドモジュールをインポート
import argparse
from handmaid_cpu_enemy import player_rule_based_action,enemy_rule_based_action  # ルールベースのエージェントをインポート


global IS_PAUSED
IS_PAUSED = False


# pygameの初期化
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()  # フレームレート制御用の時計を初期化

# 環境の登録
gym.register(
    id='FightingGame-v0',
    entry_point='gym_fighting_game_env:GymFightingGameEnv',
)

# 環境が完全に登録されるのを少し待つ
time.sleep(1)

# 環境の初期化
env = gym.make('FightingGame-v0', single_train=False)  # single_trainフラグをFalseに設定

# state_sizeとaction_sizeを取得
state_size = env.observation_space.shape[0]  
action_size = env.action_space.n

# DQNAgentのインスタンスを作成
agent = DQNAgent(state_size, action_size)

# エピソードごとの結果を保存するリストを初期化
episode_results = []

# ターミナルからの入力を監視する関数
def monitor_input():
    global RENDER, SAVE_MODEL_CONFIG_RESULTS, IS_PAUSED
    while True:
        user_input = input()
        if user_input == 'r':
            RENDER = not RENDER
            print(f"RENDER is now set to {RENDER}")
        elif user_input == 's':
            SAVE_MODEL_CONFIG_RESULTS = not SAVE_MODEL_CONFIG_RESULTS
            print(f"SAVE_MODEL_CONFIG_RESULTS is now set to {SAVE_MODEL_CONFIG_RESULTS}")
        elif user_input == 'p':
            IS_PAUSED = True
            print("Learning paused. Press Enter to continue...")
            input()
            IS_PAUSED = False
            print("Learning resumed.")

# 入力監視スレッドを開始
input_thread = threading.Thread(target=monitor_input)
input_thread.daemon = True
input_thread.start()

# モデルのロード
if PLAYER_MODEL_PATH or ENEMY_MODEL_PATH:
    agent.load_model(player_model_path=PLAYER_MODEL_PATH, enemy_model_path=ENEMY_MODEL_PATH)
    print(f"Player model loaded from {PLAYER_MODEL_PATH}")


try:
    # 学習ループ
    for episode in range(EPISODES):
        start_time = time.time()  # エピソードの開始時間を記録
        total_player_reward = INITIAL_PLAYER_REWARD
        total_enemy_reward = INITIAL_ENEMY_REWARD
        total_steps = 0  # 合計ステップ数を初期化

        # 報酬をリセット
        env.unwrapped.env.player.reward = INITIAL_PLAYER_REWARD
        env.unwrapped.env.enemy.reward = INITIAL_ENEMY_REWARD

        for battle in range(BATTLES_PER_EPISODE):
            env.unwrapped.env.current_battle = battle + 1  # 現在の試合数を設定
            if not RENDER:
                print(f"Episode {episode+1}/{EPISODES}: Battle {battle+1}/{BATTLES_PER_EPISODE}")
            state, _ = env.reset()
            done = False
            step_count = 0
            
            while not done and step_count < MAX_STEPS:
                while IS_PAUSED:
                    time.sleep(1.0)  # CPU使用率を下げるために短い待機を入れる
        
                # ランダムかルールベースかエージェントかで行動を決定
                if USE_RULE_BASED:
                    if np.random.rand() < agent.epsilon:
                        player_action = player_rule_based_action(state)
                        enemy_action = enemy_rule_based_action(state)
                    else:
                        player_action = agent.act(state, is_player=True)
                        enemy_action = agent.act(state, is_player=False)
                else:
                    if np.random.rand() < agent.epsilon:
                        player_action = env.action_space.sample()
                        enemy_action = env.action_space.sample()
                    else:
                        player_action = agent.act(state, is_player=True)
                        enemy_action = agent.act(state, is_player=False)


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
                
                clock.tick(FRAME_RATE)  # フレームレート(上限)を制御
                
                # 報酬が発生した時にログを記録
                if reward != 0:
                    # print(f"Episode {episode+1}, Step: {step_count}, Action: {action}, Reward: {reward}, Total Player Reward: {total_player_reward}, Total Enemy Reward: {total_enemy_reward}")
                    pass
        # 探索率を減少させる
        agent.epsilon = max(agent.epsilon_min, agent.epsilon * agent.epsilon_decay)

        # エピソードの終了時間を計算して表示
        elapsed_time = time.time() - start_time
        print(f"Episode {episode+1}/{EPISODES}: Total Player Reward: {total_player_reward:.2f}, Total Enemy Reward: {total_enemy_reward:.2f}, Elapsed Time: {elapsed_time:.2f} sec, Steps: {total_steps/1000:.1f}/{MAX_STEPS*BATTLES_PER_EPISODE/1000}K steps")

        # エピソードごとの結果をリストに追加
        episode_results.append([episode+1, total_player_reward, total_enemy_reward, elapsed_time, total_steps])

except KeyboardInterrupt:
    print(f"学習をエピソード {episode+1} で中断しました。")

finally:
    if SAVE_MODEL_CONFIG_RESULTS:
        # 学習が終了した後にモデルを保存
        timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M")
        player_model_path = os.path.join('player-agent', f'player_{timestamp}_Qnet.pth')
        enemy_model_path = os.path.join('enemy-agent', f'enemy_{timestamp}_Qnet.pth')
        config_path = os.path.join('agent-status', f'config_{timestamp}.csv')

        torch.save(agent.player_q_network.state_dict(), player_model_path)
        torch.save(agent.enemy_q_network.state_dict(), enemy_model_path)

        # config設定をCSV形式で保存
        config_data = {key: value for key, value in globals().items() if key.isupper()}
        config_data['NOTE'] = f"学習はエピソード {episode+1} で中断されました。"

        with open(config_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for key, value in config_data.items():
                writer.writerow([key, value])


        # エピソードごとの結果をCSVファイルに保存
        results_path = os.path.join('result', f'results_{timestamp}.csv')
        with open(results_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Episode', 'Total Player Reward', 'Total Enemy Reward', 'Elapsed Time', 'Total Steps'])
            writer.writerows(episode_results)
            
    env.close()