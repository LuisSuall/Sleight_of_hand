import math
from math import *

finger_names = ['thumb', 'index', 'middle', 'ring', 'pinky']

def palmOrientation (hand):
    palmNormal = hand.palm_normal
    y = palmNormal[1]
    x = palmNormal[0]

    #We have divided the unit sphere in four quadrants
    if cos(math.pi/4) <= y and y <= 1:
        return 'up'
    elif -1 <= y and y <= cos(3*math.pi/4):
        return 'down'
    elif x > 0:
        return 'right'
    else:
        return 'left'

def getFinger(hand, finger_type):
    for finger in hand.fingers:
        if finger_type == finger_names[finger.type]:
            return finger
