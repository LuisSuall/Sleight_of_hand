import Leap, sys, thread, time, math
import pygame
from math import *
import utils.gesture as gesture
from utils.gesture import *
from utils.sprite import *
from pygame.locals import *

def main(level = 1, tol = 10):

	#We set the tolerance to 10% by default.
	tolerance = tol
	scoreboard = 0

	print("Nivel",level)

	pygame.init()
	clock = pygame.time.Clock()

	global DISPLAYSURF
	DISPLAYSURF = pygame.display.set_mode((640,480),0,32)
	pygame.display.set_caption('Game Screen')

	player = Player('images/player.png',(100,218,32,64))
	speed_bar = SpeedBar('images/Speed_bar.png',(30,418,200,32),60)
	speed_frame = Sprite('images/Speed_frame.png',(20,408,220,52))
	scoreboard_frame = Sprite('images/Speed_frame.png',(400,408,220,52))
	obstacles = []
	coins = []
	obstacles.append(Obstacle('images/obstacle.png', (600,250,32,32)))


	controller = Leap.Controller()

	while True:#player.alive and not speed_bar.end():

		clock.tick(50) #50 fps lock

		DISPLAYSURF.fill((221,215,153))
		pygame.draw.rect(DISPLAYSURF,(96,78,8),pygame.Rect(0,272,640,208) )

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

		for coin in coins:
			coin.update()
			coin.draw(DISPLAYSURF)

		for obstacle in obstacles:
			if obstacle.isDead():
				obstacles.remove(obstacle)

		for coin in coins:
			if coin.isDead():
				coins.remove(coin)
			elif player.collisionWithCoin(coin):
				scoreboard += 1
				coins.remove(coin)



		#Random obstacle generation:
		if (random.randint(1,60) == 1):
			if (len(obstacles) == 0):
				obstacles.append(Obstacle('images/obstacle.png', (600,250,32,32)))
			elif (obstacles[-1].rect.left <= 600-32):
				obstacles.append(Obstacle('images/obstacle.png', (600,250,32,32)))

		#Randowm coin generation:
		if (random.randint(1,30) == 1):
			if (len(coins) == 0):
				coins.append(Coin('images/coin.png', (600,168,32,32)))
			elif (coins[-1].rect.left <= 600-32):
				coins.append(Coin('images/coin.png', (600,168,32,32)))

		player.update()
		player.draw(DISPLAYSURF)

		font = pygame.font.Font(None, 40)
		scoreboard_text = font.render(str(scoreboard),0,(0,0,0))
		scoreboard_frame.draw(DISPLAYSURF)
		DISPLAYSURF.blit(scoreboard_text, (scoreboard_frame.rect.left+10,scoreboard_frame.rect.top+10,30,30))
		speed_frame.draw(DISPLAYSURF)
		speed_bar.draw(DISPLAYSURF)

		if (player.collision(obstacles)):
			player.end()

		pygame.display.update()

	DISPLAYSURF.fill((0,0,0))
	pygame.display.update()

	if player.alive:
		print ("Run faster next time.")

if __name__ == '__main__':
	main(sys.argv)
