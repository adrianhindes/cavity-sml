%----------------------------------------------------------------
% function [x,y,z] = 3D(noplot)
% Matlab function to plot Finesse output data
% Usage: 
% [x,y,z] = 3D    : plots and returns the data
% [x,y,z] = 3D(1) : just returns the data
%           3D    : just plots the data
% Created automatically Mon Mar  6 14:57:55 2017
% by Finesse 2.1 (2.1-4-g71575b0), 06.02.2017
%----------------------------------------------------------------
function [x,y,z] = 3D(noplot)

data = load('3D.out');
[rows,cols]=size(data);
X=data(:,1);
Y=data(:,2);
Z=data(:,3:cols);
[x,y,z]=convert3D(X,Y,Z);
mytitle='3D                Mon Mar  6 14:57:55 2017';
if (nargin==0)

figure('name','3D');
surfc(x,y,z(:,:,1),'EdgeColor','none');
%legend('inphase n3');
set(gca, 'ZScale', 'lin');
set(gca, 'YLim', [0.5 0.9]);
ylabel('r  (m2)');
zlabel('Abs ');
set(gca, 'XLim', [-80 80]);
xlabel('phi [deg] (m1)');
grid on;
colorbar;
title(mytitle);
end

switch nargout
 case {0}
  clear x y z;
 case {3}
 otherwise
  error('wrong number of outputs');
end

%---------------------------------------------------------------
% Utility function to convert Finesse 3D data into Matlab format
function [x,y,M]=convert3D(X,Y,Z)
[row,col]=size(Z);
nxp=length(find (Y(:)==Y(1)));
nyp=row/nxp;
y=Y(1:nyp);
x=X(1:nyp:row);
M=zeros(nyp,nxp,col);
for i=1:col
M(:,:,i)=reshape(Z(:,i),nyp,nxp);
end
