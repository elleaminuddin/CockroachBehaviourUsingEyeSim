#!/usr/bin/env python3
from eye import *
import urllib.parse as urlparse
from ctypes import *
import random
SAFE = 200
ASPEED = 45
HIDE = 200

def image_diff(i1, i2):
    diff = (c_byte * QVGA_PIXELS)()
    for i in range(QVGA_PIXELS):
        diff[i] = abs(i1[i] - i2[i])
    return diff

def avg(d):
    sum=0
    for i in range(QVGA_PIXELS):
        sum += d[i]
    return int(sum/QVGA_PIXELS)

def sense():
    CAMInit(QVGA)
    image1 = CAMGetGray()
    OSWait(100) # Wait 0.1s
    image2 = CAMGetGray()
    diff = image_diff(image1, image2)
    LCDImageGray(diff)
    avg_diff = avg(diff)
    LCDSetPrintf(0,50, "Avg = %3d", avg_diff)
    OSWait(100)
    if (avg_diff !=0): # Alarm threshold
        LCDSetPrintf(2,50, "ALARM!!!")
        VWTurn(180,90)
        OSWait(100)
        VWStraight(50,50)
        OSWait(100)
    else:
        LCDSetPrintf(2,50, "CLEAR")
        VWStraight(50,50)

def main():
    LCDPrintf("Cockroach Behaviour\n", "")
    LCDMenu("", "", "", "END")
    while True:
        #wall following behaviour
        if PSDGet(PSD_LEFT) > SAFE:
            LCDSetPrintf(2,50, "turning  LEFT\n")
            VWTurn(30, ASPEED)
            VWWait()
            LCDSetPrintf(2,50, "go straight\n")
            VWStraight(100, 300)
            VWWait()
            sense()
        elif PSDGet(PSD_FRONT) > SAFE:
            VWStraight(50, 500)
            sense()
        elif PSDGet(PSD_RIGHT) > SAFE:
            LCDSetPrintf(2,50, "turning RIGHT\n")
            VWTurn(-30, ASPEED)
            VWWait()
            LCDSetPrintf(2,50, "go straight\n")
            VWStraight(50, 500)
            VWWait()
            sense()
        elif (PSDGet (PSD_FRONT) < HIDE) and (PSDGet (PSD_LEFT) < HIDE) and (PSDGet (PSD_RIGHT) < HIDE):
            #hide behaviour
            LCDSetPrintf(2,50, "found a corner, HIDING\n")
            VWTurn(180,90)
            VWWait()
            OSWait(3000)
            LCDSetPrintf(2,50, "ready to go out\n")
            VWStraight(50,100)
            VWWait()
            sense()
        else:
            LCDSetPrintf(2,50, "turn around\n")
            VWTurn(180,90)
            VWWait()
            VWStraight(50,500)
            VWWait()
            sense()


if __name__ == "__main__":
    main()
