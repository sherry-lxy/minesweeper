import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random
from itertools import product # 多重ループを減らす
import numpy as np

MS_SIZE = 8          # ゲームボードのサイズ
CLOSE, OPEN, FLAG = 0, 1, 2

class Game:
    #pass
    def __init__(self, number_of_mines = 10):
        """ ゲームボードの初期化
        
        Arguments:
        number_of_mines -- 地雷の数のデフォルト値は10

        Side effects:
        mine_map[][] -- 地雷マップ(-1: 地雷，>=0 8近傍の地雷数)
        game_board[][] -- 盤面 (0: CLOSE(初期状態), 1: 開いた状態, 2: フラグ)

        """

        self.init_game_board()
        self.init_mine_map(number_of_mines)
        self.count_mines()

    def init_game_board(self):
        """ ゲーム盤を初期化 """

        self.game_board = np.array([[CLOSE for i in range(MS_SIZE)] for j in range(MS_SIZE)])                

    def init_mine_map(self, number_of_mines):
        """ 地雷マップ(self->mine_map)の初期化
        Arguments:
        number_of_mines -- 地雷の数
        
        地雷セルに-1を設定する．      
        """

        self.mine_map = np.array([[CLOSE for i in range(MS_SIZE)] for j in range(MS_SIZE)])

        # 例外処理
        if number_of_mines < 0:
        	number_of_mines = 0
        elif number_of_mines > 64:
        	number_of_mines = 64


        fy = np.array([i for i in range(MS_SIZE**2)]) # 0~63の行列の用意する
        end = MS_SIZE ** 2 # 最後位

        for i in range(number_of_mines):
        	m = random.choice(range(0,end)) # 0~end-1までランダムに数値を取り出す
        	y = int(fy[m] / MS_SIZE) # それに対応する2次元配列の座標に変換する
        	x = fy[m] % MS_SIZE
        	self.mine_map[y][x] = -1 # 地雷として設定する
        	fy[m] = fy[end - 1] # 一番後ろの数値ともうすでに取り出した数値と書き換える
        	end -= 1 # 最後位を更新する
     
    def count_mines(self):
        """ 8近傍の地雷数をカウントしmine_mapに格納 
        地雷数をmine_map[][]に設定する．
        """

        for y in range(MS_SIZE):
        	for x in range(MS_SIZE):
        		if self.mine_map[y][x] == -1:
        			pass
        		else:
        			# 例外処理
        			y_lower = 0 if y-1<0 else y-1
        			y_upper = MS_SIZE if y+2>MS_SIZE else y+2
        			x_lower = 0 if x-1<0 else x-1
        			x_upper = MS_SIZE if x+2>MS_SIZE else x+2

        			self.mine_map[y][x] = np.sum(self.mine_map[y_lower:y_upper, x_lower:x_upper] == -1) # 地雷数をカウントする

    def open_cell(self, x, y):
        """ セル(x, y)を開ける
        Arguments:
        x, y -- セルの位置
        
        Returns:
          True  -- 8近傍セルをOPENに設定．
                   ただし，既に開いているセルの近傍セルは開けない．
                   地雷セル，FLAGが設定されたセルは開けない．
          False -- 地雷があるセルを開けてしまった場合（ゲームオーバ）
        """

        row = [-1, 0, 1]
  
        if self.mine_map[y][x] == -1: # 地雷を選んだ場合ゲーム終了
       		return False
       	elif self.game_board[y][x] == OPEN: # もうすでに開けてるセルを選んだ場合何も処理しない
       		pass
       		return True
       	elif self.game_board[y][x] == FLAG: # flagのところを選んだらセルを開ける状態に切り替える
       		self.game_board[y][x] = OPEN
       	elif self.game_board[y][x] == CLOSE: # closeのセルを開ける
       		self.game_board[y][x] = OPEN
       	
       	for j, i in product(row, row):
       		if y+j<0 or x+i<0 or y+j>7 or x+i>7: # 例外処理
       			pass
       		elif i == 0 and j == 0:
       			pass
       		else:
        		if self.game_board[y + j][x + i] == OPEN: # 既に開いているセルの近傍セルは開けない
        			pass
        		elif self.game_board[y + j][x + i] == FLAG:	# FLAGが設定されたセルは開けない
       				pass
       			elif self.game_board[y + j][x + i] == CLOSE:
       				if self.mine_map[y + j][x + i] == -1: # 地雷セルは開けない
       					pass
       				elif self.mine_map[y + j][x + i] >= 0:
       					self.game_board[y + j][x + i] = OPEN	

        return True
    
    def flag_cell(self, x, y):
        """
        セル(x, y)にフラグを設定する，既に設定されている場合はCLOSE状態にする
        """

        if self.game_board[y][x] == FLAG:
        	self.game_board[y][x] = CLOSE
        elif self.game_board[y][x] == CLOSE:
        	self.game_board[y][x] = FLAG
        else:
        	self.game_board[y][x] = OPEN
            
    def is_finished(self):
        """ 地雷セル以外のすべてのセルが開かれたかチェック """

        # openしたセルの個数が地雷でないセルと一致したらゲームクリア
        if np.sum(self.game_board[:MS_SIZE, :MS_SIZE] == OPEN) == MS_SIZE**2 - np.sum(self.mine_map[:MS_SIZE, :MS_SIZE] == -1):
        	return True
        else:
        	return False
        
    def print_game_board(self):
        marks = ['x', ' ', 'P']
        self.print_header()
        print("[y]")
        for y in range(MS_SIZE):
            print("%2d|"%y, end="")
            for x in range(MS_SIZE):
                if self.game_board[y][x] == OPEN and self.mine_map[y][x] > 0:
                    print("%3d"%self.mine_map[y][x], end="")
                else:
                    print("%3s"%marks[self.game_board[y][x]], end="")
            print("")
        self.print_footer(x, y)

