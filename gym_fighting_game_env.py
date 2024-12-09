#gym_fighting_game_env.pyは学習の環境系
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame

from fighting_game_env import FightingGameEnv
from game import Character, GROUND_Y
from config import CAN_JUMP, WINDOW_WIDTH  # 
from config import FRAME_HP_DIFFERENCES_REWARD_RATE #FTGICEの論文で出てたフレームステップごとの体力変化を報酬にするやつの倍率

class GymFightingGameEnv(gym.Env):
    def __init__(self, single_train=False):
        super(GymFightingGameEnv, self).__init__()
        player = Character('Player', 100, GROUND_Y, 'moves.csv', can_jump=CAN_JUMP)
        enemy = Character('Enemy', 500, GROUND_Y, 'moves.csv', can_jump=CAN_JUMP)
        enemy.direction = 'left'
        self.env = FightingGameEnv(player, enemy, single_train=single_train)
        self.action_space = spaces.Discrete(7)  # 何もしない、左移動、右移動、ジャンプ、パンチ、キック、上攻撃
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(10,), dtype=np.float32  # 状態ベクトルのサイズを更新
        )
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        state = self.env.reset()
        self.prev_player_hp = self.env.player.hp
        self.prev_enemy_hp = self.env.enemy.hp
        return np.array(state, dtype=np.float32), {}

    def step(self, action):
        state, reward, done = self.env.step(action)
        terminated = done
        truncated = False  # 必要に応じて設定
        player_reward, enemy_reward = reward  # 報酬をタプルに分解

        # フレームステップごとの体力変化量に基づく報酬を追加
        current_player_hp = self.env.player.hp
        current_enemy_hp = self.env.enemy.hp
        player_hp_change = self.prev_player_hp - current_player_hp
        enemy_hp_change = self.prev_enemy_hp - current_enemy_hp

        # 体力変化量に基づく報酬を追加
        player_reward += (enemy_hp_change - player_hp_change) * FRAME_HP_DIFFERENCES_REWARD_RATE
        if not self.env.single_train:
            enemy_reward += (player_hp_change - enemy_hp_change) * FRAME_HP_DIFFERENCES_REWARD_RATE

        # if self.env.single_train:
        #     enemy_reward = 0  # single_trainの場合、エネミーの報酬を0にする

        total_reward = player_reward + enemy_reward  # プレイヤーとエネミーの報酬を合計

        # 前のフレームの体力を更新
        self.prev_player_hp = current_player_hp
        self.prev_enemy_hp = current_enemy_hp

        return np.array(state, dtype=np.float32), total_reward, terminated, truncated, {}

    def render(self, mode='human'):
        self.env.render()

    def close(self):
        pygame.quit()