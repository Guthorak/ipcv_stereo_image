"""
Module containing camera calibration utilities
"""
import numpy as np
import cv2
from tqdm import tqdm


class CalibrationError(Exception):
    pass


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
        self._images = {
            "left": images_left,
            "right": images_right,
            "middle": images_middle
        }
        self._calibration_matrices = {}
        self._translation = {}
        self._rotation = {}
        self._distortion_coefficients = {}

    def calibrate(self) -> None:
        NROWS, NCOLS = 6, 9
        for key, value in self._images.items():
            print(f"Calibrating camera {key}")
            imshape = cv2.cvtColor(cv2.imread(value[0]), cv2.COLOR_BGR2GRAY).shape[::-1]
            object_points, image_points = self._get_object_and_image_points(NROWS, NCOLS, value)
            success, matrix, distortion, rotation, translation = cv2.calibrateCamera(object_points, 
                image_points, 
                imshape,
                None, 
                None)
            if not success:
                raise CalibrationError(f"Failed to calibrate camera: {key}")
            self._calibration_matrices[key] = matrix
            self._translation[key] = translation
            self._rotation[key] = rotation
            self._distortion_coefficients[key] = distortion

    @property
    def calibration_matrices(self) -> dict:
        return self._calibration_matrices

    @property
    def distortion_coefficients(self) -> dict:
        return self._distortion_coefficients

    @property
    def rotations(self) -> dict:
        return self._rotation

    def translations(self) -> dict:
        return self._translation

    def _get_object_and_image_points(self, nrows, ncols, image_set) -> tuple:
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # prepare object points, given chess board size
        objp = np.zeros((nrows*ncols, 3), np.float32)
        objp[:, :2] = np.mgrid[0:ncols, 0:nrows].T.reshape(-1, 2)

        # arrays to store object and image points
        object_points, image_points = [], []

        for fname in tqdm(image_set):
            image = cv2.imread(fname)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # find chess board corners
            success, corners = cv2.findChessboardCorners(gray, (ncols, nrows), None)

            if success:
                object_points.append(objp)
                # refine corners
                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                image_points.append(corners2)
        
        return object_points, image_points
        

if __name__ == "__main__":
    import glob
    images_left = glob.glob("samples/calibration/*L*.jpg")
    images_right = glob.glob("samples/calibration/*R*.jpg")
    images_middle = glob.glob("samples/calibration/*M*.jpg")

    calibrator = Calibrator(images_left, images_middle, images_right)
    calibrator.calibrate()
    print(calibrator.calibration_matrices)