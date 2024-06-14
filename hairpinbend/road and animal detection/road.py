import cv2
import time
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

def field1(a):

    import urllib.request as urllib2
    b=urllib2.urlopen('https://api.thingspeak.com/update?api_key=HR54PKQGW1WFFYEB&'+a)
    print("\nYour message has successfully been sent!")
    b.close()
def getObjects(img1,img2,thres, nms, draw=True, objects=[]):
    global d
    global count
    classIds1, confs1, bbox1 = net.detect(img1,confThreshold=thres,nmsThreshold=nms)
    classIds2, confs2, bbox2 = net.detect(img2,confThreshold=thres,nmsThreshold=nms)
    
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds1) != 0:
        for classId, confidence,box in zip(classIds1.flatten(),confs1.flatten(),bbox1):
            className1 = classNames[classId - 1]
            if className1 in objects:
                objectInfo.append([box,className1])
                if (draw):
                    cv2.rectangle(img1,box,color=(0,255,0),thickness=2)
                    cv2.putText(img1,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img1,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    print(className1)
                    if className1=="bus" or className1=="car" or className1=="truck":
                       print("hello1")
                       field1("field1=1")
                       time.sleep(20)
                       field1("field1=0")
                       time.sleep(20)
        cv2.imshow("Output1",img1)
        
    if len(objects) == 0: objects = classNames
    objectInfo2 =[]
    if len(classIds2) != 0:
        for classId1, confidence1,box1 in zip(classIds2.flatten(),confs2.flatten(),bbox2):
            className2 = classNames[classId1 - 1]
            if className2 in objects:
                objectInfo2.append([box1,className2])
                if (draw):
                    cv2.rectangle(img2,box1,color=(0,255,0),thickness=2)
                    cv2.putText(img2,classNames[classId1-1].upper(),(box1[0]+10,box1[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img2,str(round(confidence1*100,2)),(box1[0]+200,box1[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    print(className2)
                    if className2=="bus" or className2=="car" or className2=="truck":
                       print("hello2")
                       field1("field1=2")
                       time.sleep(20)
                       field1("field1=0")
                       time.sleep(20)
        cv2.imshow("Output2",img2)
        cv2.waitKey(1)

def fun():
    url1 = "http://192.168.200.181/cam-mid.jpg"
    url2 = "http://192.168.200.234/cam-mid.jpg"
    #cap = cv2.VideoCapture(0)
    #cap.set(3,640)
    #cap.set(4,480)
    #cap.set(10,70)


    while True:
        #success, img = cap.read()
        
        img_resp1=urllib.request.urlopen(url1)
        imgnp=np.array(bytearray(img_resp1.read()),dtype=np.uint8)
        img_rgb1= cv2.imdecode(imgnp,-1)

        img_resp2=urllib.request.urlopen(url2)
        imgnp2=np.array(bytearray(img_resp2.read()),dtype=np.uint8)
        img_rgb2= cv2.imdecode(imgnp2,-1)
        #img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        getObjects(img_rgb1,img_rgb2,0.45,0.2,objects=['bus', 'car', 'truck'])
        #print(objectInfo)
        


fun()



