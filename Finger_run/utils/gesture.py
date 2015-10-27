import math
from math import *

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
        return True
    else:
        return False

detectRunGesture.sign = -1
