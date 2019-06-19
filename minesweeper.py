# minesweeper

import random
import numpy as np

MS_SIZE = 8  # ゲームボードのサイズ(変更不可)
MINE = -1    # 地雷のセル
FLAG = 2     # フラグを設置したセル
OPEN = 1     # 開いたセル

"""""""""""""""""""""
  表示に関する関数3

"""""""""""""""""""""
# 配列 game_board の内容(ゲーム画面)を表示する関数
def print_game_board(game_board, mine_map):
    print("\n[y]")

    for y in range(MS_SIZE):
        print(" ", y, "|",end="")
        for x in range(MS_SIZE):
            # 選択したセルの8近傍のセルだけを表示する
            if game_board[y][x] == OPEN :
                if mine_map[y][x] == 0: # 選択したセルの8近傍のセルが0の場合は何も表示しない
                    print("    ", end = "")
                elif mine_map[y][x] == MINE: # 地雷のセル
                    print("   x", end = "")
                else:
                    print("  ",mine_map[y][x], end="")
            elif game_board[y][x] == FLAG:
                print("   F", end = "")
            else:
                print("   x",end = "")
        print("\n")
        
    print("     ",end="")
    for x in range(MS_SIZE):
        print("----",end = "")
    print("\n     ",end="")
    for x in range(MS_SIZE):
        print("  ", x, end="")
    print("  [x]\n") 
    
# 配列 mine_map の内容を表示する.ゲームオーバーの時に地雷の位置を表示する.
def print_mine_map(mine_map):
    print("[y]")
    for y in range(MS_SIZE):
        print(" ", y, "|",end="")
        for x in range(MS_SIZE):
            if mine_map[y][x] == MINE:
                print("   M", end="")
            elif mine_map[y][x] == 0:
                print("    ", end="")
            else:
                print("  ",mine_map[y][x], end="")
        print("\n")
    
    print("     ",end="")
    for x in range(MS_SIZE):
        print("----",end="")
    print("\n     ",end="")
    for x in range(MS_SIZE):
        print("  ", x, end="")
    print("  [x]\n")
    
    print("ここで、Mは地雷です．\n");

"""""""""""""""""""""
  ゲーム本体の関数
"""""""""""""""""""""
# ゲームに用いる変数・配列を初期化する関数
def initialization(mode, number_of_mines, mine_map, game_board):
    mode = 0
    number_of_mines = 0
    
    for y in range(MS_SIZE):
        for x in range(MS_SIZE):
            mine_map[y][x] = 0
            game_board[y][x] = 0

# 配列 mine_map にランダムに地雷をセットする関数
def set_mines(number_of_mines, mine_map):
    for i in range(number_of_mines):
        y = random.randrange(MS_SIZE)
        x = random.randrange(MS_SIZE)
        while mine_map[y][x] == MINE:
            y = random.randrange(MS_SIZE)
            x = random.randrange(MS_SIZE)
        mine_map[y][x] = MINE

#  配列 mine_map の数字セルに近傍の地雷をセットする関数
def mine_count(mine_map):
    for y in range(MS_SIZE):
        for x in range(MS_SIZE):
            if mine_map[y][x] == MINE:
                r = 0
                # セルは地雷かどうかを判断する
            else:
                for j in range(-1, 2):
                    for i in range(-1, 2):
                        if y+j<0 or x+i<0 or y+j>7 or x+i>7:
                            # 例外処理
                            r = 0
                        else:
                            if mine_map[y+j][x+i] == MINE: # 8近傍のセルは地雷かどうかを判断する
                                mine_map[y][x] += 1
                                
# セルを設置する関数
def select_cell(mode, a, b):
    mode = int(input("モードを選択してください：セルを開く(1)、フラグを設置/除去する(2)："))
    
    while mode!=1 and mode!=2:
        mode = int(input("モードを選択してください：セルを開く(1)、フラグを設置/除去する(2)："))

    # セルを指定する
    print("セルを選択してください．")
    print("[x]と[y]を入力してください．")
    a = int(input("[x]: "))
    b = int(input("[y]: "))
    print("\n");
    
    while a<0 or a>7 or b<0 or b>7: #  セル内かどうかを判断する
        print("セルを選択してください．")
        print("[x]と[y]を入力してください．")
        a = int(input("[x]: "))
        b = int(input("[y]: "))
        print("\n");
        
    return mode, a, b
        
# ユーザーが選択したセルの8近傍を開く関数
def check_neighbors(game_board, mine_map, x, y):
    # 選択したセルの8近傍のセルを設定する
    for j in range(-1, 3):
        for i in range(-1, 3):
            if y+j<0 or x+i<0 or y+j>7 or x+i>7:
                # セル内かどうかの判断
                r = 0
            else:
                if game_board[y+j][x+i] == FLAG:
                    game_board[y+j][x+i] = FLAG
                else:
                    game_board[y+j][x+i] = OPEN
                    
"""""""""""""""""""""
      main関数
"""""""""""""""""""""
n = 0

print(MS_SIZE, "×", MS_SIZE, "のボードの各セルに配置された地雷を除去するゲームです．")
print("ゲームを始めます．")

choose = 1 # 初期化
while choose == 1:
    # 初期化
    mode = 0
    number_of_mines = 0
    mine_map = []
    game_board = []
    for y in range(MS_SIZE):
        m = []
        g = []
        for x in range(MS_SIZE):
            m.append(0)
            g.append(0)
        mine_map.append(m)
        game_board.append(g)
    
    number_of_mines = int(input("地雷数を設定してください(1～64):"))
    while number_of_mines <= 0 or number_of_mines >= MS_SIZE*MS_SIZE:
        number_of_mines = int(input("地雷数が正しくありません\n地雷数を設定してください(1～64):"))

    # 地雷の位置を決める
    set_mines(number_of_mines,mine_map)
    
    # 各セルの8近傍の地雷をカウント
    mine_count(mine_map)
    
    win = 0 # ゲームを続けるかどうかを判断するため
    
    # 全体を表示する
    print_game_board(game_board,mine_map)
    
    while win == 0: # ゲームを続ける条件
        # 初期化
        a = 0
        b = 0
        
        mode, a, b = select_cell(mode, a, b) # セルの設置
        if mode == 1:
            print("セル [",a,"][",b ,"]を開きます:\n")
            if mine_map[b][a] == MINE: # 地雷を選択した場合
                print("GAME OVER!")
                win = 1
            else:
                game_board[b][a] = OPEN
                check_neighbors(game_board, mine_map, a, b) # 近傍8の地雷の状況をチェックする
        
        else:
            print("フラグを設置/除去します:\n")
            
            if game_board[b][a] == FLAG: # グラフもう設置した場合
                game_board[b][a] = OPEN
            else:
                game_board[b][a] = FLAG
        
        # 全体を表示する
        if win == 0:
            print_game_board(game_board,mine_map) 
        
        # 開いたセルを数える
        count = 0 # 初期化
        for y in range(MS_SIZE):
            for x in range(MS_SIZE):
                if game_board[y][x] == OPEN:
                    count += 1
        
        if count == (MS_SIZE*MS_SIZE - number_of_mines):
            print("Congratulation!")
            
            win = 1
    print("\n*************結果*************\n")
    
    print_mine_map(mine_map)
    choose = int(input("ゲームを続行しますか？(Yes:1 No:2):"))
