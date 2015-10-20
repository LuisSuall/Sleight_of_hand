import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

'''
Function to get the plot data of the hand
@hand: the hand object that we want to process.
'''
def getHandPlotData (hand):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    getHandPlotData.counter += 1
    dataContainer = open('handData'+str(getHandPlotData.counter), 'w')

    print "Storing hand data..."

    for finger in hand.fingers:
        dataContainer.write("Data from %s \n" %finger_names[finger.type])
        for b in range(0, 4):
            bone = finger.bone(b)
            dataContainer.write("Data from %s \n" %bone_names[bone.type])
            dataContainer.write("Start: %s \n Final: %s \n" %(bone.prev_joint, bone.next_joint))
        dataContainer.write("_______________________________________ \n")

    print "Storage complete."


getHandPlotData.counter = 0 # initialize getHandPlotData's static counter

class SampleListener(Leap.Listener):

    def on_init(self, controller):
        self.sem = 0
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def turnOn (self):
        self.sem = 1

    def on_frame(self, controller):
        frame = controller.frame()
        for hand in frame.hands:
            if (self.sem == 1):
                getHandPlotData(hand)
                self.sem = 0

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
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Select when to take the photo
    continueV = 'Y'

    while continueV == 'Y':
        print "Press Enter to take photo..."
        try:
            sys.stdin.readline()
        except KeyboardInterrupt:
            pass
        finally:
            listener.turnOn()

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
