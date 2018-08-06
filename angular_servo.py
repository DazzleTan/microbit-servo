from microbit import *
import servo

def next():
    display.show(Image.ARROW_W)
    while not button_a.is_pressed():
        pass
    while button_a.is_pressed():
        pass
    display.clear()
        
if __name__ == "__main__":
    s=servo.AngularServo(pin0,min_us=200,max_us=2200,max_angle=200)
    while True:
        s.angle(0)
        next()
        s.angle(45)
        next()
        s.angle(90)
        next()
        s.angle(-90)
        next()
