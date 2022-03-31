'''
    This file controls the entire opperation
'''
from time import sleep
from cmd_commands import start_capture, start_player, extract_data, kill_pupil

print("starting capture")
# start_capture()  # starts up the pupil capture application

# -------------------- May need to move this below extract_data() to ensure the world.mp4 is created.
from RemoteAndBackbone import rt_data_collection
from TextExtraction.RTCoordVsTesseract import set_rt_data_coords

'''
Testing if it runs 2 twice or just gets the same data.
Function has to be ran for it to generate the recording
'''
test = rt_data_collection(15)
print("Testing Function call: ", test)

# Now going to start pupil player to export the video files
print("starting player")
start_player()


print("extracting data")
extract_data()  # Waits 6 seconds before starting extraction

# kill player once extraction is done
print("Killing player", kill_pupil('player'))

'''
    Now that the data has been extracted from the recording files we can run the image processing
    for the individual frames and the video.
'''
# Running cord_frame_capture to get the list of frames will work for analysis
from cord_frame_capture import selecting_frame
select_frame = selecting_frame()
print("This is the chosen one: ", select_frame)
# Running VideoFrameCapture to split the video file into frames for analysis
from VideoFrameCapture import frame_check
frame_check() # Will check if the directory already has frames, if its empty it will create them

from cleaner import byebye_data
# Was just going to test the cleaner out.
