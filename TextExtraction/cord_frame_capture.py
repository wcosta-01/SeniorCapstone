import csv
import sys
import pandas as pd
import numpy as np

from file_dir import video_dir
points = ['world_index', 'gaze_normal0_x', 'gaze_normal0_y', 'gaze_normal0_z']

# The dataframe I plan on using
gaze_normal = pd.read_csv(r'C:\Users\deadg\OneDrive\Documents\GithubRep\SeniorCapstone\recordings\Temp\000\exports\000\gaze_positions.csv', usecols=points)

#A simplified table that consists of the x and y positions in the world image in normalized coordinates 
#norm_pt_x = ['world_index', 'norm_pos_x']
#norm_pt_y = ['world_index', 'norm_pos_y']
#norm_pt_w = ['world_index']
#norm_pt = ['world_index', 'norm_pos_x', 'norm_pos_y']

# Narrowing down data selection to only the rows we want
#gaze_pos = pd.read_csv('C:/Users/deadg/OneDrive/Documents/GithubRep/SeniorCapstone/TextExtraction/ExportedData/OldTestData/gaze_positions.csv', usecols=points)

# Assigning columns to variables
pos_x = gaze_normal["gaze_normal0_x"]
pos_y = gaze_normal["gaze_normal0_y"]
pos_z = gaze_normal["gaze_normal0_z"]
w_index = gaze_normal["world_index"]


'''
    frame_Extract takes the tOrF values from the given list and returns a list of frame numbers that fit within
    the given parameters. 
'''
# This takes out all the false values from the tOrF series
def frame_Extract(tOrF):
    list_Index = []
    count = 0 
    # Based on the size of the initial data, It runs through the list and gets the indexed number of each value that is equal to True and adds it to the list. 
    while count != tOrF.size:
        if tOrF.get(count) == True:
            #print("yes", y)
            list_Index.append(count)
        count += 1 #counter for the while loop
    
    # Splits the big list into separate list and adds them into a dictionary to be sorted
    # Still throws a index out of bounds execption tho in the
    gFrame = {}
    tempGroup = []
    count = 0
    groupNum = 0
    while count != len(list_Index) - 1:
        #if the next number is the expected number then the current number gets added to the list.
        if list_Index[count + 1] == list_Index[count] + 1:
            tempGroup.append(list_Index[count])
        else:
            # adds the last value to the current group before moving onto the next group of values.
            tempGroup.append(list_Index[count])
            gFrame["group{0}".format(groupNum)] = tempGroup
            tempGroup = []
            groupNum += 1
        count += 1

    # Time to clean up that data! Getting rid of the groups that have fewer then 10 items
    # Source: https://www.geeksforgeeks.org/python-ways-to-remove-a-key-from-dictionary/
    almostDone = {key: val for key, val in gFrame.items() if len(val) > 10}
    return match_Up(mid_part1(almostDone))

# Takes the cleaned Data and goes through each key value pair and sends the values to findMiddle
def mid_part1(almostDone):
    m_list = []
    for key in sorted(almostDone):
        m_list.append(mid_part2(almostDone[key]))
    return m_list

# Finds the middle element in the list and returns it.
# https://stackoverflow.com/questions/38130895/find-middle-of-a-list
def mid_part2(input_list):
    middle = float(len(input_list))/2
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

def set_X_coords(lowest, highest):
    tOrF_X = pos_x.between(lowest, highest)
    return tOrF_X

def set_Y_coords(lowest, highest):
    tOrF_Y = pos_y.between(lowest, highest)
    return tOrF_Y

def set_Z_coords(lowest, highest):
    tOrF_Z = pos_z.between(lowest, highest)
    return tOrF_Z

# ---------------------------------------- Main ---------------------------------------------------------------------
def selecting_frame():
    # Using the between method to make a true or false list based on a given range
    #These are the values that we will need to change.
    highest = .50
    lowest = .40
    # For the X coordinates
    tOrF_X = set_X_coords(lowest, highest)# is a list of true or false. if the value in pos_x fits within that range it becomes true if not its false.
    # For the Y coordinates
    tOrF_Y = set_Y_coords(lowest, highest)
    tOrF_Z = set_Z_coords(lowest, highest)

    # Just double checking lengths
    # Combined_TF is a combinded list of the tOrF list for the x, y and z coordinates.
    if len(tOrF_X) == len(tOrF_Y):
        Combined_TF = tOrF_X.eq(tOrF_Y)
        Combined_TF.eq(tOrF_Z)
    else:
        print("YOU DONT WANT TO SEE THIS!!!!!!!!!!!!!!!!!!!!!!!!")
        # Sending the data through the methods

    mid_combined = frame_Extract(Combined_TF)
    # print("The Combined list of coordinates is ", mid_combined)
    coord_comb = mid_combined[0]
    return coord_comb


    # Not sure if we still need this but it doesn't hurt
    ''' For some reason idk why this is having an issue 
        mid_x = frame_Extract(tOrF_X)
        print("The X coordinate Frames are ", mid_x)
        mid_y = frame_Extract(tOrF_Y)
        print("The Y coordinate Frames are ", mid_y)
        mid_z = frame_Extract(tOrF_Z)
        print("The Z coordinate Frames are ", mid_z)
    '''
