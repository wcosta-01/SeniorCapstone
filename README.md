# Welcome to Wit
Wit is an eye tracking software that uses pupil labs core eye tracking glasses to read signs and any text the user looks at. It can read a book, look up restraints when you look at an advertisement.
We test our software in three ways, images, video, and real-time.


# Pupil Labs
We have used many of the resources that pupil labs has published along with a few community projects in order to connect this software.

# Tesseract OCR


## Program Structure
We have spilt the process into a collection of files that connect and allow for easy modification. Each program has its own methods that are either ran from within the same file or from a Control file.
The program can be split into a couple different processes. The first being data collection or recording, in which the user is wearing the glasses and recording what they are looking at. Now this is where the program splits into the 3 main parts.
- **Image process**, takes the recording that was just created and extracts data using Pupil Player, this gives us a gaze_position.csv file, and a world.mp4 file. We use the gaze_position.csv file to find the frame of the video in which the user was staring in a general area.
The world.mp4 file is then split up into individual frames which are stored in a folder called Frames. Then we take the frame number that was calculated from the gaze_position data, and then run that selected frame and its corresponding coordinate data through wit.py. 
Wit then creates bounding boxes around the text that is within the given frame number. Wit also takes the coordinates and maps them to the image. If the boxes overlap Tesseract is then activated and attempts to read the text within the bounding box.

- **Video process**, works in a similar way by using the extracted video and data from Pupil Player, but instead of an image it is a video. It shows the coordinates being created while the recording is playing and Tesseract reads them as the coordinate boxes overlap with the bounding boxes.
- **Real-time process**, in theory should work similar to video but in real-time the only issue is that the camera can not be used in 2 places at once. ///stopped here

### Frame Selection
Frame selection takes the gaze data from a given recording and uses it to find which frames of the video where the user was looking in the same area. 

Frame selection does this by taking 4 columns of data from the gaze_position.csv, the world_index(the closest world video frame), and gaze_normal0_x, gaze_normal0_y, and gaze_normal0_z.
It then removes the rows that have duplicate world_index values in order to give us a cleaner set of data. Then each column gets turned into its own series, next we add the 4 series' together to create a dataframe of our cleaned data.
#### frame_Extract method
Once we have the cleaned data we now send the x and y coordinates through a method that finds the difference between each value in that series. We then use that difference to determine whether the user moves from staring in one location 
to another. When the user is staring at an object, all the coordinates and the indexes that relate to them are stored in temporary lists. Once the user looks at a different location or object the temporary lists are then saved in corresponding dictionaries as "group{#}"s.
The temporary list is then reset and the process continues until it reaches the end of the list. The method then returns the dictionaries, one containing the indexes for the coordinates and the coordinates themselves.

#### 


In layman's terms, we look for the point at which the user is not moving their eyes.
Store the coordinates that are between when the user started looking in that area to when they stopped looking in a list.
Next we take those lists and find the world_index where all three coordinates are 0.10 units apart and store them in a list.
Finally, we find the middle most world_index and return that value.

gaze_normal0 is "The visual axis goes through the center of the eyeball and the object that is looked at."



##
