import pandas as pd
import numpy as np
from file_dir import gaze_dir, test_gaze_dir, test_gaze_dir2, test_gaze_dir3
# Narrowing down data selection to only the columns we want
points = ['world_index', 'gaze_point_3d_x', 'gaze_point_3d_y', 'gaze_point_3d_z']
gaze_points = pd.read_csv(test_gaze_dir, usecols=points)

# Narrowing down data selection to only the columns we want and converting them into ints for testing
w_index = gaze_points["world_index"]
point_pox_int = gaze_points["gaze_point_3d_x"].astype(int)
point_poy_int = gaze_points["gaze_point_3d_y"].astype(int)
point_poz_int = gaze_points["gaze_point_3d_z"].astype(int)
gaze_points_ints = {"world_index":w_index, "X":point_pox_int, "Y":point_poy_int, "Z":point_poz_int}
gaze_points_ints = pd.DataFrame.from_dict(gaze_points_ints)

point_pox = gaze_points["gaze_point_3d_x"]
point_poy = gaze_points["gaze_point_3d_y"]
point_poz = gaze_points["gaze_point_3d_z"]
gaze_points = {"world_index":w_index, "X":point_pox, "Y":point_poy, "Z":point_poz}
gaze_points = pd.DataFrame.from_dict(gaze_points)

'''
    frame_Extract takes the tOrF values from the given list and returns a list of frame numbers that fit within
    perm: tOrF[] 
'''


def frame_Extract(tOrF, inputType):
    list_Index = []
    count = 0
    # Based on the size of the initial data, It runs through the list and gets the indexed number of each value that
    # is equal to True and adds it to the list.
    while count != tOrF.size:
        if tOrF.get(count):
            # print("yes", y)
            list_Index.append(count)
        count += 1  # counter for the while loop

    # Splits the big list into separate list and adds them into a dictionary to be sorted
    grouped_frames = {}
    temp_group = []
    count = 0
    groupNum = 0
    while count != len(list_Index) - 1:
        # if the next number is the expected number then the current number gets added to the list.
        if list_Index[count + 1] == list_Index[count] + 1:
            temp_group.append(list_Index[count])
        else:
            # adds the last value to the current group before moving onto the next group of values.
            temp_group.append(list_Index[count])
            grouped_frames["group{0}".format(groupNum)] = temp_group

            # Resetting the temp_group[]
            temp_group = []
            groupNum += 1
        count += 1

    # Getting rid of the groups that have fewer than 10 items.
    # Source: https://www.geeksforgeeks.org/python-ways-to-remove-a-key-from-dictionary/

    grouped_world_indexes = {key: val for key, val in grouped_frames.items() if len(val) > 10}
    if (inputType == "test"):
        return grouped_frames
    else:
        return match_Up(sorting_groups(grouped_world_indexes))

# Takes the cleaned Data and goes through each key value pair and sends the values to findMiddle
def sorting_groups(grouped_world_indexes):
    sorted_list = []
    for key in sorted(grouped_world_indexes):
        sorted_list.append(get_median(grouped_world_indexes[key]))
    return sorted_list

def get_median(input_list):
    middle = float(len(input_list)) / 2
    if middle % 2 != 0:
        return input_list[int(middle - .5)]
    else:
        return input_list[int(middle)]



# matching the selected coordinate indexes to its corresponding world_index
def match_Up(mid_index):
    mid_Frame = []
    for x in mid_index:
        mid_Frame.append(w_index.get(x))
    return mid_Frame


# ---------------------------------------- Main ---------------------------------------------------------------------

def selecting_frame():

    grouped_world_indexes = frame_Extract(point_pox_int, "test")
    mid_points = match_Up(sorting_groups(grouped_world_indexes))
    mid_points.sort()
    print("The list of coordinates: ", mid_points)
    mid_points = get_median(mid_points)
    print("The chosen number is: ", mid_points)
    return mid_points