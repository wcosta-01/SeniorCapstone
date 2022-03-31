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
import os


# Returns true if it is not empty and false if it is empty
def is_not_empty(dir_path):
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

'''
 byebye_data Removes files from a given directory.
'''
def byebye_data(input_dir):
    # folder path
    # Iterate directory
    if is_not_empty(input_dir):
        for file in os.listdir(input_dir):
            # check if current path is a file
            if os.path.isfile(os.path.join(input_dir, file)):
                # Adding the file to the end of the delete command
                del_command = r" del /f " + file
            else:  # if the dir is a folder
                del_command = r"echo y | rmdir /s " + file
            # Adding the delete command to the end of the cd command to get to the directory.
            # cmd_command = "cd C:\\Users\\deadg\\OneDrive\\Documents\\GithubRep\\SeniorCapstone\\TextExtraction\\Frames &" + del_command
            cmd_command = " cd " + input_dir + " & " + del_command

            # CMD /K – execute a command and then remain:
            # CMD /C – execute a command and then terminate:
            # Adding cmd and the operator to kill the terminal after teh command.
            final_command = 'cmd /c ' + '"' + cmd_command + '"'
            # Sending the command to the system
            os.system(final_command)
        print("data deleted")
    else:
        print("Folder is empty")
