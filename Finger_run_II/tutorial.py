import Leap, sys, thread, time, math
import pygame
from math import *
import utils.gesture as gesture
from utils.gesture import *
from utils.sprite import *
from pygame.locals import *

def main():
	pygame.init()
	clock = pygame.time.Clock()

	global DISPLAYSURF
	width = 640
	height = 480
	DISPLAYSURF = pygame.display.set_mode((width,height),0,32)
	pygame.display.set_caption('Tutorial')
	phase = 3
	steps_count = 0

	controller = Leap.Controller()
	font = pygame.font.Font(None, 40)
	player = Player('images/player.png',(width/2-32,218,32,64))
	coin = Coin('images/coin.png', (width/2-32,168,32,32))

	ok_text = font.render("Hi Frappoustache! Say OK to begin the tutorial.",0,(119,54,58))
	run_text = font.render("The new iPhone 10XXL has been released, run!",0,(119,54,58))
	jump_text = font.render("Jump to get a coin for a Frappuccino!",0,(119,54,58))
	obstacle_text = font.render("A Windows logo with a poor design, dodge it!",0,(119,54,58))
	bye_text = font.render("The tutorial has finished. Say OK to exit.",0,(119,54,58))

	while True:
		clock.tick(50) #50 fps lock

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		DISPLAYSURF.fill((221,215,153))

		frame = controller.frame()

		if phase == 1:
			DISPLAYSURF.blit(ok_text, (10,0,30,30))
			player.draw(DISPLAYSURF)
			for hand in frame.hands:
				if detectOKGesture(hand,10):
					phase += 1
		elif phase == 2:
			DISPLAYSURF.blit(run_text, (10, 0, 30, 30))
			player.draw(DISPLAYSURF)
			for hand in frame.hands:
				if detectRunGesture(hand,0):
					steps_count += 1
					player.update()
			if steps_count == 10:
				phase += 1
		elif phase == 3:
			DISPLAYSURF.blit(jump_text, (60, 0, 30, 30))
			player.draw(DISPLAYSURF)
			coin.draw(DISPLAYSURF)
		elif phase == 4:
			DISPLAYSURF.blit(obstacle_text, (10,0,30,30))
		else:
			DISPLAYSURF.blit(bye_text,(50,0,30,30))



		pygame.display.update()


if __name__ == "__main__":
	main()
