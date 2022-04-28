'''
    This file contains all of the file paths across the entire program.
    All you have to do is change a path here and it
    changes everywhere.

    Reach run it also prints out The directories that are being used in that specific run.


Sources and helpfull links
    https://datatofish.com/command-prompt-python/
    https://pynative.com/python-count-number-of-files-in-a-directory/
'''


# Paths for running the Pupil software for cmd commands
import os.path

cap_dir = "C:\\Program Files (x86)\\Pupil-Labs\\Pupil v3.5.1\\Pupil Capture v3.5.1"
play_dir = "C:\\Program Files (x86)\\Pupil-Labs\\Pupil v3.5.1\\Pupil Player v3.5.1"

# Path for all the created frames when video is split up in VideoFrameCapture.py
githubRep = "C:\\Users\\deadg\\OneDrive\\Documents\\GithubRep\\SeniorCapstone"
frame_dir = githubRep + "\\TextExtraction\\Frames"
recordings_dir = "C:\\Users\\deadg\\OneDrive\\Documents\\GithubRep\\recordings"
east_text_det = "C:\\Users\\deadg\\OneDrive\\Documents\\GithubRep\\SeniorCapstone\\Tesseract\\frozen_east_text_detection.pb"

# Path for the CRAFT implementation
craft_dir = r"C:\Users\deadg\OneDrive\Documents\GithubRep\SeniorCapstone\CRAFT-pytorch-master"
selected_frame_dir = craft_dir + "\\selected"
result_dir = githubRep + "\\results"

# Testing data paths
eng_signs_1920 = r"C:\Users\deadg\OneDrive\Documents\GithubRep\recordings\Temp\eng_sign_1920\exports\000"
slapYaMama_1280 = r"C:\Users\deadg\OneDrive\Documents\GithubRep\recordings\Temp\SlapYaMama\exports\000"
test_dir_1920 = recordings_dir + "\\Compare_resolutions\\1920x1080\\000\\exports\\000"
test_dir_1280 = recordings_dir + "\\Compare_resolutions\\1280X720\\000\\exports\\000"
test_error = r"C:\Users\deadg\OneDrive\Documents\GithubRep\recordings\Temp\Test_error\exports\000"
standard_test = r"C:\Users\deadg\OneDrive\Documents\GithubRep\recordings\Temp\BleachNaruto\exports\000"
# Real world tests
rw_dir_1920 = r"C:\Users\deadg\OneDrive\Documents\GithubRep\recordings\pupil_real_world\1280X720\000\exports\000"
rw_dir_1280 = recordings_dir + "\\pupil_real_world\\1280X720\\000\\exports\\000"
red_bull_can = r"C:\Users\deadg\OneDrive\Documents\GithubRep\recordings\Temp\rebullCan\exports\000"
# Michael's Sign Tests
cal_michaels_1920 = r"C:\Users\deadg\OneDrive\Documents\GithubRep\recordings\Michael'sTests\cal_michaels_1920X1080\000\exports\000"
michaels_1280 = r"C:\Users\deadg\OneDrive\Documents\GithubRep\recordings\Michael'sTests\michaels_1280X720\000\exports\000"
michaels_1920 = r"C:\Users\deadg\OneDrive\Documents\GithubRep\recordings\Michael'sTests\michaels_1920X1080\000\exports\000"
michaels_1920_drone = r"C:\Users\deadg\OneDrive\Documents\GithubRep\recordings\Michael'sTests\wdrone_michaels_1920X1080\000\exports\000"

# Language Tests
lang_1280 = r"C:\Users\deadg\OneDrive\Documents\GithubRep\recordings\Pupil_rl_Languages\1280_rl_world_language\000\exports\000"
lang_1920 = r"C:\Users\deadg\OneDrive\Documents\GithubRep\recordings\Pupil_rl_Languages\1920_rl_world_language\000\exports\000"

# Paths to all the temporary data that will be created once program is ran
temp_dir = recordings_dir + "\\Temp"
temp_recording = recordings_dir + "\\Temp\\000"
default_dir = temp_recording + "\\exports\\000"

# default_dir is the default temp path
video_dir = red_bull_can + "\\world.mp4"
gaze_dir = red_bull_can + "\\gaze_positions.csv"

import pandas as pd

def get_gaze_coords_image(h, w):
    from TextExtraction.frame_selection import matching_gaze
    df = matching_gaze
    df["norm_pos_x"] = df["norm_pos_x"] * w
    df["norm_pos_y"] = df["norm_pos_y"] * h

    df["norm_pos_x"] = df["norm_pos_x"].astype(int)
    df["norm_pos_y"] = df["norm_pos_y"].astype(int)
    df["norm_pos_y"] = h - df["norm_pos_y"]
    #df.drop_duplicates(subset = "world_index", keep = "first", inplace=False)

    return df.values.tolist()


def get_gaze_coords_vid(h, w):
    columns = ["world_index", "norm_pos_x", "norm_pos_y"]
    df = pd.read_csv(gaze_dir, usecols=columns)
    # The y values are mirrored...
    df["norm_pos_x"] = df["norm_pos_x"] * w
    df["norm_pos_y"] = df["norm_pos_y"] * h

    df["norm_pos_x"] = df["norm_pos_x"].astype(int)
    df["norm_pos_y"] = df["norm_pos_y"].astype(int)
    df["norm_pos_y"] = h - df["norm_pos_y"]

    df = df.drop_duplicates(subset=["world_index"]).reset_index(drop=True)

    return df.values.tolist()


def get_gaze_coords_rt(h, w, norm_pos):
    # pos_x =0 pos_y =1
    norm_pos[0] = norm_pos[0] * w
    norm_pos[1] = norm_pos[1] * h

    norm_pos[0] = int(norm_pos[0])
    norm_pos[1] = int(norm_pos[1])
    norm_pos[1] = h - norm_pos[1]

    return norm_pos


# displaying the paths when file_dir is run so output has history
print("----------Directory file Paths----------")
print("This is the recording path", temp_recording, "\n")
print("This is the frames path", frame_dir, "\n")
print("This csv file path", gaze_dir, "\n")
print("The world video path: ", video_dir, "\n")
print("Saved results can be found here: ", result_dir, "\n")

