function [left, right, mask_l, mask_r] = preprocessImages(left_img, right_img, stereo_params)
    [left, mask_l] = removeBackground(rgb2gray(left_img));
    [right, mask_r] = removeBackground(rgb2gray(right_img));
    [mask_l, mask_r] = rectifyStereoImages(mask_l, mask_r, stereo_params,...
                                           'OutputView', 'full');
    [left, right] = rectifyStereoImages(left, right, stereo_params,...
                                        'OutputView', 'full');
end