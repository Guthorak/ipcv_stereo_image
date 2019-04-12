function mesh = surfaceMeshFromPointCloud(pc, disparityMap, J1, res)
  unreliable = disparityMap == 0;
  %% Matlab code for creating a 3D surface mesh
  %% create a connectivity structure
  [M, N] = size(disparityMap);
  [nI,mI] = meshgrid(1:res:N,1:res:M);
  TRI = delaunay(nI(:),mI(:));
  indI = sub2ind([M,N],mI(:),nI(:));

  %% linearize the arrays and adapt to chosen resolution
  pcl = reshape(pc,N*M,3);
  % reshape to (N*M)x3
  J1l = reshape(J1,N*M,3);
  % reshape to (N*M)x3
  pcl = pcl(indI,:);
  % select 3D points that are on resolution grid
  J1l = J1l(indI,:);
  % select pixels that are on the resolution grid
  %% remove the unreliable points and the associated triangles
  ind_unreliable = find(unreliable(indI));% get the linear indices of unreliable 3D points
  imem = ismember(TRI(:), ind_unreliable); % find indices of references to unreliable points
  [ir, ~] = ind2sub(size(TRI), find(imem)); % get the indices of rows with refs to unreliable points.
  TRI(ir, :) = [];
  % dispose them
  iused = unique(TRI(:));
  % find the ind's of vertices that are in use
  used = zeros(length(pcl), 1);
  % pre-allocate
  used(iused) = 1;
  % create a map of used vertices
  map2used = cumsum(used);
  % conversion table from indices of old vertices to the new one
  pcl = pcl(iused,:);
  % remove the unused vertices
  J1l = J1l(iused,:);
  TRI = map2used(TRI);
  % update the ind's of vertices
  %% create the 3D mesh
  mesh = triangulation(TRI,double(pcl));
end
