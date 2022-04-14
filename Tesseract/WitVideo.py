# import the necessary packages
from os import O_WRONLY
from imutils.video import VideoStream
from imutils.object_detection import non_max_suppression
import pandas as pd
import numpy as np
import pytesseract
import argparse
import imutils
import time
import cv2
import time
from file_dir import video_dir, get_gaze_coords, east_text_det

print("Running WitVideo")
def decode_predictions(scores, geometry):
    # grab the number of rows and columns from the scores volume, then
    # initialize our set of bounding box rectangles and corresponding
    # confidence scores
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    # loop over the number of rows
    for y in range(0, numRows):
    # extract the scores (probabilities), followed by the
    # geometrical data used to derive potential bounding box
    # coordinates that surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]

        # loop over the number of columns
        for x in range(0, numCols):
        # if our score does not have sufficient probability,
        # ignore it
            if scoresData[x] < 0.7:
                continue

            # compute the offset factor as our resulting feature
            # maps will be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)

            # extract the rotation angle for the prediction and
            # then compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # use the geometry volume to derive the width and height
            # of the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]

            # compute both the starting and ending (x, y)-coordinates
            # for the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            # add the bounding box coordinates and probability score
            # to our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])

        # return a tuple of the bounding boxes and associated confidences
    return (rects, confidences)
'''
def get_gaze_coords(h, w):
    columns = ["world_index", "gaze_point_3d_x", "gaze_point_3d_y"]
    df = pd.read_csv(test_gaze_dir, usecols=columns)

    df["gaze_point_3d_x"] = df["gaze_point_3d_x"].astype(int) + int(w/2)
    df["gaze_point_3d_y"] = df["gaze_point_3d_y"].astype(int) + int(h/2)

    df = df.drop_duplicates(subset = ["world_index"]).reset_index(drop = True)
    # gaze_points.drop_duplicates(subset=["world_index"], inplace=True)
    return df.values.tolist()
'''

#if __name__ == "__main__":
def wit_video():

    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    R_wid = 1280
    R_hig = 720
    toCheck = get_gaze_coords(R_wid, R_hig)

    # initialize the original frame dimensions, new frame dimensions,
    # and ratio between the dimensions

    (W, H) = (None, None)
    (newW, newH) = (320, 320)
    (rW, rH) = (None, None)

    # define the two output layer names for the EAST detector model that
    # we are interested -- the first is the output probabilities and the
    # second can be used to derive the bounding box coordinates of text
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]

    # load the pre-trained EAST text detector
    print("[INFO] loading EAST text detector...")
    net = cv2.dnn.readNet(east_text_det)

    # if a video path was not supplied, grab the reference to the web cam

    # otherwise, grab a reference to the video file
    vs = cv2.VideoCapture(video_dir)

    index = 0
    # loop over frames from the video stream
    while True:
        # grab the current frame, then handle if we are using a
        # VideoStream or VideoCapture object
        if not vs.isOpened():
            vs = cv2.VideoCapture(0)

        _, frame = vs.read()

        # check to see if we have reached the end of the stream
        if frame is None:
            break
        # resize the frame, maintaining the aspect ratio
        frame = imutils.resize(frame, width=1000)
        (oH, oW) = frame.shape[:2]
        oRW = R_wid / float(oW)
        oRH = R_hig / float(oH)
        orig = frame.copy()
        # print(oH, oW)

        # new is the size required for EAST, r is the ratio compared to the actual frame dimension and for EAST
        if W is None or H is None:
            (H, W) = frame.shape[:2]
            rW = W / float(newW)
            rH = H / float(newH)

        # resize the frame, this time ignoring aspect ratio
        frame = cv2.resize(frame, (newW, newH))
        # construct a blob from the frame and then perform a forward pass
        # of the model to obtain the two output layer sets
        blob = cv2.dnn.blobFromImage(frame, 1.0, (newW, newH), (123.68, 116.78, 103.94), swapRB=True, crop=False)
        net.setInput(blob)
        (scores, geometry) = net.forward(layerNames)
        # decode the predictions, then  apply non-maxima suppression to
        # suppress weak, overlapping bounding boxes
        (rects, confidences) = decode_predictions(scores, geometry)
        boxes = non_max_suppression(np.array(rects), probs=confidences)

        # putting in an auto quit

        x = int(toCheck[index][1] / oRW)
        y = int(toCheck[index][2] / oRH)

        newBound = [x - 50, y - 50, x + 50, y + 50]

        cv2.rectangle(orig, (int(newBound[0]), int(newBound[1])), (int(newBound[2]), int(newBound[3])), (0, 255, 0), 2)

        # loop over the bounding boxes
        for (startX, startY, endX, endY) in boxes:
            # scale the bounding box coordinates based on the respective
            # ratios
            # print(startX, startY, endX, endY)
            startX = int(startX * rW)
            startY = int(startY * rH)
            endX = int(endX * rW)
            endY = int(endY * rH)
            # draw the bounding box on the frame
            # print(startX, startY, endX, endY)
            cv2.rectangle(orig, (startX-15, startY-15), (endX+15, endY+15), (0, 255, 0), 2)

            if (newBound[0] < endX and newBound[2] > startX and newBound[1] < endY and newBound[3] > startY):
                r = orig[startY:endY, startX:endX]
                r = cv2.cvtColor(r, cv2.COLOR_BGR2GRAY)
                r = cv2.GaussianBlur(r, (7, 7), 0)
                r = cv2.adaptiveThreshold(r, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 4)
                text = pytesseract.image_to_string(r)
                cv2.putText(frame, text, (newBound[0], newBound[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                print(text)
        # rW = 3.125, rH = 1.75625
        # x = int((-65.8343650936389 + (1280/2)) / oRW)
        # print(x)
        # y = int((-11.8607818305806 + (720/2)) / oRH)
        # print(y)
        # newBound = [(x - 50), (y - 50), (x + 50), (y + 50)]
        # print(newBound)

        # show the output frame
        cv2.imshow("Text Detection", orig)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
        index += 1

    # if we are using a webcam, release the pointer
    # if not args.get("video", False):
    #     vs.stop()
    # otherwise, release the file pointer
    vs.release()
    # close all windows
    cv2.destroyAllWindows()

