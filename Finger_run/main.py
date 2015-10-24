import Leap, sys, thread, time, math
from math import *
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

palm_orientations = ['up', 'down', 'right', 'left']

'''
Function that returns the orientation of the hand's palm.
@hand: the hand that we want to get its palm orientation
'''
def palmOrientation (hand):
    palmNormal = hand.palm_normal
    y = palmNormal[1]
    x = palmNormal[0]

    #We have divided the unit sphere in four quadrants
    if cos(math.pi/4) <= y and y <= 1:
        return palm_orientations[0]
    elif -1 <= y and y <= cos(3*math.pi/4):
        return palm_orientations[1]
    elif x > 0:
        return palm_orientations[2]
    else:
        return palm_orientations[3]

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

'''
Function that detect the Run Gesture
@index: information from the middle finger in the frame
@middle: information from the index finger in the frame
@middle:
'''
def detectRunGesture(hand):
    for finger in hand.fingers:
        if finger.type == 1:
            index = finger
        elif finger.type == 2:
            middle = finger
    #We use the index and the middle finger like two legs and we're going to simulate de run action.
    #Then we need the position information about these fingers.
    index_tip_pos = index.bone(3).next_joint
    middle_tip_pos = middle.bone(3).next_joint

    diffBtwTipsY = index_tip_pos[1] - middle_tip_pos[1] #We compare the Y coordenates of the tips.

    #We check the palm orientation and we want a minimum distance between the two fingers.
    if detectRunGesture.sign*diffBtwTipsY <= -30 and palmOrientation(hand) == 'down':
        detectRunGesture.sign = copysign(1, diffBtwTipsY)
        print ('El signo de la variable global es ' + str(detectRunGesture.sign))
        return True
    else:
        return False

detectRunGesture.sign = -1



def main():
    # Create a sample listener and controller
    photographer = Photographer()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(photographer)

    # Select when to take the photo

    continueV = 'Y'

    while continueV == 'Y':
        #photographer.turnOnCamera()
        frame = controller.frame()

        for i, hand in enumerate(frame.hands):
            if detectRunGesture(hand):
                print ('Has dado un paso')
            else:
                print ('Estas parado')

        continueV = raw_input("Do you want take another photo? Y/N: ")


    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(photographer)

if __name__ == '__main__':
    main()
