'''
    This is the command center of the project.
    - All of the commands are created and ran from this file.
'''
import file_dir
import os

# Path that links to the exported World.mp4 file.
video_dir = file_dir.video_dir
# Used to start pupil capture
cap_dir = file_dir.cap_dir
# Used to start pupil player
play_dir = file_dir.play_dir
# Used to link the recording that will be exported in pupil player
record_folder = file_dir.temp_recording
# frames directory
frame_dir = file_dir.frame_dir
# craft directories
craft_dir = file_dir.craft_dir
results_dir = file_dir.results_dir
selected_frame_dir = file_dir.selected_frame_dir
# command for running CRAFT
def craft_image(frame_name):
    # Craft requires a lot of other stuff to run it properly. I advise testing it on its own before tying it into this program.
    # Here is their git hub: https://github.com/clovaai/CRAFT-pytorch We made very minor changes to the code in order to run it.
    craft_command = "cd " + results_dir
    move_image = craft_command + " & move " + frame_dir + "\\" + frame_name + " " + selected_frame_dir
    run_command = move_image + " & py -m test --test_folder=" + selected_frame_dir
    cmd = 'cmd /c '+ '"' + run_command + '"'
    os.system(cmd)
    return " craft getting crafty"

def start_capture():
    cap_command = "cd " + cap_dir + " & start pupil_capture.exe"
    cap = 'cmd /c ' + '"' + cap_command + '"'
    os.system(cap)
    return " capture started"


# Opens player with a given recording directory
def start_player():
    play_command = " cd " + play_dir + " & start pupil_player.exe "
    add_dir = play_command + record_folder
    play = 'cmd /c ' + '"' + add_dir + '"'
    os.system(play)
    return " player started"
'''
    Takes any pupil exe file and kills it.
    input = player or capture
    returns string explaining execution
'''
def kill_pupil(input):
    if input == 'capture' or input == 'player':
        kill_command = "taskkill/im pupil_" + input + ".exe"
        kill = 'cmd /c ' + '"' + kill_command + '"'
        os.system(kill)
        return input, " Terminated"
    else:
        return "input incorrect must be player or capture"


# Extracts the data from player
def extract_data():
    cmd_command = "powershell ; $wsh = New-Object -ComObject WScript.Shell ; $wsh.SendKeys('{e}')"
    shell_command = 'cmd /c ' + '"' + cmd_command + '"'
    os.system(shell_command)
    return "Video and CSV extracted"

'''
 byebye_data Removes files from a given directory.
'''
def byebye_data(input_dir):
    # folder path
    # Iterate directory
    if dir_not_empty(input_dir):
        for file in os.listdir(input_dir):
            # check if current path is a file
            if os.path.isfile(os.path.join(input_dir, file)):
                # Adding the file to the end of the delete command
                del_command = r" del /f " + file
            else:  # if the dir is a folder
                del_command = r"echo y | rmdir /s " + file
            # Adding the delete command to the end of the cd command to get to the directory.
            # cmd_command = "cd C:\\Users\\deadg\\OneDrive\\Documents\\GithubRep\\SeniorCapstone\\Collection_Manipulation\\Frames &" + del_command
            cmd_command = " cd " + input_dir + " & " + del_command

            # CMD /K – execute a command and then remain:
            # CMD /C – execute a command and then terminate:
            # Adding cmd and the operator to kill the terminal after teh command.
            final_command = 'cmd /c ' + '"' + cmd_command + '"'
            # Sending the command to the system
            os.system(final_command)
        print("Data has been deleted!")
    else:
        print("Folder is empty")

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