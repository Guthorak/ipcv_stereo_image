function pc = mergePointClouds(pc1, pc2, grid_step, stereo_params1, stereo_params2)
    %[~, pc2_transformed] = pcregistericp(pc1, pc2);
    tform1 = affine3d();
    tform1.T(1:3, 1:3) = stereo_params1.RotationOfCamera2;
    tform2 = affine3d();
    tform2.T(1:3, 1:3) = inv(stereo_params2.RotationOfCamera2);
    pc1_aligned = pctransform(pc1, tform1);
    pc2_aligned = pctransform(pc2, tform2);
    pc = pcmerge(pc1_aligned, pc2_aligned, grid_step);
end