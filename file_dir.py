'''
This fill will be a list of commands that will be called at the end of the process to delete all the created files.

!!!!!!!!!!It will also act as the master File for all the file paths throughout the structure for this project!!!!!!!!!!!!!!!!


- All of the captured frames from VideoFrameCapture that are located in the Frames folder.
- The world.mp4 video located in the ExportedData folder
- The exported CSV file from batchExport located in ExportedData folder.


Sources and helpfull links
    https://datatofish.com/command-prompt-python/
    https://pynative.com/python-count-number-of-files-in-a-directory/
'''

# All the file paths that will be used in this program will be stored here.
# Where the created frames will be stored after splitting the video into frames
frame_dir = "C:\\Users\\deadg\\OneDrive\\Documents\\GithubRep\\SeniorCapstone\\TextExtraction\\Frames"
#change folder at end of recordings_dir to match the one created
recordings_dir = "C:\\Users\\deadg\\OneDrive\\Documents\\GithubRep\\SeniorCapstone\\recordings\\OldRecordings\\2022_01_25"
video_dir = 'C:\\Users\\deadg\\OneDrive\\Documents\\GithubRep\\SeniorCapstone\\recordings\\Temp\\000\\exports\\000\\world.mp4'
# Change this to the folder that will be created
ext_recordings_dir = r"C:\\Users\\deadg\\OneDrive\\Documents\\GithubRep\\SeniorCapstone\\recordings\\Temp\\000"
cap_dir = "C:\Program Files (x86)\Pupil-Labs\Pupil v3.5.1\Pupil Capture v3.5.1"
play_dir = "C:\Program Files (x86)\Pupil-Labs\Pupil v3.5.1\Pupil Player v3.5.1"

'''
    Making a directory checker that checks to see if files or locations are created
    Going to use this before running kill_pupil in cmd_commands.py
'''
#def checking_files(input_dir):
# Returns true if dir is not empty and false if the dir is empty
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