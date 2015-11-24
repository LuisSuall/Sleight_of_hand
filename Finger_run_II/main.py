import Leap, sys, thread, time, math
import pygame
from math import *
import utils.gesture as gesture
from utils.gesture import *
from pygame.locals import *
from utils.sprite import *

def close():
	sys.exit()

def back():
	global current_menu
	current_menu = current_menu.father

def goGameMenu():
	global current_menu, game_menu
	current_menu = game_menu

class Menu:
	def __init__(self, buttons, name, father = None):
		self.buttons = buttons
		self.father = father
		self.name = name

	def sayName(self):
		print(self.name)

	def draw(self, surface):
		for button in self.buttons:
			button.draw(surface)
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
	global current_menu
	DISPLAYSURF = pygame.display.set_mode((1000,800),0,32)
	pygame.display.set_caption('Game Screen')
	DISPLAYSURF.fill((255,255,255))

	'''
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
	#cursor_sprite = Sprite('images/ph_cursor.png',(400,500,43,43))
	cursor = Cursor('images/ph_cursor.png',(400,500,43,43))

	#we create a new controller
	controller = Leap.Controller()

	initial_buttons = []
	game_buttons = []

	exit_button = Button('images/ph_button.png','images/ph_pressedbutton.png',(1000-80,0,80,80),"EXIT",close)

	back_button = Button('images/ph_button.png','images/ph_pressedbutton.png',(1000-80,800-80,80,80),"BACK",back)

	tutorial_button = Button('images/ph_button.png','images/ph_pressedbutton.png',(10,100,80,80),"TUTORIAL")
	game_button = Button('images/ph_button.png','images/ph_pressedbutton.png',(120,100,80,80),"GAME", goGameMenu)

	play_button = Button('images/ph_button.png','images/ph_pressedbutton.png',(10,100,80,80),"PLAY")
	level_button = Button('images/ph_button.png','images/ph_pressedbutton.png',(120,100,80,80),"LEVEL")

	initial_buttons.append(tutorial_button)
	initial_buttons.append(game_button)

	game_buttons.append(play_button)
	game_buttons.append(level_button)
	game_buttons.append(back_button)

	global initial_menu, game_menu
	initial_menu = Menu(initial_buttons, "Initial menu")
	game_menu = Menu(game_buttons, "Game menu", initial_menu)

	current_menu = initial_menu


	pygame.display.update()
	# run the game loop

	while  True:
		DISPLAYSURF.fill((255,255,255))
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		#frame = controller.frame()
		exit_button.draw(DISPLAYSURF)
		current_menu.draw(DISPLAYSURF)
		cursor.update()
		cursor.collision(current_menu.buttons+[exit_button])
		cursor.draw(DISPLAYSURF)
		#drawCursor(cursor, frame)
		pygame.display.update()





if __name__ == '__main__':
	main(sys.argv)
