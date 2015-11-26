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
	phase = 1
	steps_count = 0

	controller = Leap.Controller()
	font = pygame.font.Font(None, 40)

	drawCoin = True

	rungestureimages = [pygame.image.load("images/rungesture1.png"),pygame.image.load("images/rungesture2.png")]

	#Create the tutorial's elements
	okgestureimage = Sprite("images/okgesture.png",(width-290,height-280,290,280))
	rungestureimage = Sprite("images/rungesture1.png",(width-290,height-280,290,280))
	player = Player('images/player.png',(width/2-32,218,32,64))
	coin = Coin('images/coin.png', (width/2-32,168,32,32))
	obstacle = Obstacle('images/obstacle.png', (600,250,32,32))

	ok_text = font.render("Hi Frappoustache! Say OK to begin the tutorial.",0,(119,54,58))
	run_text = font.render("The new iPhone 10XXL has been released, run!",0,(119,54,58))
	jump_text = font.render("Jump to get a coin for a Frappuccino!",0,(119,54,58))
	obstacle_text = font.render("A Windows logo with a poor design, dodge it!",0,(119,54,58))
	bye_text = font.render("The tutorial has finished. Say OK to exit.",0,(119,54,58))
	runimage_index = 0

	while phase <= 5:
		clock.tick(50) #50 fps lock

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		DISPLAYSURF.fill((221,215,153))

		frame = controller.frame()

		if phase == 1:
			okgestureimage.draw(DISPLAYSURF)
			DISPLAYSURF.blit(ok_text, (10,0,30,30))
			player.draw(DISPLAYSURF)
			#We have to make the OK gesture to continue
			for hand in frame.hands:
				if detectOKGesture(hand,10):
					phase += 1
		elif phase == 2:
			rungestureimage.draw(DISPLAYSURF)
			DISPLAYSURF.blit(run_text, (10, 0, 30, 30))
			player.draw(DISPLAYSURF)
			#Check run gesture
			for hand in frame.hands:
				if detectRunGesture(hand,0):
					runimage_index = (runimage_index+1)%2
					rungestureimage.image = rungestureimages[runimage_index]
					steps_count += 1
					player.update()

			#We have to make the some steps to continue
			if steps_count == 10:
				phase += 1
		elif phase == 3:
			DISPLAYSURF.blit(jump_text, (60, 0, 30, 30))
			player.update()
			player.draw(DISPLAYSURF)
			if drawCoin:
				coin.draw(DISPLAYSURF)

			#Check jump gesture
			for hand in frame.hands:
				if detectJumpGesture(hand,0):
					player.jump()

			#Check if we have caught the coin
			if player.collisionWithCoin(coin):
				drawCoin = False

			#We have to complete a jump to continue
			if (not drawCoin and player.rect.top == 218):
				phase += 1
		elif phase == 4:
			DISPLAYSURF.blit(obstacle_text, (10,0,30,30))
			player.draw(DISPLAYSURF)
			player.update()
			obstacle.update()
			obstacle.draw(DISPLAYSURF)

			#If we don't dodge the obstacle then we reset
			if player.collision([obstacle]):
				obstacle.rect.left = 600

			#Check jump gesture
			for hand in frame.hands:
				if detectJumpGesture(hand,0):
					player.jump()

			#We have to dodge the obstacle to continue
			if obstacle.isDead():
				phase += 1
		else:
			DISPLAYSURF.blit(bye_text,(50,0,30,30))
			player.update()
			player.draw(DISPLAYSURF)

			#We have to make OK gesture to continue
			for hand in frame.hands:
				if detectOKGesture(hand,10):
					phase += 1




		pygame.display.update()


if __name__ == "__main__":
	main()
