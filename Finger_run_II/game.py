import Leap, sys, thread, time, math
import pygame
from math import *
import utils.gesture as gesture
from utils.gesture import *
from utils.sprite import *
from pygame.locals import *

def main(arguments):

	#We set the tolerance to 10% by default.
	tolerance = 10

	if (len(arguments) == 2):
		tolerance = int(arguments[1]) #We change the tolerance if we get an argument.

	pygame.init()
	clock = pygame.time.Clock()

	global DISPLAYSURF
	DISPLAYSURF = pygame.display.set_mode((640,480),0,32)
	pygame.display.set_caption('Game Screen')

	player = Player('images/player.png',(100,218,32,64))
	speed_bar = SpeedBar('images/Speed_bar.png',(30,418,200,32),60)
	speed_frame = Sprite('images/Speed_frame.png',(20,408,220,52))
	obstacles = []
	obstacles.append(Obstacle('images/obstacle.png', (600,250,32,32)))


	controller = Leap.Controller()

	while  player.alive and not speed_bar.end():

		clock.tick(50) #50 fps lock

		DISPLAYSURF.fill((221,215,153))

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

		speed_frame.draw(DISPLAYSURF)
		speed_bar.draw(DISPLAYSURF)

		if (player.collision(obstacles)):
			player.end()

		pygame.display.update()

	DISPLAYSURF.fill((0,0,0))
	pygame.display.update()

	if player.alive:
		print ("Run faster next time.")

	raw_input("End")

if __name__ == '__main__':
	main(sys.argv)