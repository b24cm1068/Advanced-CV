import cv2
import mediapipe as mp
import  time


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # RGB image will be sent to hands object
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                # mpDraw.draw_landmarks(img, handLms)      for points on hands
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)    # for connections in hands
        return img

    def findPosition(self, img, HandsNo = 0, draw=True):
                    # object, img, no. of hands, draw
        lmList = []

        if self.results.multi_hand_landmarks:
            mpHands = self.results.multi_hand_landmarks[HandsNo]

            for id, lm in enumerate(mpHands.landmark):
                # print(id, lm)   # ids of every landmark
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)   # exact coordinates of every id
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (int(cx), int(cy)), 10, (0, 0, 255), cv2.FILLED)
                    # makes circle for id = 4 of radius 15

        return lmList



def main():
    cTime = 0
    pTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if lmList != 0:
            print(lmList[4])

        cTime = time.time()     # For current time
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
                    # image, string output, coordinates, font, fontscale, color, thickness

        cv2.imshow("Image", img)
        cv2.waitKey(1)



if __name__ == '__main__':
    main()