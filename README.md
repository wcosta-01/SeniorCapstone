# Welcome to Wit
Wit is an eye tracking software that uses pupil labs core eye tracking glasses to read signs and any text the user looks at. It can read a book, look up restraints when you look at an advertisement.


# Pupil Labs
We have used many of the resources that pupil labs has published along with a few community projects in order to connect this software.

# Tesseract OCR


## Program Structure
We have spilt the process into a collection of files that connect and allow for easy modification. Each file has its own methods that are either ran from within the same file or from a Control file.

### Frame Selection
Frame selection takes the gaze data from a given recording and uses it to find which frames of the video where the user was looking in the same area. 

Frame selection does this by taking 4 columns of data from the gaze_position.csv, the world_index(the closest world video frame), and gaze_normal0_x, gaze_normal0_y, and gaze_normal0_z.


We then look for the smallest rate of change in each coordinate column. Then we compare each coordinate and select the world_index where all 3 coordinates are within 
0.10 units of one another. 


In layman's terms, we look for the point at which the user is not moving their eyes.
Store the coordinates that are between when the user started looking in that area to when they stopped looking in a list.
Next we take those lists and find the world_index where all three coordinates are 0.10 units apart and store them in a list.
Finally, we find the middle most world_index and return that value.

gaze_normal0 is "The visual axis goes through the center of the eyeball and the object that is looked at."



##
