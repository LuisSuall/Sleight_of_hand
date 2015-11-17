import Leap, sys, thread, time, math
from math import *
import utils.gesture as gesture

def main(arguments):
	
	#We set the tolerance to 10% by default.
	tolerance = 10

	if (len(arguments) == 2):
		tolerance = int(arguments[1]) #We change the tolerance if we get an argument.
	
	#We create a new controller.
	controller = Leap.Controller()
	

	while True:
		frame = controller.frame()

		for hand in frame.hands:
			if gesture.detectJumpGesture(hand,0):
				print ("Jumping")
			else:
				print ("Not jumping")


if __name__ == '__main__':
	main(sys.argv)
