'''
    This file takes the real-time data coords captured during the recording and compares it
    to the grid that tesseract creates and finds the matching area where the user is looking.
'''
import file_dir
# Gets the rt data coords from a function call inside Control.py
rt_coords = {}
# rt_data is a dictionary
def set_rt_data_coords(rt_data):
    rt_coords = rt_data


