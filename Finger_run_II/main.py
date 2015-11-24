import Leap, sys, thread, time, math
import pygame
from math import *
import utils.gesture as gesture
from utils.gesture import *
from pygame.locals import *

STEP = 4

class Sprite(pygame.sprite.Sprite):
	def __init__ (self, image_path, rect):
		self.image = pygame.image.load(image_path)
		self.rect = pygame.Rect(rect[0],rect[1],rect[2],rect[3])

	def draw (self, surface):
		surface.blit(self.image, self.rect)

class Obstacle(Sprite):
	def update(self):
		self.rect.left = self.rect.left- STEP

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
Function that draws the cursor imagen on the screen
@cursor: the cursor image
@frame: the current Leap frame
'''

def drawCursor(cursor, frame):
	for hand in frame.hands:
		cursor_pos = getTipPosition(hand, 'index')
		cursor_x = cursor_pos[0]
		cursor_y = cursor_pos[1]
		DISPLAYSURF.blit(cursor, (cursor_x+400,-cursor_y+1000))

def main(arguments):

	#We set the tolerance to 10% by default.
	tolerance = 10

	if (len(arguments) == 2):
		tolerance = int(arguments[1]) #We change the tolerance if we get an argument.

	pygame.init()

	clock = pygame.time.Clock()

	global DISPLAYSURF
	DISPLAYSURF = pygame.display.set_mode((1000,800),0,32)
	pygame.display.set_caption('Game Screen')
	DISPLAYSURF.fill((255,255,255))

	player = Player('images/ph_player.png',(200,368,32,64))
	speed_bar = SpeedBar('images/Speed_bar.png',(50,700,200,32),60)
	obstacles = []
	obstacles.append(Obstacle('images/ph_obstacle.png', (1000,400,32,32)))

	controller = Leap.Controller()

	while  player.alive and not speed_bar.end():

		clock.tick(60) #60 fps lock

		DISPLAYSURF.fill((255,255,255))
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		frame = controller.frame()

		for hand in frame.hands:
			if detectJumpGesture(hand,0):
				player.jump()

			speed_bar.update(detectRunGesture(hand,0))

		for obstacle in obstacles:
			obstacle.update()
			obstacle.draw(DISPLAYSURF)

		player.update()
		player.draw(DISPLAYSURF)

		speed_bar.draw(DISPLAYSURF)

		if (player.collision(obstacles)):
			player.end()

		pygame.display.update()

	DISPLAYSURF.fill((0,0,0))
	pygame.display.update()

	if player.alive:
		print ("Run faster next time.")

	raw_input("End")
'''
	#create cursor's sprite
	cursor_sprite = Sprite('images/cursor.png',(500,400))

	#we create a new controller
	controller = Leap.Controller()


	pygame.display.update()
	# run the game loop

	while  True:
		DISPLAYSURF.fill((255,255,255))
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		frame = controller.frame()
		cursor_sprite.draw(DISPLAYSURF)
		#drawCursor(cursor, frame)
		pygame.display.update()
'''

'''
	#We create a new controller.
	controller = Leap.Controller()


	while True:
		frame = controller.frame()

		for hand in frame.hands:
			if gesture.detectJumpGesture(hand,0):
				print ("Jumping")
			else:
				print ("Not jumping")
'''


if __name__ == '__main__':
	main(sys.argv)
