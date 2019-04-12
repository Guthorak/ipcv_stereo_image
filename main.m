clear all;
close all;

addpath('src');

load('calibration/caliblm.mat');
load('calibration/calibmr.mat');

image_left = imread('samples/subjects/2/subject2_Left_1.jpg');
image_middle = imread('samples/subjects/2/subject2_Middle_1.jpg');
image_right = imread('samples/subjects/2/subject2_Right_1.jpg');

drange = [160, 416];

sigma = 2;

[pclm, dmlm] = createPointCloud(image_left, image_middle, drange, sigma, 'l', stereoParamsLM);
[pcmr, dmmr] = createPointCloud(image_middle, image_right, drange, sigma, 'l', stereoParamsMR);

[im_left_rect, im_mid_rect1] = rectifyStereoImages(image_left, image_middle, stereoParamsLM, 'OutputView', 'full');
[im_mid_rect2, im_right_rect] = rectifyStereoImages(image_middle, image_right, stereoParamsMR, 'OutputView', 'full');

pc = mergePointClouds(pclm, pcmr, 10, stereoParamsLM, stereoParamsMR);

figure;
subplot(1, 2, 1);
imshow(dmlm, drange);
subplot(1, 2, 2);
imshow(dmmr, drange);
colormap jet;
colorbar;

