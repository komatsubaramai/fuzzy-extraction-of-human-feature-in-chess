import subprocess
import os
import time

#stockfishの実行ファイルへのパス
stockfish_path = "C:/Users/m1261/Desktop/chesseval/stockfish/stockfish-windows-x86-64-avx2.exe"

#ファイルのパス
path = "C:/Users/m1261/Desktop/pgnToFen-master/whitekihu"

error_num = 0
num = 0
for i in range(104, 105):
    #fenファイルへのパス
    fenpath = os.path.join(path, f"replacedfen/replacedwhite_{i}.fen")

    #outputファイルへのパス
    evalout = os.path.join(path, f"eval/evalwhite_{i}.txt")

    #stockfishを起動
    stockfish = subprocess.Popen(
        [stockfish_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        bufsize=1,  #行単位でバッファリング
        universal_newlines=True
    )

    sendflag = False
    

    #fen形式の棋譜を一行ずつ送信して評価値を取得
    try:
        with open(fenpath, 'r') as f, open(evalout, 'w') as outf:
            #棋譜を送信 > positionコマンドを送信 > evalコマンドを送信 > 評価値を取得
            for fenline in f:
                if '[r' in fenline:
                    sendflag = True
                    fenline = fenline.replace('[', '')
                if sendflag:
                    if ']' in fenline:
                        fenline = fenline.replace(']' and ')', '')
                        num += 1
                    if '}' in fenline:
                        fenline = fenline.replace(']' and '}', '')
                    stockfish.stdout.flush()
                    print(fenline.strip())
                    outf.write(fenline.strip() + '\n')
                    stockfish.stdin.write(f'position fen {fenline.strip()}\n')  #改行削除
                    stockfish.stdin.flush()
                    stockfish.stdin.write('eval\n')
                    stockfish.stdin.flush()
                    if ']' in fenline:
                        sendflag = False
                    #出力を待つ
                    start_time = time.time()
                    while True:
                        output = stockfish.stdout.readline().strip()  #改行削除
                        #評価値が出力されたら表示して、出力を待つループを抜ける
                        #経過時間を計算
                        elapsed_time = time.time() - start_time

                        #3秒以上結果が返ってこなかったらループを抜ける
                        if elapsed_time >= 3:
                            error_num += 1
                            outf.write("error\n")
                            break
                        if 'Final evaluation' in output:
                            value = output.split(' ')[2]
                            if value != 'none':
                              value = output.split(' ')[8]
                            print(value)
                            outf.write(value + '\n')
                            outf.flush()
                            break
        print(num)
        print(error_num)
    except Exception as e:
        print(f"error: {e}\n")
    finally:
        #stockfishを終了
        stockfish.terminate()
