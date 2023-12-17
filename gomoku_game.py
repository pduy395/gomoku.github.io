import os, sys
import pygame
import math

grid = []
good_position ={(-1,-1)}
good_position.remove((-1,-1))
last_step = (1,1)


def game():
	pygame.init()
	frames = pygame.time.Clock()
	running = True
	human =1
	AI =0
	status =3
	
	while running:
		Game = gomoku_game()
		Game.create_chessboard()
		while running:
			
			
			if AI == 1 and status==3:
				Game.AI_turn()
				AI = 0
				human = 1
				status = Game.check_status() 


			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					running = False
					
				if event.type == pygame.MOUSEBUTTONUP:
					mouse = pygame.mouse.get_pos()
					
					if human==1:
						mouse = pygame.mouse.get_pos()
						valid = Game.human_turn(mouse)
						if valid == True:
							AI=1
							human=0
							status=Game.check_status()

					if status !=3 and 170 < mouse[0] < 270 and 370 < mouse[1] < 415 :
						Game.restart() 
						status=3
						human =1
						AI =0
					if status !=3 and 370 < mouse[0] < 465 and 370 < mouse[1] < 415 :
						running = False

			frames.tick(30)	
						
			
			
			if status != 3:
				AI=0
				human=0
				

				if  status==-1:
					Game.draw_line()
					Game.display_msg('YOU WON THE GAME')
				if  status==1:
					Game.draw_line()
					Game.display_msg('YOU LOSE THE GAME')
				if  status==0:
					Game.display_msg('DRAWN GAME')
					
			pygame.display.update()
			


class gomoku_game:
	def __init__(self):
		self.number = 20
		for row in range(self.number):
			grid.append([])
			for column in range(self.number): 
				grid[row].append(0)
		self.last_step=(0,0)
		self.DEPTH = 2
		self.WIDTH = 30
		self.MARGIN = 2
		self.size = self.number*(self.MARGIN + self.WIDTH) + self.MARGIN 
		self.screen = pygame.display.set_mode((self.size,self.size))

	def create_chessboard(self): 
		x = self.WIDTH
		y = self.MARGIN
		pygame.display.set_caption("Gomoku game")
		self.screen.fill((100,100,100))	

		
		for row in range(self.number):
			for column in range(self.number):
				pygame.draw.rect(self.screen,(255,255,255),((x + y) * column + y,(x + y) * row + y, x, x))
				

	def draw_box(self,row,column,color_o,color_x):
		x = self.WIDTH
		y = self.MARGIN
		
		if grid[row][column] == 1:
					pygame.draw.circle(self.screen,color_o,((x + y) * column + y + x / 2, (x + y) * row + y + x / 2), x/3 , width =  3)
		if grid[row][column] == -1:
			pygame.draw.line(self.screen,color_x, ((x + y) * column + y + x / 5, (x + y) * row + y + x /5), ((y + x) * column + y + x * 4/5, (x + y) * row + y + x * 4/5), width = 4)
			pygame.draw.line(self.screen,color_x, ((x + y) * column + y + x / 5, (x + y) * row + y + x * 4/5), ((y + x) * column + y + x * 4/5, (x + y) * row + y + x /5), width = 4)
		
		


	def draw_line(self):
		#draw the winner line
		x = self.WIDTH
		y = self.MARGIN
		for i in range (self.number):
			for j in range (self.number):
				if j<self.number-4 and grid[i][j]!=0 and grid[i][j]==grid[i][j+1] and grid[i][j]==grid[i][j+2] and grid[i][j]==grid[i][j+3] and grid[i][j]==grid[i][j+4]:
					pygame.draw.line(self.screen,(0,0,0), (((x + y) * j + y + x / 2, (x + y) * i + y + x / 2)), ((((x + y) * (j+4) + y + x / 2, (x + y) * i + y + x / 2))), width= 4)
					return
				if i<self.number-4 and grid[i][j]!=0 and grid[i][j]==grid[i+1][j] and grid[i][j]==grid[i+2][j] and grid[i][j]==grid[i+3][j] and grid[i][j]==grid[i+4][j]:
					pygame.draw.line(self.screen,(0,0,0), (((x + y) * j + y + x / 2, (x + y) * i + y + x / 2)), ((((x + y) * j + y + x / 2, (x + y) * (i+4) + y + x / 2))), width= 4)
					return
				if i<self.number-4 and j<self.number-4 and grid[i][j]!=0 and grid[i][j]==grid[i+1][j+1] and grid[i][j]==grid[i+2][j+2] and grid[i][j]==grid[i+3][j+3] and grid[i][j]==grid[i+4][j+4]:
					pygame.draw.line(self.screen,(0,0,0), (((x + y) * j + y + x / 2, (x + y) * i + y + x / 2)), ((((x + y) * (j+4) + y + x / 2, (x + y) * (i+4) + y + x / 2))), width= 4)
					return
				if i<self.number-4 and j>=4 and grid[i][j]!=0 and grid[i][j]==grid[i+1][j-1] and grid[i][j]==grid[i+2][j-2] and grid[i][j]==grid[i+3][j-3] and grid[i][j]==grid[i+4][j-4]:
					pygame.draw.line(self.screen,(0,0,0), (((x + y) * j + y + x / 2, (x + y) * i + y + x / 2)), ((((x + y) * (j-4) + y + x / 2, (x + y) * (i+4) + y + x / 2))), width= 4)
					return
	def draw_border(self,x,y,a,b):
		#pygame.draw.rect(self.screen, (0,0,255), (x,y,150,150), 0)
		pygame.draw.rect(self.screen, (0,0,0), (x-1,y-1,a,b), 1)
		pygame.draw.rect(self.screen, (0,0,0), (x-2,y-2,a,b), 1)
		pygame.draw.rect(self.screen, (0,0,0), (x-3,y-3,a,b), 1)
		pygame.draw.rect(self.screen, (0,0,0), (x-4,y-4,a,b), 1)
	

	def display_msg(self, msg):
		center = (self.size/2,self.size/2)
		self.draw_border(center[0]-200,center[1]-75,400,200)
		pygame.draw.rect(self.screen,(150,150,150),(center[0]+50,center[1]+50,100,50))
		pygame.draw.rect(self.screen,(150,150,150),(center[0]-150,center[1]+50,100,50))
		self.draw_border(center[0]+50,center[1]+50,100,50)
		self.draw_border(center[0]-150,center[1]+50,100,50)

		font = pygame.font.Font(None, 40)
		text = font.render(msg, True, (5,5,5))
		pos = text.get_rect()
		pos.center = (self.size/2,self.size/2)
		self.screen.blit(text,pos)

		font = pygame.font.Font(None, 30)
		text = font.render("Quit", True, (5,5,5))
		pos = text.get_rect()
		pos.center = (center[0]+100,center[1]+75)
		self.screen.blit(text,pos)

		font = pygame.font.Font(None, 30)
		text = font.render("Restart", True, (5,5,5))
		pos = text.get_rect()
		pos.center = (center[0]-100,center[1]+75)
		self.screen.blit(text,pos)

	def restart(self):
		global good_position, last_step
		for i in range (self.number):
			for j in range (self.number):
				grid[i][j] = 0
		
		self.create_chessboard()
		good_position ={(-1,-1)}
		good_position.remove((-1,-1))
		last_step = (1,1)
		
	
