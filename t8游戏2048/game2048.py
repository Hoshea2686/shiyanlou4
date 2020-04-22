import random # 产生随机2和4，选择随机位置
import curses	# 终端的curses模式，键盘输入，而不需要回车


class Action:
	"""定义行为并关联按键"""
	actions = ['up', 'down', 'left', 'right', 'restart', 'exit']
	buttons = [ord(ch) for ch in "wsadrqWSADRQ"]
	button_action = dict(zip(buttons, actions * 2))

	def get_action(self, stdscr):
		'''得到行为，循环加阻塞'''
		button = -1
		while button not in self.button_action:
			button = stdscr.getch()
		return self.button_action[button]

class Grid:
	"""网格中的逻辑"""
	def __init__(self, size=4, win=16):
		self.size = size
		self.win = win
		self.reset()

	def reset(self):
		self.score = 0
		self.cells = [[0 for i in range(self.size)] for j in range(self.size)]
		self.spawn()
		self.spawn()

	def spawn(self):
		i, j = random.choice([(i, j) for i in range(self.size) for j in range(self.size) if self.cells[i][j] == 0])
		self.cells[i][j] = 4 if random.randrange(100) > 89 else 2

	def move_left_row(self, row):
		def merge(row):
			for i in range(1, len(row)):
				if row[i] == row[i-1]:
					row[i-1] = 2*row[i-1]
					self.score += row[i-1]
					row[i] = 0
			return row
		def shrink(row):
			new_row = [num for num in row if num != 0]
			new_row += [0 for i in range(len(row) - len(new_row))]
			return new_row
		return shrink(merge(shrink(row)))

	def move_left(self):
		self.cells = [self.move_left_row(row) for row in self.cells]

	def inverst(self):
		self.cells = [row[::-1] for row in self.cells]

	def transpose(self):
		self.cells = [list(row) for row in zip(*self.cells)]

	def move_right(self):
		self.inverst()
		self.move_left()
		self.inverst()

	def move_up(self):
		self.transpose()
		self.move_left()
		self.transpose()

	def move_down(self):
		self.transpose()
		self.move_right()
		self.transpose()

	@staticmethod
	def can_move_left_row(row):
		for i in range(1, len(row)):
			if row[i] == row[i-1] or row[i-1] == 0:
				return True
		return False

	def can_move_left(self):
		can = any(self.can_move_left_row(row) for row in self.cells)
		return can

	def can_move_right(self):
		self.inverst()
		can = self.can_move_left()
		self.inverst()
		return can

	def can_move_up(self):
		self.transpose()
		can = self.can_move_left()
		self.transpose()
		return can

	def can_move_down(self):
		self.transpose()
		can = self.can_move_right()
		self.transpose()
		return can

	@property
	def is_win(self):
		return any(self.cells[i][j]>=self.win for i in range(self.size) for j in range(self.size))
	
	@property
	def is_over(self):
		return not any(getattr(self, 'can_move_' + direction, None)() for direction in ['up', 'down', 'right', 'left'])

class Display:
	move_str = "(W)Up (S)Down (A)Left (D)Right"
	global_str = "     (R)Restart (Q)Exit"
	over_str = "          GAME OVER"
	win_str = "          YOU WIN!"

	def __init__(self, stdscr, cells, state, score, best):
		self.stdscr = stdscr
		self.cells = cells
		self.state = state
		self.score = score
		self.best = best

	def cast(self, string):
		self.stdscr.addstr(string + '\n')

	def draw_row(self, row):
		self.cast(''.join('|{: ^5}'.format(num) if num > 0 else '|     ' for num in row ) + '|')

	def draw(self):
		self.stdscr.clear()
		self.cast("Best Score: {}\n".format(self.best))
		self.cast("Score: {}".format(self.score))
		for row in self.cells:
			self.cast('+-----'*len(row) + '+')
			self.draw_row(row)
		self.cast('+-----'*len(row) + '+')
		if self.state == 'state_win':
			self.cast(self.win_str)
		elif self.state == 'state_over':
			self.cast(self.over_str)
		else:
			self.cast(self.move_str)
		self.cast(self.global_str)

class GameManager:
	def __init__(self):
		self.action = Action()
		self.win = 2048
		self.grid = Grid(win=self.win)
		self.score = 0
		self.best = 0

	@property
	def display(self):
		return Display(self.stdscr, self.grid.cells, self.state, self.score, self.best)
	
	# 状态机，分析状态，当前状态的界面，得到用户行为，执行相应操作，最后返回下一个状态
	def state_init(self):
		self.grid.reset()
		self.score = 0
		return 'state_game'

	def state_game(self):
		self.display.draw()
		act = self.action.get_action(self.stdscr)
		if act == 'restart':
			return 'state_init'
		if act == 'exit':
			return 'state_exit'
		# 当用户移动操作的时候，就执行移动
		if getattr(self.grid, 'can_move_' + act, None)():
			getattr(self.grid, 'move_' + act, None)()
			self.grid.spawn()
			self.score = self.grid.score
			if self.score>self.best:
				self.best = self.score
			if self.grid.is_win:
				return 'state_win'
			if self.grid.is_over:
				return 'state_over'
		return 'state_game'

	def state_win(self):
		self.display.draw()
		act = self.action.get_action(self.stdscr)
		if act == 'restart':
			return 'state_init'
		if act == 'exit':
			return 'state_exit'
		return 'state_win'

	def state_over(self):
		self.display.draw()
		act = self.action.get_action(self.stdscr)
		if act == 'restart':
			return 'state_init'
		if act == 'exit':
			return 'state_exit'
		return 'state_over'

	# 循环状态机
	def __call__(self, stdscr):
		self.stdscr = stdscr
		self.state = 'state_init'
		while self.state != 'state_exit':
			self.state = getattr(self, self.state, None)()

if __name__ == '__main__':
	curses.wrapper(GameManager())