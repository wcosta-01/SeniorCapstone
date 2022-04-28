'''
    This file controls the entire operation.
    Used to connect, run and test all the methods of the other files in the correct order.
'''

from time import sleep

import pandas as pd

from cmd_commands import start_capture, start_player, extract_data, kill_pupil, byebye_data, get_craft_image
from file_dir import frame_dir, selected_frame_dir, result_dir

# removing data from holding directories
byebye_data(frame_dir)
byebye_data(selected_frame_dir)
byebye_data(result_dir)
sleep(2)

def run_recording():
    # starts up the pupil capture application.
    # print("starting capture", start_capture())
    sleep(10)
    # Starts the recording and saving the data that is received in real-time
    from TextExtraction.real_time_recording import data_collection
    data_collection(10)

    # Now going to start Pupil Player to export the video and csv files
    sleep(7)
    print("Starting player", start_player())
    sleep(7)
    print("extracting data", extract_data())  # Waits 6 seconds before starting extraction
    sleep(15)
    '''
    # kill player and capture once extraction is done
    try:
        print("Killing player", kill_pupil('player'))
        print("Killing capture", kill_pupil('capture'))
    except :
        print("failed to kill player or capture")
    '''
'''
    ---------------------- Video and Image Analysis ---------------------- 
    Now that the data has been extracted, we can run the image and video
    processing for that data.
    
'''
def gen_frame():
    from TextExtraction.frame_selection import image_data
    from TextExtraction.VideoFrameCapture import frame_check, grabbingFrame
    # Checks the Frames' directory to see if the video has already been split
    frame_check()
    # Assigning the selected frame to a variable that is then passed to Wit for image processing
    frame_name = grabbingFrame(image_data)
    print(frame_name)
    return frame_name
'''
    ---------------------- Visualization of Analysis ----------------------
    Once the data has been sorted and organized we can then see the comparison
    between the video and the imaging processing. 
    - Wit.py is for images
    - WitVideo.py is for videos 
    - get_crafty
'''

def wit_craft(frame_name):
    # Image processing
    from Tesseract import Wit
    img_results = Wit.wit_image(frame_name)

    # Image processing with Craft
    print(get_craft_image(frame_name))
    '''from Tesseract import get_crafty
    crafty_results = get_crafty.craft_image(frame_name, 'eng')
    '''
    # removing data from Frame directory and from selected directory
    byebye_data(selected_frame_dir)
    byebye_data(frame_dir)
    sleep(3)
    return img_results



def wit_vid():
    from Tesseract import WitVideo
    # Video processing
    vid_results = WitVideo.wit_video()
    return vid_results

# just making it easyer to uncomment stuff
# run_recording()
frame_name = gen_frame()

img_results = wit_craft(frame_name)
vid_results = wit_vid()


# Taking all the results and creating a data frame to display them
END_results = {"Wit(image)":img_results, "Wit Video": vid_results}
END_results = pd.DataFrame.from_dict(END_results)

# Saving the data frame as a csv file
saved_results = result_dir + "text_results.csv"
END_results.to_csv(saved_results)
#sleep(60)
#byebye_data(temp_dir)

print("All done, Goodbye!")