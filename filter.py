#pgn形式の棋譜から、壊れている棋譜を取り除くプログラム
#Desktop/pgnToFen-master/white.pgnから壊れた棋譜を取り除いて、Desktop/pgnToFen-master/whitekihu/white.pgnに保存する
#with open('kihuwhite.pgn', 'r') as wf, open('whitekihu/white.pgn', 'w') as f:
with open('kihublack.pgn', 'r') as bf, open('blackkihu/black.pgn', 'w') as f:
    #lines = wf.readlines()
    lines = bf.readlines()
    i = 0
    while i < len(lines)-18:
        if lines[i].find('[Event') != -1 and lines[i+14].find('[Termination') != -1 and lines[i+16].find('1.') != -1 and lines[i+16].find('%') == -1:
            for j in range(18):
                f.write(lines[i+j])
            i += 18
        else:
            i += 1
