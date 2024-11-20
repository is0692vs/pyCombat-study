#config.pyファイルには、ゲームの設定を記述します。


# キャラクタの幅と高さの設定
CHARACTER_WIDTH = 30
CHARACTER_HEIGHT = 60

# キャラクタの初期距離の設定
CHARACTER_DISTANCE = 200  

# フレームレートの設定
FRAME_RATE = 40  # ゲームの最大フレームレート

# 画面を描画するかどうかの設定
RENDER = True


# モデルと設定と結果を記録するかどうかの設定
SAVE_MODEL_CONFIG_RESULTS = True

# 1エピソードでの対戦回数
BATTLES_PER_EPISODE = 10  

#学習ループのエピソード数
EPISODES = 200  

# 1試合の最大ステップ数
MAX_STEPS = 2000


# ジャンプ許可の設定
CAN_JUMP = True

# プレイヤーの報酬の設定
PLAYER_REWARD_HIT = 20.0  # 攻撃が当たった場合の報酬
PLAYER_PENALTY_MISS = -0  # 攻撃が外れた場合のペナルティ
PLAYER_REWARD_KILL = 100  # 敵を倒した場合の報酬
PLAYER_PENALTY_LOSE = -0  # プレイヤーが負けた場合のペナルティ
PLAYER_REWARD_DISTANCE_CLOSE = 0  # 敵に近づいた場合の報酬
PLAYER_PENALTY_DISTANCE_FAR = -0  # 敵から離れた場合のペナルティ
PLAYER_PENALTY_ON_TOP = -0  # 相手の上に乗った場合のペナルティ
PLAYER_PENALTY_HIT = -1  # 攻撃を受けた場合のペナルティ

# 敵の報酬の設定
ENEMY_REWARD_HIT = 20.0  # 攻撃が当たった場合の報酬
ENEMY_PENALTY_MISS = -0  # 攻撃が外れた場合のペナルティ
ENEMY_REWARD_KILL = 100  # プレイヤーを倒した場合の報酬
ENEMY_PENALTY_LOSE = -0  # 敵が負けた場合のペナルティ
ENEMY_REWARD_DISTANCE_CLOSE = 0 # プレイヤーに近づいた場合の報酬
ENEMY_PENALTY_DISTANCE_FAR = -0 # プレイヤーから離れた場合のペナルティ
ENEMY_PENALTY_ON_TOP = -0  # 相手の上に乗った場合のペナルティ
ENEMY_PENALTY_HIT = -1  # 攻撃を受けた場合のペナルティ

# 画面端のペナルティの設定
EDGE_PENALTY = -0.001  # 画面端にいる場合のペナルティの強さ
# ペナルティを受けないエリアの幅の設定
NO_PENALTY_AREA_WIDTH = 100  # ペナルティを受けないエリアの幅

#体力差の報酬の設定
HEALTH_DIFFERENCE_REWARD_RATE = 1.0 # 体力差に基づく報酬の倍率



# ウィンドウの大きさの設定
WINDOW_WIDTH = 640  # ウィンドウの幅
WINDOW_HEIGHT = 480  # ウィンドウの高さ




# DQNの初期化パラメータ
MEMORY_SIZE = 15000  # リプレイバッファのサイズ:エージェントが過去の経験を保存するためのバッファ
GAMMA = 0.8  # 割引率:0に近いほど短期的な報酬を重視し、1に近いほど長期的な報酬を重視する
EPSILON = 1.0  # 初期の探索率;初期にはランダムな行動を選択する(最大1.0)
EPSILON_MIN = 0.1  # 最小の探索率:エージェントが最後に探索を行う確率(常に少しの確率で探索を行う)
EPSILON_DECAY = 0.9  # 探索率の減衰率：１に近いほど急速に探索率が減少する
BATCH_SIZE = 128  # バッチサイズ:ミニバッチ学習のサイズ
UPDATE_TARGET_EVERY = 10# ターゲットネットワークの更新間隔:何エピソードごとにターゲットネットワークを更新するか
LEARNING_RATE = 0.0005  # 学習率:ネットワークの重みを更新するステップサイズ
# 学習率スケジューラの設定
LR_STEP_SIZE = 100  # 学習率を更新する間隔
LR_GAMMA = 0.7  # 学習率を減衰させる割合