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

# https://docs.pupil-labs.com/developer/core/network-api/#pupil-remote
ctx = zmq.Context()
pupil_remote = zmq.Socket(ctx, zmq.REQ)
pupil_remote.connect('tcp://127.0.0.1:50020')


print("Running Real_time_recording")

def start_stop_recording(seconds):  # start recording
    sleep(1)
    pupil_remote.send_string('R')
    print("Recording Starting", pupil_remote.recv_string())
    sleep(seconds)
    pupil_remote.send_string('r')
    print("Recording stopping ", pupil_remote.recv_string())


def export_recoding():
    import os
    sleep(5)
    cmd_command = "powershell ; $wsh = New-Object -ComObject WScript.Shell ; $wsh.SendKeys('{e}')"
    shell_command = 'cmd /c ' + '"' + cmd_command + '"'
    os.system(shell_command)


'''
    rt_data_collection or real-time data collection will connect to the pupil remote via local host.
    Once connected it will then connect a sub port that will pass the data from the glasses to the API,
    where it will be analysed and then returned to the machine. Then the code gets the desired topic from 
    the data and returns the coordinates
    rt_data is where the real-time coordinates are from while the glasses where recording      
'''


def rt_data_collection(seconds):
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

    start_stop_recording(seconds)  # starts recording
    count = 0
    numID = 0  # ID for the incoming data
    rt_data = {}
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
        rt_data[rt_timestamp] = message[b'gaze_point_3d']
        # print(rt_data)
        cur_message = message[b'gaze_point_3d']
        numID += 1
        count += 1

        # Getting all the coordinate values into their own lists for calibration
        # This data will need to be run by tesseract either here or from another method from another file.
        time_stamps.append(rt_timestamp)
        point_pox.append(cur_message[0])
        point_poy.append(cur_message[1])
        point_poz.append(cur_message[2])
    rt_data = DataFrame.from_dict(rt_data)
    return rt_data
