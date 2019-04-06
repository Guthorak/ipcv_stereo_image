function plotSurfaceMesh(TR, J1l)
  %% visualize
  figure;
  TM = trimesh(TR);
  set(TM,'FaceVertexCData',J1l);
  set(TM,'Facecolor','interp');
  % set(TM,'FaceColor','red');
  set(TM,'EdgeColor','none');
  xlabel('x (mm)')
  ylabel('y (mm)')
  zlabel('z (mm)')
  axis([-250 250 -250 250 400 900])
  set(gca,'xdir','reverse')
  set(gca,'zdir','reverse')
  daspect([1,1,1])
  axis tight
end
