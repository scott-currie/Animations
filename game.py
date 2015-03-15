from animation import Animation
import cfg
import os
from player import Player
import pygame
import sys

SCR_WIDTH, SCR_HEIGHT = 800, 600
FPS = cfg.FPS

pygame.init()
screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
background = pygame.Surface(screen.get_size())
background.fill((0,0,0))
background.convert()

player = Player(screen)

fpsTimer = pygame.time.Clock()

while True:
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	player.update()
	
	background.fill((32,32,32))
	player.render(background)
	screen.blit(background, (0,0))	
	pygame.display.flip()
	fpsTimer.tick(FPS)
