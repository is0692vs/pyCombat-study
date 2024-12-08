# dqn_agent.pyは以下の通りです。
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
from config import (
    MEMORY_SIZE, GAMMA, EPSILON, EPSILON_MIN, EPSILON_DECAY, BATCH_SIZE, UPDATE_TARGET_EVERY, LEARNING_RATE,
    LR_STEP_SIZE, LR_GAMMA
)
import torch.optim.lr_scheduler as lr_scheduler

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size  # 自分と相手の行動分を追加
        self.action_size = action_size
        self.memory = deque(maxlen=MEMORY_SIZE)
        self.gamma = GAMMA
        self.epsilon = EPSILON
        self.epsilon_min = EPSILON_MIN
        self.epsilon_decay = EPSILON_DECAY
        self.batch_size = BATCH_SIZE
        self.update_target_every = UPDATE_TARGET_EVERY
        self.player_q_network = self._build_model()
        self.enemy_q_network = self._build_model()
        self.player_target_network = self._build_model()
        self.enemy_target_network = self._build_model()
        self.update_target_network(is_player=True)
        self.update_target_network(is_player=False)
        self.player_optimizer = optim.Adam(self.player_q_network.parameters(), lr=LEARNING_RATE)
        self.enemy_optimizer = optim.Adam(self.enemy_q_network.parameters(), lr=LEARNING_RATE)
        self.player_scheduler = lr_scheduler.StepLR(self.player_optimizer, step_size=LR_STEP_SIZE, gamma=LR_GAMMA)
        self.enemy_scheduler = lr_scheduler.StepLR(self.enemy_optimizer, step_size=LR_STEP_SIZE, gamma=LR_GAMMA)

    def _build_model(self):
        model = nn.Sequential(
            nn.Linear(self.state_size, 24),
            nn.ReLU(),
            nn.Linear(24, 24),
            nn.ReLU(),
            nn.Linear(24, self.action_size)
        )
        return model
    
    def load_model(self, player_model_path=None, enemy_model_path=None):
        if player_model_path:
            self.player_q_network.load_state_dict(torch.load(player_model_path))
            self.update_target_network(is_player=True)
        if enemy_model_path:
            self.enemy_q_network.load_state_dict(torch.load(enemy_model_path))
            self.update_target_network(is_player=False)

    def act(self, state, is_player=True):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        state = torch.FloatTensor(state).unsqueeze(0)
        if is_player:
            q_values = self.player_q_network(state)
        else:
            q_values = self.enemy_q_network(state)
        return q_values.max(1)[1].item()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def learn(self, is_player=True, single_train=False):
        if len(self.memory) < self.batch_size:
            return
        experiences = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*experiences)
        states = torch.FloatTensor(np.array(states))
        if single_train:
            rewards = torch.FloatTensor(rewards)  # 報酬をそのまま使用
        else:
            rewards = torch.FloatTensor([reward[0] if is_player else reward[1] for reward in rewards])
        next_states = torch.FloatTensor(np.array(next_states))
        dones = torch.FloatTensor(dones)

        # actions を整形
        actions = torch.LongTensor([action[0] if is_player else action[1] for action in actions]).unsqueeze(1)

        if is_player:
            q_values = self.player_q_network(states).gather(1, actions).squeeze(1)
            next_q_values = self.player_target_network(next_states).max(1)[0]
            optimizer = self.player_optimizer
            scheduler = self.player_scheduler
        else:
            q_values = self.enemy_q_network(states).gather(1, actions).squeeze(1)
            next_q_values = self.enemy_target_network(next_states).max(1)[0]
            optimizer = self.enemy_optimizer
            scheduler = self.enemy_scheduler

        target_q_values = rewards + self.gamma * next_q_values * (1 - dones)

        loss = nn.MSELoss()(q_values, target_q_values)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        scheduler.step()  # 学習率を更新

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_target_network(self, is_player=True):
        if is_player:
            self.player_target_network.load_state_dict(self.player_q_network.state_dict())
        else:
            self.enemy_target_network.load_state_dict(self.enemy_q_network.state_dict())