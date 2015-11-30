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
		self.image = pygame.image.load(image_path) #image of the sprite to draw
		self.rect = pygame.Rect(rect[0],rect[1],rect[2],rect[3]) #rectangle of the sprite

	'''
	Function that draws the sprite image in its rectangle
	@surface: the surface where we draw the image
	'''
	def draw (self, surface):
		surface.blit(self.image, self.rect)

'''
Obstacle class
'''
class Obstacle(Sprite):
	'''
	Function that updates the obstacle position
	'''
	def update(self):
		self.rect.left = self.rect.left- STEP

	'''
	Function that checks if the obstacle is out of the screen
	'''
	def isDead(self):
		return self.rect.right < 0


'''
Coin class
'''
class Coin(Sprite):
	'''
	Function that updates the coin position
	'''
	def update(self):
		self.rect.left = self.rect.left- STEP

	'''
	Function that checks if the coin is out of the screen
	'''
	def isDead(self):
		return self.rect.right < 0

'''
Cloud class
'''
class Cloud(Sprite):
	'''
	Function that updates the coin position
	'''
	def update(self):
		self.rect.left = self.rect.left - 1

'''
SpeedBar class
'''
class SpeedBar(Sprite):
	'''
	@image_path: the path of the image of the sprite
	@rect: the Rect of the sprite
	@idle_time: the maximun time that the player can be stood
	'''
	def __init__(self, image_path, rect, idle_time):
		Sprite.__init__(self, image_path, rect)
		self.max_idle_time = idle_time
		self.rect_width = self.rect.width
		self.idle_time = 0 #idle time meter

	'''
	Function that updates the speedbar data
	@step: is the player running? (bool)
	'''
	def update(self, step):
		#Check if the player is running
		if step:
			self.idle_time = 0
		else:
			self.idle_time += 1

		#Update the speedbar length according to the amount of idle time
		self.rect.width = self.rect_width * (((self.max_idle_time - self.idle_time)*1.0)/self.max_idle_time)

	'''
	Function that draws the speedbar
	'''
	def draw(self, surface):
		rect = pygame.Rect(0,0,self.rect.width, self.rect.height)
		surface.blit(self.image, (self.rect.left, self.rect.top), rect)

	'''
	Function that checks if the idle time is too much large
	'''
	def end(self):
		if self.idle_time >= self.max_idle_time:
			return True
		return False

'''
Player class
'''
class Player(Sprite):
	'''
	@image_path: the path of the image of the sprite
	@rect: the Rect of the sprite
	'''
	def __init__(self, image_path, rect):
		Sprite.__init__(self, image_path, rect)
		self.jump_status = 0 #is the player jumping?
		self.image_status = 0
		self.alive = True #is the player alive?

	'''
	Function that begins the jump
	'''
	def jump(self):
		if self.jump_status == 0:
			self.jump_status = 1

	'''
	Function that update the player data
	'''
	def update(self):
		#Change the image to show
		self.image_status = (self.image_status + 1) % 16

		#If the player is falling, move the sprite down
		if self.jump_status < 0:
			self.jump_status += 1
			self.rect.top = self.rect.top + STEP
		#If the player is going up, move the sprite up
		else:
			if self.jump_status > 0:
				self.jump_status += 1
				self.rect.top = self.rect.top - STEP
				#If the player is at the top of the jump, start falling
				if self.jump_status >= 23:
					self.jump_status = -22

	'''
	Function that checks if the player has crashed with a obstacle
	'''
	def collision(self, obstacles):
		for obstacle in obstacles:
			if self.rect.colliderect(obstacle.rect):
				return True

		return False

	'''
	Function that checks if the player has crashed with a coin
	'''
	def collisionWithCoin(self, coin):
		return self.rect.colliderect(coin.rect)

	'''
	Function that draws the player
	'''
	def draw(self, surface):
		image_number = self.image_status /4
		rect = pygame.Rect(image_number * 32,0,32, 64)
		surface.blit(self.image, (self.rect.left, self.rect.top), rect)

	'''
	Function that kills the player
	'''
	def end(self):
		self.alive = False

'''
Button class

'''
class Button(Sprite):
	'''
	@image_path: the path of the image of the sprite
	@rect: the Rect of the sprite
	@button_text: the button's text
	@action: action that the button executes
	'''
	def __init__(self, image_path, rect, button_text, action = idle):
		Sprite.__init__(self, image_path, rect)
		self.text = button_text
		self.action = action
		self.ON = False #is the button on?

	'''
	Function that draws the button and its text
	'''
	def draw(self, surface):
		font = pygame.font.Font(None, 20)
		Sprite.draw(self, surface)
		text = font.render(self.text,0,(119,54,58))
		surface.blit(text, (self.rect.left + 10,self.rect.top + self.rect.height/ 2 -10))

	'''
	Function that executes the button's action
	'''
	def act(self, *args):
		self.action(*args)

'''
Cursor class
'''
class Cursor(Sprite):
	'''
	@image_path: the path of the image of the sprite
	@rect: the Rect of the sprite
	'''
	def __init__(self, image_path, rect):
		Sprite.__init__(self, image_path, rect)
		self.click = False

	'''
	Function that updates the cursor data
	'''
	def update(self, frame):

		cursor_x = self.rect.left
		cursor_y = self.rect.top

		#Set cursor position
		for hand in frame.hands:
			cursor_pos = hand.palm_position
			cursor_x = cursor_pos[0] * 4 + 300    #Adjustment to match the screen
			cursor_y = -cursor_pos[1] * 4 + 1000

		for hand in frame.hands:
			if detectOKGesture(hand, 10):
				self.click = True

		self.rect.left = cursor_x
		self.rect.top =  cursor_y

	'''
	Functions that ckecks if the cursor is over a button
	'''
	def collision(self, buttons):
		for button in buttons:
			if self.rect.colliderect(button.rect) and self.click and button.ON:
				button.act()

		self.click = False
