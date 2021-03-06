"""Module with utilities for creating disparity maps of stereo images"""

import numpy as np
import cv2
from matplotlib import pyplot as plt

if __name__ == '__main__':
    
    image_left = cv2.imread('src/subject1_Left_1.jpg', cv2.IMREAD_GRAYSCALE)
    image_middle = cv2.imread('src/subject1_Middle_1.jpg', cv2.IMREAD_GRAYSCALE)
    image_right = cv2.imread('src/subject1_Right_1.jpg', cv2.IMREAD_GRAYSCALE)
    
    print(image_left)
    
    stereo = cv2.StereoBM_create(512, 5) # NumDesparities, BoxSize
    disparity = stereo.compute(image_left, image_middle)
    
    plt.imshow(disparity)
    plt.show()
    
def DisparityMapper(image_left, image_right, num_desparities, box_size):

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
    stereo = cv2.StereoBM_create(num_desparities, box_size)
    disparity_map = stereo.compute(image_left, image_right)
    return disparity_map