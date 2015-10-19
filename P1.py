import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

def f():
    print "I'm f"

class Gesture:
    def __init__(self, func):
        self.f = func

    def execute(self):
        self.f()

def main():
    a = Gesture(f)
    a.execute()

    print "End"

if __name__ == '__main__':
    main()
