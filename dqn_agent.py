# dqn_agent.py
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
from config import (
    MEMORY_SIZE, GAMMA, EPSILON, EPSILON_MIN, EPSILON_DECAY, BATCH_SIZE, UPDATE_TARGET_EVERY, LEARNING_RATE
)
import torch.optim.lr_scheduler as lr_scheduler

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
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
        self.update_target_network()
        self.player_optimizer = optim.Adam(self.player_q_network.parameters(), lr=LEARNING_RATE)
        self.enemy_optimizer = optim.Adam(self.enemy_q_network.parameters(), lr=LEARNING_RATE)
        self.player_scheduler = lr_scheduler.StepLR(self.player_optimizer, step_size=100, gamma=0.9)
        self.enemy_scheduler = lr_scheduler.StepLR(self.enemy_optimizer, step_size=100, gamma=0.9)

    def _build_model(self):
        model = nn.Sequential(
            nn.Linear(self.state_size, 24),
            nn.ReLU(),
            nn.Linear(24, 24),
            nn.ReLU(),
            nn.Linear(24, self.action_size)
        )
        return model

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

    def learn(self, is_player=True):
        if len(self.memory) < self.batch_size:
            return
        experiences = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*experiences)
        states = torch.FloatTensor(states)
        rewards = torch.FloatTensor([reward[0] if is_player else reward[1] for reward in rewards])
        next_states = torch.FloatTensor(next_states)
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

    def update_target_network(self):
        self.player_target_network.load_state_dict(self.player_q_network.state_dict())
        self.enemy_target_network.load_state_dict(self.enemy_q_network.state_dict())