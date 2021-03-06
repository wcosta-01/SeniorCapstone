"""
(*)~----------------------------------------------------------------------------------
 Pupil Helpers
 Copyright (C) 2012-2016  Pupil Labs
 Distributed under the terms of the GNU Lesser General Public License (LGPL v3.0).
 License details are in the file license.txt, distributed as part of this software.
----------------------------------------------------------------------------------~(*)
"""
from pandas import DataFrame

"""
This example demonstrates how to send simple messages to the Pupil Remote plugin
    'R' start recording with auto generated session name
    'R rec_name' start recording and name new session name: rec_name
    'r' stop recording
    'C' start currently selected calibration
    'c' stop currently selected calibration
    'T 1234.56' Timesync: make timestamps count form 1234.56 from now on.
    't' get pupil timestamp
    '{notification}' send a notification via pupil remote.
"""
import zmq
import msgpack
from time import sleep

'''
    These lines are from https://docs.pupil-labs.com/developer/core/network-api/#pupil-remote and are used to connect
    locally to the network-api allowing us to get the live feed from the glasses. This is normally used to connect to 
    the glasses remotely but in this case we are just using it to have access to the remote controls inorder to allow 
    us to automate the process.
'''
ctx = zmq.Context()
pupil_remote = zmq.Socket(ctx, zmq.REQ)
pupil_remote.connect('tcp://127.0.0.1:50020')

ip = 'localhost'  # If you talk to a different machine use its IP.
port = 50020  # The port defaults to 50020. Set in Pupil Capture GUI.

# Request 'SUB_PORT' for reading data
pupil_remote.send_string('SUB_PORT')
sub_port = pupil_remote.recv_string()

# Request 'PUB_PORT' for writing data
pupil_remote.send_string('PUB_PORT')
pub_port = pupil_remote.recv_string()

# Assumes `sub_port` to be set to the current subscription port
subscriber = ctx.socket(zmq.SUB)
subscriber.connect(f'tcp://{ip}:{sub_port}')
subscriber.subscribe('gaze.')  # receive all gaze messages


'''
    start_stop_recording uses the hotkeys within the Pupil API connection to start and stop a recording within Pupil
    Capture. It takes in the number of seconds that the recording needs to be and sleeps inbetween pressing start and stop.
'''
def start_stop_recording(seconds):  # start recording
    sleep(1)
    pupil_remote.send_string('R')
    print("Recording Starting", pupil_remote.recv_string())
    sleep(seconds)
    pupil_remote.send_string('r')
    print("Recording stopping ", pupil_remote.recv_string())

'''
    Export_recording uses powershell commands to press the 'e' key once pupil player is started. This then starts 
    Pupil players' export process which creates a collection of files based on the data within the initial recording.
'''
def export_recoding():
    import os
    sleep(5)
    cmd_command = "powershell ; $wsh = New-Object -ComObject WScript.Shell ; $wsh.SendKeys('{e}')"
    shell_command = 'cmd /c ' + '"' + cmd_command + '"'
    os.system(shell_command)
    return "Data Exported"


'''
    Data_collection takes in a value for number of seconds that the user would like the recording to be. 
    It then starts a recording, and connects to the glasses locally to receive a live data feed of the gaze coordinates.
    It stores that data into a dictionary that can accessed later to compare against the post processed data from 
    Pupil Player.    
'''

def data_collection(seconds):
    print("Recording for Video and Imaging")
    start_stop_recording(seconds)  # starts recording
    count = 0
    numID = 0  # ID for the incoming data
    recording_data = {}
    time_stamps = []  # stores the timestamps from the live feed
    point_pox = []  # stores the X coordinate values from the live feed
    point_poy = []  # store the Y coordinates values from the live feed
    point_poz = []  # store the Z coordinates values from the live feed

    while True and count != seconds:  # Will keep running till the program is terminated
        topic, payload = subscriber.recv_multipart()
        message = msgpack.loads(payload)
        # print(f"{topic}: {message}")
        rt_num = "real_time_{0}".format(numID)
        rt_timestamp = message[b'timestamp']
        recording_data[rt_timestamp] = message[b'norm_pos']
        # print(rt_data)
        cur_message = message[b'norm_pos']
        numID += 1
        count += 1



