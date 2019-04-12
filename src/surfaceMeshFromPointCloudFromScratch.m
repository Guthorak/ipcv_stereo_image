function kaas = surfaceMeshFromPointCloudFromScratch(pointCloud, texture)
    %% Create 2D Mesh
    coordinates = pointCloud.Location;
    xCoordinates = coordinates(:, 1);
    yCoordinates = coordinates(:, 2);
    zCoordinates = coordinates(:, 3);
%     connectivityList = delaunay(double(xCoordinates), double(yCoordinates));

%     trisurf(connectivityList, xCoordinates, yCoordinates, zCoordinates, 'FaceColor', 'interp', 'EdgeColor', 'none');
    
    
    F = scatteredInterpolant(double(xCoordinates), double(yCoordinates), double(zCoordinates), 'natural', 'nearest');
    x = linspace(min(xCoordinates), max(xCoordinates), 1024);
    y = linspace(min(yCoordinates), max(yCoordinates), 1024);
    [X, Y] = meshgrid(x, y);
    Z = F(double(X), double(Y));
    
%     surf(X, Y, Z, 'EdgeColor', 'none', 'FaceLighting', 'gouraud');
    warp(X, Y, Z, texture);
end