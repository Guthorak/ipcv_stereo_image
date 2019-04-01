"""
Module containing camera calibration utilities
"""
import numpy as np
import cv2


class CalibrationError(Exception):
    pass


class Calibrator:

    def __init__(self, images_left: list, images_right: list):
        """
        Class for calibration of stereographic camera sets using
        calibration images of chessboards        

        Parameters
        ----------
        images_left: list
            List of paths to left calibration images 
        images_right: list
            List of paths to right calibration images 
        """
        self._images = {
            "left": images_left,
            "right": images_right,
        }
        self._calibration_matrices = {}
        self._distortion_coefficients = {}
        self._fundamental = None
        self._essential = None
        self._rotation = None
        self._translation = None

    def calibrate(self) -> None:
        NROWS, NCOLS = 6, 9
        imshape = cv2.imread(self._images["left"][0], cv2.IMREAD_GRAYSCALE).shape[::-1]
        object_points, image_points_left, image_points_right = self._get_object_and_image_points(NROWS, NCOLS, 
            (self._images["left"], self._images["right"]))
        success, matrix_left, distortion_left, matrix_right, distortion_right, r, t, e, f = cv2.stereoCalibrate(
            object_points,
            image_points_left,
            image_points_right,
            np.zeros((3, 3)),
            None,
            np.zeros((3, 3)),
            None,
            imshape,
            flags=cv2.CALIB_SAME_FOCAL_LENGTH)
        if not success:
            raise CalibrationError(f"Failed to calibrate cameras")
        self._fundamental = f
        self._essential = e
        self._translation = t
        self._rotation = r
        self._calibration_matrices = {"left": matrix_left, "right": matrix_right}
        self._distortion_coefficients = {"left": distortion_left, "right": distortion_right}

    @property
    def rotation(self) -> np.ndarray:
        return self._rotation

    @property
    def translation(self) -> np.ndarray:
        return self._translation

    @property
    def calibration_matrices(self) -> dict:
        return self._calibration_matrices

    @property
    def distortion_coefficients(self) -> dict:
        return self._distortion_coefficients

    @property
    def fundamental(self) -> np.ndarray:
        return self._fundamental

    @property
    def essential(self) -> np.ndarray:
        return self._essential

    def _get_object_and_image_points(self, nrows, ncols, image_set) -> tuple:
        imgs_left, imgs_right = image_set
        imgs_left = sorted(imgs_left)
        imgs_right = sorted(imgs_right)
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # prepare object points, given chess board size
        objp = np.zeros((nrows*ncols, 3), np.float32)
        objp[:, :2] = np.mgrid[0:ncols, 0:nrows].T.reshape(-1, 2)

        # arrays to store object and image points
        object_points, image_points_left, image_points_right = [], [], []

        for fname_l, fname_r in zip(imgs_left, imgs_right):
            image_l = cv2.imread(fname_l)
            image_r = cv2.imread(fname_r)
            gray_l = cv2.cvtColor(image_l, cv2.COLOR_BGR2GRAY)
            gray_r = cv2.cvtColor(image_r, cv2.COLOR_BGR2GRAY)

            # find chess board corners
            success_l, corners_l = cv2.findChessboardCorners(gray_l, (ncols, nrows), None)
            if not success_l:
                continue
            success_r, corners_r = cv2.findChessboardCorners(gray_r, (ncols, nrows), None)

            if success_r:
                object_points.append(objp)
                # refine corners
                corners_l2 = cv2.cornerSubPix(gray_l, corners_l, (11, 11), (-1, -1), criteria)
                corners_r2 = cv2.cornerSubPix(gray_r, corners_r, (11, 11), (-1, -1), criteria)
                image_points_left.append(corners_l2)
                image_points_right.append(corners_r2)
        
        return object_points, image_points_left, image_points_right
        

def calibrate(images_dir, out_dir):
    import glob
    images_left = glob.glob(images_dir + "/*L*.jpg")
    images_right = glob.glob(images_dir + "/*R*.jpg")

    calibrator = Calibrator(images_left, images_right)
    calibrator.calibrate()

    for camera in ["left", "right"]:
        np.save(out_dir + f"/calibration_matrix_{camera}.npy", calibrator.calibration_matrices[camera])
        np.save(out_dir + f"/distortion_{camera}.npy", calibrator.distortion_coefficients[camera])
        np.save(out_dir + f"/distortion_{camera}.npy", calibrator.distortion_coefficients[camera])
    np.save(out_dir + f"/essential.npy", calibrator.essential)
    np.save(out_dir + f"/fundamental.npy", calibrator.fundamental)
    np.save(out_dir + f"/translation.npy", calibrator.translation)
    np.save(out_dir + f"/rotation.npy", calibrator.rotation)
