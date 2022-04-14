'''
    This file takes the real-time data coords captured during the recording and compares it
    to the grid that tesseract creates and finds the matching area where the user is looking.
'''
import pandas as pd
from matplotlib import pyplot as plt
from file_dir import test_gaze_dir, frame_dir

from TextExtraction.cord_frame_capture import gaze_points, selecting_frame
from TextExtraction.VideoFrameCapture import frame_check

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True


# columns = ["gaze_point_3d_x", "gaze_point_3d_y"]
# df = pd.read_csv(test_gaze_dir, usecols=columns)
# print("Contents in csv file:\n", gaze_points)

# --------------- gaze_points --------------------------------------------------
print("Contents in csv file:\n", gaze_points)
# df.loc[:, "gaze_normal0_x"] = -df.gaze_normal0_x
gaze_points["gaze_point_3d_x"] = gaze_points["gaze_point_3d_x"].astype(int)
gaze_points["gaze_point_3d_y"] = gaze_points["gaze_point_3d_y"].astype(int)
gaze_points.loc[:, "gaze_point_3d_y"] = -gaze_points.gaze_point_3d_y
plt.plot(gaze_points.gaze_point_3d_x, gaze_points.gaze_point_3d_y)
# plt.xlim(-640, 640)
# plt.ylim(-360, 360)


print(frame_check())
file_path = frame_dir + "\\" + frame_check()
imag = plt.imread(file_path)
# h, w = imag.shape[:2]

im = plt.imshow(imag, extent=[-640, 640, -360, 360])
plt.show()

from cmd_commands import byebye_data

byebye_data(frame_dir)
