from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import pytesseract
import cv2
from file_dir import get_gaze_coords_image, frame_dir, result_dir, selected_frame_dir, get_gaze_coords_vid
from torch import empty

print("Running get_crafty")
if __name__ == '__main__':
#def craft_image(frame_name):
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    frame_name = ""
    # This needs to be replaced by the frame
    img = cv2.imread(frame_name)
    h, w = img.shape[:2]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    if np.mean(binary) < 127:
        binary = cv2.bitwise_not(binary)

    toCheck = get_gaze_coords_vid(h, w)
    word = " "
    words = []

    # constructing the result file path
    temp_frame = frame_name.replace(".jpg", "")
    result_txt = result_dir + "\\" + "res_" + temp_frame + ".txt"
    print("get_crafty", result_txt)

    my_file = open(result_txt, "r")
    # reading the file
    data = my_file.read()
    data_into_list = data.split("\n")
    newRects = []
    toInt = []
    for box in data_into_list:
        if box.strip():
            toInt = [int(a) for a in box.split(',')]
            newRects.append(toInt)
    print(newRects)
    # binary = img[newRects[0][1]:newRects[0][5], newRects[0][0]:newRects[0][4]]

    for i in range(len(toCheck)):
        x = toCheck[i][1]
        y = toCheck[i][2]

        newBound = [x - 50, y - 50, x + 50, y + 50]
        # cv2.rectangle(img, (newBound[0], newBound[1]), (newBound[2], newBound[3]), (255, 0, 0), 2)

        for j in range(len(newRects)):
            # If one rectangle is on left side of other
            # 607,378 |827,370 |829,430 |609,438
            # top left, top right, bottom right, bottom left
            endX = newRects[j][4]
            startX = newRects[j][0]
            endY = newRects[j][5]
            startY = newRects[j][1]
            # cv2.rectangle(img, (newRects[j][0], newRects[j][1]), (newRects[j][4], newRects[j][5]), (255, 0, 0), 2)

            if(newBound[0] < endX and newBound[2] > startX and newBound[1] < endY and newBound[3] > startY):
                continue
            else:
                binary = img[newRects[j][1]-25:newRects[j][5]+25, newRects[j][0]-25:newRects[j][4]+25]
                text = pytesseract.image_to_string(binary)
                if word != text:
                    words.append(text)
                    word = text
                    print(text)
                break
        # break
    im = plt.imshow(binary)
    plt.show()        