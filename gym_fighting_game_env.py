#gym_fighting_game_env.py
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame

from fighting_game_env import FightingGameEnv
from game import Character, WINDOW_WIDTH, WINDOW_HEIGHT, GROUND_Y

class GymFightingGameEnv(gym.Env):
    def __init__(self):
        super(GymFightingGameEnv, self).__init__()
        player = Character('Player', 100, GROUND_Y, 'moves.csv', can_jump=True)
        enemy = Character('Enemy', 500, GROUND_Y, 'moves.csv', can_jump=True)
        enemy.direction = 'left'
        self.env = FightingGameEnv(player, enemy)
        self.action_space = spaces.Discrete(6)  # 何もしない、左移動、右移動、ジャンプ、パンチ、キック
        self.observation_space = spaces.Box(low=0, high=WINDOW_WIDTH, shape=(8,), dtype=np.float32)  # 8次元状態

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        state = self.env.reset()
        return np.array(state, dtype=np.float32), {}

    def step(self, action):
        state, reward, done = self.env.step(action)
        terminated = done
        truncated = False  # 必要に応じて設定
        player_reward, enemy_reward = reward  # 報酬をタプルに分解
        return np.array(state, dtype=np.float32), (player_reward, enemy_reward), terminated, truncated, {}

    def render(self, mode='human'):
        self.env.render()

    def close(self):
        pygame.quit()