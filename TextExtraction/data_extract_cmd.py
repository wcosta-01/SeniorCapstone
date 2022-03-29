import file_dir
import os
from time import sleep
video_dir = file_dir.video_dir
# Pupil Capture C:\Program Files (x86)\Pupil-Labs\Pupil v3.5.1\Pupil Capture v3.5.1\pupil_capture.exe
# pupil player C:\Program Files (x86)\Pupil-Labs\Pupil v3.5.1\Pupil Player v3.5.1\pupil_player.exe
cap_dir = "C:\Program Files (x86)\Pupil-Labs\Pupil v3.5.1\Pupil Capture v3.5.1"
play_dir = "C:\Program Files (x86)\Pupil-Labs\Pupil v3.5.1\Pupil Player v3.5.1"
record_dir = file_dir.ext_recordings_dir

def start_cap():
    cap_command = "cd " + cap_dir + " & start pupil_capture.exe"
    cap = 'cmd /c ' + '"' + cap_command + '"'
    os.system(cap)

#opens player with a give recording directory
# may take a few seconds to load
def start_player():
    play_command = " cd " + play_dir + " & start pupil_player.exe "
    add_dir = play_command + record_dir
    play = 'cmd /c ' + '"' + add_dir + '"'
    os.system(play)

# Extracts the data from player
def extract_data():
    sleep(6)
    # run a cmd command that opens powershell and runs the following command in order to press the letter e to export the
    # previously uploaded recording file.
    cmd_command = "powershell ; $wsh = New-Object -ComObject WScript.Shell ; $wsh.SendKeys('{e}')"
    shell_command = 'cmd /c ' + '"' + cmd_command + '"'
    os.system(shell_command)
