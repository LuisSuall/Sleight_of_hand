import Leap, sys, thread, time, math
import pygame
from math import *
import utils.gesture as gesture
from utils.gesture import *
from pygame.locals import *

class Sprite(pygame.sprite.Sprite):
	def __init__ (self, image_path, pos):
		self.image = pygame.image.load(image_path)
		self.pos = pos

	def draw (self, surface):
		surface.blit(self.image, self.pos)

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

	global DISPLAYSURF
	DISPLAYSURF = pygame.display.set_mode((1000,800),0,32)
	pygame.display.set_caption('Game Screen')
	DISPLAYSURF.fill((255,255,255))


	#load de cursor image
	cursor = pygame.image.load('images/cursor.png')

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
