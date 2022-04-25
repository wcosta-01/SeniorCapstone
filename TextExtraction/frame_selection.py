import random
import pandas as pd
import numpy as np
from file_dir import gaze_dir, results_dir

print("Running Frame_selection")


'''
    Frame_Extract that finds the difference between each value in the given series.
    If the difference between two elements is greater than 0.2 all the elements before that difference get added to a 
    dictionary as a group. 
    - Returns two dictionaries
        - grouped_indexes:  contains all the world Indexes in groups
        - grouped_coord_vals: contains all the coordinates in groups
'''
def frame_Extract(coord_list):
    count = 0
    groupNum = 0
    grouped_frames = {}  # for the world_index(frame numbers)
    grouped_coords = {}  # for the coordinates
    # Temporary lists that hold individual groups before being added to the dictionaries
    temp_frames = []
    temp_coords = []

    # Finding the difference between each element in the given list
    dif_between = np.diff(abs(coord_list))
    # print(dif_between)
    # Getting the first element in the list as an initial Value
    initial_Val = coord_list[0]


    for key, val in coord_list.items():
        # Find the differences between the initial and the rest of the list.
        if key + 1 != len(coord_list):
            if abs(dif_between[count]) >= 0.2:
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
    # Returning both groups for testing purposes
    return grouped_indexes, grouped_coord_vals


'''
    combines the groups within a dictionary into one big list
'''
def mega_list(selected_world):
    world = []
    for key in selected_world:
        world += (selected_world[key])
    return world

'''
    Comparing the x and y world_indexes to see if there are any that match and returning a list of them.
'''
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

while True:
    # gaze_point values
    points = ['world_index', 'norm_pos_x', 'norm_pos_y']
    gaze_points = pd.read_csv(gaze_dir, usecols=points)
    # Drops duplicates
    gaze_points = gaze_points.drop_duplicates(subset=["world_index"]).reset_index(drop=True)
    # Narrowing down data selection to only the columns we want and converting them into ints for testing
    w_index = gaze_points["world_index"]
    point_pox = gaze_points["norm_pos_x"]
    point_poy = gaze_points["norm_pos_y"]
    gaze_points = {"world_index": w_index, "norm_pos_x": point_pox, "norm_pos_y": point_poy}
    gaze_points = pd.DataFrame.from_dict(gaze_points)

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

    matching_gaze = gaze_points.iloc[matching_indexes].reset_index(drop=True)
    # saving the data just in case
    saved_gaze = results_dir + 'video_rt_data.csv'
    matching_gaze.to_csv(saved_gaze)


    # This will go to videoFrameCapture
    # add a check so if there is no frame that is uncommon it defaults ro runs a test again
    try:
        image_data = int(matching_gaze.iloc[random.randint(0, len(matching_gaze["world_index"]))][0])
        print(image_data)
    except IndexError:
        print("Johnson: 'Uh oh?' "
              "Admin: 'Johnson! WHAT HAPPENED?!'"
              "Johnson: 'I don't know sir it just broke'"
              "Admin: 'YOU DON'T KNOW?!?!?! YOUR THE HALF-WIT THAT PROGRAMMED THIS THING, GET BACK TO WORK!'")
    if (image_data > 20):
        break