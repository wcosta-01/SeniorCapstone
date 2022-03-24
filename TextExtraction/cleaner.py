'''
This fill will be a list of commands that will be called at the end of the process to delete all the created files.

- All of the captured frames from VideoFrameCapture that are located in the Frames folder.
- The world.mp4 video located in the ExportedData folder
- The exported CSV file from batchExport located in ExportedData folder.


Sources and helpfull links
    https://datatofish.com/command-prompt-python/
    https://pynative.com/python-count-number-of-files-in-a-directory/
'''
import os
dir_path = r"C:\Users\deadg\OneDrive\Documents\GithubRep\SeniorCapstone\TextExtraction\Frames"

def byebye_frames():
    # Removing the frame jpg files from the directory Frames.
    # folder path
    #dir_path = r"C:\Users\deadg\OneDrive\Documents\GithubRep\SeniorCapstone\TextExtraction\Frames"
    # Iterate directory
    for file in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, file)):
            # Adding the file to the end of the delete command
            del_command = r" del /f " + file

            # Adding the delete command to the end of the cd command to get to the directory.
            cmd_command = "cd C:\\Users\\deadg\\OneDrive\\Documents\\GithubRep\\SeniorCapstone\\TextExtraction\\Frames &" + del_command

            # CMD /K – execute a command and then remain:
            # CMD /C – execute a command and then terminate:
            # Adding cmd and the operator to kill the terminal after teh command.
            final_command = 'cmd /c ' + '"' + cmd_command + '"'
            # Sending the command to the system
            os.system(final_command)
    print("Frames cleaned")

#Returns true if it is not empty and false if it is empty
def is_not_empty(dir_path):
    count = 0
    # Iterate directory
    for file in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, file)):
            count += 1
    #print('File count:', count)
    if count == 0:
        return False
    else:
        return True
#end of is_empty

byebye_frames()