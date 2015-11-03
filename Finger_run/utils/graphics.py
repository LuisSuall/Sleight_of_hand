import OpenGL
import time
from OpenGL.GLUT import *
from OpenGL.GL import *
import sys, math, os
from math import *
import pygame
import gesture

'''
Values to configure OpenGL
'''
camera_angle_x = 0

window_pos_x = 50
window_pos_y = 50
window_width = 1024
window_height= 800

frustum_near = 100
frustum_far = 500
frustum_width = 150
frustum_height = frustum_width * ((window_height*1.0) / window_width)

'''
Values to track game status
'''
steps = 0
running = False
counter = 0


'''
Function that sets the projection
'''
def setProjection ():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Create frustum
    glFrustum(-frustum_width,frustum_width,-frustum_height,frustum_height, frustum_near, frustum_far)

    # Center frustum
    glTranslatef(0.0,-300.0,-0.50*(frustum_far+frustum_near))

'''
Function that sets the window
'''
def setViewport ():
	glViewport(0,0,window_width, window_height)

'''
Function that sets the camera
'''
def setCamera ():
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	glRotatef(camera_angle_x,1.0,0,0)

'''
Auxiliary function to draw the axis to help with debugging
'''
def drawAxis():
	long_ejes = 300.0

	glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

	glBegin(GL_LINES)

	glColor3f( 1.0, 0.0, 0.0 )
	glVertex3f( 0.0, 0.0, 0.0 )
	glVertex3f( +long_ejes, 0.0, 0.0 )

	glColor3f( 0.0, 1.0, 0.0 )
	glVertex3f( 0.0, 0.0, 0.0 )
	glVertex3f( 0.0, +long_ejes, 0.0 )

	glColor3f( 0.0, 0.0, 1.0 )
	glVertex3f( 0.0, 0.0, 0.0)
	glVertex3f( 0.0, 0.0, +long_ejes )
	glEnd()

	glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
	glColor3f(0.0,0.0,0.0)
	glutSolidSphere(8,8,8)

'''
Function that draws a Leap in (0,0,0)
'''

def drawLeap():
	width = 80
	hight = 12
	depth = 30


	glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )

	glBegin(GL_QUADS)

	glColor3f( 0.0, 0.0, 0.0 )

	glVertex3f(0.5*width,0.5*hight,0.5*depth)
	glVertex3f(-0.5*width,0.5*hight,0.5*depth)
	glVertex3f(-0.5*width,0.5*hight,-0.5*depth)
	glVertex3f(0.5*width,0.5*hight,-0.5*depth)

	glVertex3f(0.5*width,-0.5*hight,0.5*depth)
	glVertex3f(-0.5*width,-0.5*hight,0.5*depth)
	glVertex3f(-0.5*width,-0.5*hight,-0.5*depth)
	glVertex3f(0.5*width,-0.5*hight,-0.5*depth)

	glColor3f( 1.0, 1.0, 1.0 )

	glVertex3f(0.5*width,0.5*hight,0.5*depth)
	glVertex3f(0.5*width,-0.5*hight,0.5*depth)
	glVertex3f(0.5*width,-0.5*hight,-0.5*depth)
	glVertex3f(0.5*width,0.5*hight,-0.5*depth)

	glVertex3f(-0.5*width,0.5*hight,0.5*depth)
	glVertex3f(-0.5*width,-0.5*hight,0.5*depth)
	glVertex3f(-0.5*width,-0.5*hight,-0.5*depth)
	glVertex3f(-0.5*width,0.5*hight,-0.5*depth)

	glVertex3f(0.5*width,0.5*hight,0.5*depth)
	glVertex3f(-0.5*width,0.5*hight,0.5*depth)
	glVertex3f(-0.5*width,-0.5*hight,0.5*depth)
	glVertex3f(0.5*width,-0.5*hight,0.5*depth)

	glVertex3f(0.5*width,0.5*hight,-0.5*depth)
	glVertex3f(-0.5*width,0.5*hight,-0.5*depth)
	glVertex3f(-0.5*width,-0.5*hight,-0.5*depth)
	glVertex3f(0.5*width,-0.5*hight,-0.5*depth)

	glEnd()

'''
Function that draws a sphere at @pos
'''
def drawSphere(pos):
	glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )

	glPushMatrix()
	glLoadIdentity()

	glColor3f(1.0,0.0,0.0)
	glTranslatef(pos[0],pos[1],pos[2])
	glutSolidSphere(10,8,8)

	glPopMatrix()
'''
Function that draws a line from @start_pos to @end_pos
'''
def drawLine(start_pos, end_pos):
	glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
	glColor3f(1.0,1.0,1.0)

	glBegin(GL_LINES)
	glVertex3f( start_pos[0], start_pos[1], start_pos[2] )
	glVertex3f( end_pos[0], end_pos[1], end_pos[2] )
	glEnd()

