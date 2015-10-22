import Leap, sys, thread, time
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

'''
Function that detect the Run Gesture
@index: information from the middle finger in the frame
@middle: information from the index finger in the frame
'''
def detectRunGesture(index, middle):
    #We use the index and the middle finger like two legs and we're going to simulate de run action.
    #Then we need the position information about these fingers.
    index_tip_pos = index.tip_position
    middle_tip_pos = middle.tip_position

def main():
    # Create a sample listener and controller
    photographer = Photographer()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(photographer)

    # Select when to take the photo
    continueV = 'Y'

    while continueV == 'Y':
        photographer.turnOnCamera()
        continueV = raw_input("Do you want take another photo? Y/N: ")


    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == '__main__':
    main()