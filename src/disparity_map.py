"""Module with utilities for creating disparity maps of stereo images"""

import numpy as np
import cv2
from matplotlib import pyplot as plt

    
def disparity_map(image_left, image_right, min_disparities, num_desparities, box_size):

    '''
    Class for determining the disparity between two images

    Parameters:
    -----------
    image_left
        image taken by left camera
    image_right
        image taken by right camera
    num_disparity
        disparity range. Class will find disparity for each pixel between 0 and num_disparity. Must be divisible by 16 (i think)
    box_size
        size of block compared by algorithm. Size should be odd as block is centered at current pixel
    '''
    window_size = 3
    stereo = cv2.StereoSGBM_create(
        minDisparity=min_disparities, 
        numDisparities=num_desparities, 
        blockSize=box_size,
        disp12MaxDiff=1,
        uniquenessRatio=10,
        speckleWindowSize=100,
        speckleRange=32,
        P1 = 8*3*window_size**2,
        P2 = 32*3*window_size**2)
    return stereo.compute(image_left, image_right)