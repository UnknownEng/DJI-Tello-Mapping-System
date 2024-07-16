#########################IMPORT LIBRARIES ############################

from djitellopy import tello
from time import sleep
import cv2
import math
import kp
import numpy as np

##########################Defining variables##########################

fspeed = 15
aspeed = 50
interval = 0.25

dInterval = 4
aInterval = 12.5

a,d, thetha = 0,0,0   #Initial angle and yaw
x,y = 500, 500  #Origin

points = [(0,0), (0,0)]

########################## Started Defining Functions###################

me = tello.Tello()

me.connect()
print("Connected")

print("Battery is " , me.get_battery())

kp.init()
print("Keyboard Initialized")

me.send_rc_control(0,0,0,0)
sleep(10)
def move():
    lr , fb , ud , yv = 0 ,0 ,0, 0
    
    v = 15 # Linear Sppeed
    aw = 50 #angullar speed
    
    d = 0
    global thetha, x, y, a 
    
    
    if kp.getKey("w"):
        print("Moving Forward")
        fb = v
        d = dInterval
        a = 90
        print("Command Sucessfully Operated")
    elif kp.getKey("x"):
        print("Moving Downwards")
        fb = -v
        d =  - dInterval
        a =  - 90
        print("Command Sucessfully Operated")
    elif kp.getKey("a"):
        print("Moving Left")
        lr = v
        d = - dInterval
        a = 180
        print("Command Sucessfully Operated")
    elif kp.getKey("d"):
        print("Moving Right")
        lr = v
        d = dInterval
        a = -180
        print("Command Sucessfully Operated")
    elif kp.getKey("s"):
        print("Command Hovering Recieved")
        me.hover()
        print("Command Sucessfully Operated")
    elif kp.getKey("z"):
        print("Rotating AntiClockwise")
        yv = -aspeed
        thetha -= aInterval
        print("Command Sucessfully Operated")
    elif kp.getKey("c"):
        print("Rotating Clockwise")
        yv = aspeed
        thetha += aInterval
        print("Command Sucessfully Operated")
    elif kp.getKey("UP"):
        print("Moving Upward")
        ud = v
        print("Command Sucessfully Operated")
    elif kp.getKey("DOWN"):
        print("Moving Down")
        ud = -v
        print("Command Sucessfully Operated")
    elif kp.getKey("v"):
        print("Mission ABorted Drone IS Landed Soon")
        me.land()
        sleep(10)
        me.disconnect()
        print("Command Sucessfully Operated")
    elif kp.getKey("b"):
        print("mISSION Started Drone is takking off")
        me.takeoff()
        print("Command Sucessfully Operated")
    elif kp.getKey("y"):
        print("Emergency Landing")
        while True:
            ud = -v
            if me.get_height() < 10:
                me.land()
                me.disconnect()
                break
            sleep(0.1)      
        print("Command Sucessfully Operated")

    sleep(interval)

    a += thetha

    x += int(d * math.cos(math.radians(a)))                           #building Trajector comonents

    y += int(d * math.sin(math.radians(a)))                        #building tajectory components

    return [lr, fb, ud, yv, x, y]


def drawPoints(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)

    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)

    cv2.putText(img, f'({(points[-1][0] - 500) / 100},{(points[-1][1] - 500) / 100})m',

                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1,

                (255, 0, 255), 1)



while True:
    vals = move()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = np.zeros((1000, 1000, 3), np.uint8)

    if points[-1][0] != vals[4] or points[-1][1] != vals[5]:
        points.append((vals[4], vals[5]))

    drawPoints(img, points)

    cv2.imshow("Output", img)

    cv2.waitKey(1)
        
me.land()

print("Drone Landed")

print("Program Run Sucessfull")
    