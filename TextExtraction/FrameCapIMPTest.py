import csv
import sys
import pandas as pd
import numpy as np

points = ['world_index', 'gaze_point_3d_x', 'gaze_point_3d_y', 'gaze_point_3d_z']

#table that consists of world_index and the gaze point locations
gaze_point_3d = pd.read_csv(r'C:/Users/deadg/OneDrive/Documents/GithubRep/SeniorCapstone/TextExtraction/ExportedData/OldTestData/gaze_positions.csv')

#A simplified table that consists of the x and y positions in the world image in normalized coordinates 
#norm_pt_x = ['world_index', 'norm_pos_x']
#norm_pt_y = ['world_index', 'norm_pos_y']
#norm_pt_w = ['world_index']

norm_pt = ['world_index', 'norm_pos_x', 'norm_pos_y']
gaze_pos = pd.read_csv('C:/Users/deadg/OneDrive/Documents/GithubRep/SeniorCapstone/TextExtraction/ExportedData/OldTestData/gaze_positions.csv', usecols=norm_pt)


#gaze_pos_x = pd.read_csv("C:/Users/deadg/recordings/CapstoneCode/gaze_positions.csv", usecols=norm_pt_x)
#gaze_pos_y = pd.read_csv("C:/Users/deadg/recordings/CapstoneCode/gaze_positions.csv", usecols=norm_pt_y)
#gaze_pos_w = pd.read_csv("C:/Users/deadg/recordings/CapstoneCode/gaze_positions.csv", usecols=norm_pt_w)

#contains the positional data for the users pupil(where the user is looking at a certian point in the video)
gaze_positions = pd.read_csv(r'C:/Users/deadg/OneDrive/Documents/GithubRep/SeniorCapstone/TextExtraction/ExportedData/OldTestData/gaze_positions.csv')

#Contains World Timestamps
world_timestamps = pd.read_csv(r'C:/Users/deadg/OneDrive/Documents/GithubRep/SeniorCapstone/TextExtraction/ExportedData/OldTestData/world_timestamps.csv')

#containts pupil positions
pupil_positions = pd.read_csv(r'C:/Users/deadg/OneDrive/Documents/GithubRep/SeniorCapstone/TextExtraction/ExportedData/OldTestData/pupil_positions.csv')

#To complete step 2 we have to figure out the data looks like when the user is focused on an object
#The distance or size of an object is goind to present an issue with the way I have decided to select the frame
#pd.set_option("display.max_rows", None, "display.max_columns", None)
pos_x = gaze_pos["norm_pos_x"]
pos_y = gaze_pos["norm_pos_y"]
w_index = gaze_pos["world_index"]

#IT WORKS THIS IS IT BABY
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

# ---------------------------------------- Main ---------------------------------------------------------------------
# Using the between method to make a true or false list based on a given range
#These are the values that we will need to change.
highest = .50
lowest = .40
# For the X coordinates
tOrF_X = set_X_coords(lowest, highest)# is a list of true or false. if the value in pos_x fits within that range it becomes true if not its false.
# For the Y coordinates
tOrF_Y = set_Y_coords(lowest, highest)

# Just double checking lengths
if len(tOrF_X) == len(tOrF_Y):
    Combined_TF = tOrF_X.eq(tOrF_Y)
else:
    print("YOU DONT WANT TO SEE THIS!!!!!!!!!!!!!!!!!!!!!!!!")
# Sending the data through the methods
mid_combined = frame_Extract(Combined_TF)
print("The Combined list of coordinates is ", mid_combined)
coord_comb = mid_combined[0]
# Not sure if we still need this but it doesn't hurt
mid_x = frame_Extract(tOrF_X)
coord_x = mid_x[0]
mid_y = frame_Extract(tOrF_Y)
coord_y = mid_y[0]
print("The X coordinate Frames are ", mid_x)
print("The Y coordinate Frames are ", mid_y)