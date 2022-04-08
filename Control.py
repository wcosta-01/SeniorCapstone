'''
    This file controls the entire operation.
    Used to connect, run and test all the methods of the other files in the correct order.
'''

from time import sleep
from cmd_commands import start_capture, start_player, extract_data, kill_pupil
# from TextExtraction.RemoteAndBackbone import rt_data_collection

from cmd_commands import byebye_data

print("starting capture")
# start_capture()  # starts up the pupil capture application *** NEED TO ADJUST TIMING IN ORDER TO GIVE IT ENOUGHT TIME TO LAUNCH.


'''
Testing if it runs 2 twice or just gets the same data.
Function has to be ran for it to generate the recording
'''
# test = rt_data_collection(15)
# print("Testing Function call: ", test)

# Now going to start pupil player to export the video files
print("starting player")
# start_player()

print("extracting data")
# extract_data()  # Waits 6 seconds before starting extraction

# ---------------------- Realtime analysis and Video Analysis Split -----------#


# kill player once extraction is done
# print("Killing player", kill_pupil('player'))

'''
    Now that the data has been extracted from the recording files we can run the image processing
    for the individual frames and the video.
'''
# Running cord_frame_capture to get the list of frames will work for analysis
from TextExtraction.cord_frame_capture import selecting_frame
from TextExtraction.VideoFrameCapture import frame_check, grabbingFrame
frame_check() # Will check if the directory already has frames, if its empty it will create them
select_frame = selecting_frame()
grabbingFrame(select_frame)


