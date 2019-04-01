"""Module containing class for holding parameters of a set of stereo cameras"""
import numpy as np
from collections import namedtuple


StereoParameters = namedtuple(
    "StereoParameters",
    [
        "camera_matrix_left",
        "camera_matrix_right",
        "distortion_left",
        "distortion_right",
        "rotation",
        "translation",
        "essential",
        "fundamental"
    ]
)


def get_stereo_params(path) -> StereoParameters:
    return StereoParameters(
        np.load(path + "/calibration_matrix_left.npy"),
        np.load(path + "/calibration_matrix_right.npy"),
        np.load(path + "/distortion_left.npy"),
        np.load(path + "/distortion_right.npy"),
        np.load(path + "/rotation.npy"),
        np.load(path + "/translation.npy"),
        np.load(path + "/essential.npy"),
        np.load(path + "/fundamental.npy")
    )