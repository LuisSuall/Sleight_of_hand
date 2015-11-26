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

	#Set the game speed 
	game_speed = 30 + level * 10

	#Set up pygame
	pygame.init()
	clock = pygame.time.Clock()

	global DISPLAYSURF
	DISPLAYSURF = pygame.display.set_mode((640,480),0,32)
	pygame.display.set_caption('Game Screen')

	#Load all sprites
	player = Player('images/player.png',(100,218,32,64))
	speed_bar = SpeedBar('images/Speed_bar.png',(30,418,200,32),60)
	speed_frame = Sprite('images/Speed_frame.png',(20,408,220,52))
	scoreboard_frame = Sprite('images/Speed_frame.png',(400,408,220,52))

	obstacles = []
	obstacles.append(Obstacle('images/obstacle.png', (600,250,32,32)))

	coins = []

	clouds = []
	clouds.append(Cloud('images/cloud.png', (600, 50,32,64)))
	clouds.append(Cloud('images/cloud.png', (200, 50,32,64)))
	clouds.append(Cloud('images/cloud.png', (350, 50,32,64)))

	#Create Leap controller
	controller = Leap.Controller()

	#Game main Loop
	while player.alive and not speed_bar.end():

		clock.tick(game_speed) #FPS Lock

		#Draw background and ground
		DISPLAYSURF.fill((221,215,153))
		pygame.draw.rect(DISPLAYSURF,(96,78,8),pygame.Rect(0,272,640,208) )

		#Handle pygame events
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		#Handle controller
		frame = controller.frame()

		for hand in frame.hands:
			if detectJumpGesture(hand,0):
				player.jump()

			speed_bar.update(detectRunGesture(hand,0))

		#Draw all obstacles
		for obstacle in obstacles:
			obstacle.update()
			obstacle.draw(DISPLAYSURF)
		#Draw all coins
		for coin in coins:
			coin.update()
			coin.draw(DISPLAYSURF)
		#Draw all clouds
		for cloud in clouds:
			cloud.update()
			cloud.draw(DISPLAYSURF)

		#Remove unneeded obstacles
		for obstacle in obstacles:
			if obstacle.isDead():
				obstacles.remove(obstacle)

		#Remove coins
		#Also keeps the scoreboard updated
		for coin in coins:
			if coin.isDead():
				coins.remove(coin)
			elif player.collisionWithCoin(coin):
				scoreboard += 1
				coins.remove(coin)



		#Random obstacle generation:
		if (random.randint(1,50 - level * 10) == 1):
			if (len(obstacles) == 0):
				obstacles.append(Obstacle('images/obstacle.png', (600,250,32,32)))
			elif (obstacles[-1].rect.left <= 600-(32*5)):
				obstacles.append(Obstacle('images/obstacle.png', (600,250,32,32)))

		#Random coin generation:
		if (random.randint(1,30) == 1):
			if (len(coins) == 0):
				coins.append(Coin('images/coin.png', (600,168,32,32)))
			elif (coins[-1].rect.left <= 600-32):
				coins.append(Coin('images/coin.png', (600,168,32,32)))

		#Random cloud generation:
		if (random.randint(1,150) == 1):
			if (len(clouds) == 0):
				clouds.append(Cloud('images/cloud.png', (600, 50,32,64)))
			elif (clouds[-1].rect.left <= 600-32):
				clouds.append(Cloud('images/cloud.png', (600, 50,32,64)))

		#Draw player
		player.update()
		player.draw(DISPLAYSURF)

		#Draw scoreboard and speed bar
		font = pygame.font.Font(None, 40)
		scoreboard_text = font.render(str(scoreboard),0,(0,0,0))
		scoreboard_frame.draw(DISPLAYSURF)
		DISPLAYSURF.blit(scoreboard_text, (scoreboard_frame.rect.left+10,scoreboard_frame.rect.top+10,30,30))
		speed_frame.draw(DISPLAYSURF)
		speed_bar.draw(DISPLAYSURF)

		#If the player hits an obstacle, the game ends
		if (player.collision(obstacles)):
			player.end()

		#Update display
		pygame.display.update()

	#Blue Screen Of Death
	DISPLAYSURF.fill((0,0,128))

	font = pygame.font.Font(None, 22)
	text = font.render("A problem has been detected and Windows has been shut down to prevent damage",0,(255,255,255))
	DISPLAYSURF.blit(text, (0,10))
	text = font.render("to your computer.",0,(255,255,255))
	DISPLAYSURF.blit(text, (0,35))
	
	#Show cause of death
	if player.alive:
		text = font.render("RUN_FASTER_IPHONE_XXL10_SOLD_OUT",0,(255,255,255))
		DISPLAYSURF.blit(text, (0,70))
	else:
		text = font.render("AVOID_WINDOWS_AVOID_BSOD",0,(255,255,255))
		DISPLAYSURF.blit(text, (0,70))

	text = font.render("Try again and beat your score. If you think is just too difficult, buy the DLC.",0,(255,255,255))
	DISPLAYSURF.blit(text, (0,120))

	#Show score
	text = font.render("Score: " + str(scoreboard),0,(255,255,255))
	DISPLAYSURF.blit(text, (0,145))

	text = font.render("Ok gesture to continue.",0,(255,255,255))
	DISPLAYSURF.blit(text, (0,200))

	pygame.display.update()

	#Detect OK gesture to exit
	waiting_ok = True
	while waiting_ok:
		frame = controller.frame()

		for hand in frame.hands:
			if detectOKGesture(hand,0):
				waiting_ok = False

if __name__ == '__main__':
	main(sys.argv)
