function [left, right, mask] = preprocessImages(left_img, right_img, stereo_params)
    [left, right] = rectifyStereoImages(rgb2gray(left_img), rgb2gray(right_img), stereo_params,...
                                        'OutputView', 'valid');
    [left, mask] = removeBackground(left);
    [right, ~] = removeBackground(right);
end