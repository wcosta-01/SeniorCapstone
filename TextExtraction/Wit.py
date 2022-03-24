import pyttsx3 #Text-To-Speech
import translators as ts #Translator
import pandas as pd #For ease of managing the text
import csv #Writing files
import cv2
import easyocr #Text Detection for images
import pytesseract #Python implementation for Tesseract
from PIL import Image #Pythong Imaging library; use to open images
import matplotlib.pyplot as plt #To show the bounding boxes and detection

#The following is for the APIs: Yelp, Google Search
import requests 
import json
import cleaner

"""
Using Webcam for now; Figure out how to implement the glasses with this
For some reason, look into YOLO


cap = cv2.VideoCapture(0) 
    #Webcam index is 0
#cap = cv2.VideoCapture("freshavacado.mkv")

# Need to test if plt works better instead

if not cap.isOpened():
    cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open video")
"""

#Use this for real time and taking a screenshot
def tesseract():
        #You need to install tesseract first and put in the path where I have mine
    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    image_path = 'test1.jpg'
    pytesseract.tesseract_cmd = path_to_tesseract
    text = pytesseract.image_to_string(Image.open(image_path))
    print(text)

#This one works better with images; reads better
#Currently has a problem with detecting the image from cv2
# takes the image
def easyoc(image):
    reader = easyocr.Reader(['en'])
    #getting the file path from cleaner
    frame_dir = cleaner.dir_path
    #adding the rest of the path to the file
    image_dir = frame_dir + '/' + image
    output = reader.readtext(image_dir)
    for detection in output:
        text = detection[1]
        return print(text)

#Text-To-Speech implementation
def textToSpeech():
    engine = pyttsx3.init()
    engine.say("Target")
    engine.runAndWait()

#Translation implementation
#THIS REQUIRES A CSV FILE
def translate():
    df = pd.read_csv('words.csv')

    translations = {}
    for column in df.columns:
    # Unique elements of the column
        unique_elements = df[column].unique()
        for element in unique_elements:
        # Adding all the translations to a dictionary (translations)
            translations[element] = ts.google(element)
    translations

    """
    Might want to make a method that can either say the word or put it in a file; or just print.
    """

    #Puts all words into a csv
    with open('translated.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        for key in translations:
            writer.writerow(translations.get(key).split())


#Need to code methods that allows you to search for specific things; takes in image or brand
#Or uses texts from EasyOCR or Tesseract as key inputs
#Also somehow use geolocation for this?? 
def yelpSearch():
    api_key= 'AtJYUSjIsRxvWXW8QeItLPf6e0llj845eiPUwugLadUsrqhONyeZixgKz9bVEVPSS_VxoaQJxg6KSDyAHSf2CsGy2xkaaVsOFYcaHZ8JLG32ZtVwUChrxl_UA-gPYnYx'
    headers = {'Authorization': 'Bearer %s' % api_key}

    url='https://api.yelp.com/v3/businesses/search'

    #This would need to be updated with either the brand or the text of the place
    params = {'term':'seafood','location':'New York City'}

    req=requests.get(url, params=params, headers=headers)