class MyPushButton(QPushButton):
    
    def __init__(self, text, x, y, parent):
        """ セルに対応するボタンを生成 """
        super(MyPushButton, self).__init__(text, parent)
        self.parent = parent # MinesweeperWindow
        self.x = x
        self.y = y
        self.setMinimumSize(25, 25)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, 
            QSizePolicy.MinimumExpanding)
        
    def set_bg_color(self, colorname):
        """ セルの色を指定する
        Arguments:
            self
            colorname: 文字列 -- 色名 (例, "white")
        """
        self.setStyleSheet("MyPushButton{{background-color: {}}}".format(colorname))
        
    def on_click(self):
        """ セルをクリックしたときの動作 """

        self.resize(250, 150)

        key = QApplication.keyboardModifiers() # キーを認識する
        #print(self.x, self.y)
        if key == Qt.ShiftModifier: # shiftキーの場合
        	self.parent.game.flag_cell(self.x, self.y) # フラグを立つ
        	#print("flag")
        else:
        	if self.parent.game.open_cell(self.x, self.y) == False: # 地雷セルを開けた場合
        		if self.parent.game.game_board[self.y][self.x] == FLAG: 
        			self.parent.game.game_board[self.y][self.x] == CLOSE
        		else:
        			print("Game Over!") # gameoverを表示する
        			QMessageBox.information(self, "Game Over", "ゲームオーバー！") # メッセージボックスでgameoverを表示する

        			self.parent.show_answer()
        			QMessageBox.information(self, "Answer", "答え")

        			self.parent.close() # アプリケーションを終了する
        	if self.parent.game.open_cell(self.x, self.y) == FLAG: # フラグ立っているところが開けたら何も起きない
        		pass

        self.parent.show_cell_status() # セル状態を表示する

        if self.parent.game.is_finished() == True:
        	print("Game Clear!")
        	QMessageBox.information(self, "Game Clear", "ゲームクリア！") # メッセージボックスでgameclearを表示する
        	self.parent.close() # アプリケーションを終了する


            
class MinesweeperWindow(QMainWindow):
    
    def __init__(self):
        """ インスタンスが生成されたときに呼び出されるメソッド """
        super(MinesweeperWindow, self).__init__()
        self.game = Game()
        self.initUI()
    
    def initUI(self):
        """ UIの初期化 """        
        self.resize(800, 800) 
        self.setWindowTitle('Minesweeper')
        
        sb = self.statusBar()
        sb.showMessage("Shift+クリックでフラグをセット") # ステータスバーにメッセージを表示

        self.button = [[0 for i in range(MS_SIZE)] for j in range(MS_SIZE)]

        vbox = QVBoxLayout(spacing = 0)
        for y in range(MS_SIZE):
        	hbox = QHBoxLayout(spacing = 0)
        	for x in range(MS_SIZE):
        		self.button[y][x] = MyPushButton('x', x, y, self)
        		self.button[y][x].clicked.connect(self.button[y][x].on_click)

        		hbox.addWidget(self.button[y][x])
        	
        	vbox.addLayout(hbox)
        

        container = QWidget()
        container.setLayout(vbox)

        self.setCentralWidget(container)

        self.show_cell_status()
        
        self.show()
    
    def show_cell_status(self):
        """ ゲームボードを表示 """
		
        for y in range(MS_SIZE):
        	for x in range(MS_SIZE):
        		if self.game.game_board[y][x] == CLOSE:
        			self.button[y][x].setText('x')
        			self.button[y][x].set_bg_color("#6D3F00")
        		elif self.game.game_board[y][x] == FLAG:
        			self.button[y][x].setText('🚩')
        			self.button[y][x].set_bg_color("#91002C")
        		else:
        			if self.game.mine_map[y][x] == -1:
        				pass
        			else:
        				if self.game.mine_map[y][x] == 0:
        					self.button[y][x].setText(' ')
        				else:
        					self.button[y][x].setText(str(self.game.mine_map[y][x]))
        				self.button[y][x].set_bg_color("#EB6100")

    def show_answer(self):
    	for y in range(MS_SIZE):
    		for x in range(MS_SIZE):
        		if self.game.mine_map[y][x] == 0:
       				if self.game.game_board[y][x] == FLAG:
        				self.button[y][x].setText(' ')
        				self.button[y][x].set_bg_color("#F39800")
       				else:
        				self.button[y][x].setText(' ')
        				self.button[y][x].set_bg_color("#EB6100")
       			elif self.game.mine_map[y][x] == -1:
       				if self.game.game_board[y][x] == FLAG:
       					self.button[y][x].setText('🚩')
       					self.button[y][x].set_bg_color("#91002C")
       				else:
       					self.button[y][x].setText('💣')
       					self.button[y][x].set_bg_color("#5B5300")
       			else:
       				if self.game.game_board[y][x] == FLAG:
        				self.button[y][x].setText(str(self.game.mine_map[y][x]))
        				self.button[y][x].set_bg_color("#F39800")
        			else:
        				self.button[y][x].setText(str(self.game.mine_map[y][x]))
        				self.button[y][x].set_bg_color("#EB6100")






                 
def main():
    app = QApplication(sys.argv)
    w = MinesweeperWindow()
    app.exec_()
            
if __name__ == '__main__':
    main()

