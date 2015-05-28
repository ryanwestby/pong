import pygame, sys
from pygame.locals import *

BLACK = (0,0,0)
WHITE = (255,255,255)

window_width = 400
window_height = 300

display_surf = pygame.display.set_mode((window_width,window_height))

fps_clock = pygame.time.Clock()
fps = 40

class Game():
	def __init__(self,line_thickness=10,speed=4):
		self.line_thickness = line_thickness
		self.speed = speed
		self.score = 0
		
		# Initiate variables and set starting positions
		ball_x = int(window_width/2 - self.line_thickness/2)
		ball_y = int(window_height/2 - self.line_thickness/2)
		self.ball = Ball(ball_x,ball_y,self.line_thickness,self.line_thickness,self.speed)
		
		self.paddles = {}
		paddle_height = 50
		paddle_width = self.line_thickness
		user_paddle_x = 20
		computer_paddle_x = window_width - paddle_width - 20
		self.paddles['user'] = Paddle(user_paddle_x, paddle_width, paddle_height)
		self.paddles['computer'] = AutoPaddle(computer_paddle_x, paddle_width, paddle_height, self.ball, self.speed)
	
	# Draw the arena for the game to be played in
	def draw_arena(self):
		display_surf.fill(BLACK)
		
		# Draw outline of arena
		pygame.draw.rect(display_surf, WHITE, ((0,0),(window_width,window_height)),self.line_thickness*2)
		
		# Draw center line
		pygame.draw.line(display_surf, WHITE,(int(window_width/2),0),(int(window_width/2),window_height),int(self.line_thickness/4))
		
	def update(self):
		self.ball.move()
		self.paddles['computer'].move()
		
		if self.ball.hit_paddle(self.paddles['computer']):
			self.ball.bounce('x')
		elif self.ball.hit_paddle(self.paddles['user']):
			self.ball.bounce('x')
		
		self.draw_arena()
		self.ball.draw()
		self.paddles['user'].draw()
		self.paddles['computer'].draw()

class Paddle(pygame.sprite.Sprite):
	def __init__(self,x,w,h):
		self.x = x
		self.w = w
		self.h = h
		self.y = int(window_height/2 - self.h/2)
		
		# Create rectangle for paddle
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
		
	# Draw the paddle
	def draw(self):
		#Stops paddle moving too low
		if self.rect.bottom > window_height - self.w:
			self.rect.bottom = window_height - self.w
		#Stops paddle moving too high
		elif self.rect.top < self.w:
			self.rect.top = self.w
		pygame.draw.rect(display_surf, WHITE, self.rect)

	def move(self,pos):
		self.rect.y = pos[1]
		
class AutoPaddle(Paddle):
	def __init__(self,x,w,h,ball,speed):
		super(self.__class__,self).__init__(x,w,h)
		self.ball = ball
		self.speed = speed

	def move(self):
		if self.rect.centery < self.ball.rect.centery:
			self.rect.y += self.speed
		else:
			self.rect.y -= self.speed
		
class Ball(pygame.sprite.Sprite):
	def __init__(self,x,y,w,h,speed):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.speed = speed
		self.dir_x = -1
		self.dir_y = -1
		
		self.rect = pygame.Rect(self.x,self.y,self.w,self.h)
	
	# Draw the ball
	def draw(self):
		pygame.draw.rect(display_surf,WHITE,self.rect)
	
	# Move the ball
	def move(self):
		self.rect.x += (self.dir_x * self.speed)
		self.rect.y += (self.dir_y * self.speed)
		
		# Check for a collision with a wall, then bounce off it
		if self.hit_ceiling() or self.hit_floor():
			self.bounce('y')
		if self.hit_wall():
			self.bounce('x')
			
	def bounce(self,axis):
		if axis == 'x':
			self.dir_x *= -1
		elif axis == 'y':
			self.dir_y *= -1
	
	def hit_paddle(self,paddle):
		if pygame.sprite.collide_rect(self,paddle):
			return True
		else:
			return False
	
	def hit_wall(self):
		if ((self.dir_x == -1 and self.rect.left <= self.w) or (self.dir_x == 1 and self.rect.right >= window_width - self.w)):
			return True
		else:
			return False
			
	def hit_ceiling(self):
		if self.dir_y == -1 and self.rect.top <= self.w:
			return True
		else:
			return False
	
	def hit_floor(self):
		if self.dir_y == 1 and self.rect.bottom >= window_height - self.w:
			return True
		else:
			return False
		
# Main function
def main():
	pygame.init()
	
	pygame.display.set_caption('Pong')
	pygame.mouse.set_visible(0) # make cursor invisible
	
	game = Game()
	
	while True: # main game loop
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				game.paddles['user'].move(event.pos)
		
		game.update()
		pygame.display.update()
		fps_clock.tick(fps)

if __name__=='__main__':
	main()