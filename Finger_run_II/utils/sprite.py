import pygame
from pygame.locals import *

STEP = 4

def idle():
	pass

'''
	Basic Sprite class
'''
class Sprite(pygame.sprite.Sprite):
	def __init__ (self, image_path, rect):
		self.image = pygame.image.load(image_path)
		self.rect = pygame.Rect(rect[0],rect[1],rect[2],rect[3])

	def draw (self, surface):
		surface.blit(self.image, self.rect)

'''
Obstacle class
'''
class Obstacle(Sprite):
	def update(self):
		self.rect.left = self.rect.left- STEP

'''
SpeedBar class
'''
class SpeedBar(Sprite):
	def __init__(self, image_path, rect, idle_time):
		Sprite.__init__(self, image_path, rect)
		self.max_idle_time = idle_time
		self.rect_width = self.rect.width
		self.idle_time = 0

	def update(self, step):
		if step:
			self.idle_time = 0
		else:
			self.idle_time += 1

		self.rect.width = self.rect_width * (((self.max_idle_time - self.idle_time)*1.0)/self.max_idle_time)

	def draw(self, surface):
		rect = pygame.Rect(0,0,self.rect.width, self.rect.height)
		surface.blit(self.image, (self.rect.left, self.rect.top), rect)

	def end(self):
		if self.idle_time >= self.max_idle_time:
			return True
		return False

'''
Player class
'''
class Player(Sprite):
	def __init__(self, image_path, rect):
		Sprite.__init__(self, image_path, rect)
		self.jump_status = 0
		self.alive = True

	def jump(self):
		if self.jump_status == 0:
			self.jump_status = 1

	def update(self):
		if self.jump_status < 0:
			self.jump_status += 1
			self.rect.top = self.rect.top + STEP * 1.5

		else:
			if self.jump_status > 0:
				self.jump_status += 1
				self.rect.top = self.rect.top - STEP * 1.5

				if self.jump_status >= 30:
					self.jump_status = -29

	def collision(self, obstacles):
		for obstacle in obstacles:
			if self.rect.colliderect(obstacle.rect):
				return True

		return False

	def end(self):
		self.alive = False

'''
Button class
'''
class Button(Sprite):
	def __init__(self, image_path_normal, image_path_pressed, rect, button_text, action = idle):
		Sprite.__init__(self, image_path_normal, rect)
		self.image_normal = pygame.image.load(image_path_normal)
		self.image_pressed = pygame.image.load(image_path_pressed)
		self.pressed = False
		self.text = button_text
		self.action = action

	def press(self):
		self.pressed = not self.pressed

		if self.pressed:
			self.image = self.image_pressed
		else:
			self.image = self.image_normal

	def draw(self, surface):
		font = pygame.font.Font(None, 20)
		Sprite.draw(self, surface)
		text = font.render(self.text,0,(255,255,255))
		surface.blit(text, self.rect)


	def act(self, *args):
		self.action(*args)

'''
Cursor class
'''
class Cursor(Sprite):
	def __init__(self, image_path, rect):
		Sprite.__init__(self, image_path, rect)

	def update(self):
		self.rect.left = pygame.mouse.get_pos()[0]
		self.rect.top = pygame.mouse.get_pos()[1]

	def collision(self, buttons):
		for button in buttons:
			if self.rect.colliderect(button.rect) and pygame.mouse.get_pressed()[0]:
				button.press()
