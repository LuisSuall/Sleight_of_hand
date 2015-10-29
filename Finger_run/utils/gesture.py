import extendedHand
from extendedHand import *
import math
from math import *

def detectRunGesture(hand):
    index = getFinger(hand, 'index')
    middle = getFinger(hand, 'middle')
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

def detectOKGesture(hand):
	thumb = getFinger(hand, 'thumb')
	index = getFinger(hand, 'index')

	thumb_tip_pos = thumb.bone(3).next_joint
	index_tip_pos = index.bone(3).next_joint

	distanceBtwTips = sqrt(pow(thumb_tip_pos[0]-index_tip_pos[0],2) + pow(thumb_tip_pos[1]-index_tip_pos[1],2) + pow(thumb_tip_pos[2]-index_tip_pos[2],2))

	if distanceBtwTips < 30 and palmOrientation(hand) == 'down':
		return 1
	elif palmOrientation(hand) != "down":
		return 0
	else:
		return 2
