clear all;
close all;

addpath('src');

load('calibration/caliblm.mat');
load('calibration/calibmr.mat');

image_left = imread('samples/subjects/1/subject1_Left_1.jpg');
image_middle = imread('samples/subjects/1/subject1_Middle_1.jpg');
image_right = imread('samples/subjects/1/subject1_Right_1.jpg');

drange = [160, 320];

sigma = 5;

[pclm, dmlm] = createPointCloud(image_left, image_middle, drange, sigma, stereoParamsLM);
[pcmr, dmmr] = createPointCloud(image_middle, image_right, drange, sigma, stereoParamsMR);

%imshow(dmlm, [0, 128]);
%colormap jet;
%colorbar