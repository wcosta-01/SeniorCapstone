import pandas as pd
import numpy as np
from file_dir import gaze_dir, test_gaze_dir
# Narrowing down data selection to only the columns we want
points = ['world_index', 'gaze_normal0_x', 'gaze_normal0_y', 'gaze_normal0_z']
gaze_points = pd.read_csv(test_gaze_dir, usecols=points)
# Narrowing down data selection to only the columns we want and converting them into ints for testing
point_pox_int = gaze_points["gaze_point_3d_x"].astype(int)
point_poy_int = gaze_points["gaze_point_3d_y"].astype(int)
point_poz_int = gaze_points["gaze_point_3d_z"].astype(int)
w_index = gaze_points["world_index"]
point_pox = gaze_points["gaze_point_3d_x"]
point_poy = gaze_points["gaze_point_3d_y"]
point_poz = gaze_points["gaze_point_3d_z"]

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

    highest = .10
    lowest = 0.0


    # Using the between method to make a true or false list based on a given range
    # For the X coordinates
    tOrF_pX = point_pox.between(lowest, highest)
    # For the Y coordinates
    tOrF_pY = point_poy.between(lowest, highest)
    # For the Z coordinates
    tOrF_pZ = point_poz.between(lowest, highest)

    points_list = tOrF_pX.eq(tOrF_pY)

    grouped_world_indexes = frame_Extract(points_list)


    mid_points = match_Up(sorting_groups(grouped_world_indexes))


    print("The Combined list of coordinates is ", mid_points)
    print("The chosen number is: ", mid_points[0])
    return mid_points[0]
