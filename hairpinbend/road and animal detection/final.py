import cv2
import time
from tkinter import *
from PIL import Image, ImageTk
import urllib.request
import requests
import numpy as np

classNames = []
classFile = "coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

print(classNames)

configPath = "ssd_yolo_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)
#.save_value({'value':0})
d=0
count=0
def getObjects(img, thres, nms, draw=True, objects=[]):
    global d
    global count
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    print(className)
                    if className=='elephant' and d==0:
                        print("hai")
                        d=1
                        
                        
                    if d==1 :
                        count=count+1
                   
                    if count>5:
                        count=0
                        d=0
    return img,objectInfo



   

    
def fun():
    url = "http://192.168.227.1/cam-mid.jpg"
    cap = cv2.VideoCapture(url)
    
    
     
   

    
    #img_gray = cv2.cvtColor(img_resp, cv2.COLOR_BGR2GRAY)
    while True:
        img_resp=urllib.request.urlopen(url)
        imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        img_rgb= cv2.imdecode(imgnp,-1)
        #img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        result, objectInfo = getObjects(img_rgb,0.45,0.2)
        

        #print(objectInfo)
        cv2.imshow("Output",img_rgb)
        cv2.waitKey(1)
# Designing window for login 
def login():
    global login_screen
    login_screen = Tk()
    login_screen.title("Login")
    login_screen.geometry("800x700")
    login_screen.configure(background='#3d5705')
    load = Image.open("Elephants.jpg")
    render = ImageTk.PhotoImage(load)
    img = Label(login_screen, image=render)
    img.image = render
    img.place(x=0, y=0)

    
    Label(login_screen, text="Please enter details below to login",bg="#c6eb73", font=("Calibri", 30)).place(x=150,y=10)
    Button(login_screen, text="1", width=30, height=2,bd=5, command = fun,bg="#a6ed07",activebackground="#c6eb73").place(x=100,y=200)
    

 


   
def main_account_screen():
    login()
   
    login_screen.mainloop()
          
         
 
main_account_screen()





