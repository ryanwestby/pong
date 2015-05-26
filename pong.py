import pygame, sys
from pygame.locals import *

fps_clock = pygame.time.Clock()
fps = 40

window_width = 400
window_height = 300

# Main function
def main():
	pygame.init()
	global display_surf
	
	display_surf = pygame.display.set_mode((window_width,window_height))
	pygame.display.set_caption('Pong')
	pygame.mouse.set_visible(0) # make cursor invisible
	
	while True: # main game loop
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		
		pygame.display.update()
		fps_clock.tick(fps)

if __name__=='__main__':
	main()