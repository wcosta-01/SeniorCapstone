import numpy as np
import cv2
import pytesseract
import pandas as pd
from matplotlib import pyplot as plt
from imutils.object_detection import non_max_suppression

def east_detect(image):
    layerNames = [
    	"feature_fusion/Conv_7/Sigmoid",
    	"feature_fusion/concat_3"]
    
    orig = image.copy()
    
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    
    (H, W) = image.shape[:2]
    
    # set the new width and height and then determine the ratio in change
    # for both the width and height: Should be multiple of 32
    (newW, newH) = (320, 320)
    
    rW = W / float(newW)
    rH = H / float(newH)
    
    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (newW, newH))
    
    (H, W) = image.shape[:2]
    
    net = cv2.dnn.readNet("frozen_east_text_detection.pb")
    
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H), (123.68, 116.78, 103.94), swapRB=True, crop=False)
    
    net.setInput(blob)
    
    (scores, geometry) = net.forward(layerNames)
    
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []
    # loop over the number of rows
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the geometrical
        # data used to derive potential bounding box coordinates that
        # surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]
    
        for x in range(0, numCols):
    		# if our score does not have sufficient probability, ignore it
            # Set minimum confidence as required
            if scoresData[x] < 0.5:
                continue
    		# compute the offset factor as our resulting feature maps will
            #  x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)
            # extract the rotation angle for the prediction and then
            # compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)
            # use the geometry volume to derive the width and height of
            # the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]
            # compute both the starting and ending (x, y)-coordinates for
            # the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)
            # add the bounding box coordinates and probability score to
            # our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])
                        
    boxes = non_max_suppression(np.array(rects), probs=confidences)
    newRects = []
    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
    	# scale the bounding box coordinates based on the respective
    	# ratios
        startX = int(startX * rW) - 10
        startY = int(startY * rH) - 10
        endX = int(endX * rW) + 10
        endY = int(endY * rH) + 10

        # r = orig[startY:endY, startX:endX]
        newRects.append([startX, startY, endX, endY])

        # text = pytesseract.image_to_string(r)
        # print(text)

        # newRects.append((startX, startY, endX, endY))
    	# draw the bounding box on the image
        cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

    return orig, newRects

def get_gaze_coords(h, w):
    columns = ["gaze_point_3d_x", "gaze_point_3d_y"]
    df = pd.read_csv("newTest/gaze_positions.csv", usecols=columns)
    print("Contents in csv file:\n", df)

    df["gaze_point_3d_x"] = df["gaze_point_3d_x"].astype(int) + w/2
    df["gaze_point_3d_y"] = df["gaze_point_3d_y"].astype(int) + h/2
    df.loc[:, "gaze_point_3d_y"] = -df.gaze_point_3d_y

    plt.plot(df.gaze_point_3d_x, df.gaze_point_3d_y)

if __name__ == "__main__":

    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    img = cv2.imread("save\\newTest\world\\50.png")
    h, w = img.shape[:2]

    # Preprocessing for the image, binarizing it
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 4)
    
    orig, newRects = east_detect(thresh)
    # print(newRects)

    # Test input of a gaze
    x = int(-135.636716707316 + (w/2))
    y = int(-75.8148250095352 + (h/2))
    newBound = [x - 50, y - 50, x + 50, y + 50]
    cv2.rectangle(orig, (newBound[0], newBound[1]), (newBound[2], newBound[3]), (0, 255, 0), 2)

    for i in range(len(newRects)):
        # If one rectangle is on left side of other
        if(newBound[0] >= newRects[i][2] or newBound[2] <= newRects[i][0]):
            continue
        # If one rectangle is above other
        elif(newBound[1] >= newRects[i][3] or newBound[3] <= newRects[i][3]):
            continue
        else: 
            r = orig[newRects[i][1]:newRects[i][3], newRects[i][0]:newRects[i][2]]
            text = pytesseract.image_to_string(r)
            print(text)
            break

    im = plt.imshow(orig)
    plt.show()

# Shout out to this guy. Now let's do it in real time
# https://medium.com/technovators/scene-text-detection-in-python-with-east-and-craft-cbe03dda35d5