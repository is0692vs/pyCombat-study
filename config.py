# プレイヤーの報酬の設定
PLAYER_REWARD_HIT = 0.2  # 攻撃が当たった場合の報酬を増やす
PLAYER_PENALTY_MISS = -0.05  # 攻撃が外れた場合のペナルティを減らす
PLAYER_REWARD_KILL = 5  # 敵を倒した場合の報酬を増やす
PLAYER_PENALTY_LOSE = -5  # プレイヤーが負けた場合のペナルティを増やす
PLAYER_REWARD_DISTANCE_CLOSE = 0.02  # 敵に近づいた場合の報酬を増やす
PLAYER_PENALTY_DISTANCE_FAR = -0.03  # 敵から離れた場合のペナルティを増やす
PLAYER_PENALTY_ON_TOP = -0.5  # 相手の上に乗った場合のペナルティ
PLAYER_PENALTY_HIT = -0.2  # 攻撃を受けた場合のペナルティ

# 敵の報酬の設定
ENEMY_REWARD_HIT = 0.2  # 攻撃が当たった場合の報酬を増やす
ENEMY_PENALTY_MISS = -0.05  # 攻撃が外れた場合のペナルティを減らす
ENEMY_REWARD_KILL = 5  # プレイヤーを倒した場合の報酬を増やす
ENEMY_PENALTY_LOSE = -5  # 敵が負けた場合のペナルティを増やす
ENEMY_REWARD_DISTANCE_CLOSE = 0.02  # プレイヤーに近づいた場合の報酬を増やす
ENEMY_PENALTY_DISTANCE_FAR = -0.03  # プレイヤーから離れた場合のペナルティを増やす
ENEMY_PENALTY_ON_TOP = -0.5  # 相手の上に乗った場合のペナルティ
ENEMY_PENALTY_HIT = -0.2  # 攻撃を受けた場合のペナルティ

# フレームレートの設定
FRAME_RATE = 120  # ゲームのフレームレート

# 1エピソードでの対戦回数
BATTLES_PER_EPISODE = 20  

#学習ループのエピソード数
EPISODES = 150  

# ジャンプ許可の設定
CAN_JUMP = True

# DQNの初期化パラメータ
MEMORY_SIZE = 20000  # リプレイバッファのサイズ:エージェントが過去の経験を保存するためのバッファ
GAMMA = 0.99  # 割引率:0に近いほど短期的な報酬を重視し、1に近いほど長期的な報酬を重視する
EPSILON = 1.0  # 初期の探索率;初期にはランダムな行動を選択する(最大1.0)
EPSILON_MIN = 0.05  # 最小の探索率:エージェントが最後に探索を行う確率(常に少しの確率で探索を行う)
EPSILON_DECAY = 0.97  # 探索率の減衰率：１に近いほど急速に探索率が減少する
BATCH_SIZE = 64  # バッチサイズ:ミニバッチ学習のサイズ
UPDATE_TARGET_EVERY = 5  # ターゲットネットワークの更新間隔:何エピソードごとにターゲットネットワークを更新するか
LEARNING_RATE = 0.0005  # 学習率:ネットワークの重みを更新するステップサイズ