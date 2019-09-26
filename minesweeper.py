import random

MS_SIZE = 8          # ゲームボードのサイズ
CLOSE, OPEN, FLAG = 0, 1, 2

class Game:

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

        self.game_board = [[CLOSE for i in range(MS_SIZE)] for j in range(MS_SIZE)]

        '''
        self.game_board = [[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]
        '''                   

    def init_mine_map(self, number_of_mines):
        """ 地雷マップ(self->mine_map)の初期化
        Arguments:
        number_of_mines -- 地雷の数
        
        地雷セルに-1を設定する．      
        """

        self.mine_map = [[CLOSE for i in range(MS_SIZE)] for j in range(MS_SIZE)]
        if number_of_mines < 0:
        	number_of_mines = 0
        elif number_of_mines > 64:
        	number_of_mines = 64
        

        for i in range(number_of_mines):
        	x = random.randrange(MS_SIZE)
       		y = random.randrange(MS_SIZE)
       		while self.mine_map[y][x] == -1:
       			x = random.randrange(MS_SIZE)
       			y = random.randrange(MS_SIZE)
       		self.mine_map[y][x] = -1
     
    def count_mines(self):
        """ 8近傍の地雷数をカウントしmine_mapに格納 
        地雷数をmine_map[][]に設定する．
        """

        for y in range(MS_SIZE):
        	for x in range(MS_SIZE):
        		if self.mine_map[y][x] == -1:
        			pass
        		else:	
        			for j in range(-1, 2):
        				for i in range(-1, 2):
        					if y+j<0 or x+i<0 or y+j>7 or x+i>7: # 例外処理
        						pass
        					else:
        						if self.mine_map[y + j][x + i] == -1:
        							self.mine_map[y][x] += 1


    
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

        
        if self.mine_map[y][x] == -1:
       		return False
       	elif self.game_board[y][x] == OPEN:
       		pass
       		return True
       	elif self.game_board[y][x] == FLAG:
       		self.game_board[y][x] = OPEN
       	elif self.game_board[y][x] == CLOSE:
       		self.game_board[y][x] = OPEN
       	
       	for j in range(-1, 2):
       		for  i in range(-1, 2):
       			if y+j<0 or x+i<0 or y+j>7 or x+i>7:
       				pass
       			elif i == 0 and j == 0:
       				pass
       			else:
        			if self.game_board[y + j][x + i] == OPEN:
        				pass
        			elif self.game_board[y + j][x + i] == FLAG:	
       					pass
       				elif self.game_board[y + j][x + i] == CLOSE:
       					if self.mine_map[y + j][x + i] == -1:
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

        count = 0

        for y in range(MS_SIZE):
        	for x in range(MS_SIZE):
        		if self.game_board[y][x] != OPEN and self.mine_map[y][x] == -1:
        			count += 1
        		elif self.game_board[y][x] == OPEN and self.mine_map[y][x] >= 0:
        			count += 1

        if count == MS_SIZE ** 2:
        	return True
        else:
        	return False


        
    def print_header(self):
        print("=====================================")
        print("===  Mine Sweeper Python Ver. 1  ====")
        print("=====================================")

    def print_footer(self):
        print("   ", end="")
        for x in range(MS_SIZE):
            print("---", end="")
        print("[x]\n   ", end="")
        for x in range(MS_SIZE):
            print("%3d"%x, end="")
        print("")
        
    def print_mine_map(self):
        print(" [y]")
        for y in range(MS_SIZE):
            print("%2d|"%y, end="")
            for x in range(MS_SIZE):
                print("%2d"%self.mine_map[y][x], end="")
            print("")
        
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
        self.print_footer()

if __name__ == '__main__':
    b = Game()
    quitGame = False
    while not quitGame:
        b.print_game_board()
        print("o x y: セルを開く，f x y: フラグ設定/解除, q: 終了 -->", end="")
        command_str = input()

        try:
            cmd = command_str.split(" ")
            if cmd[0] == 'o':
                x, y = cmd[1:]
                if b.open_cell(int(x), int(y)) == False:
                    print("ゲームオーバー!")
                    quitGame = True
            elif cmd[0] == 'f':
                x, y = cmd[1:]
                b.flag_cell(int(x), int(y))
            elif cmd[0] == 'q':
                print("ゲームを終了します．")
                quitGame = True
                break
            else:
                print("コマンドはo, f, qのいずれかを指定してください．")
        except:
            print("もう一度，コマンドを入力してください．")
            
        if b.is_finished():
            b.print_game_board()
            print("ゲームクリア!")
            quitGame = True
