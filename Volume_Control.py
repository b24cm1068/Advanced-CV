import numpy as np
import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import math
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL



cap = cv2.VideoCapture(0)
detector = htm.handDetector()

cTime = 0
pTime = 0

detector = htm.handDetector(detectionCon=0.7)



# Maps my distance range of (20,180) to function range of (-63.5,0)
def map_my_value_to_scalar(my_value, in_min=20, in_max=180):
    my_value = max(in_min, min(in_max, my_value))  # Clamp to range
    scalar = (my_value - in_min) / (in_max - in_min)
    return scalar


def set_volume_level(my_value):
    scalar = map_my_value_to_scalar(my_value)  # 0.0 to 1.0

    # Access system audio interface
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Set scalar volume
    volume.SetMasterVolumeLevelScalar(scalar, None)

# set_volume_level(100)  # ~50%
# set_volume_level(180)  # 100%
# set_volume_level(20)   # 0%



while True:
    success, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)


    if len(lmList) != 0:
        # print(hdList[4])
        x1 = lmList[4][1]
        y1 = lmList[4][2]
        x2 = lmList[8][1]
        y2 = lmList[8][2]
        # print(x1,y1,x2,y2)

        cv2.circle(img, (int(x1), int(y1)), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (int(x2), int(y2)), 10, (0, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), 	(0, 0, 0), 3)
        # Line ban gyi

        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        print(distance)   # (180 - 20 range of max to min)

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        if distance < 20:
            cv2.circle(img, (int(cx), int(cy)), 10, (0, 255, 0), cv2.FILLED)
        elif distance >180:
            cv2.circle(img, (int(cx), int(cy)), 10, (255, 0, 0), cv2.FILLED)
        else:
            cv2.circle(img, (int(cx), int(cy)), 10, (0, 0, 255), cv2.FILLED)
            # Centre pr circle ban gya

        set_volume_level(distance)
        # Sets the volume according to distance between finger and thumb



    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime


    cv2.putText(img, "FPS: " + str(int(fps)), (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 3)


    cv2.imshow("Image", img)
    cv2.waitKey(1)
