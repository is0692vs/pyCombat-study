# プレイヤーの報酬の設定
PLAYER_REWARD_HIT = 0.5  # 攻撃が当たった場合の報酬
PLAYER_PENALTY_MISS = -0.1  # 攻撃が外れた場合のペナルティ
PLAYER_REWARD_KILL = 5  # 敵を倒した場合の報酬
PLAYER_PENALTY_LOSE = -5  # プレイヤーが負けた場合のペナルティ
PLAYER_REWARD_DISTANCE_CLOSE = 0.05  # 敵に近づいた場合の報酬
PLAYER_PENALTY_DISTANCE_FAR = -0.05  # 敵から離れた場合のペナルティ
PLAYER_PENALTY_ON_TOP = -0.5  # 相手の上に乗った場合のペナルティ
PLAYER_PENALTY_HIT = -0.2  # 攻撃を受けた場合のペナルティ

# 敵の報酬の設定
ENEMY_REWARD_HIT = 0.5  # 攻撃が当たった場合の報酬
ENEMY_PENALTY_MISS = -0.1  # 攻撃が外れた場合のペナルティ
ENEMY_REWARD_KILL = 5  # プレイヤーを倒した場合の報酬
ENEMY_PENALTY_LOSE = -5  # 敵が負けた場合のペナルティ
ENEMY_REWARD_DISTANCE_CLOSE = 0.05  # プレイヤーに近づいた場合の報酬
ENEMY_PENALTY_DISTANCE_FAR = -0.05  # プレイヤーから離れた場合のペナルティ
ENEMY_PENALTY_ON_TOP = -0.5  # 相手の上に乗った場合のペナルティ
ENEMY_PENALTY_HIT = -0.2  # 攻撃を受けた場合のペナルティ

# フレームレートの設定
FRAME_RATE = 120  # ゲームのフレームレート

# 1エピソードでの対戦回数
BATTLES_PER_EPISODE = 5  # 1エピソードでの対戦回数

# DQNの初期化パラメータ
MEMORY_SIZE = 10000  # リプレイバッファのサイズ
GAMMA = 0.95  # 割引率
EPSILON = 1.0  # 初期の探索率
EPSILON_MIN = 0.01  # 最小の探索率
EPSILON_DECAY = 0.99  # 探索率の減衰率
BATCH_SIZE = 64  # バッチサイズ
UPDATE_TARGET_EVERY = 5  # ターゲットネットワークの更新間隔
LEARNING_RATE = 0.001  # 学習率