# ALGORITHM FUCTION

	def check_status(self):
		# return the current status value of chessboard 
		for i in range (self.number):
			for j in range (self.number):
				if j<self.number-4 and grid[i][j]!=0 and grid[i][j]==grid[i][j+1] and grid[i][j]==grid[i][j+2] and grid[i][j]==grid[i][j+3] and grid[i][j]==grid[i][j+4]:
					return grid[i][j]
				if i<self.number-4 and grid[i][j]!=0 and grid[i][j]==grid[i+1][j] and grid[i][j]==grid[i+2][j] and grid[i][j]==grid[i+3][j] and grid[i][j]==grid[i+4][j]:
					return grid[i][j]
				if i<self.number-4 and j<self.number-4 and grid[i][j]!=0 and grid[i][j]==grid[i+1][j+1] and grid[i][j]==grid[i+2][j+2] and grid[i][j]==grid[i+3][j+3] and grid[i][j]==grid[i+4][j+4]:
					return grid[i][j]
				if i<self.number-4 and j>=4 and grid[i][j]!=0 and grid[i][j]==grid[i+1][j-1] and grid[i][j]==grid[i+2][j-2] and grid[i][j]==grid[i+3][j-3] and grid[i][j]==grid[i+4][j-4]:
					return grid[i][j]
		flag = 0
		for i in range (self.number):
			for j in range (self.number):
				if(grid[i][j] ==0):
					flag = 1
		if(flag==0):
			return 0
		return 3

	def check_pos(self,x,y):
		# return the true if move (x,y) in the chessboard
		if x>=0 and x<self.number and y>=0 and y<self.number:
			return 1
		return 0


	def human_turn(self,idx):
	# update the step in chessboard and return the valid of step 
		global last_step
		i = int(idx[1] / (self.MARGIN + self.WIDTH))
		j = int(idx[0] / (self.MARGIN + self.WIDTH))
		if self.check_pos(i,j) == 0:
			return False
		if self.check_pos(i,j) and grid[i][j] != 0:
			return False
		grid[i][j] = -1
		self.add_goodposition(i,j)
		self.draw_box(i,j,(0,0,255),(255, 150, 150))
		self.draw_box(last_step[0],last_step[1],(0,0,255),(255, 0, 0))
		last_step = (i,j)
		return True

	def add_goodposition(self,i,j):
		# update good_position when move (i,j)
		if (i,j) in good_position:
			good_position.remove((i,j))
		k = [(i-1,j-1),(i-1,j),(i-1,j+1), (i,j-1),(i,j+1), (i+1,j-1),(i+1,j),(i+1,j+1)]
		for (x,y) in k:
			if self.check_pos(x,y) and grid[x][y]==0:
				good_position.add((x,y))

	def good_pos(self,x,y):
		k=0
		for i in range(-1,2):
			for j in range(-1,2):
				if self.check_pos(x+i,y+j) and grid[x+i][y+j] !=0:
					return 1
		return 0

	def remove_goodposition(self,i,j):
		# update good_position when withdraw the move (i,j)
		if self.good_pos(i,j):
			good_position.add((i,j))
		k = [(i-1,j-1),(i-1,j),(i-1,j+1), (i,j-1),(i,j+1), (i+1,j-1),(i+1,j),(i+1,j+1)]
		for (x,y) in k:
			if (not self.good_pos(x,y)) and self.check_pos(x,y) and ((x,y) in good_position):
				good_position.remove((x,y))
	

	def AI_turn(self):	
		#print(good_position)
		#return the max MAX value of chessboard
		global last_step
		ido = self.alpha_beta()
		grid[ido[0]][ido[1]] = 1
		self.add_goodposition(ido[0],ido[1])
		self.draw_box(ido[0],ido[1],(150,150,255),(255, 0, 0))
		self.draw_box(last_step[0],last_step[1],(0,0,255),(255, 0, 0))
		last_step = ido
		


	def alpha_beta(self):
		#return the max MAX value of chessboard
		move = (-1,-1)
		v = -math.inf
		loop_aray = good_position.copy()
		for (i,j) in loop_aray:
			grid[i][j]= 1
			self.add_goodposition(i,j)
			v0 = self.min_value(-math.inf,math.inf,1)
			grid[i][j]=0
			self.remove_goodposition(i,j)
			if v <= v0:
				v = v0
				move  = (i,j)
		return move

	def max_value(self, alpha, beta, deep):
		status = self.check_status()
		if status == 1:
			return math.inf
		elif status == -1:
			return -math.inf
		elif status == 0:
			return 0

		if deep >= self.DEPTH:
			return self.heuristic()

		v = -math.inf
		loop_aray = good_position.copy()
		for (i,j) in loop_aray:
			grid[i][j] = 1
			self.add_goodposition(i,j)
			v = max(v, self.min_value(alpha,beta, deep+1))
			grid[i][j] = 0
			self.remove_goodposition(i,j)
			if v >= beta:
				return v
			alpha = max(alpha, v)

		return v


	def min_value(self, alpha, beta, deep):
		status = self.check_status()
		if status == -1:
			return -math.inf
		elif status == 1:
			return math.inf
		elif status == 0:
			return 0

		if deep >= self.DEPTH:
			return self.heuristic()

		v = math.inf
		loop_aray = good_position.copy()
		for (i,j) in loop_aray:
			grid[i][j] = -1
			self.add_goodposition(i,j)
			v = min(v, self.max_value(alpha,beta, deep+1))
			grid[i][j] = 0
			self.remove_goodposition(i,j)
			if v <= alpha:
				return v
			beta = min(beta, v)
		return v


	def heuristic(self):
		# estimate of the utility fuction
		h = 0
		for i in range(self.number):
			for j in range(self.number):
				if(grid[i][j]!=0):
					h = h + self.cal_point(i,j,1,0)*grid[i][j]
					h = h + self.cal_point(i,j,0,1)*grid[i][j]
					h = h + self.cal_point(i,j,1,1)*grid[i][j]
					h = h + self.cal_point(i,j,1,-1)*grid[i][j]
		return h
	
	def cal_point(self,x,y,v1,v2):
		if self.check_pos(x-v1,y-v2) == 1 and grid[x-v1][y-v2] == grid[x][y]:
			return 0
		
		c = 1
		while self.check_pos(x + c*v1, y + c*v2)==1 and grid[x + c*v1][y + c*v2]==grid[x][y]:
			c = c + 1

		if c <= 2:
			return pow(5,c)
		
		point = pow(10,c)

		if self.check_pos(x + c*v1, y + c*v2)==0 or grid[x + c*v1][y + c*v2] !=0:
			if self.check_pos(x-v1,y-v2) == 0 or grid[x-v1][y-v2] != 0:
				return 0
		

		if self.check_pos(x + c*v1, y + c*v2)==1 and grid[x + c*v1][y + c*v2] ==0:
			point = point*5

		if self.check_pos(x-v1,y-v2) == 1 and grid[x-v1][y-v2] == 0:
			point = point*5
		


		return point


game()