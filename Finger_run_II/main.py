import Leap, sys, thread, time, math
import pygame
from math import *
import utils.gesture as gesture
from utils.gesture import *
from pygame.locals import *
from utils.sprite import *
import game
import tutorial

'''
Function that closes the program
'''
def close():
	sys.exit()

'''
Function that goes to the previous menu
'''
def back():
	global current_menu
	current_menu.turnOffButtons()
	current_menu = current_menu.father

'''
Function that goes to the game menu
'''
def goGameMenu():
	global current_menu, game_menu
	current_menu.turnOffButtons()
	current_menu = game_menu
'''
Function that loads the tutorial
'''
def goTutorial():
	global current_menu
	current_menu.turnOffButtons()
	tutorial.main()
	
'''
Function that loads the game's level 1
'''
def play1():
	global current_menu
	current_menu.turnOffButtons()
	game.main(1)
	
'''
Function that loads the game's level 2
'''
def play2():
	global current_menu
	current_menu.turnOffButtons()
	game.main(2)
	
'''
Function that loads the game's level 3
'''
def play3():
	global current_menu
	current_menu.turnOffButtons()
	game.main(3)

'''
class Menu
'''
class Menu:
	'''
	@buttons: menu's buttons
	@name: menu's name
	@father: previous menu
	'''
	def __init__(self, buttons, name, father = None):
		self.buttons = buttons
		self.father = father
		self.name = name

	'''
	Function that activates all the menu's buttons
	'''
	def turnOnButtons(self):
		for button in self.buttons:
			button.ON = True
	'''
	Function that turns off all the menu's buttons
	'''
	def turnOffButtons(self):
		for button in self.buttons:
			button.ON = False
	
	'''
	Function that draws the menu
	'''
	def draw(self, surface, frame):
		#Check OK gesture
		OK_detected = False
		for hand in frame.hands:
			if detectOKGesture(hand, 10):
				OK_detected = True
				
		#If no OK gesture then activate menu's buttons
		if not OK_detected:
			self.turnOnButtons()
			
		#Draw menu's buttons
		for button in self.buttons:
			button.draw(surface)

def main(arguments):

	#We set the tolerance to 10% by default.
	tolerance = 10

	if (len(arguments) == 2):
		tolerance = int(arguments[1]) #We change the tolerance if we get an argument.

	pygame.init()

	clock = pygame.time.Clock()

	global DISPLAYSURF
	global current_menu
	
	#Configure game screen and its title
	DISPLAYSURF = pygame.display.set_mode((640,480),0,32)
	pygame.display.set_caption('Game Screen')
	
	#Fill the screen with white
	DISPLAYSURF.fill((255,255,255))

	#create cursor's sprite
	cursor = Cursor('images/ph_cursor.png',(400,500,43,43))

	#we create a new controller
	controller = Leap.Controller()
	
	initial_buttons = []
	game_buttons = []
	
	#Create menus' buttons
	title = Button('images/title.png', (170,25,300,150),"")
	exit_button = Button('images/button.png',(220,380,200,80),"EXIT",close)

	back_button = Button('images/button.png',(220,290,200,80),"BACK",back)

	tutorial_button = Button('images/button.png',(220,290,200,80),"TUTORIAL",goTutorial)
	game_button = Button('images/button.png',(220,200,200,80),"GAME", goGameMenu)

	level1_button = Button('images/button.png',(220,20,200,80),"LEVEL 1",play1)
	level2_button = Button('images/button.png',(220,110,200,80),"LEVEL 2",play2)
	level3_button = Button('images/button.png',(220,200,200,80),"LEVEL 3",play3)

	initial_buttons.append(title)
	initial_buttons.append(tutorial_button)
	initial_buttons.append(game_button)
	initial_buttons.append(exit_button)

	game_buttons.append(level1_button)
	game_buttons.append(level2_button)
	game_buttons.append(level3_button)
	game_buttons.append(back_button)
	#game_buttons.append(exit_button)
	
	#Create menus
	global initial_menu, game_menu
	initial_menu = Menu(initial_buttons, "Initial menu")
	game_menu = Menu(game_buttons, "Game menu", initial_menu)
	
	#The first menu is the initial menu
	current_menu = initial_menu

	#Update game screen
	pygame.display.update()
	# run the game loop

	while  True:
		#Fill the screen with white
		DISPLAYSURF.fill((221,215,153))
		
		#Check for QUIT method to close game
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
				
		#Get the new frame
		frame = controller.frame()
		
		#Update cursor data
		cursor.update(frame)
		
		#Draw Exit button and current menu buttons
		exit_button.draw(DISPLAYSURF)
		current_menu.draw(DISPLAYSURF, frame)
		
		#Check buttons clicked
		cursor.collision(current_menu.buttons+[exit_button])
		
		#Draw cursor
		cursor.draw(DISPLAYSURF)
	
		#Update screen
		pygame.display.update()





if __name__ == '__main__':
	main(sys.argv)
