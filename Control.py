'''
    This file controls the entire operation.
    Used to connect, run and test all the methods of the other files in the correct order.
'''

from time import sleep
from cmd_commands import start_capture, start_player, extract_data, kill_pupil, byebye_data
from file_dir import frame_dir
'''


# starts up the pupil capture application.
print("starting capture", start_capture())
sleep(10)
# Starts the recording and saving the data that is received in real-time
from TextExtraction.real_time_recording import data_collection
data_collection(10)

# Now going to start Pupil Player to export the video and csv files
sleep(7)
print("Starting player", start_player())
sleep(7)
print("extracting data", extract_data())  # Waits 6 seconds before starting extraction
sleep(15)
'''

# kill player and capture once extraction is done
print("Killing player", kill_pupil('player'))
print("Killing capture", kill_pupil('capture'))

'''
    ---------------------- Video and Image Analysis ---------------------- 
    Now that the data has been extracted, we can run the image and video
    processing for that data.
    
'''
from TextExtraction.frame_selection import image_data
from TextExtraction.VideoFrameCapture import frame_check, grabbingFrame
# Checks the Frames' directory to see if the video has already been split
frame_check()
# Assigning the selected frame to a variable that is then passed to Wit for image processing
frame_name = grabbingFrame(image_data)

'''
    ---------------------- Visualization of Analysis ----------------------
    Once the data has been sorted and organized we can then see the comparison
    between the video and the imaging processing. 
    - Wit.py is for images
    - WitVideo.py is for videos 
'''
from Tesseract import Wit, WitVideo
# Image processing
Wit.wit_image(frame_name)
sleep(5)
byebye_data(frame_dir)
# Video processing
WitVideo.wit_video()

#sleep(60)
#byebye_data(temp_dir)