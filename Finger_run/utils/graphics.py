import OpenGL
from OpenGL.GLUT import *
from OpenGL.GL import *
import sys

camera_angle_x = 0

window_pos_x = 50
window_pos_y = 50
window_width = 1024
window_height= 800

frustum_near = 100
frustum_far = 1000
frustum_width = 150
frustum_height = frustum_width * ((window_height*1.0) / window_width)

def setProjection ():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity() 

    # Create frustum
    glFrustum(-frustum_width,frustum_width,-frustum_height,frustum_height, frustum_near, frustum_far) 

    # Center frustum
    glTranslatef(0.0,-500.0,-0.50*(frustum_far+frustum_near))

def setViewport ():
	glViewport(0,0,window_width, window_height)

def setCamera ():
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	glRotatef(camera_angle_x,1.0,0,0)


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

def drawSphere(pos):
	glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )

	glPushMatrix()
	glLoadIdentity()

	glColor3f(1.0,0.0,0.0)
	glTranslatef(pos[0],pos[1],pos[2])
	glutSolidSphere(10,8,8)

	glPopMatrix()

def drawLine(start_pos, end_pos):
	glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
	glColor3f(1.0,1.0,1.0)

	glBegin(GL_LINES)
	glVertex3f( start_pos[0], start_pos[1], start_pos[2] )
	glVertex3f( end_pos[0], end_pos[1], end_pos[2] )
	glEnd()

def drawBone(bone):
	drawSphere(bone.prev_joint)
	drawLine(bone.prev_joint, bone.next_joint)

def drawFinger(finger):
	for b in range(0,4):
		drawBone(finger.bone(b))

def drawHand(hand):
	for finger in hand.fingers:
		drawFinger(finger)

def drawHands(hands):
	for hand in hands:
		glColor3f(1.0,1.0,1.0)
		drawHand(hand)

def drawTexts():
	pass

def drawPredefinedHands():
	pass

def draw():
	glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT)

	setViewport()
	setProjection()
	setCamera()

	frame = controller.frame()

	drawAxis()
	drawLeap()
	drawHands(frame.hands)
	drawTexts()
	drawPredefinedHands()

	glutSwapBuffers()

def keyboardFunc(key, x_mouse, y_mouse):
	if key == 'q' or key == 'Q':
		sys.exit(0)


def initGlut(arguments):

	glutInit(arguments)
	glutInitDisplayMode( GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH )

	glutInitWindowPosition( window_pos_x, window_pos_y )
	glutInitWindowSize( window_width, window_height )

	glutCreateWindow("Finger run")

	glutKeyboardFunc( keyboardFunc )
	glutDisplayFunc(draw)
	glutIdleFunc(draw)


def initOpenGL():
	glEnable( GL_DEPTH_TEST )

	glClearColor(0.0,0.1,0.1,1.0)

	glLineWidth( 8.0 )
	glPointSize( 2.0 )

	glPolygonMode ( GL_FRONT_AND_BACK, GL_LINE)

	setViewport()
	setProjection()
	setCamera()

def init(arguments, newController):
	global controller	
	initGlut(arguments)
	initOpenGL()
	controller = newController

	glutMainLoop()