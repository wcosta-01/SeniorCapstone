'''
This is the code for discord sent on 3/25
Creates bounding boxes around single characters from a video file.

'''


import numpy as np
import cv2
import pytesseract
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

font_scale = 1.5
font = cv2.QT_FONT_BLACK
RanVidTest= r'C:\Users\deadg\Videos\Rocket League\Rocket League 2019.11.21 - 23.01.18.02\mp4'
#cap = cv2.VideoCapture(2)
cap = cv2.VideoCapture(r"C:\Users\deadg\OneDrive\Documents\GithubRep\SeniorCapstone\recordings\2022_03_25\BookPagein1280\world.mp4")
if not cap.isOpened():
    cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open video")

cntr = 0
while True:
    ret, frame = cap.read()
    cntr = cntr + 1
    if ((cntr%1)==0):

        imgH, imgW, unknownNum = frame.shape
        x1,y1,w1,h1 = 0,0,imgH,imgW
        imgchar = pytesseract.image_to_string(frame)
        imgboxes = pytesseract.image_to_boxes(frame)
        for boxes in imgboxes.splitlines():
            boxes = boxes.split()
            x,y,w,h = int(boxes[1]), int(boxes[2]), int(boxes[3]), int(boxes[4])
            cv2.rectangle(frame, (x, imgH-y), (w,imgH-h), (0,0,255), 3)

        cv2.putText(frame, imgchar, (x1 + int(w1/50), y1 + int(h1/50)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

        font = cv2.FONT_HERSHEY_SIMPLEX

        cv2.imshow('boop', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()