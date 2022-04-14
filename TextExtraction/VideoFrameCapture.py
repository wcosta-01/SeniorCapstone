"""
Used to split the video into frames and used to find the matching Image to the value received
from FrameCapture
Returns a string value that is the name of the image that is inside of the Frames directory.
https://www.codegrepper.com/code-examples/python/python+split+video+into+frames
"""

#  C:/Users/deadg/AppData/Local/Programs/Python/Python310/python.exe needs to be rain from this exe idk where its getting the other from because it no longer exists
import cv2
import os

# importing from other files
from cmd_commands import dir_not_empty
import file_dir

# directories to be changed if need be
frame_dir = file_dir.frame_dir
video_dir = file_dir.video_dir
'''
    Takes the video file that was just recorded and splits it into separate frames. 
'''
print("Running VideoFrameCapture")
def videoToFrames():
    # The location of the exported video file
    vidcap = cv2.VideoCapture(video_dir)
    success, image = vidcap.read()
    count = 0
    create_frame = frame_dir + "/" + "frame%d.jpg"
    while success:
        cv2.imwrite(create_frame % count, image)  # save frame as JPEG file
        success, image = vidcap.read()
        # print('Read a new frame: ', success)
        count += 1

    print("Folder populated")
    return 1
'''
    Finds the given frame within the /Frames directory and makes a string to then be used to connect the 2
'''
def grabbingFrame(image_data):
    for file in os.listdir(frame_dir):
        if os.path.isfile(os.path.join(frame_dir, file)):
            # file will look like this frame1.jpg
            # creating a string to iterate through the folder of frames
            expectedStr = "frame" + str(image_data) + ".jpg"
            # checking if created string matches any of the file names inside the dir
            if file == expectedStr:
                return file

# Checking to make sure there are frames inside the Frames dir
# and adding them if there are not any.
# ---------------------Call this method to run this file
def frame_check():
    from TextExtraction.frame_selection import image_data
    if dir_not_empty(frame_dir):
        print("Already contains frames")
        return grabbingFrame(image_data)
    else:
        print("No frames on file, populating now")
        videoToFrames()
        return frame_check()
