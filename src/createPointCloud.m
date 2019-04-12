function [pc, dm] = createPointCloud(left_img, right_img, drange, sigma, mask_to_use, texture_to_use, stereo_parameters)
  [left, right, mask_l, mask_r] = preprocessImages(left_img, right_img, sigma, stereo_parameters);
  dm = disparity(left, right, ...
    'BlockSize', 5, ...
    'DisparityRange', drange, ...
    'Method', 'SemiGlobal',...
    'UniquenessThreshold', 15,...
    'DistanceThreshold', 15,...
    'ContrastThreshold', 0.7);
  % remove unreliable pixels
  if strcmp(mask_to_use, 'l')
    mask = mask_l;
  elseif strcmp(mask_to_use, 'r')
    mask = mask_r;
  elseif strcmp(mask_to_use, 'both')
    mask = mask_l | mask_r;
  end
  unreliable = dm == -realmax('single') | (1 - mask);
  dm = dm .* (1 - unreliable);
  % rectify colored images for color
  [left_rect, right_rect] = rectifyStereoImages(left_img, right_img, stereo_parameters,...
                                                'OutputView', 'full');
  if strcmp(texture_to_use, 'l')
    texture = left_rect;
  elseif strcmp(texture_to_use, 'r')
    texture = right_rect;
  end
  pc = pointCloud(reconstructScene(dm, stereo_parameters), 'Color', texture);
end
