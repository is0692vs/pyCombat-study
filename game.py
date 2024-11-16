# game.py
import pygame
import csv

# ウィンドウと地面の設定
WINDOW_WIDTH, WINDOW_HEIGHT = 640, 480
GROUND_Y = WINDOW_HEIGHT+60   # 地面の高さ

# キャラクタークラス
class Character:
    def __init__(self, name, x, y, moveset_file, can_jump=True):
        self.name = name
        self.hp = 100
        self.down_counter = 0
        self.position = pygame.Rect(x, y, 30, 60)
        self.moves = self.load_moves(moveset_file)
        self.is_down = False
        self.down_time = 0
        self.speed = 10  # 移動速度
        self.jump_speed = 15
        self.gravity = 1  # 重力の強さ
        self.vertical_velocity = 0  # 垂直方向の速度
        self.is_jumping = False  # ジャンプ中かどうか
        self.direction = 'right'  # 向き ('right' または 'left')
        self.attack_timer = 0  # 攻撃範囲の表示タイマー
        self.attack_range_rect = None  # 攻撃範囲表示用
        self.can_attack = True  # 攻撃可能かどうかのフラグ
        self.enemy = None  # 敵キャラクターの参照を保持
        self.can_jump = can_jump  # ジャンプ許可フラグ

    def load_moves(self, moveset_file):
        moves = {}
        with open(moveset_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                moves[row['command']] = {
                    'damage': int(row['damage']),
                    'range': int(row.get('range', 0))  # 'range'列が存在しない場合はデフォルト値0を設定
                }
        return moves

    def set_enemy(self, enemy):
        self.enemy = enemy

    def draw_stats(self, screen, x, y):
        pygame.font.init()  # フォントモジュールの初期化
        font = pygame.font.Font(None, 36)

        # キャラクタの体力表示
        hp_text = font.render(f"HP: {self.hp}", True, (255, 255, 255))
        screen.blit(hp_text, (x, y))  # 指定位置に表示

        # キャラクタのダウンカウント表示
        down_counter_text = font.render(f"Down: {self.down_counter}", True, (255, 255, 255))
        screen.blit(down_counter_text, (x, y + 40))  # 指定位置に表示

    def draw_eyes(self, screen):
        # 目を描画するための簡単な例
        eye_color = (255, 255, 255)
        if self.direction == 'right':
            left_eye = pygame.Rect(self.position.x + 15, self.position.y + 10, 5, 5)
            right_eye = pygame.Rect(self.position.x + 25, self.position.y + 10, 5, 5)
        else:
            left_eye = pygame.Rect(self.position.x + 5, self.position.y + 10, 5, 5)
            right_eye = pygame.Rect(self.position.x + 15, self.position.y + 10, 5, 5)
        pygame.draw.rect(screen, eye_color, left_eye)
        pygame.draw.rect(screen, eye_color, right_eye)

    def move(self, direction, opponent):
        if direction == 'left':
            self.move_left()
        elif direction == 'right':
            self.move_right()
        self.apply_gravity(opponent)

    def move_left(self):
        new_position = self.position.move(-self.speed, 0)
        if not new_position.colliderect(self.enemy.position):  # 敵と重ならない場合のみ移動
            self.position = new_position
        self.direction = 'left'
        self.position.x = max(0, min(self.position.x, WINDOW_WIDTH - self.position.width))
    
    def move_right(self):
        new_position = self.position.move(self.speed, 0)
        if not new_position.colliderect(self.enemy.position):  # 敵と重ならない場合のみ移動
            self.position = new_position
        self.direction = 'right'
        self.position.x = max(0, min(self.position.x, WINDOW_WIDTH - self.position.width))

    def jump(self):
        if self.can_jump and not self.is_jumping:  # ジャンプ許可フラグとジャンプ中でない場合のみジャンプ
            self.vertical_velocity = -self.jump_speed
            self.is_jumping = True  

    def apply_gravity(self, opponent):
        if self.is_jumping:
            self.vertical_velocity += self.gravity  # 重力を加える
            new_position = self.position.move(0, self.vertical_velocity)
    
            # 他のキャラクターと重なりをチェックせず、垂直移動
            if new_position.colliderect(opponent.position):
                # 敵の上に乗らないように調整
                if self.position.y + self.position.height <= opponent.position.y:
                    self.position.y = opponent.position.y - self.position.height  # 敵の上に乗らないように
                    self.vertical_velocity = -self.jump_speed  # もう一度ジャンプ
                    self.is_jumping = True  # ジャンプ継続
                else:
                    self.position = new_position  # 他の場所での移動はそのまま
            else:
                self.position = new_position
    
            # 地面に着いたらジャンプを終了
            if self.position.y >= GROUND_Y:
                self.position.y = GROUND_Y
                self.is_jumping = False
                self.vertical_velocity = 0

    def attack(self, move_name, enemy):
        if self.can_attack and move_name in self.moves:
            move = self.moves[move_name]
            attack_range = move['range']
            damage = move['damage']
    
            if self.direction == 'right':
                attack_rect = pygame.Rect(self.position.right, self.position.top, attack_range, self.position.height)
            else:
                attack_rect = pygame.Rect(self.position.left - attack_range, self.position.top, attack_range, self.position.height)
    
            if attack_rect.colliderect(enemy.position):
                enemy.hp -= damage
                if enemy.hp <= 0:
                    enemy.hp = 0
                    enemy.is_down = True
                    enemy.down_counter += 1
    
                self.attack_timer = 10  # 攻撃範囲の表示時間
                self.attack_range_rect = attack_rect
                self.can_attack = False  # 攻撃後は一時的に攻撃不可
                return True  # 攻撃が当たった場合
            else:
                self.attack_timer = 10  # 攻撃範囲の表示時間
                self.attack_range_rect = attack_rect
                self.can_attack = False  # 攻撃後は一時的に攻撃不可
                return False  # 攻撃が外れた場合
        return False  # 攻撃が実行されなかった場合

    def update(self):
        if self.attack_timer > 0:
            self.attack_timer -= 1
        else:
            self.attack_range_rect = None
            self.can_attack = True  # 攻撃可能に戻す

# 環境クラス
class FightingGameEnv:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Fighting Game')

    def step(self, action):
        player_action, enemy_action = action
    
        # プレイヤーの行動
        if player_action == 0:
            self.player.move('left', self.enemy)
        elif player_action == 1:
            self.player.move('right', self.enemy)
        elif player_action == 2:
            self.player.jump()
        elif player_action == 3:
            self.player.attack('punch', self.enemy)
        elif player_action == 4:
            self.player.attack('kick', self.enemy)
    
        # 敵の行動
        if enemy_action == 0:
            self.enemy.move('left', self.player)
        elif enemy_action == 1:
            self.enemy.move('right', self.player)
        elif enemy_action == 2:
            self.enemy.jump()
        elif enemy_action == 3:
            self.enemy.attack('punch', self.player)
        elif enemy_action == 4:
            self.enemy.attack('kick', self.player)
    
        self.player.apply_gravity(self.enemy)
        self.enemy.apply_gravity(self.player)
    
        self.player.update()
        self.enemy.update()
    
        done = self.player.hp <= 0 or self.enemy.hp <= 0
        reward = 1 if self.enemy.hp <= 0 else 0
    
        # 距離に基づいて報酬を調整
        current_distance = abs(self.player.position.x - self.enemy.position.x)
        if current_distance < self.prev_distance:  # 距離が縮まった場合に報酬を与える
            reward += 0.1
        self.prev_distance = current_distance
    
        return self.get_state(), reward, done

    def get_state(self):
        return [
            self.player.position.x, self.player.position.y, self.player.hp, self.player.down_counter,
            self.enemy.position.x, self.enemy.position.y, self.enemy.hp, self.enemy.down_counter
        ]

    def render(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 0, 0), self.player.position)
        pygame.draw.rect(self.screen, (0, 0, 255), self.enemy.position)
    
        self.player.draw_stats(self.screen, 10, 10)  # キャラクタ1のステータス表示
        self.enemy.draw_stats(self.screen, WINDOW_WIDTH - 200, 10)  # キャラクタ2のステータス表示
    
        self.player.draw_eyes(self.screen)  # 目を描画
        self.enemy.draw_eyes(self.screen)  # 目を描画
    
        if self.player.attack_range_rect:
            pygame.draw.rect(self.screen, (255, 255, 0), self.player.attack_range_rect, 2)
    
        pygame.display.flip()
    def close(self):
        pygame.quit()