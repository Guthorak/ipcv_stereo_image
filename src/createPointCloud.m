function [pc, dm] = createPointCloud(left, right, drange, sigma, mask_to_use, stereo_parameters)
  [left, right, mask_l, mask_r] = preprocessImages(left, right, sigma, stereo_parameters);
  dm = disparity(left, right, ...
    'BlockSize', 5, ...
    'DisparityRange', drange, ...
    'Method', 'SemiGlobal',...
    'UniquenessThreshold', 15,...
    'DistanceThreshold', 15,...
    'ContrastThreshold', 0.7);
  % remove unreliable pixels
  %mask = mask_l | mask_r;
  if strcmp(mask_to_use, 'l')
    mask = mask_l;
  elseif strcmp(mask_to_use, 'r')
    mask = mask_r;
  elseif strmp(mask_to_use, 'both')
    mask = mask_l | mask_r;
  end
  unreliable = dm == -realmax('single') | (1 - mask);
  dm = dm .* (1 - unreliable);
  dm = medfilt2(dm);
  pc = reconstructScene(dm, stereo_parameters);
end
