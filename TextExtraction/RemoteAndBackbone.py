"""
(*)~----------------------------------------------------------------------------------
 Pupil Helpers
 Copyright (C) 2012-2016  Pupil Labs
 Distributed under the terms of the GNU Lesser General Public License (LGPL v3.0).
 License details are in the file license.txt, distributed as part of this software.
----------------------------------------------------------------------------------~(*)
"""

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

from time import sleep, time

# https://docs.pupil-labs.com/developer/core/network-api/#pupil-remote
ctx = zmq.Context()
pupil_remote = zmq.Socket(ctx, zmq.REQ)
pupil_remote.connect('tcp://127.0.0.1:50020')
rt_data = {}


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
    # rt_data = {}  # real-time coordinates captured during recording
    numID = 0  # ID for the incoming data
    '''
    Good for doing real-time but for just a quick start stop recording not so much
    '''
    while True and count != seconds:  # Will keep running till the program is terminated
        topic, payload = subscriber.recv_multipart()
        message = msgpack.loads(payload)
        # print(f"{topic}: {message}")
        rt_data["real_time_{0}".format(numID)] = message[b'gaze_normal_3d']
        print(rt_data)
        numID += 1
        count += 1
    return rt_data
rt_data_collection(10000)