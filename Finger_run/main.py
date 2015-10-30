import Leap, sys, thread, time, math
from math import *
import utils.graphics as graphics
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

def main(arguments):
	
	#We set the tolerance to 10% by default.
	tolerance = 10

	if (len(arguments) == 2):
		tolerance = int(arguments[1]) #We change the tolerance if we get an argument.
	
	#We create a new controller.
	controller = Leap.Controller()
	
	#Launch the game
	graphics.init(arguments, controller, tolerance)

if __name__ == '__main__':
	main(sys.argv)
