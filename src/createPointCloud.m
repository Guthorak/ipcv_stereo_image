function [pc, dm] = createPointCloud(left, right, drange, sigma, stereo_parameters)
  [left, right, mask_l, mask_r] = preprocessImages(left, right, sigma, stereo_parameters);
  dm = disparity(left, right, ...
    'BlockSize', 15, ...
    'DisparityRange', drange, ...
    'Method', 'SemiGlobal',...
    'UniquenessThreshold', 15,...
    'DistanceThreshold', 15,...
    'ContrastThreshold', 0.7);
  % remove unreliable pixels
  mask = mask_l | mask_r;
  unreliable = dm == -realmax('single') | (1 - mask);
  dm = dm .* (1 - unreliable);
  %dm = medfilt2(dm);
  figure;
  imshow(dm, drange);
  colormap(gca, jet);
  colorbar
  pc = reconstructScene(dm, stereo_parameters);
end
