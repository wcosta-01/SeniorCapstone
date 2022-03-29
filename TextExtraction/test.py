import pandas as pd
points = ['world_index', 'gaze_point_3d_x',
          'gaze_point_3d_y', 'gaze_point_3d_z']

#table that consists of world_index and the gaze point locations
gaze_point_3d = pd.read_csv('C:/Users/deadg/recordings/CapstoneCode/gaze_positions.csv', usecols=points)

#A simplified table that consists of the x and y positions in the world image in normalized coordinates
#norm_pt_x = ['world_index', 'norm_pos_x']
#norm_pt_y = ['world_index', 'norm_pos_y']
#norm_pt_w = ['world_index']

norm_pt = ['world_index', 'norm_pos_x', 'norm_pos_y']
gaze_pos = pd.read_csv('C:/Users/deadg/recordings/CapstoneCode/gaze_positions.csv', usecols=norm_pt)


#gaze_pos_x = pd.read_csv("C:/Users/deadg/recordings/CapstoneCode/gaze_positions.csv", usecols=norm_pt_x)
#gaze_pos_y = pd.read_csv("C:/Users/deadg/recordings/CapstoneCode/gaze_positions.csv", usecols=norm_pt_y)
#gaze_pos_w = pd.read_csv("C:/Users/deadg/recordings/CapstoneCode/gaze_positions.csv", usecols=norm_pt_w)

#contains the positional data for the users pupil(where the user is looking at a certian point in the video)
gaze_positions = pd.read_csv(
    r'C:/Users/deadg/recordings/CapstoneCode/gaze_positions.csv')

#Contains World Timestamps
world_timestamps = pd.read_csv(
    r'C:/Users/deadg/recordings/CapstoneCode/world_timestamps.csv')

#containts pupil positions
pupil_positions = pd.read_csv(r'C:/Users/deadg/recordings/CapstoneCode/pupil_positions.csv')

pd.set_option("display.max_rows", None, "display.max_columns", None)
#gaze_pos.head()

#Finding a group or series of numbers where the rate of change is less then .10 and saving them in a list
# Look into maybe going back to Data Frames to make it easier to search for the desired variables
pos_x = gaze_pos["norm_pos_x"]
temp = []
gFrame = {}
count = 0
for x in pos_x:
    #the current value selected
    current = x
    above = current + .054321
    below = current - .054321
    count += 1
    temp.clear
    if current <= above and current >= below:
        temp.append(current)
        pos_x.drop(labels=range(pos_x.size - count))
    gFrame["group{0}".format(count)] = temp

gData = pd.DataFrame(gFrame)
gData.head()
