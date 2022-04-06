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
video_dir = "C:\\Users\\deadg\\OneDrive\\Documents\\GithubRep\\SeniorCapstone\\recordings\\Temp\\000\\exports\\000\\world.mp4"
gaze_dir = "C:\\Users\\deadg\\OneDrive\\Documents\\GithubRep\\SeniorCapstone\\recordings\\Temp\\004\\exports\\000\\gaze_positions.csv"
record_folder = "C:\\Users\\deadg\\OneDrive\\Documents\\GithubRep\\SeniorCapstone\\recordings\\Temp\\000"

# Paths for running the pupil programs for cmd commands
cap_dir = "C:\\Program Files (x86)\\Pupil-Labs\\Pupil v3.5.1\\Pupil Capture v3.5.1"
play_dir = "C:\\Program Files (x86)\\Pupil-Labs\\Pupil v3.5.1\\Pupil Player v3.5.1"

'''
    Making a directory checker that checks to see if files or locations are created
    Going to use this before running kill_pupil in cmd_commands.py
'''
#def checking_files(input_dir):
# Returns true if dir is not empty and false if the directory is empty
def dir_not_empty(dir_path):
    import os
    count = 0
    # Iterate directory
    for file in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, file)):
            count += 1
    # print('File count:', count)
    if count == 0:
        return False
    else:
        return True
# end of is_empty