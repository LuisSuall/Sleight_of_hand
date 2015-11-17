import math
from math import *

#We have put this in the same order as the types in the LeapSDK.
finger_names = ['thumb', 'index', 'middle', 'ring', 'pinky']

'''
Function that returns the palm orientation
@hand: the hand that we're analysing.
'''
def palmOrientation (hand):
    palmNormal = hand.palm_normal
    y = palmNormal[1]
    x = palmNormal[0]

    #We have divided the unit sphere in four quadrants and we check the palm_normal's quadrant
    if cos(math.pi/4) <= y and y <= 1:
        return 'up'
    elif -1 <= y and y <= cos(3*math.pi/4):
        return 'down'
    elif x > 0:
        return 'right'
    else:
        return 'left'

'''
Function that returns a finger from a hand.
@hand: the hand whose finger we want to get.
@finger_type: the finger that we want to get.
'''
def getFinger(hand, finger_type):
	 #We try to find the finger in the hand.
    for finger in hand.fingers:
        if finger_type == finger_names[finger.type]:
            return finger
