import csv
import sys
import pandas as pd
import numpy as np
import zmq
import msgpack

# https://docs.pupil-labs.com/developer/core/network-api/#pupil-remote
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

count = 0
rt_data = {}  # real-time coordinates captured during recording
numID = 0  # ID for the incoming data
time_stamps = []
point_pox = []
point_poy = []
point_poz = []

while True and count != 500:  # Will keep running till the program is terminated
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

    # Saving coordinates from real-time capture
    time_stamps.append(rt_timestamp)
    point_pox.append(cur_message[0])
    point_poy.append(cur_message[1])
    point_poz.append(cur_message[2])
    cur_x = cur_message[0]
    cur_y = cur_message[1]
    cur_z = cur_message[2]


    # DONT NEED THIS
    '''
    last_val = point_pox[point_pox.index(cur_x) - 1]
    if abs(last_val > cur_x):
        dif = abs(last_val) - abs(cur_x)
    else:
        dif = abs(cur_x) - abs(last_val)
    if dif > dif_x:
        index = point_pox.index(cur_x)
        initial_x = point_pox[index - 1]
        temp_group.append(cur_x)
        grouped_coords["group{0}".format(groupNum)] = temp_group
        print("grouped coords ", grouped_coords)
        groupNum += 1
        temp_group = []
    else:
        temp_group.append(cur_x)

    grouped_world_indexes = {key: val for key, val in grouped_coords.items() if len(val) > 10}
    sorted_groups = sorting_groups(grouped_world_indexes)
    '''
    # The problem here is that there is no world index to get a video frame number, thus making it hard to use
    # coordinates to locate what the user is looking at.
