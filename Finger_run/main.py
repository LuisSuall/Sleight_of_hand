import Leap, sys, thread, time, math
from math import *
import utils.graphics as graphics
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class Photographer(Leap.Listener):

    def turnOnCamera():
        photo_name = raw_input("Insert photo's basis name, please: ")

        print "Press Enter to take photo..."
        try:
            sys.stdin.readline()
        except KeyboardInterrupt:
            pass
        finally:
            takePhoto(photo_name)

    def takePhoto(photo_name):
        frame = controller.frame()
        finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
        bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

        for hand in frame.hands:
            dataContainer = open(photoName+str(hand.id), 'w')

            print "Storing hand data..."

            for finger in hand.fingers:
                dataContainer.write("Data from %s \n" %finger_names[finger.type])
                for b in range(0, 4):
                    bone = finger.bone(b)
                    dataContainer.write("Data from %s \n" %bone_names[bone.type])
                    dataContainer.write("Start: %s \n Final: %s \n" %(bone.prev_joint, bone.next_joint))
                dataContainer.write("_______________________________________ \n")

            print "Storage complete."

def main(arguments):

	tolerance = 10

	if (len(arguments) == 2):
		tolerance = int(arguments[1])

	controller = Leap.Controller()

	graphics.init(arguments, controller, tolerance)

if __name__ == '__main__':
	main(sys.argv)
