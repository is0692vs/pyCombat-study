#fighting_game_env.py
import pygame
import random
import numpy as np
from game import GROUND_Y

# ウィンドウのサイズを設定
WINDOW_WIDTH = 800  # 幅を指定
WINDOW_HEIGHT = 600  # 高さを指定

class FightingGameEnv:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.player.set_enemy(self.enemy)  # プレイヤーに敵を設定
        self.enemy.set_enemy(self.player)  # 敵にプレイヤーを設定
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.prev_distance = abs(self.player.position.x - self.enemy.position.x)  # 初期距離を設定

    def reset(self):
        # プレイヤーと敵の初期化
        self.player.hp = 100
        self.enemy.hp = 100
        self.player.position = pygame.Rect(100, GROUND_Y, 30, 60)
        self.enemy.position = pygame.Rect(500, GROUND_Y, 30, 60)
        self.player.is_down = False
        self.enemy.is_down = False
        self.player.down_counter = 0
        self.enemy.down_counter = 0
        self.prev_distance = abs(self.player.position.x - self.enemy.position.x)  # 初期距離を設定
        return self.get_state()

    def get_state(self):
        # 現在の状態を返す
        player_pos = (self.player.position.x, self.player.position.y)
        enemy_pos = (self.enemy.position.x, self.enemy.position.y)
        player_hp = self.player.hp
        enemy_hp = self.enemy.hp
        player_is_jumping = self.player.is_jumping
        enemy_is_jumping = self.enemy.is_jumping
        return np.array([player_pos[0], player_pos[1], enemy_pos[0], enemy_pos[1], player_hp, enemy_hp, player_is_jumping, enemy_is_jumping], dtype=np.float32)

    def step(self, action):
        player_action, enemy_action = action
        reward = 0

        # プレイヤーの行動
        if player_action == 0:
            self.player.move('left', self.enemy)
        elif player_action == 1:
            self.player.move('right', self.enemy)
        elif player_action == 2:
            self.player.jump()
        elif player_action == 3:
            if self.player.attack('punch', self.enemy):
                reward += 0.5  # 攻撃が当たった場合の報酬
            else:
                reward -= 0.1  # 攻撃が外れた場合のマイナス報酬
        elif player_action == 4:
            if self.player.attack('kick', self.enemy):
                reward += 0.5  # 攻撃が当たった場合の報酬
            else:
                reward -= 0.1  # 攻撃が外れた場合のマイナス報酬

        # 敵の行動
        if enemy_action == 0:
            self.enemy.move('left', self.player)
        elif enemy_action == 1:
            self.enemy.move('right', self.player)
        elif enemy_action == 2:
            self.enemy.jump()
        elif enemy_action == 3:
            if self.enemy.attack('punch', self.player):
                reward -= 0.5  # 敵の攻撃が当たった場合のマイナス報酬
            else:
                reward += 0.1  # 敵の攻撃が外れた場合の報酬
        elif enemy_action == 4:
            if self.enemy.attack('kick', self.player):
                reward -= 0.5  # 敵の攻撃が当たった場合のマイナス報酬
            else:
                reward += 0.1  # 敵の攻撃が外れた場合の報酬

        self.player.apply_gravity(self.enemy)
        self.enemy.apply_gravity(self.player)

        self.player.update()
        self.enemy.update()

        done = self.player.hp <= 0 or self.enemy.hp <= 0
        if self.enemy.hp <= 0:
            reward += 1  # 敵を倒した場合の報酬
    
        # 距離に基づいて報酬を調整
        current_distance = abs(self.player.position.x - self.enemy.position.x)
        if current_distance < self.prev_distance:  # 距離が縮まった場合に報酬を与える
            reward += 0.1
        self.prev_distance = current_distance
    
        # 相手の上に乗った場合のマイナス報酬
        if self.player.position.colliderect(self.enemy.position) and self.player.position.y + self.player.position.height <= self.enemy.position.y:
            reward -= 0.5
        if self.enemy.position.colliderect(self.player.position) and self.enemy.position.y + self.enemy.position.height <= self.player.position.y:
            reward -= 0.5
    
        return self.get_state(), reward, done

    def render(self):
        # ゲーム画面の描画
        self.screen.fill((169, 169, 169))  # 背景を灰色に設定
        pygame.draw.rect(self.screen, (0, 0, 255), self.player.position)  # プレイヤー
        pygame.draw.rect(self.screen, (255, 0, 0), self.enemy.position)   # 敵
        if self.player.attack_range_rect:
            pygame.draw.rect(self.screen, (255, 255, 0), self.player.attack_range_rect, 2)  # プレイヤーの攻撃範囲
        if self.enemy.attack_range_rect:
            pygame.draw.rect(self.screen, (255, 255, 0), self.enemy.attack_range_rect, 2)  # 敵の攻撃範囲
        self.player.draw_eyes(self.screen)
        self.enemy.draw_eyes(self.screen)
        self.player.draw_stats(self.screen, 10, 10)  # 位置を指定してステータスを描画
        self.enemy.draw_stats(self.screen, WINDOW_WIDTH - 200, 10)  # 位置を指定してステータスを描画
        pygame.display.flip()
        self.clock.tick(20)  # フレームレート
    
        # Pygameのイベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()