# game.pyは以下の通りです。
import pygame
import csv
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, CHARACTER_HP, CHARACTER_WIDTH, CHARACTER_HEIGHT, MAX_DOWN_COUNT, DOWN_LENGTH, DOWNCOUNT_DECREASE_RATE, DOWNED_PENALTY
)

GROUND_Y = WINDOW_HEIGHT - CHARACTER_HEIGHT   # 地面の高さ

class Character:
    def __init__(self, name, x, y, moveset_file, can_jump=True):
        self.name = name
        self.hp = CHARACTER_HP
        self.down_counter = 0
        self.position = pygame.Rect(x, y, CHARACTER_WIDTH, CHARACTER_HEIGHT)
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
        self.step_count = 0  # ステップカウント


    def set_enemy(self, enemy):
        self.enemy = enemy

        
    def load_moves(self, moveset_file):
        moves = {}
        with open(moveset_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                moves[row['command']] = {
                    'damage': int(row['damage']),
                    'x1_offset': int(row['x1_offset']),
                    'y1_offset': int(row['y1_offset']),
                    'x2_offset': int(row['x2_offset']),
                    'y2_offset': int(row['y2_offset']),
                    'down_counter_add': int(row['down_counter_add']),
                    'duration': int(row['duration']),
                    'range': int(row['range'])
                }
        return moves


    def draw(self, screen):
        # プレイヤーと敵の色を設定
        if self.name == 'Player':
            base_color = (0, 0, 255)  # 青
        else:
            base_color = (255, 0, 0)  # 赤

        # ダウン状態の時のみ色を薄くする
        if self.is_down:
            color = tuple(int(c * 0.1) for c in base_color)
        else:
            color = base_color

        pygame.draw.rect(screen, color, self.position)
        
        
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
            damage = move['damage']
            x1_offset = move['x1_offset']
            y1_offset = move['y1_offset']
            x2_offset = move['x2_offset']
            y2_offset = move['y2_offset']

            if self.direction == 'right':
                attack_rect = pygame.Rect(
                    self.position.right + x1_offset,  # 攻撃範囲の左下のx座標
                    self.position.top + y1_offset,    # 攻撃範囲の左下のy座標
                    x2_offset - x1_offset,           # 攻撃範囲の幅
                    y2_offset - y1_offset            # 攻撃範囲の高さ
                )
            else:
                attack_rect = pygame.Rect(
                    self.position.left - x2_offset,  # 攻撃範囲の左下のx座標
                    self.position.top + y1_offset,   # 攻撃範囲の左下のy座標
                    x2_offset - x1_offset,           # 攻撃範囲の幅
                    y2_offset - y1_offset            # 攻撃範囲の高さ
                )

            if attack_rect.colliderect(enemy.position):
                enemy.hp -= damage
                if not enemy.is_down:  # 敵がダウン状態でない場合にのみダウンカウントを加算
                    enemy.down_counter += move['down_counter_add']
                    if enemy.down_counter >= MAX_DOWN_COUNT:
                        enemy.is_down = True
                        enemy.down_time = DOWN_LENGTH
                        print(f'{enemy.name} is down!')
                        enemy.down_counter = 0  # ダウンカウントをリセット

                if enemy.hp <= 0:
                    enemy.hp = 0
                    enemy.is_down = True

                self.attack_timer = move['duration']  # 攻撃範囲の表示時間
                self.attack_range_rect = attack_rect
                self.can_attack = False  # 攻撃後は一時的に攻撃不可
                return True  # 攻撃が当たった場合
            else:
                self.attack_timer = move['duration']  # 攻撃範囲の表示時間
                self.attack_range_rect = attack_rect
                self.can_attack = False  # 攻撃後は一時的に攻撃不可
                return False  # 攻撃が外れた場合
        return False  # 攻撃が実行されなかった場合

    def update(self):
        self.step_count += 1

        if self.attack_timer > 0:
            self.attack_timer -= 1
        else:
            self.attack_range_rect = None
            self.can_attack = True  # 攻撃可能に戻す

        if self.is_down:
            self.down_time -= 1
            if self.down_time <= 0:
                self.is_down = False

        if self.step_count % DOWNCOUNT_DECREASE_RATE == 0:
            self.down_counter = max(0, self.down_counter - 1)  # ダウンカウントを減少


        # ダウン状態の変化を検出してペナルティを適用
        if self.is_down and not self.was_down:
            # print("test3")
            self.reward += DOWNED_PENALTY

        # ダウン状態の変化を記録
        self.was_down = self.is_down
