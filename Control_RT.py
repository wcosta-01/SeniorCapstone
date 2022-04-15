'''
    This file controls the entire operation.
    Used to connect, run and test all the methods of the other files in the correct order.
'''

from time import sleep
from cmd_commands import start_capture, kill_pupil
from file_dir import get_gaze_coords_rt


# print("starting capture", start_capture())
# sleep(10) # waits 10 seconds to fully load capture

# Starts the recording and saving the data that is received in real-time
from Real_Time import rt_data_collection
rt_data_collection(1080, 1920)



