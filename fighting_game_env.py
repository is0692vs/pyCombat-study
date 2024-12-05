#fighting_game_env.pyは以下の通りです。
import pygame
import numpy as np
from game import GROUND_Y, WINDOW_WIDTH
from config import (
    PLAYER_REWARD_HIT, PLAYER_PENALTY_MISS, PLAYER_REWARD_KILL, PLAYER_REWARD_DISTANCE_CLOSE, PLAYER_PENALTY_DISTANCE_FAR, PLAYER_PENALTY_ON_TOP, PLAYER_PENALTY_HIT,
    ENEMY_REWARD_HIT, ENEMY_PENALTY_MISS, ENEMY_REWARD_KILL, ENEMY_REWARD_DISTANCE_CLOSE, ENEMY_PENALTY_DISTANCE_FAR, ENEMY_PENALTY_ON_TOP, ENEMY_PENALTY_HIT,
    FRAME_RATE,  # フレームレートをインポート
    PLAYER_PENALTY_LOSE, ENEMY_PENALTY_LOSE,  # 負けた時のペナルティをインポート
    EDGE_PENALTY, NO_PENALTY_AREA_WIDTH,  # ペナルティの設定をインポート
    WINDOW_WIDTH, WINDOW_HEIGHT,  # ウィンドウの大きさの設定をインポート
    MAX_STEPS, # 最大ステップ数をインポート
    HEALTH_DIFFERENCE_REWARD_RATE, # 体力差に基づく報酬の倍率をインポート
    BATTLES_PER_EPISODE,  # 1エピソードでの対戦回数をインポート
    CHARACTER_WIDTH, CHARACTER_HEIGHT, # キャラクタの幅、高さをインポート
    CHARACTER_DISTANCE,  # 初期距離をインポート
    CHARACTER_HP, #キャラクタの体力をインポート
    INITIAL_PLAYER_REWARD, INITIAL_ENEMY_REWARD
)

