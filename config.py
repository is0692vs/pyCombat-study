#config.pyファイルには、ゲームの設定を記述します。

# ウィンドウの大きさの設定
# WINDOW_WIDTH = 640  # ウィンドウの幅
WINDOW_WIDTH = 640  # ウィンドウの幅
WINDOW_HEIGHT = 480  # ウィンドウの高さ

# キャラクタの幅と高さとHPの設定
CHARACTER_WIDTH = 30
CHARACTER_HEIGHT = 60
CHARACTER_HP=200
# キャラクタの初期距離の設定
CHARACTER_DISTANCE = 200  

# フレームレートの設定
FRAME_RATE = 60# ゲームの最大フレームレート

# 画面を描画するかどうかの設定(実行中に可変)
global RENDER
RENDER = True

# モデルと設定と結果を記録するかどうかの設定(実行中に可変)
global SAVE_MODEL_CONFIG_RESULTS
SAVE_MODEL_CONFIG_RESULTS = False


# 1エピソードでの対戦回数
BATTLES_PER_EPISODE = 1  

#学習ループのエピソード数
EPISODES = 2000  

# 1試合の最大ステップ数
MAX_STEPS = 2000

# ペナルティを受けないエリアの幅の設定
NO_PENALTY_AREA_WIDTH = 100  # ペナルティを受けないエリアの幅

#体力差の報酬の設定
HEALTH_DIFFERENCE_REWARD_RATE = 0.0 # 体力差に基づく報酬の倍率

# ジャンプ許可の設定
CAN_JUMP = True

# ダウン周り
MAX_DOWN_COUNT = 10  # ダウンカウントの最大値
DOWN_LENGTH = 500  # ダウン状態のステップ数
DOWNCOUNT_DECREASE_RATE = 100  # ダウンカウント減少レートstep
DOWNED_PENALTY = -10  # ダウンさせられた時のペナルティ


# プレイヤーの報酬の設定
PLAYER_REWARD_HIT = 3.0  # 攻撃が当たった場合の報酬を増加
PLAYER_PENALTY_MISS = -1.0  # 攻撃が外れた場合のペナルティを追加
PLAYER_REWARD_KILL = 10  # 敵を倒した場合の報酬はそのまま
PLAYER_PENALTY_LOSE = -10  # プレイヤーが負けた場合のペナルティを増加
PLAYER_REWARD_DISTANCE_CLOSE = 0  # 敵に近づいた場合の報酬を追加
PLAYER_PENALTY_DISTANCE_FAR = -0  # 敵から離れた場合のペナルティを追加
PLAYER_PENALTY_ON_TOP = -1  # 相手の上に乗った場合のペナルティを増加
PLAYER_PENALTY_HIT = -1  # 攻撃を受けた場合のペナルティ
INITIAL_PLAYER_REWARD = 0 # 初期報酬を設定

# 敵の報酬の設定
ENEMY_REWARD_HIT = 0.0  # 攻撃が当たった場合の報酬を増加
ENEMY_PENALTY_MISS = -0.0  # 攻撃が外れた場合のペナルティを追加
ENEMY_REWARD_KILL = 00  # プレイヤーを倒した場合の報酬はそのまま
ENEMY_PENALTY_LOSE = -0  # 敵が負けた場合のペナルティを増加
ENEMY_REWARD_DISTANCE_CLOSE = 0  # プレイヤーに近づいた場合の報酬を追加
ENEMY_PENALTY_DISTANCE_FAR = -0  # プレイヤーから離れた場合のペナルティを追加
ENEMY_PENALTY_ON_TOP = -0  # 相手の上に乗った場合のペナルティを増加
ENEMY_PENALTY_HIT = -0  # 攻撃を受けた場合のペナルティ
INITIAL_ENEMY_REWARD = 0 # 初期報酬を設定

# 画面端のペナルティの設定
EDGE_PENALTY = -0.00  # 画面端にいる場合のペナルティ


# 論文のフレームステップ数ごとの体力変化の報酬倍率
HP_DIFFERENCES_REWARD_RATE=1.0


# 右側の指定した範囲にとどまることで得られる報酬を追加
TEST_REWARD = 0  # 右側の指定した範囲にとどまることで得られる報酬
RIGHT_SIDE_START = WINDOW_WIDTH * 0.65  # 右側の範囲の開始位置
RIGHT_SIDE_END = WINDOW_WIDTH*0.7  # 右側の範囲の終了位置




# DQNの初期化パラメータ
MEMORY_SIZE = 1000000  # 保存できる経験のサイズ
GAMMA = 0.8  # 将来の報酬をどれだけ重視するかを決定するパラメータ,1に近いと長期的な報酬を重視
EPSILON = 1.0  # 初期の探索率
EPSILON_MIN = 0.1 # 最小の探索率、0に近づけると、エージェントは最終的に探索を完全にやめ、最適な行動のみを取る
EPSILON_DECAY = 0.99  # 探索率の減衰率を緩やかにして、徐々に最適行動を学習
BATCH_SIZE = 128  # 学習時にリプレイバッファからサンプリングする経験の数。バッチサイズが大きいほど、学習が安定しますが、計算コストが増加します。
UPDATE_TARGET_EVERY = 5  # 小さい値に設定すると、ターゲットネットワークが頻繁に更新され、学習が安定しますが、計算コストが増加
LEARNING_RATE = 0.0001  # Qネットワークの重みを更新する速度,小さい値に設定すると、学習が遅くなりますが、安定した学習が期待できる
# 学習率スケジューラの設定
LR_STEP_SIZE = 5  # 学習率を更新する間隔を短縮
LR_GAMMA = 0.99  # 学習率の減衰率を調整