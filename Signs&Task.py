from operator import and_
import cv2 as cv
import os
import time
import handtracking as htm
import socket
import time
from requests import get
import requests
import pyautogui

Wcam, Hcam = 640, 480

cam = cv.VideoCapture(0)
cam.set(3, Wcam)
cam.set(4, Hcam)
pTime = 0
detector = htm.handDetector(dectCon=0.75)

tipIds = [4, 8, 12, 16, 20]
ip = socket.gethostname()
local_ip = socket.gethostbyname(ip)
while True:
    success, img = cam.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv.putText(img, f'FPS: {int(fps)}', (40, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv.imshow("Image", img)
    cv.waitKey(1)

    if len(lmList) != 0:

        if lmList[20][2] > lmList[18][2] and lmList[4][1] < lmList[3][1] and lmList[16][2] < lmList[15][2] and lmList[12][2] < lmList[11][2] and lmList[8][2] < lmList[7][2]:
            print("Showing Weather")

        elif (lmList[4][1] < lmList[3][1] and lmList[4][2] < lmList[16][2] and lmList[8][2] > lmList[5][2] > lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] < lmList[19][2]) or(lmList[4][1] > lmList[3][1] and lmList[8][2] > lmList[5][2] > lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] < lmList[19][2] < lmList[18][2]):
            print("Showing ip address of your device")
            print(local_ip)
            time.sleep(3)

        # elif (lmList[4][1] < lmList[3][1] and lmList[8][2] < lmList[7][2] < lmList[6][2] < lmList[4][2] and lmList[10][2] < lmList[12][2] and lmList[14][2] < lmList[15][2] and lmList[18][2] < lmList[19][2] and lmList[5][1] > lmList[10][1]) or (lmList[4][1] > lmList[3][1] and lmList[4][2] < lmList[16][2] and lmList and lmList[8][2] < lmList[7][2] < lmList[6][2] and lmList[10][2] < lmList[12][2] and lmList[14][2] < lmList[15][2] and lmList[18][2] < lmList[19][2] and lmList[5][1] < lmList[10][1]):
        #     print("Showing news.")
        #     main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=3801ee1289054d0b931574de41a92cd0'
        #     main_page = requests.get(main_url).json()
        #     print(main_page)
        #     articles = main_page["articles"]
        #     # print(articles)
        #     head = []
        #     day = ["first", "second", "third", "fourth", "fifth"]
        #     for ar in articles:
        #         head.append(ar["title"])
        #     for i in range(len(day)):
        #         print(f"Today's {day[i]} news is: {head[i]}")
        #     time.sleep(3)

        elif (lmList[4][2] < lmList[3][2] < lmList[2][2] < lmList[1][2] < lmList[0][2] and lmList[5][1] > lmList[7][1] > lmList[6][1] and lmList[9][1] > lmList[11][1] > lmList[10][1] and lmList[17][1] > lmList[19][1] > lmList[18][1]) or (lmList[4][2] < lmList[3][2] < lmList[2][2] < lmList[1][2] < lmList[0][2] and lmList[5][1] < lmList[7][1] < lmList[6][1] and lmList[9][1] < lmList[11][1] < lmList[10][1] and lmList[17][1] < lmList[19][1] < lmList[18][1]):
            print("Showing location.")

        elif lmList[4][2] < lmList[3][2] < lmList[2][2] < lmList[1][2] < lmList[0][2] and lmList[8][2] > lmList[4][2] and lmList[8][1] > lmList[7][1] > lmList[6][1] > lmList[5][1] and lmList[10][1] > lmList[11][1] > lmList[12][1] and lmList[18][1] > lmList[19][1] > lmList[17][1]:
            print("Sliding to the next window")
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            pyautogui.keyUp("alt")
            time.sleep(3)

        elif lmList[4][2] < lmList[3][2] < lmList[2][2] < lmList[1][2] < lmList[0][2] and lmList[8][2] > lmList[4][2] and lmList[8][1] < lmList[7][1] < lmList[6][1] < lmList[5][1] and lmList[10][1] < lmList[11][1] < lmList[12][1] and lmList[18][1] < lmList[19][1] < lmList[17][1]:
            print("Sliding to the 2nd window")
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            pyautogui.press("tab")
            pyautogui.keyUp("alt")
            time.sleep(3)
        
        elif (lmList[8][2]<lmList[6][2] and lmList[4][1]<lmList[3][1] and lmList[12][2]>lmList[10][2] and lmList[16][2]>lmList[14][2] and lmList[20][2]>lmList[18][2]) or (lmList[8][2]<lmList[6][2] and lmList[4][1]>lmList[3][1] and lmList[12][2]>lmList[10][2] and lmList[16][2]>lmList[14][2] and lmList[20][2]>lmList[18][2]):
            print("Volup")
        
        elif (lmList[8][2]>lmList[6][2] and lmList[4][1]>lmList[3][1] and lmList[12][2]<lmList[10][2] and lmList[16][2]<lmList[14][2] and lmList[20][2]<lmList[18][2]) or (lmList[8][2]<lmList[6][2] and lmList[4][1]<lmList[3][1] and lmList[12][2]<lmList[10][2] and lmList[16][2]<lmList[14][2] and lmList[20][2]<lmList[18][2]):
            print("voldown")

    # print("Do u want me to perform something?")

