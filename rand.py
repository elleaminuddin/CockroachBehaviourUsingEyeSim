from eye import *
from random import *

safe=300

LCDMenu("","","","END")
while True:
    OSWait(100)
    if(PSDGet(PSD_FRONT)>safe and PSDGet(PSD_LEFT)>safe and PSDGet(PSD_RIGHT)>safe):
        VWStraight(100,50)
    else:
        VWStraight(-25,50)
        VWWait()
        dir=int(180*(random()-0.5))
        VWTurn(dir,45)
        VWWait()