"""Module to create point clouds from disparity maps"""
import cv2
import numpy as np
from rectification import rectify_images
from disparity_map import disparity_map


PLY_HEADER = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''


def create_point_cloud(disp_map, projection):
    return cv2.reprojectImageTo3D(disp_map, projection)


def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'wb') as f:
        f.write((PLY_HEADER % dict(vert_num=len(verts))).encode('utf-8'))
        np.savetxt(f, verts, fmt='%f %f %f %d %d %d ')


#def create_point_cloud(disparity_map, stereo_params):
#    fx = stereo_params.camera_matrix_left[0, 0]
#    fy = stereo_params.camera_matrix_left[1, 1]
#    nmax, mmax = disparity_map.shape
#    #pc = np.zeros((nmax*mmax, 3))
#    pc = []
#    for n in range(nmax):
#        for m in range(mmax):
#            if disparity_map[n, m] != 0.0:
#                z = (fx*stereo_params.translation[0]/disparity_map[n, m])[0]
#                x = (n+1)*z/fx
#                y = (m+1)*z/fy
#                pc.append(np.array([x, y, z]))
#                #pc[n*m + m, :] = np.array([x, y, z])
#    return pc


if __name__ == "__main__":
    import sys
    import matplotlib.pyplot as plt
    from pyqtgraph.Qt import QtCore, QtGui
    import pyqtgraph.opengl as gl
    from mpl_toolkits.mplot3d import axes3d 
    from stereo_params import get_stereo_params

    STEREO_PARAMS = get_stereo_params("calibration")

    left_img = cv2.imread("samples/subjects/1/subject1_Left_1.jpg", cv2.IMREAD_GRAYSCALE)
    right_img_color = cv2.imread("samples/subjects/1/subject1_Right_1.jpg")
    right_img = cv2.cvtColor(right_img_color, cv2.COLOR_BGR2GRAY)

    color = cv2.cvtColor(right_img_color, cv2.COLOR_BGR2RGB)

    right_rect, q = rectify_images(right_img, STEREO_PARAMS)

    disp_map = disparity_map(left_img, right_rect, 32, 64, 15)
    mask = disp_map > disp_map.min()

    point_cloud = create_point_cloud(disp_map, q)

    point_cloud = point_cloud[mask]
    color = color[mask]

    write_ply("test.ply", point_cloud, color)

    fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    ax = fig.add_subplot(111)
    plt.imshow(disp_map)
    plt.colorbar()
    #ax.scatter(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2])
    plt.show()
