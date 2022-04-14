'''
    This file contains all of the file paths across the entire program. All you have to do is change a path here and it
    it changes everywhere.

Sources and helpfull links
    https://datatofish.com/command-prompt-python/
    https://pynative.com/python-count-number-of-files-in-a-directory/
'''
# Paths for running the pupil programs for cmd commands

cap_dir = "C:\\Program Files (x86)\\Pupil-Labs\\Pupil v3.5.1\\Pupil Capture v3.5.1"
play_dir = "C:\\Program Files (x86)\\Pupil-Labs\\Pupil v3.5.1\\Pupil Player v3.5.1"

# Path for all the created frames when video is split up in VideoFrameCapture.py
import pandas as pd
githubRep = "C:\\Users\\deadg\\OneDrive\\Documents\\GithubRep\\SeniorCapstone"
frame_dir = githubRep + "\\TextExtraction\\Frames"
recordings_dir = "C:\\Users\\deadg\\OneDrive\\Documents\\GithubRep\\recordings"
east_text_det = "C:\\Users\\deadg\\OneDrive\\Documents\\GithubRep\\SeniorCapstone\\Tesseract\\frozen_east_text_detection.pb"

# Paths to all the temporary data that will be created once program is ran
temp_dir = recordings_dir + "\\Temp"
temp_recording = recordings_dir + "\\Temp\\000"
export_temp_dir = temp_recording + "\\exports\\000"


# testing data paths
test_dir_1920 = recordings_dir + "\\recordings\\1920x1080_tests\\000\\exports\\001"
test_dir_1280 = recordings_dir + "\\recordings\\Compare_resolutions\\1280X720\\000\\exports\\000"


# Just change the folder that is added
# export_temp_dir is the default temp path
video_dir = test_dir_1280 + "\\world.mp4"
gaze_dir = test_dir_1280 + "\\gaze_positions.csv"



def get_gaze_coords_image(h, w):
    from TextExtraction.frame_selection import video_rt_data
    df = video_rt_data
    df["X"] = video_rt_data["X"].astype(int) + int(w/2)
    df["Y"] = video_rt_data["Y"].astype(int) + int(h/2)

    # df.drop_duplicates(subset = "world_index", keep = "first", inplace=False)

    return df.values.tolist()

def get_gaze_coords(h, w):
    columns = ["world_index", "gaze_point_3d_x", "gaze_point_3d_y"]
    df = pd.read_csv(gaze_dir, usecols=columns)

    df["gaze_point_3d_x"] = df["gaze_point_3d_x"].astype(int) + int(w / 2)
    df["gaze_point_3d_y"] = df["gaze_point_3d_y"].astype(int) + int(h / 2)

    df = df.drop_duplicates(subset=["world_index"]).reset_index(drop=True)

    return df.values.tolist()
# displaying the paths when file_dir is run so output has history
print("----------Directory file Paths----------")
print("This is the recording path", temp_recording, "\n")
print("This is the frames path", frame_dir, "\n")
print("This csv file path", gaze_dir, "\n")
print("The world video path: ", video_dir, "\n")