# ペナルティを受けないエリアの開始位置と終了位置を計算
NO_PENALTY_AREA_START = (WINDOW_WIDTH // 2) - (NO_PENALTY_AREA_WIDTH // 2)
NO_PENALTY_AREA_END = (WINDOW_WIDTH // 2) + (NO_PENALTY_AREA_WIDTH // 2)

class FightingGameEnv:
    def __init__(self, player, enemy, single_train=False):
        self.player = player
        self.enemy = enemy
        self.player.set_enemy(self.enemy)  # プレイヤーに敵を設定
        self.enemy.set_enemy(self.player)  # 敵にプレイヤーを設定
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.prev_distance = abs(self.player.position.x - self.enemy.position.x)  # 初期距離を設定
        self.step_count = 0  # ステップ数を初期化
        self.current_battle = 0  # 現在の試合数を初期化
        self.player_reward = INITIAL_PLAYER_REWARD
        self.enemy_reward = INITIAL_ENEMY_REWARD
        self.player_action = 0
        self.enemy_action = 0
        self.single_train = single_train

    def reset(self):
        # プレイヤーと敵の初期化
        self.player.hp = CHARACTER_HP
        self.enemy.hp = CHARACTER_HP
        center_x = WINDOW_WIDTH // 2
        self.player.position = pygame.Rect(center_x - CHARACTER_DISTANCE // 2, GROUND_Y, CHARACTER_WIDTH, CHARACTER_HEIGHT)  # プレイヤーの初期位置を設定
        self.enemy.position = pygame.Rect(center_x + CHARACTER_DISTANCE // 2, GROUND_Y, CHARACTER_WIDTH, CHARACTER_HEIGHT)  # 敵の初期位置を設定
        self.player.is_down = False
        self.enemy.is_down = False
        self.player.down_counter = 0
        self.enemy.down_counter = 0
        self.prev_distance = abs(self.player.position.x - self.enemy.position.x)  # 初期距離を設定
        self.step_count = 0  # ステップ数をリセット
        self.player_reward = INITIAL_PLAYER_REWARD
        self.enemy_reward = INITIAL_ENEMY_REWARD
        return self.get_state()

    def get_state(self):
        # 現在の状態を返す
        player_pos = (self.player.position.x, self.player.position.y)
        enemy_pos = (self.enemy.position.x, self.enemy.position.y)
        player_hp = self.player.hp
        enemy_hp = self.enemy.hp
        player_is_jumping = self.player.is_jumping
        enemy_is_jumping = self.enemy.is_jumping
        return np.array([
            player_pos[0], player_pos[1], enemy_pos[0], enemy_pos[1],
            player_hp, enemy_hp, player_is_jumping, enemy_is_jumping,
            self.player_action, self.enemy_action  # 現在の行動を追加
        ], dtype=np.float32)

    def step(self, action):
        player_action, enemy_action = action
        self.player_action = player_action
        self.enemy_action = enemy_action
        player_reward = 0
        enemy_reward = 0
        self.step_count += 1  # ステップ数をカウント

        # プレイヤーの行動
        if player_action == 0:
            pass  # 何もしない
        elif player_action == 1:
            self.player.move('left', self.enemy)
        elif player_action == 2:
            self.player.move('right', self.enemy)
        elif player_action == 3:
            self.player.jump()
        elif player_action == 4:
            if self.player.attack('punch', self.enemy):
                player_reward += PLAYER_REWARD_HIT  # 攻撃が当たった場合の報酬
                enemy_reward += ENEMY_PENALTY_HIT  # 攻撃を受けた場合のペナルティ
            else:
                player_reward += PLAYER_PENALTY_MISS  # 攻撃が外れた場合のペナルティ
        elif player_action == 5:
            if self.player.attack('kick', self.enemy):
                player_reward += PLAYER_REWARD_HIT  # 攻撃が当たった場合の報酬
                enemy_reward += ENEMY_PENALTY_HIT  # 攻撃を受けた場合のペナルティ
            else:
                player_reward += PLAYER_PENALTY_MISS  # 攻撃が外れた場合のペナルティ
        elif player_action == 6:
            if self.player.attack('uppercut', self.enemy):  # 前上方向への攻撃
                player_reward += PLAYER_REWARD_HIT  # 攻撃が当たった場合の報酬
                enemy_reward += ENEMY_PENALTY_HIT  # 攻撃を受けた場合のペナルティ
            else:
                player_reward += PLAYER_PENALTY_MISS  # 攻撃が外れた場合のペナルティ

        # 敵の行動
        if enemy_action == 0:
            pass  # 何もしない
        elif enemy_action == 1:
            self.enemy.move('left', self.player)
        elif enemy_action == 2:
            self.enemy.move('right', self.player)
        elif enemy_action == 3:
            self.enemy.jump()
        elif enemy_action == 4:
            if self.enemy.attack('punch', self.player):
                enemy_reward += ENEMY_REWARD_HIT  # 攻撃が当たった場合の報酬
                player_reward += PLAYER_PENALTY_HIT  # 攻撃を受けた場合のペナルティ
            else:
                enemy_reward += ENEMY_PENALTY_MISS  # 攻撃が外れた場合のペナルティ
        elif enemy_action == 5:
            if self.enemy.attack('kick', self.player):
                enemy_reward += ENEMY_REWARD_HIT  # 攻撃が当たった場合の報酬
                player_reward += PLAYER_PENALTY_HIT  # 攻撃を受けた場合のペナルティ
            else:
                enemy_reward += ENEMY_PENALTY_MISS  # 攻撃が外れた場合のペナルティ
        elif enemy_action == 6:
            if self.enemy.attack('uppercut', self.player):  # 前上方向への攻撃
                enemy_reward += ENEMY_REWARD_HIT  # 攻撃が当たった場合の報酬
                player_reward += PLAYER_PENALTY_HIT  # 攻撃を受けた場合のペナルティ
            else:
                enemy_reward += ENEMY_PENALTY_MISS  # 攻撃が外れた場合のペナルティ

        self.player.apply_gravity(self.enemy)
        self.enemy.apply_gravity(self.player)

        self.player.update()
        self.enemy.update()

        done = self.player.hp <= 0 or self.enemy.hp <= 0
        if done or self.step_count >= MAX_STEPS:
            # 試合終了時点での体力差*倍率を報酬に追加
            health_difference_reward = (self.player.hp - self.enemy.hp) * HEALTH_DIFFERENCE_REWARD_RATE
            player_reward += health_difference_reward 
            enemy_reward -= health_difference_reward
        if self.enemy.hp <= 0:
            player_reward += PLAYER_REWARD_KILL  # 敵を倒した場合の報酬
            enemy_reward += ENEMY_PENALTY_LOSE  # 敵が負けた場合のペナルティ
        if self.player.hp <= 0:
            enemy_reward += ENEMY_REWARD_KILL  # プレイヤーを倒した場合の報酬
            player_reward += PLAYER_PENALTY_LOSE  # プレイヤーが負けた場合のペナルティ

        # 距離に基づいて報酬を調整
        current_distance = abs(self.player.position.x - self.enemy.position.x)
        if current_distance < self.prev_distance:  # 距離が縮まった場合に報酬を与える
            player_reward += PLAYER_REWARD_DISTANCE_CLOSE
            enemy_reward += ENEMY_REWARD_DISTANCE_CLOSE
        else:  # 距離が広がった場合にペナルティを与える
            player_reward += PLAYER_PENALTY_DISTANCE_FAR
            enemy_reward += ENEMY_PENALTY_DISTANCE_FAR
        self.prev_distance = current_distance

        # 敵に近づく移動に対する報酬
        if player_action in [1, 2] and current_distance < self.prev_distance:
            player_reward += 0.1
        if enemy_action in [1, 2] and current_distance < self.prev_distance:
            enemy_reward += 0.1

        # 相手の上に乗った場合のペナルティ
        if self.player.position.colliderect(self.enemy.position) and self.player.position.y + self.player.position.height <= self.enemy.position.y:
            player_reward += PLAYER_PENALTY_ON_TOP
        if self.enemy.position.colliderect(self.player.position) and self.enemy.position.y + self.enemy.position.height <= self.player.position.y:
            enemy_reward += ENEMY_PENALTY_ON_TOP

        # 画面端に行くにつれてマイナスの報酬を与える
        if self.player.position.x < NO_PENALTY_AREA_START:
            player_reward += ((NO_PENALTY_AREA_START - self.player.position.x) / NO_PENALTY_AREA_START) * EDGE_PENALTY
        elif self.player.position.x > NO_PENALTY_AREA_END:
            player_reward += ((self.player.position.x - NO_PENALTY_AREA_END) / (WINDOW_WIDTH - NO_PENALTY_AREA_END)) * EDGE_PENALTY

        if self.enemy.position.x < NO_PENALTY_AREA_START:
            enemy_reward += ((NO_PENALTY_AREA_START - self.enemy.position.x) / NO_PENALTY_AREA_START) * EDGE_PENALTY
        elif self.enemy.position.x > NO_PENALTY_AREA_END:
            enemy_reward += ((self.enemy.position.x - NO_PENALTY_AREA_END) / (WINDOW_WIDTH - NO_PENALTY_AREA_END)) * EDGE_PENALTY
        
        
        
        if self.single_train:
            enemy_reward = 0  # single_trainの場合、エネミーの報酬を0にする
        total_reward = (player_reward, enemy_reward)
        return self.get_state(), total_reward, done

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
        self.enemy.draw_stats(self.screen, WINDOW_WIDTH - 120, 10)  # 位置を指定してステータスを描画
        
        

        # 試合数の表示
        pygame.font.init()
        font = pygame.font.Font(None, 36)
        battle_text = font.render(f"{self.current_battle}/{BATTLES_PER_EPISODE}", True, (255, 255, 255))
        text_width, text_height = font.size(f"{self.current_battle}/{BATTLES_PER_EPISODE}")
        text_rect = battle_text.get_rect(center=(WINDOW_WIDTH // 2, 20))
        self.screen.blit(battle_text, (WINDOW_WIDTH // 2 - text_width // 2, 20))
        
        pygame.display.flip()
        self.clock.tick(FRAME_RATE)  # フレームレート

        # Pygameのイベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()