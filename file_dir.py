'''
    This file contains all of the file paths across the entire program. All you have to do is change a path here and it
    it changes everywhere.

Sources and helpfull links
    https://datatofish.com/command-prompt-python/
    https://pynative.com/python-count-number-of-files-in-a-directory/
'''

# Path for all of the created frames when video is split up in VideoFrameCapture.py
frame_dir = "C:\\Users\\deadg\\OneDrive\\Documents\\GithubRep\\SeniorCapstone\\TextExtraction\\Frames"

# Paths to all the temporary data that will be created once program is ran
record_folder = "C:\\Users\\deadg\\OneDrive\\Documents\\GithubRep\\SeniorCapstone\\recordings\\Temp\\000"
export_folder = record_folder + "\\exports"
video_dir = export_folder + "\\000\\world.mp4"
gaze_dir = export_folder + "\\000\\gaze_positions.csv"

# testing data paths
test_video_dir = "C:\\Users\\deadg\\OneDrive\\Documents\\GithubRep\\SeniorCapstone\\recordings\\1920x1080\\000\\exports\\000\\world.mp4"
test_gaze_dir = "C:\\Users\\deadg\\OneDrive\\Documents\\GithubRep\\SeniorCapstone\\recordings\\1920x1080\\000\\exports\\000\\gaze_positions.csv"

# Paths for running the pupil programs for cmd commands
cap_dir = "C:\\Program Files (x86)\\Pupil-Labs\\Pupil v3.5.1\\Pupil Capture v3.5.1"
play_dir = "C:\\Program Files (x86)\\Pupil-Labs\\Pupil v3.5.1\\Pupil Player v3.5.1"


# displaying the paths when file_dir is run so output has history
print("----------Directory file Paths----------")
print("This is the recording path", record_folder, "\n")
print("This is the frames path", frame_dir, "\n")
print("This csv file path", test_gaze_dir, "\n")
print("The world video path: ", test_video_dir, "\n")
