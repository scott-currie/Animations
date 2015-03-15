# from animation import Animation
import copy
from animation import Animation
import itertools
from spritesheet import SpriteSheet 
import pygame
import random

class Player(pygame.sprite.Sprite):
	def __init__(self, screen):
		pygame.sprite.Sprite.__init__(self)
		spriteSheet = SpriteSheet('john_26x28.png', 8, 4)	
		self.anims = {}
		self.get_animations(spriteSheet)
		self.animation = self.anims['idle_r']
		self.animation.play()
		self.image = None
		#Get player rect from first frame of default animation.
		self.rect = self.anims['idle_r'].frames[0].get_rect()
		self.rect.center = screen.get_rect().center
		self.state = {'idle': True, 'walk': False, 'punch': False, 
						'kick': False, 'left': False, 'right': True}

	def get_animations(self, spriteSheet):
		self.anims['idle_r'] = Animation(spriteSheet, (0,0), (1,0), .7)
		self.anims['walk_r'] = Animation(spriteSheet, (2,0), (3,0), .5)
		self.anims['punch_r'] = Animation(spriteSheet, (0,1), (2,1), .25)
		self.anims['kick_r'] = Animation(spriteSheet, (0,2), (2,2), .25)
		self.anims['reel_r'] = Animation(spriteSheet, (0,3), (0,3), 1.0) 
		self.anims['idle_l'] = Animation(spriteSheet, (4,0), (5,0), .7)
		self.anims['walk_l'] = Animation(spriteSheet, (6,0), (7,0), .5)
		self.anims['punch_l'] = Animation(spriteSheet, (4,1), (6,1), .25)
		self.anims['kick_l'] = Animation(spriteSheet, (4,2), (6,2), .25)
		self.anims['reel_l'] = Animation(spriteSheet, (4,3), (4,3), 1.0) 
		#for animation in self.anims:
		#	print(animation + ' length = ' + str(len(self.anims[animation].frames)))		

	def check_state_changed(self):
		# State change is only valid if currently in idle or walk state.
		if self.state['idle'] or self.state['walk'] or ((self.state['punch'] or self.state['kick']) and self.animation.finished):
			# Copy current state to prevState to quickly recognize changes
			prevState = dict(self.state)
			keys = pygame.key.get_pressed()
			if keys[pygame.K_RIGHT]:
				# Already facing right? Walk right. Else idle.
				if self.state['right']:
					self.state['walk'] = True
					self.state['idle'] = False
				else:
					self.state['idle'] = True 
				self.state['left'] = False
				self.state['right'] = True
			elif keys[pygame.K_LEFT]:
				# Already facing left? Walk left, else idle.
				if self.state['left']:
					self.state['walk'] = True
					self.state['idle'] = False
				else:
					self.state['idle'] = True
				self.state['right'] = False
				self.state['left'] = True
			elif keys[pygame.K_z]:
				self.state['punch'] = True
				self.state['kick'] = False
				self.state['idle'] = False
			elif keys[pygame.K_x]:
				self.state['kick'] = True
				self.state['punch'] = False
				self.state['idle'] = False
			else:
				self.state['punch'], self.state['kick'], self.state['walk'] = False, False, False
				self.state['idle'] = True
			# Can't be idle if doing anything else.
			if self.state['walk'] or self.state['punch'] or self.state['kick']:
				self.idle = False
			#Did state change from previous check? Return True.
			if prevState != self.state:
				return True
			else:
				return False
		else:
			# Wasn't eligible for state change.
			return False

	def choose_animation(self):
		""" Analyze player state and return correct animation object. """
		if self.state['walk']:
			if self.state['right']:
				animation = 'walk_r'
			elif self.state['left']:
				animation = 'walk_l'
		elif self.state['punch']:
			if self.state['right']:
				animation = 'punch_r'
			elif self.state['left']:
				animation = 'punch_l'				
		elif self.state['kick']:
			if self.state['right']:
				animation = 'kick_r'
			elif self.state['left']:
				animation = 'kick_l'				
		else:
			if self.state['right']:
				animation = 'idle_r'
			elif self.state['left']:
				animation = 'idle_l'				
		return self.anims[animation]

	def update(self):
		#Need to change or restart animation if current animation
		#finishes or a valid state change takes place. check_events()
		#will return False if player is in uninterruptable state\animation.
		if self.check_state_changed() or self.animation.finished:
			self.animation = self.choose_animation()
			self.animation.play()
		self.image = self.animation.next_frame()
		
	def render(self, background):
		background.blit(self.image, self.rect)