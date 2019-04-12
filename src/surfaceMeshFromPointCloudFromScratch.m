function mesh = surfaceMeshFromPointCloudFromScratch(pointCloud, image, meshGridStep)
    %% Create 2D Mesh
    coordinates = pointCloud.Location;
    xCoordinates = coordinates(:, 1);
    yCoordinates = coordinates(:, 2);
    zCoordinates = coordinates(:, 3);
    connectivityList = delaunay(double(xCoordinates), double(yCoordinates));
    
    trisurf(connectivityList, xCoordinates, yCoordinates, zCoordinates, pointCloud.Color);
    
    
end