import extendedHand
from extendedHand import *
import math
from math import *

'''
Function that calculates the @percent % of @whole
'''
def percentage(whole, percent):
	return (whole * percent) / 100.0

'''
Function that detects the run gesture.
@hand: the hand that we're analysing.
@tolerance: the percentage of tolerance in the measurements.
'''
def detectRunGesture(hand, tolerance):
    #We use the index and the middle finger like two legs and we're going to simulate de run action.
    #Then we need the position information about these fingers.
    index = getFinger(hand, 'index')
    middle = getFinger(hand, 'middle')
    
    #We get the tips position of the two fingers.
    index_tip_pos = index.bone(3).next_joint
    middle_tip_pos = middle.bone(3).next_joint
	 
	
	#We calculate the signed difference between the Y coordenates.
	#We use the sign to check that the fingers have been moved.
	
    diffBtwTipsY = index_tip_pos[1] - middle_tip_pos[1]

    #We check the palm orientation and we want a minimum distance between the two fingers.
    if detectRunGesture.sign*diffBtwTipsY <= (-30 + percentage(30, tolerance)) and palmOrientation(hand) == 'down':
        detectRunGesture.sign = copysign(1, diffBtwTipsY)
        return True
    else:
        return False

detectRunGesture.sign = -1

'''
Function that detects the OK gesture.
@hand: the hand that we're analysing.
@tolerance: the percentage of tolerance in the measurements.
'''
def detectOKGesture(hand, tolerance):
	#We use the index finger and the thumb so we need the position information about these fingers.
	thumb = getFinger(hand, 'thumb')
	index = getFinger(hand, 'index')

	#We get the tips position of the two fingers.
	thumb_tip_pos = thumb.bone(3).next_joint
	index_tip_pos = index.bone(3).next_joint

	#We calculate the distance between the tips.
	distanceBtwTips = sqrt(pow(thumb_tip_pos[0]-index_tip_pos[0],2) + pow(thumb_tip_pos[1]-index_tip_pos[1],2) + pow(thumb_tip_pos[2]-index_tip_pos[2],2))

	#We check the palm orientation and the distance between tips.
	if distanceBtwTips < (30 + percentage(30, tolerance)) and palmOrientation(hand) == 'down':
		return True
	else:
		return False
