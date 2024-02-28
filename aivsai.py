import subprocess
import os
import time
import chess
import chess.engine

stockfish_path = "C:/Users/m1261/Desktop/chesseval/stockfish/stockfish-windows-x86-64-avx2.exe"
path = "C:/Users/m1261/Desktop/pgnToFen-master/aikihu/aieval"
human_path = "C:/Users/m1261/Desktop/pgnToFen-master/blackkihu/eval"

error_num = 0
num = 0
movelist = []

def is_checkmate(fen):
    global error_num
    board = chess.Board(fen)
    return board.is_checkmate()

def is_kings_only(fen):
    board = chess.Board(fen)
    #盤面上にキング以外の駒が存在する場合はFalseを返す
    if board.occupied != board.pieces_mask(chess.KING, chess.WHITE) | board.pieces_mask(chess.KING, chess.BLACK):
        return False
    #それ以外の場合はTrueを返す
    return True

def d_cmd():
    global error_num
    stockfish.stdout.flush()
    stockfish.stdin.write('d\n')
    stockfish.stdin.flush()
    start_time = time.time()
    while True:
        output = stockfish.stdout.readline().strip()
        elapsed_time = time.time() - start_time
        if elapsed_time >= 3:
            error_num += 1
            fenline = 'error'
            break
        if 'Fen' in output:
            #print(output)
            fenline = ' '.join(output.split(' ')[1:])
            break
    return fenline

def eval_cmd():
    global error_num
    stockfish.stdout.flush()
    stockfish.stdin.write('eval\n')
    stockfish.stdin.flush()
    start_time = time.time()
    while True:
        output = stockfish.stdout.readline().strip()
        elapsed_time = time.time() - start_time
        if elapsed_time >= 3:
            error_num += 1
            value = 'error'
            break
        if 'Final evaluation' in output:
            #print(output)
            value = output.split(' ')[2]
            if value != 'none':
                value = output.split(' ')[8]
            break
    return value

def go_cmd():
    next_move = None  #初期化
    global error_num
    stockfish.stdout.flush()
    stockfish.stdin.write('go depth 20\n')
    stockfish.stdin.flush()
    start_time = time.time()
    while True:
        output = stockfish.stdout.readline().strip()
        elapsed_time = time.time() - start_time
        if elapsed_time >= 3:
            stockfish.stdin.write('stop\n') #3秒以内に終わらなければ見つかったところまでで手を返す
            stockfish.stdin.flush()
            error_num += 1
            #next_move = 'error'
        if 'bestmove' in output:
            print(output)
            next_move = output.split(' ')[1]
            break
    return next_move

def count_lines(file_path):
    with open(file_path, 'r') as file:
        line_count = sum(1 for line in file)
    return line_count

def find_line_numbers(file_path, target_string, line_count):
    line_numbers = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            if target_string in line:
                next_line_number = line_number + 12 #上から12行目までない試合(それぞれ三手ずつ打たずに終わった試合)は使わない
                if(next_line_number <= line_count):
                    line_numbers.append(next_line_number)
    return line_numbers

def get_line_content(file_path, line_number):
    with open(file_path, 'r') as file:
        for current_line, line_content in enumerate(file, start=1):
            if current_line == line_number:
                return line_content.strip()

evallog = os.path.join(path, 'aivsailog_black.txt')
with open(evallog, 'a+') as logf:
    for i in range(666, 1682):    
        try:
            stockfish = subprocess.Popen(
                [stockfish_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            #fenline = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
            humanline = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -'
            evalout = os.path.join(path, f'aieval_black_{i}.txt')
            humanfen = os.path.join(human_path, f'evalblack_{i}.txt')
            line_numbers = [] #line_numbers初期化
            with open(evalout, 'a+') as outf:
                line_count = count_lines(humanfen)
                line_numbers = find_line_numbers(humanfen, humanline, line_count)
                print(line_numbers)
                logf.write('\n' + str(len(line_numbers)) + '\n')
                logf.write(' '.join(map(str, line_numbers)) + '\n')
                logf.flush()
                for j in range(len(line_numbers)):
                    line_con = get_line_content(humanfen, line_numbers[j])#7move
                    movelist = [] #movelist初期化
                    num = 0 #num初期化
                    error_num = 0 #error_num初期化
                    stockfish.stdin.write(f'position fen {line_con}\n')
                    stockfish.stdin.flush()
                    while True:
                        fenline = d_cmd()
                        print(fenline)
                        outf.write(fenline + '\n')
                        eval = eval_cmd()
                        outf.write(eval + '\n')
                        print(eval)
                        next_move = go_cmd()
                        print(next_move)
                        if next_move == '(none)' or next_move == 'None' or next_move == 'error':
                            logf.write(f'next_move is {next_move} \n')
                            logf.flush()
                            break
                        if is_kings_only(fenline):
                            logf.write('kings only \n')
                            logf.flush()
                            break
                        if int(fenline.split(' ')[4]) >= 50:
                            logf.write('50 moves rule \n')
                            logf.flush()
                            break
                        movelist.append(f' {next_move}')
                        stockfish.stdin.write(f'position fen {line_con} moves {"".join(movelist)}\n')
                        stockfish.stdin.flush()
                        num += 1
                    print(f"Iteration {i}, Subprocess {j}: {num} moves, {error_num} errors")
                    logf.write(f"Iteration {i}, Subprocess {j}: {num} moves, {error_num} errors\n")
                    logf.flush()

        except Exception as e:
            print(f"error: {e}\n")
            logf.write(f"error: {e}\n")
            logf.flush()

        finally:  
            #stockfishを終了
            stockfish.terminate()
