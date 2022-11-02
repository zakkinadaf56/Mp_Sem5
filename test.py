import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time
from cvzone.ClassificationModule import Classifier
import tensorflow
import socket
import requests
from bs4 import BeautifulSoup
import pywhatkit as kit
import pyautogui
import os
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume
import sys


cam=cv.VideoCapture(0)
detector=HandDetector(maxHands=1)
classifier=Classifier("Model/keras_model.h5","Model/labels.txt")

devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(
    IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()

minVol=volRange[0]
maxVol=volRange[1]

offset=20
imgSize=300

folder="data/C"
counter=0
# labels=["A","B","C","D","E","F","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","G","H","1","3","4","5","7","8","10"]
labels=["ip","location","music","news","switchwindow","voldown","volup","weather","heart","end"]

ip = socket.gethostname()
local_ip = socket.gethostbyname(ip)

while True:
    success,img=cam.read()
    imgOutput=img.copy()
    hands,img=detector.findHands(img)
    if hands:
        hand=hands[0]
        x,y,w,h=hand['bbox']
        # blank=np.zeros((500,700,3), dtype='uint8')
        blan=cv.imread('Model/blueback.jpg')
        blank=cv.resize(blan,(1000,1000))
        imgWhite=np.ones((imgSize,imgSize,3),np.uint8)*255   #uint8--Unsigned integers of 8 bits

        imgCrop=img[y-offset:y+h+offset,x-offset:x+w+offset]
        imgCropShape=imgCrop.shape


        aspectRatio=h/w
        if aspectRatio>1:
            k=imgSize/h
            wCal=math.ceil(k*w)   #ceil-to round off the decimal
            imgResize=cv.resize(imgCrop,(wCal,imgSize))
            imgResizeShape=imgResize.shape
            wGap=math.ceil((imgSize-wCal)/2)
            imgWhite[0:imgResizeShape[0],wGap:wCal+wGap]=imgResize
            prediction,index=classifier.getPrediction(imgWhite,draw=False)
            print(prediction,index)
            if index==0:
                cv.putText(blank,f"ip address is {local_ip}",(40,250),cv.FONT_HERSHEY_TRIPLEX,1.0,(255,255,255),thickness=2)
            elif index==1:
                time.sleep(3)
                try:
                    ipAdd= requests.get('https://api.ipify.org').text
                    print(ipAdd)
                    url='https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
                    geo_request=requests.get(url)
                    geo_data=geo_request.json()
                    #print(geo_data)
                    city=geo_data['city']
                    #state=geo_data['state']
                    country=geo_data['country']
                    cv.putText(blank,f'Sir I think we are in {city} of {country}',(40,250),cv.FONT_HERSHEY_TRIPLEX,1.0,(255,255,255),thickness=1)
                    time.sleep(3)
                except Exception as e:
                    cv.putText(blank,f'Sorry sir ,I am not able to find our location',(40,250),cv.FONT_HERSHEY_TRIPLEX,1.0,(255,255,255),thickness=1)
                    time.sleep(3)

            elif index==2:
                kit.playonyt("Janam Fidah-e-Haideri by Sadiq Hussain")
                cv.putText(blank,f'Playing music',(40,250),cv.FONT_HERSHEY_TRIPLEX,1.0,(255,255,255),thickness=1)
                time.sleep(3)

            elif index==3:
                main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=3801ee1289054d0b931574de41a92cd0'
                main_page = requests.get(main_url).json()
                print(main_page)
                articles = main_page["articles"]
                # print(articles)
                head = []
                day = ["first", "second", "third", "fourth", "fifth"]
                for ar in articles:
                    head.append(ar["title"])
                for i in range(len(day)):
                    cv.putText(blank,f"Today's {day[i]} news is: {head[i]}\n",(40,250),cv.FONT_HERSHEY_TRIPLEX,1.0,(255,255,255),thickness=1)
                time.sleep(3)
            
            elif index==4:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                # pyautogui.press("tab")
                pyautogui.keyUp("alt")
                time.sleep(3)

            elif index==5:
                volume.SetMasterVolumeLevel(minVol,None)
                cv.putText(blank,f"Volume increased to 0%",(40,250),cv.FONT_HERSHEY_TRIPLEX,1.0,(255,255,255),thickness=1)

                time.sleep(3)
            elif index==6:
                volume.SetMasterVolumeLevel(maxVol,None)
                cv.putText(blank,f"Volume increased to 100%",(40,250),cv.FONT_HERSHEY_TRIPLEX,1.0,(255,255,255),thickness=1)
                time.sleep(3)


            elif index==7:
                search="Temperature in Mumbai"
                url=f"https://www.google.com/search?q={search}"
                we=requests.get(url)
                data=BeautifulSoup(we.text,"html.parser")
                weather=data.find("div",class_="BNeawe").text
                cv.putText(blank,f"{search} is {weather} ",(40,250),cv.FONT_HERSHEY_TRIPLEX,1.0,(255,255,255),thickness=1)
            
            elif index==8:
                
                os.system("shutdown /s /t 5")

            elif index==9:
                print("end")
                quit()
                

        else:
            k=imgSize/w
            hCal=math.ceil(k*h)   #ceil-to round off the decimal
            imgResize=cv.resize(imgCrop,(imgSize,hCal))
            imgResizeShape=imgResize.shape
            hGap=math.ceil((imgSize-hCal)/2)
            imgWhite[hGap:hCal+hGap,0:imgResizeShape[1]]=imgResize
            prediction,index=classifier.getPrediction(imgWhite,draw=False)


        # cv.rectangle(imgOutput,(x-offset,y-offset-50),(x-offset+90,y-offset-50+50),(255,0,255),cv.FILLED)
        cv.putText(imgOutput,labels[index],(x,y-25),cv.FONT_HERSHEY_COMPLEX,1.7,(255,0,255),2)
        cv.rectangle(imgOutput,(x-offset,y-offset),(x+w+offset,y+h+offset),(255,0,255),4)

        cv.imshow("cropped",imgCrop)
        cv.imshow("White",imgWhite)
        cv.imshow('Text',blank)


    cv.imshow("Image",imgOutput)
    cv.waitKey(1)
     