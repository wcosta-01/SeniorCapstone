import csv
import sys
import pandas as pd
import numpy as np
from file_dir import gaze_dir, test_gaze_dir, test_gaze_dir2, test_gaze_dir3

# gaze_point values
points = ['world_index', 'gaze_point_3d_x', 'gaze_point_3d_y', 'gaze_point_3d_z']
gaze_points = pd.read_csv(test_gaze_dir, usecols=points)
# Narrowing down data selection to only the columns we want and converting them into ints for testing
w_index = gaze_points["world_index"]
point_pox_int = gaze_points["gaze_point_3d_x"].astype(int)
point_poy_int = gaze_points["gaze_point_3d_y"].astype(int)
point_poz_int = gaze_points["gaze_point_3d_z"].astype(int)
gaze_points_ints = {"world_index": w_index, "X": point_pox_int, "Y": point_poy_int, "Z": point_poz_int}
gaze_points_ints = pd.DataFrame.from_dict(gaze_points_ints)

point_pox = gaze_points["gaze_point_3d_x"]
point_poy = gaze_points["gaze_point_3d_y"]
point_poz = gaze_points["gaze_point_3d_z"]
gaze_points = {"world_index": w_index, "X": point_pox, "Y": point_poy, "Z": point_poz}
gaze_points = pd.DataFrame.from_dict(gaze_points)

# Drops duplicates
gaze_points.drop_duplicates(subset=["world_index"], inplace=True)
gaze_points_ints.drop_duplicates(subset=["world_index"], inplace=True)

'''
    frame_Extract takes the tOrF values from the given list and returns a list of frame numbers that fit within
    perm: tOrF[] 
'''


def frame_Extract(coord_list, inputType):
    avg_dif = np.diff(abs(coord_list))  # finding the average difference of the entire list.
    # highest_dif is the difference allowed between the first element in coord_list and the rest of the elements in the list
    highest_dif = max(avg_dif)  # Using the largest difference to be the highest_dif
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
            if abs(initial_Val) > abs(coord_list[key + 1]):
                dif = abs(initial_Val) - abs(coord_list[key + 1])
            else:
                dif = abs(coord_list[key + 1]) - abs(initial_Val)

            if dif > highest_dif:
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

    # Getting rid of the groups that have fewer than 10 items.
    # Source: https://www.geeksforgeeks.org/python-ways-to-remove-a-key-from-dictionary/
    grouped_world_indexes = {key: val for key, val in grouped_frames.items() if len(val) > 10}
    grouped_coord_vals = {key: val for key, val in grouped_coords.items() if len(val) > 10}

    if (inputType == "world"):
        return sorting_groups(grouped_world_indexes)
    else:
        return grouped_coord_vals


# Takes the cleaned Data and goes through each key value pair and sends one list at a time to match_up
def sorting_groups(grouped_world_indexes):
    sorted_list = {}
    for key in sorted(
            grouped_world_indexes):  # maybe remove sorted in order to not get the frames confused???++++++++++++++++++++++++++++++++++++++++++++++++
        sorted_list[key] = match_up(grouped_world_indexes[key])
        sorted_list[key] = get_average(sorted_list[key])
    return sorted_list


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


# ---------------------------------------- Main ---------------------------------------------------------------------

# STILL working on finding the best way to find the right frame to select for judgement.


# For x
avg_dif = np.diff(abs(point_pox_int))
print("The largest average difference is: ", max(avg_dif))
selected_groups_X = frame_Extract(point_pox_int, "awda")
print("The dictionary of the world_index for X ", selected_groups_X)

# for y
avg_dif = np.diff(abs(point_poy_int))
print("The largest average difference is: ", max(avg_dif))
selected_groups_Y = frame_Extract(point_poy_int, "adaw")
print("The dictionary of the world_index for Y ", selected_groups_Y)

# return mid_points
