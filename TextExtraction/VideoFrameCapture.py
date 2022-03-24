"""
Used to split the video into frames and used to find the matching Image to the value received
from FrameCapture

Returns a string value that is the name of the image that is inside of the Frames directory.


https://www.codegrepper.com/code-examples/python/python+split+video+into+frames

"""

#  C:/Users/deadg/AppData/Local/Programs/Python/Python310/python.exe needs to be rain from this exe idk where its getting the other from because it no longer exists
import cv2
import os

#importing from other files
import FrameCapIMPTest as fCap
from cleaner import is_not_empty
# Assinging values from FrameCapIMPTest
# Make sure to change these to the correct final version of FrameCapture
combined = fCap.coord_comb
ycoord = fCap.coord_y
xcoord = fCap.coord_x

#directories to be changed if need be
frame_dir = r"C:\Users\deadg\OneDrive\Documents\GithubRep\SeniorCapstone\TextExtraction\Frames"
video_dir = r'C:\Users\deadg\OneDrive\Documents\GithubRep\SeniorCapstone\TextExtraction\ExportedData\OldTestData\world.mp4'

def videoToFrames():
  # The location of the exported video file
  vidcap = cv2.VideoCapture(video_dir)
  success, image = vidcap.read()
  count = 0
  while success:
    cv2.imwrite("C:/Users/deadg/OneDrive/Documents/GithubRep/SeniorCapstone/TextExtraction/Frames/frame%d.jpg" % count, image)  # save frame as JPEG file
    success, image = vidcap.read()
    #print('Read a new frame: ', success)
    count += 1

def grabingFrame():
  for file in os.listdir(frame_dir):
    if os.path.isfile(os.path.join(frame_dir, file)):
      # file will look like this frame1.jpg
      # creating a string to iterate through the folder of frames
      expectedStr = "frame" + str(xcoord) + ".jpg"
      # checking if created string matches any of the file names inside the dir
      if file == expectedStr:
        chosenFrame = file
        return chosenFrame

# Checking to make sure there are frames inside the Frames dir
# and adding them if there are not any.
if is_not_empty(frame_dir) == True:
  print("Already contains frames")
  chosenFrame = grabingFrame()
else:
  print("No frames on file, populating now")
  videoToFrames()