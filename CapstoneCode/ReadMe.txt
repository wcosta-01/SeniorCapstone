FrameCapture.ipynb
    This program will go iterate through the norm_pos_x and norm_pos_y coordinates in the gaze_position.csv file and will group coordinates together if they fit within a specified range.
    It then takes the groups and pick the mean frame from that group. That coordinate Value also has a Frame Value(world_index). Once we have the exact frame from gaze_position.csv we
    then pass that onto [insert file name].
VideoFrameCapture
    VideoFrameCapture will be used to capture the frame specified in FrameCapture. It will take the MP4 file and find extract the frame into a image file. Then that image will be passed onto
    Easyocr.ipynb tp be analyzed.
Easyocr.ipynb
    This program uses the library Easyocr to take the captured frame from the video and anylizes the text within that image. Whether that be a road sign, restrant menu, or text on a page.
    It then translate the information from the image into text that we can then direct to any other process.