'''
Function that draws a bone:
	Draws a sphere at the joint closer to the wrist
	Draws a line from one joint to the other
'''
def drawBone(bone):
	drawSphere(bone.prev_joint)
	drawLine(bone.prev_joint, bone.next_joint)

'''
Function that draws a finger
'''
def drawFinger(finger):
	for b in range(0,4):
		drawBone(finger.bone(b))

'''
Function that draws a hand
'''
def drawHand(hand):
	for finger in hand.fingers:
		drawFinger(finger)

'''
Function that draws a list of hands
'''
def drawHands(hands):
	for hand in hands:
		glColor3f(1.0,1.0,1.0)
		drawHand(hand)

'''
Function that shows @steps
'''
def drawSteps(steps):
	glPushMatrix()
	glLoadIdentity()

	glColor3f(1.0,1.0,0.0)
	glRasterPos2f( 250.0,0 )
	glScalef(20.0,20.0,20.0)

	for letter in steps:
		glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(letter))

	glPopMatrix()

'''
Function that shows @text
'''
def drawText(text):
	glPushMatrix()
	glLoadIdentity()

	glColor3f(1.0,1.0,0.0)
	glRasterPos2f( -300.0,0 )
	glScalef(20.0,20.0,20.0)

	for letter in text:
		glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(letter))

	glPopMatrix()

'''
Function that draws the scene
'''
def draw():
	glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT) #Clean the frame

	setViewport()
	setProjection()
	setCamera()

	#Game status control
	global steps, running, counter

	frame = controller.frame()

	if running:
		drawText("Hold Ok gesture to close")
		for hand in frame.hands:

			if gesture.detectRunGesture(hand, tolerance): #If a step is detected, count it
				steps = steps + 1

			#If ok gesture is detected for 60 frames, close the game

			if gesture.detectOKGesture(hand, tolerance): 
				counter = counter + 1
			else:
				counter = 0

			if counter > 60:
				sys.exit(0)



	else:
		drawText("Ok gesture to start")

		for hand in frame.hands:
			if gesture.detectOKGesture(hand, tolerance):
				running = True
				pygame.mixer.music.play(-1)
			

	drawLeap()
	drawHands(frame.hands)
	drawSteps(str(steps))

	glutSwapBuffers() #Change this frame and the old frame

'''
Function to recognize the letter 'q' as exit
'''
def keyboardFunc(key, x_mouse, y_mouse):
	if key == 'q' or key == 'Q':
		sys.exit(0)

'''
Function that sets window and OpenGL loop
'''
def initGlut(arguments):

	glutInit(arguments)
	glutInitDisplayMode( GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH )

	glutInitWindowPosition( window_pos_x, window_pos_y )
	glutInitWindowSize( window_width, window_height )

	glutCreateWindow("Finger run")

	glutKeyboardFunc( keyboardFunc )
	glutDisplayFunc(draw)
	glutIdleFunc(draw)

'''
Function that sets graphics configurations
'''
def initOpenGL():
	glEnable( GL_DEPTH_TEST ) #Needed to use 3D graphics

	glClearColor(0.0,0.1,0.1,1.0) 

	glLineWidth( 8.0 )
	glPointSize( 2.0 )

	glPolygonMode ( GL_FRONT_AND_BACK, GL_LINE)

	setViewport()
	setProjection()
	setCamera()

def init(arguments, newController, newTolerance):
	global controller
	controller = newController #Set the controller

	global tolerance
	tolerance = newTolerance #Set the tolerance


	#Tutorial
	pygame.init()
	img = pygame.image.load(os.path.abspath('utils/images/tutorial1.jpg'))
	screen = pygame.display.set_mode((1024,800))
	screen.blit(img,(0,0))
	pygame.display.flip()

	img = pygame.image.load(os.path.abspath('utils/images/tutorial2.jpg'))
	screen.blit(img,(0,0))
	time.sleep(5)
	pygame.display.flip()

	img = pygame.image.load(os.path.abspath('utils/images/tutorial3.jpg'))
	screen.blit(img,(0,0))

	waitingOk = True

	# Wait gesture "OK" to start the game
	while waitingOk:
		time.sleep(0.02)
		frame = controller.frame()

		for hand in frame.hands:

			if gesture.detectOKGesture(hand, tolerance) == 1:
				waitingOk = False

	pygame.display.flip()

	time.sleep(3)

	pygame.display.quit()

	#Load music
	pygame.mixer.init()
	pygame.mixer.music.load(os.path.abspath('utils/epic_music.mp3'))

	#Set OpenGL
	initGlut(arguments)
	initOpenGL()

	#Start OpenGL loop
	glutMainLoop()
