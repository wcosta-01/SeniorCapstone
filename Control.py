'''
    This file controls the entire operation.
    Used to connect, run and test all the methods of the other files in the correct order.
'''

from time import sleep
from cmd_commands import start_capture, start_player, extract_data, kill_pupil, byebye_data
from file_dir import frame_dir, temp_dir

# starts up the pupil capture application *** NEED TO ADJUST TIMING IN ORDER TO GIVE IT ENOUGHT TIME TO LAUNCH.

print("starting capture", start_capture())
sleep(10) # waits 10 seconds to fully load capture

# Starts the recording and saving the data that is received in real-time
from TextExtraction.real_time_recording import rt_data_collection
rt_data = rt_data_collection(10)
# Now going to start pupil player to export the video files
sleep(10)
print("Starting player", start_player())
sleep(10)
print("extracting data", extract_data())  # Waits 6 seconds before starting extraction
sleep(20)

# kill player once extraction is done
# print("Killing player", kill_pupil('player'))

# ---------------------- Realtime / video analysis and Image Analysis Split -----------#

'''
    Now that the data has been extracted from the recording files we can run the image processing
    for the individual frames and the video.
    Wit.py is for images
    WitVideo.py is for videos
'''
# Running cord_frame_capture to get the list of frames will work for analysis
from TextExtraction.frame_selection import image_data, video_rt_data
from TextExtraction.VideoFrameCapture import frame_check, videoToFrames, grabbingFrame

frame_check()  # splits the video into individual frames
frame_name = grabbingFrame(image_data)
# Sending the data from the video


from Tesseract import Wit, WitVideo, WitVideoRT_Data

# for image processing
Wit.wit_image(frame_name)
# sleep(5)
byebye_data(frame_dir)
print("Real-Time data", rt_data)
# for video or live processing
WitVideo.wit_video()
WitVideoRT_Data.wit_video(rt_data)


#sleep(60)
#byebye_data(temp_dir)