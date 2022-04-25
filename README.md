# Welcome to Wit
Wit is an eye tracking software that uses pupil labs core eye tracking glasses to read signs and any text the user looks at. It can read a book, look up restraints when you look at an advertisement.
We test our software in three ways, images, video, and real-time.


# Pupil Labs
We have used many of the resources that pupil labs has published along with a few community projects in order to connect this software.


## File Structure
We have spilt the program into a collection of files that connect and allow for easy modification. 
Each file has their own methods that are either ran from within or are called from a Control file.
The program can be split two sections. The first being data collection or recording, in which the user is wearing the glasses and recording what they are looking at. Then the analysis of the recorded data.

**Programs that Analyse**
- **Wit.py**: Images
- **WitVideo.py**: Video
- **Real-time.py**: Real-time

### Text Extraction
Contains all the files needed to collect and manipulate data that can then be used while analysing data.

### Frame Selection
Frame selection takes the gaze data from a given recording and uses it to find which frame of the video where the user is staring at a single object.
It does this by taking 3 columns of data from the gaze_position.csv. Which are norm_pos_x, norm_pos_y, and world_index(the closest world video frame).
- perms: gaze_position.csv file
- image_data: is an int that contains the selected frame number.

### VideoFrameCapture
Purpose is to split the video into frames, save them, retrieve them, and check if they have already been created.
Contains three methods, videoToFrames(), grabbingFrame(), and frame_check().

- **videoToFrames**
    - Uses the video file that is linked from file_dir to get the world.mp4, then splits it into frames and saves them 
to the Frames directory.

- **grabbingFrame**
    - Finds the frame that matches the given frame number and returns the name of it as a string.

- **frame_check**
    - Used to check the /Frames directory for files. Designed to eliminate the need to constantly re-create the same frame files while testing.
    - If there are not any it will call videoToFrames to create them.

### Real_Time_Recording
Built off of Pupil Labs network-api (https://docs.pupil-labs.com/developer/core/network-api/). It is used to start a recording and collect real-time data. 
Contains three methods, start_stop_recording(), export_recoding(), and data_collection().

- **start_stop_recording**
    - starts and stops a recording based on a given amount of seconds. It is a slightly modified version of the Pupil Remote found in the link mentioned above.
    - Parms: Seconds (The desired length of the recording)

- **export_recording**
    - Uses powershell commands to press the 'e' key once pupil player is started. This then starts 
    Pupil players' export process which creates a collection of files based on the data within the initial recording.

- **data_collection**
    - Acting as a main method, data_collection takes in a value for number of seconds that the user would like the recording to be. 
    It then starts a recording, and connects to the glasses locally to receive a live data feed of the gaze coordinates.
    It stores that data into a dictionary that can accessed later to compare against the post processed data from 
    Pupil Player.

## Tesseract
Contains the files needed to extract text from images and videos.

### Wit (images)
Combines East and Tesseract to build bounding boxes around text that is found within the given frame.
Then takes the cleaned data frame from frame_selection and remaps them to match the Tesseracts
bounding box grid. If any of the coordinates overlap with a bounding box that contains text, the word is added to a list that is returned one the program has finished.

### Wit Video
Used to process video, by combining East and Tesseract we are able to take the world.mp4 file from the Pupil recording and create bounding boxes around the text that show up in the video.
Then we take the raw coordinate data     from frame_selection and convert to the Tesseract grid.
If any of the coordinates overlap with a bounding box that contains text, the word is printed out and saved to a list.

