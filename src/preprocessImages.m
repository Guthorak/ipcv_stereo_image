function [left, right, mask_l, mask_r] = preprocessImages(left_img, right_img, sigma, stereo_params)

    [left, mask_l] = removeBackground(imgaussfilt(rgb2gray(left_img), sigma));
    [right, mask_r] = removeBackground(imgaussfilt(rgb2gray(right_img), sigma));
    [mask_l, mask_r] = rectifyStereoImages(mask_l, mask_r, stereo_params,...
                                           'OutputView', 'full');
    [left, right] = rectifyStereoImages(left, right, stereo_params,...
                                        'OutputView', 'full');
end