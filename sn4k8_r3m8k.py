'''
descriptions:
	classic snake game
	made with python' OOP (object-oriented programming)
	and the pygame API
	I am currently using pygame-ce (community edition)
programmer:
	zZz
email:
	dangthitruchanh10a03@gmail.com
ps:
	DO NOT reup at any kinds of content without my permission(^-^)
	and have fun while playing around with it!

'''
from random import randint
import pygame as pg
pg.init()


class Fruit(object): 
	color = 'red'
	def __init__(self):
		self.rect = self.randomise_position()
	def randomise_position(self):
		fruit_left = randint(0,CELLNUM-1) * CELLSIZE
		fruit_top  = randint(0,CELLNUM-1) * CELLSIZE
		fruit_rect = pg.Rect(fruit_left,fruit_top,CELLSIZE,CELLSIZE)
		return fruit_rect
	def draw(self, src):
		pg.draw.rect(src, self.color, self.rect)


class Snake(object): 
	color = 'green'
	MOVE = pg.event.custom_type()
	pg.time.set_timer(MOVE, 90)  ##get triggers after every 90ms
	def __init__(self):
		self.pos = [[3,10],[4,10],[5,10]]
		self.direction = NOT_MOVE  ##keep our snake not moving until the user press one of the four arrows key
		self.add_segment = 0
	def draw(self, src): 
		##loop through our snake' entire body position
		for col,row in self.pos:
			snake_rect = col*CELLSIZE,row*CELLSIZE,CELLSIZE,CELLSIZE
			pg.draw.rect(src, self.color, snake_rect)


class Game(object):
	def __init__(self):
		self.fruit = Fruit()
		self.snake = Snake()

	def draw_grid(self, src):
		##also note that we don't want to draw any
		##lines at screen' edges!
		##and because the stop(in the for..loop below) is not included
		##so you don't need to subtract 1 from it
		LINE_COLOR = 'lightgrey'
		for n in range(1,CELLNUM,1):  
			p = n * CELLSIZE
			pg.draw.line(src, LINE_COLOR, (p,0), (p,WINH), 1)
			pg.draw.line(src, LINE_COLOR, (0,p), (WINW,p), 1)

	def draw_elements(self, src):
		##draw the fruit first
		self.fruit.draw(src)

		##then draw the snake
		self.snake.draw(src)

	def update_elements(self):
		if self.snake.direction != NOT_MOVE:
			if not self.snake.add_segment:
				pos_cpy = self.snake.pos[1:]
			else:
				pos_cpy = self.snake.pos[:]
				self.snake.add_segment = 0
			new_head_col = pos_cpy[-1][0]+self.snake.direction[0]
			new_head_row = pos_cpy[-1][1]+self.snake.direction[1]
			new_head_direction = [new_head_col, new_head_row]
			pos_cpy.append(new_head_direction)
			##applying changes to the real snake body' position
			self.snake.pos = pos_cpy.copy()

		##unpacking datas need for detecting collisions
		fruit_col, fruit_row = self.fruit.rect.left//CELLSIZE, self.fruit.rect.top//CELLSIZE
		snake_head_col, snake_head_row = self.snake.pos[-1]

		##our snake eat the fruit
		if [snake_head_col, snake_head_row] == [fruit_col, fruit_row]:
			##re-spawn the fruit at random location 
			self.fruit.rect = self.fruit.randomise_position()
			
			##make snake growth one segment each time!
			self.snake.add_segment = 1

		##snake collide with walls
		##remember you need for both vertical(top and bottom edges)
		##and horizontal(left and right edges) of the screen!
		if not (0 <= snake_head_col < CELLNUM) or\
		not (0 <= snake_head_row < CELLNUM):
			print('hits wall')
			return 1
		
		##snake hits itself so sad:-(
		for body_col,body_row in self.snake.pos[:-1]:
			if [snake_head_col, snake_head_row] == [body_col, body_row]:
				print('oops:-(')
				return 1
		return 0


class App(object):
	def __init__(self, dims, framesrate, title):
		pg.display.set_caption(title)
		flags = pg.SRCALPHA|pg.HWSURFACE
		bpp = pg.display.mode_ok(dims,flags)
		self.win = pg.display.set_mode(dims, flags, bpp)
		self.clk = pg.time.Clock()
		self.fps = framesrate
		self.done = 0
		
		self.game = Game()
	def run(self):
		self._mainloop()
	def _onkeydown(self, e):
		if e.key == pg.K_LEFT: 
			if self.game.snake.direction != MOVE_RIGHT:
				self.game.snake.direction = MOVE_LEFT
		elif e.key == pg.K_RIGHT: 
			if self.game.snake.direction != MOVE_LEFT:
				self.game.snake.direction = MOVE_RIGHT
		elif e.key == pg.K_UP: 
			if self.game.snake.direction != MOVE_DOWN:
				self.game.snake.direction = MOVE_UP
		elif e.key == pg.K_DOWN: 
			if self.game.snake.direction != MOVE_UP:
				self.game.snake.direction = MOVE_DOWN
	def _process_event(self): 
		for e in pg.event.get():
			if e.type in (pg.QUIT, pg.WINDOWCLOSE):
				self.done = 1
			elif e.type == self.game.snake.MOVE:
				self.done = self.game.update_elements()
			elif e.type == pg.KEYDOWN:
				self._onkeydown(e)
	def _process_drawing(self): 
		self.win.fill('black')
		self.game.draw_elements(self.win)
		self.game.draw_grid(self.win)
		pg.display.flip()  ##update everything we've drawn
	def _mainloop(self):
		while not self.done:
			self.clk.tick(self.fps)
			self._process_event()
			self._process_drawing()
		pg.quit()
CELLSIZE = 20
CELLNUM = 20
WINW = WINH = CELLSIZE*CELLNUM
FPS = 30
TITLE = 'sn4k8 r3m8k'

MOVE_LEFT  = [-1, 0]
MOVE_UP    = [ 0,-1]
MOVE_DOWN  = [ 0, 1]
MOVE_RIGHT = [ 1, 0]
NOT_MOVE   = [ 0, 0]

if __name__ == '__main__':
	app = App((WINW, WINH), FPS, TITLE)
	app.run()