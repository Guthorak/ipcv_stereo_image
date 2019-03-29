"""
Module containing camera calibration utilities
"""
import numpy as np
import cv2


class Calibrator:

    def __init__(self, images_left: list, images_middle: list, images_right: list):
        """
        Class for calibration of stereographic camera sets using
        calibration images of chessboards        

        Parameters
        ----------
        images_left: list
            List of paths to left calibration images 
        images_middle: list
            List of paths to middle calibration images 
        images_right: list
            List of paths to right calibration images 
        """
        self._images_left = images_left
        self._images_middle = images_middle
        self._images_right = images_right

    def calibrate(self) -> None:
        raise NotImplementedError

    def calibration_matrix(self) -> np.ndarray:
        raise NotImplementedError

    def distortion_coefficients(self):
        raise NotImplementedError

    def rotation(self):
        raise NotImplementedError

    def translation(self):
        raise NotImplementedError