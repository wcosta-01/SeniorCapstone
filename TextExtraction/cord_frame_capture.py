import csv
import random
import sys

import pandas as pd
import numpy as np
from file_dir import gaze_dir, test_gaze_dir, test_gaze_dir2, test_gaze_dir3

'''
    frame_Extract takes the tOrF values from the given list and returns a list of frame numbers that fit within
    perm: tOrF[] 
'''


def frame_Extract(coord_list):
    avg_dif = np.diff(abs(coord_list))  # finding the difference between each element in the list
    # We will use this to judge where to split the groups
    groupNum = 0
    grouped_frames = {}  # for the frame numbers
    grouped_coords = {}  # for the coordinates
    temp_frames = []
    temp_coords = []
    count = 0
    initial_Val = coord_list[0]
    for key, val in coord_list.items():
        # Find the differences between the initial and the rest of the list.
        if key + 1 != len(coord_list):
            if abs(avg_dif[count]) >= 10:
                initial_Val = val
                temp_coords.append(val)
                temp_frames.append(key)

                grouped_frames["group{0}".format(groupNum)] = temp_frames
                grouped_coords["group{0}".format(groupNum)] = temp_coords
                temp_frames = []
                temp_coords = []
                groupNum += 1
            else:
                temp_coords.append(val)
                temp_frames.append(key)
            count += 1
    # Getting rid of the groups that have fewer than 10 items.
    # Source: https://www.geeksforgeeks.org/python-ways-to-remove-a-key-from-dictionary/
    # stores the world index for the coordinates
    grouped_indexes = {key: val for key, val in grouped_frames.items() if len(val) > 10}

    # stores the coordinates
    grouped_coord_vals = {key: val for key, val in grouped_coords.items() if len(val) > 10}
    return grouped_indexes, grouped_coord_vals

    # return match_up(sorting_groups(grouped_indexes)), grouped_coord_vals


# Takes the cleaned Data and goes through each key value pair and sends one list at a time to match_up
def sorting_groups(grouped_indexes):
    sorted_list = {}
    for key in grouped_indexes:
        sorted_list[key] = match_up(grouped_indexes[key])
        sorted_list[key] = get_average(sorted_list[key])
    return sorted_list.values()


# takes the index of the coordinates and matches them with their corresponding world_index(frame number)
def match_up(list_index):
    list_world = []
    for x in list_index:
        list_world.append(w_index[x])
    return list_world


# Gets the average number of a given list
def get_average(input_list):
    return (sum(input_list) / len(input_list)).astype(int)


def get_median(input_list):
    middle = float(len(input_list)) / 2
    if middle % 2 != 0:
        return input_list[int(middle - .5)]
    else:
        return input_list[int(middle)]


def mega_list(selected_world):
    world = []
    for key in selected_world:
        world += (selected_world[key])
    return world


def comparing_xy(world_x, world_y):
    matching_indexes = []
    if len(world_x) > len(world_y):
        size = len(world_y)
    else:
        size = len(world_x)
    for i in range(size):
        if world_y[i] in world_x:
            matching_indexes.append(world_y[i])
    return matching_indexes


# ---------------------------------------- Main ---------------------------------------------------------------------
# gaze_point values
points = ['world_index', 'gaze_point_3d_x', 'gaze_point_3d_y', 'gaze_point_3d_z']
gaze_points = pd.read_csv(gaze_dir, usecols=points)

# Drops duplicates
gaze_points = gaze_points.drop_duplicates(subset=["world_index"]).reset_index(drop=True)

# Narrowing down data selection to only the columns we want and converting them into ints for testing
w_index = gaze_points["world_index"]
point_pox = gaze_points["gaze_point_3d_x"]
point_poy = gaze_points["gaze_point_3d_y"]
point_poz = gaze_points["gaze_point_3d_z"]
gaze_points = {"world_index": w_index, "X": point_pox, "Y": point_poy}
gaze_points = pd.DataFrame.from_dict(gaze_points)

# For testing purposes
point_pox_int = gaze_points["gaze_point_3d_x"].astype(int)
point_poy_int = gaze_points["gaze_point_3d_y"].astype(int)
point_poz_int = gaze_points["gaze_point_3d_z"].astype(int)
gaze_points_ints = {"world_index": w_index, "X": point_pox_int, "Y": point_poy_int}
gaze_points_ints = pd.DataFrame.from_dict(gaze_points_ints)


# For x
selected_world_x, selected_coord_x = frame_Extract(point_pox)

# For y
selected_world_y, selected_coord_y = frame_Extract(point_poy)

# putting the groups together in order to compare x and y world indexes to see which ones match up.
world_x = mega_list(selected_world_x)
world_y = mega_list(selected_world_y)
# finding the matching world index of both x and y
matching_indexes = comparing_xy(world_x, world_y)

# a dataframe that contains the matching x and y coordinates
# This will go to Tesseract video processing
video_rt_data = gaze_points.iloc[matching_indexes].reset_index(drop=True)

# This will go to videoFrameCapture
image_data = int(video_rt_data.iloc[random.randint(0, len(video_rt_data["world_index"]))][0])
