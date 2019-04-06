function out = removeBackground(image)
	% detect the face edges
	edges = findFaceContour(image);
	% make edges fully connected
	se = strel('diamond', 5);
	edges = imclose(edges, se);
	% remove everything but the face
	mask = imfill(edges, 'holes');
	out = uint8(image) .* uint8(mask);
  out(find(out == 0)) = NaN;
end


function edges = findFaceContour(image)
	edges = ut_edge(image, 'c', 'h', 's', 2);
end
