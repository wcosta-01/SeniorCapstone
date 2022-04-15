"""
(*)~----------------------------------------------------------------------------------
 Pupil Helpers
 Copyright (C) 2012-2016  Pupil Labs
 Distributed under the terms of the GNU Lesser General Public License (LGPL v3.0).
 License details are in the file license.txt, distributed as part of this software.
----------------------------------------------------------------------------------~(*)
This example demonstrates how to send simple messages to the Pupil Remote plugin
    'R' start recording with auto generated session name
    'R rec_name' start recording and name new session name: rec_name
    'r' stop recording
    'C' start currently selected calibration
    'c' stop currently selected calibration
    'T 1234.56' Timesync: make timestamps count form 1234.56 from now on.
    't' get pupil timestamp
    '{notification}' send a notification via pupil remote.
"""
import zmq
import msgpack
from imutils.object_detection import non_max_suppression
import pandas as pd
import numpy as np
import pytesseract
import argparse
import imutils
import time
import cv2
import time
from file_dir import video_dir, east_text_det, get_gaze_coords_rt

# https://docs.pupil-labs.com/developer/core/network-api/#pupil-remote
ctx = zmq.Context()
pupil_remote = zmq.Socket(ctx, zmq.REQ)
pupil_remote.connect('tcp://127.0.0.1:50020')

ip = 'localhost'  # If you talk to a different machine use its IP.
port = 50020  # The port defaults to 50020. Set in Pupil Capture GUI.

# Request 'SUB_PORT' for reading data
pupil_remote.send_string('SUB_PORT')
sub_port = pupil_remote.recv_string()

# Request 'PUB_PORT' for writing data
pupil_remote.send_string('PUB_PORT')
pub_port = pupil_remote.recv_string()

# Assumes `sub_port` to be set to the current subscription port
subscriber = ctx.socket(zmq.SUB)
subscriber.connect(f'tcp://{ip}:{sub_port}')
subscriber.subscribe('gaze.')  # receive all gaze messages
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

def rt_data_collection(R_hig, R_wid):
    from file_dir import get_gaze_coords_rt
    count = 0
    numID = 0  # ID for the incoming data
    rt_data = []
    time_stamps = []  # stores the timestamps from the live feed
    norm_pos_x = []  # stores the X coordinate values from the live feed
    norm_pos_y = []  # store the Y coordinates values from the live feed

    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
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

    # otherwise, grab a reference to the video file
    vs = cv2.VideoCapture(0)

    index = 0
    # loop over frames from the video stream

    while True:  # Will keep running till the program is terminated

        topic, payload = subscriber.recv_multipart()
        message = msgpack.loads(payload)
        rt_num = "real_time_{0}".format(numID)
        rt_timestamp = message[b'timestamp']
        rt_data = message[b'norm_pos']
        cur_message = message[b'norm_pos']
        numID += 1
        '''
        time_stamps.append(rt_timestamp)
        norm_pos_x.append(cur_message[0])
        norm_pos_y.append(cur_message[1])
        norm_pos = {"Time_stamps": time_stamps, "norm_pos_x": norm_pos_x, "norm_pos_y": norm_pos_y}
        '''

        # pos_x =0 pos_y =1
        rt_data[0] = rt_data[0] * R_wid
        rt_data[1] = rt_data[1] * R_hig

        rt_data[0] = int(rt_data[0])
        rt_data[1] = int(rt_data[1])
        rt_data[1] = R_hig - rt_data[1]

        toCheck = rt_data
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

        # x = int(toCheck[index][1] / oRW)
        # y = int(toCheck[index][2] / oRH)
        x = int(toCheck[0] / oRW)
        y = int(toCheck[1] / oRH)


        newBound = [x - 25, y - 25, x + 25, y + 25]

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
                # Add padding
                cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

                if(newBound[0] < endX and newBound[2] > startX and newBound[1] < endY and newBound[3] > startY):
                    r = orig[startY:endY, startX:endX]
                    r = cv2.cvtColor(r, cv2.COLOR_BGR2GRAY)
                    r = cv2.GaussianBlur(r, (7, 7), 0)
                    r = cv2.adaptiveThreshold(r, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 4)
                    text = pytesseract.image_to_string(r)
                    cv2.putText(frame, text, (newBound[0], newBound[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                    print(text)
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