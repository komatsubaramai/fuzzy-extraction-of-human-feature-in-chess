import matplotlib.pyplot as plt
import numpy as np

from matplotlib.font_manager import FontProperties

#日本語フォント
font_path = "C:/Windows/Fonts/YuGothB.ttc"

#フォントプロパティの設定
font_prop = FontProperties(fname=font_path)


human_white_path = "C:/Users/m1261/Desktop/pgnToFen-master/whitekihu/feature/queen/queen_all.txt"
human_black_path = "C:/Users/m1261/Desktop/pgnToFen-master/blackkihu/feature/queen/queen_all.txt"
ai_white_path = "C:/Users/m1261/Desktop/pgnToFen-master/aikihu/feature/queen/queen_white.txt"
ai_black_path = "C:/Users/m1261/Desktop/pgnToFen-master/aikihu/feature/queen/queen_black.txt"


with open(human_white_path, 'r') as human_white_file, open(human_black_path, 'r') as human_black_file, open(ai_white_path, 'r') as ai_white_file, open(ai_black_path, 'r') as ai_black_file:
    human_white_lines = human_white_file.readlines()
    human_black_lines = human_black_file.readlines()
    ai_white_lines = ai_white_file.readlines()
    ai_black_lines = ai_black_file.readlines()
    human_white_numbers = [float(line.strip()) for line in human_white_lines[:]]
    human_black_numbers = [float(line.strip()) for line in human_black_lines[:]]
    ai_white_numbers = [float(line.strip()) for line in ai_white_lines[:]]
    ai_black_numbers = [float(line.strip()) for line in ai_black_lines[:]]
    

    #結合して1つの配列にする
    combined_data = np.concatenate([human_white_numbers, human_black_numbers, ai_white_numbers, ai_black_numbers])

    #ヒストグラムのビンのエッジを計算する
    bins = np.histogram_bin_edges(combined_data, bins='auto')
    #print(bins)


#ヒストグラムのプロット

plt.subplot(2, 2, 1)
plt.hist(human_white_numbers, color='blue', edgecolor='black', bins = bins, alpha=0.7, label = 'human_white')
plt.xlabel('評価値の差(後-前)', fontproperties=font_prop)
plt.ylabel('回数', fontproperties=font_prop)
plt.xlim(-50, 50)
plt.legend()  #凡例を表示

plt.subplot(2, 2, 2)
plt.hist(human_black_numbers, color='blue', edgecolor='black', bins = bins, alpha=0.7, label = 'human_black')
plt.xlabel('評価値の差(後-前)', fontproperties=font_prop)
plt.ylabel('回数', fontproperties=font_prop)
plt.xlim(-50, 50)
plt.legend()  #凡例を表示

plt.subplot(2, 2, 3)
plt.hist(ai_white_numbers, color='blue', edgecolor='black', bins = bins, alpha=0.7, label = 'ai_white')
plt.xlabel('評価値の差(後-前)', fontproperties=font_prop)
plt.ylabel('回数', fontproperties=font_prop)
plt.xlim(-50, 50)
plt.legend()  #凡例を表示

plt.subplot(2, 2, 4)
plt.hist(ai_black_numbers, color='blue', edgecolor='black', bins = bins, alpha=0.7, label = 'ai_black')
plt.xlabel('評価値の差(後-前)', fontproperties=font_prop)
plt.ylabel('回数', fontproperties=font_prop)
plt.xlim(-50, 50)
plt.legend()  #凡例を表示


#グラフの表示
plt.tight_layout()
plt.show()
