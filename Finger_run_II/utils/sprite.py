import Leap, random
from utils.gesture import *
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

	def isDead(self):
		return self.rect.right < 0


'''
Coin class
'''

class Coin(Sprite):
	def update(self):
		self.rect.left = self.rect.left- STEP

	def isDead(self):
		return self.rect.right < 0


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
		self.image_status = 0
		self.alive = True

	def jump(self):
		if self.jump_status == 0:
			self.jump_status = 1

	def update(self):
		self.image_status = (self.image_status + 1) % 16

		if self.jump_status < 0:
			self.jump_status += 1
			self.rect.top = self.rect.top + STEP

		else:
			if self.jump_status > 0:
				self.jump_status += 1
				self.rect.top = self.rect.top - STEP

				if self.jump_status >= 23:
					self.jump_status = -22

	def collision(self, obstacles):
		for obstacle in obstacles:
			if self.rect.colliderect(obstacle.rect):
				return True

		return False

	def collisionWithCoin(self, coin):
		return self.rect.colliderect(coin.rect)


	def draw(self, surface):
		image_number = self.image_status /4
		rect = pygame.Rect(image_number * 32,0,32, 64)
		surface.blit(self.image, (self.rect.left, self.rect.top), rect)

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
		self.ON = False

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
		self.click = False

	def update(self, frame):

		cursor_x = self.rect.left
		cursor_y = self.rect.top

		for hand in frame.hands:
			cursor_pos = getTipPosition(hand, 'middle')
			cursor_x = cursor_pos[0] * 4 + 300
			cursor_y = -cursor_pos[1] * 2 + 500

		for hand in frame.hands:
			if detectOKGesture(hand, 10):
				self.click = True

		self.rect.left = cursor_x
		self.rect.top =  cursor_y

	def collision(self, buttons):
		for button in buttons:
			if self.rect.colliderect(button.rect) and self.click and button.ON:				
				button.act()

		self.click = False
