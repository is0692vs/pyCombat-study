#plot.py resultをプロットする
import pandas as pd
import matplotlib.pyplot as plt

csv_file = '/Users/hirokimukai/pyFighting/result/results_2024-11-19-12:17.csv'
y_variable = 'Elapsed Time'  # プロットしたい変数を指定

# 結果をプロットする関数
def plot_results(csv_file, y_variable):
    # CSVファイルを読み込む
    df = pd.read_csv(csv_file)

    # エピソード数を横軸に設定
    x = df['Episode']

    # 指定された変数を縦軸に設定
    y = df[y_variable]

    # プロットを作成
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='b')

    # グラフのタイトルとラベルを設定
    plt.title(f'{y_variable} over Episodes')
    plt.xlabel('Episode')
    plt.ylabel(y_variable)

    # グリッドを表示
    plt.grid(True)

    # プロットを表示
    plt.show()

plot_results(csv_file, y_variable)