"""Utilities for rectifying two stereo images"""
import cv2
import numpy as np
import matplotlib.pyplot as plt


def rectify_images(right, stereo_params):
    rotation_1 = np.zeros((3, 3))
    rotation_2 = np.zeros((3, 3))
    projection_1 = np.zeros((3, 3))
    projection_2 = np.zeros((3, 3))
    disp_to_depth = np.zeros((4, 4))
    size = right.shape
    cv2.stereoRectify(
        stereo_params.camera_matrix_left,
        stereo_params.distortion_left,
        stereo_params.camera_matrix_right,
        stereo_params.distortion_right,
        size[1::-1],
        stereo_params.rotation,
        stereo_params.translation,
        rotation_1,
        rotation_2,
        projection_1,
        projection_2,
        Q=disp_to_depth
        )
    map1, map2 = cv2.initUndistortRectifyMap(
        stereo_params.camera_matrix_right,
        stereo_params.distortion_right,
        rotation_2,
        stereo_params.camera_matrix_right,
        size[1::-1],
        cv2.CV_32FC1)
    return cv2.remap(right, map1, map2, cv2.INTER_LINEAR), disp_to_depth


if __name__ == "__main__":
    from stereo_params import get_stereo_params
    STEREO_PARAMS = get_stereo_params("calibration")

    left_img = cv2.imread("samples/subjects/1/subject1_Left_1.jpg")
    right_img = cv2.imread("samples/subjects/1/subject1_Right_1.jpg", cv2.IMREAD_GRAYSCALE)

    right_rect, _ = rectify_images(right_img, STEREO_PARAMS)

    fig = plt.figure()
    ax = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax.imshow(left_img)
    ax2.imshow(right_rect)
    plt.show()
