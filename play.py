#play.pyを実行すると、学習済みモデルを使ってゲームをプレイすることができます。
import gymnasium as gym
import torch
from dqn_agent import DQNAgent
import pygame
import time
from game import GROUND_Y  
from config import FRAME_RATE, MAX_STEPS, BATTLES_PER_EPISODE, INITIAL_PLAYER_REWARD, INITIAL_ENEMY_REWARD  # フレームレート、最大ステップ数、対戦回数、初期報酬をインポート 

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
env = gym.make('FightingGame-v0')

# state_sizeとaction_sizeを取得
state_size = env.observation_space.shape[0] + 2  # 現在の行動分を追加
action_size = env.action_space.n

# DQNAgentのインスタンスを作成
agent = DQNAgent(state_size, action_size)


# 学習済みモデルのロード関数
def load_model(agent, player_model_path, enemy_model_path):
    agent.player_q_network.load_state_dict(torch.load(player_model_path))
    agent.enemy_q_network.load_state_dict(torch.load(enemy_model_path))
    agent.update_target_network()

# 学習済みモデルのロード
player_model_path = 'player-agent/player_2024-11-21-09:20_Qnet.pth'  # 実際のファイルパス
enemy_model_path = 'enemy-agent/enemy_2024-11-21-09:20_Qnet.pth'  # 実際のファイルパス
load_model(agent, player_model_path, enemy_model_path)



# 探索率を低く設定
agent.epsilon = 0.01

# 勝利数と時間切れのカウントを初期化
player_wins = 0
enemy_wins = 0
timeouts = 0

# 初期報酬を設定
total_player_reward = INITIAL_PLAYER_REWARD
total_enemy_reward = INITIAL_ENEMY_REWARD

# 指定した回数だけ連続で対戦
for battle in range(BATTLES_PER_EPISODE):
    env.unwrapped.env.current_battle = battle + 1  # 現在の試合数を設定
    state, _ = env.reset()
    done = False
    step_count = 0
    while not done and step_count < MAX_STEPS:
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
        env.render()
        clock.tick(FRAME_RATE)  # フレームレートの制御

        # 報酬が発生した時にログを記録
        if player_reward != 0 or enemy_reward != 0:
            # print(f"Step: {step_count}, Action: {action}, Player Reward: {player_reward}, Enemy Reward: {enemy_reward}, Total Player Reward: {total_player_reward}, Total Enemy Reward: {total_enemy_reward}")
            pass

    # 勝利数と時間切れのカウントを更新
    if step_count >= MAX_STEPS:
        timeouts += 1
    elif env.unwrapped.env.enemy.hp <= 0:
        player_wins += 1
    elif env.unwrapped.env.player.hp <= 0:
        enemy_wins += 1

# 結果を表示
print(f"Player Wins: {player_wins}/{BATTLES_PER_EPISODE}")
print(f"Enemy Wins: {enemy_wins}/{BATTLES_PER_EPISODE}")
print(f"Timeouts: {timeouts}/{BATTLES_PER_EPISODE}")

# 環境を閉じる
env.close()