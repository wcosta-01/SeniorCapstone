'''
    Control_RT.py is used to start the real-time data testing.
'''

from time import sleep
from cmd_commands import start_capture, kill_pupil

print("starting capture", start_capture())
sleep(10) # waits 10 seconds to fully load capture

# Starts the recording and saving the data that is received in real-time
from Real_Time import rt_data_collection
rt_data_collection(1080, 1920)



