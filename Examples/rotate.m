%----------------------------------------------------------------
% function [x,y,z] = rotate(noplot)
% Matlab function to plot Finesse output data
% Usage: 
% [x,y,z] = rotate    : plots and returns the data
% [x,y,z] = rotate(1) : just returns the data
%           rotate    : just plots the data
% Created automatically Sat Mar  4 20:41:36 2017
% by Finesse 2.1 (2.1-4-g71575b0), 06.02.2017
%----------------------------------------------------------------
function [x,y,z] = rotate(noplot)

data = load('rotate.out');
[rows,cols]=size(data);
X=data(:,1);
Y=data(:,2);
Z=data(:,3:cols);
[x,y,z]=convert3D(X,Y,Z);
mytitle='rotate                Sat Mar  4 20:41:36 2017';
if (nargin==0)

figure('name','rotate');
surfc(x,y,z(:,:,1),'EdgeColor','none');
%legend('b1 n4 (wx0=10m, wy0=10m)');
set(gca, 'ZScale', 'lin');
set(gca, 'YLim', [-4e-05 4e-05]);
ylabel('xbeta [rad] (bs1)');
zlabel('Abs ');
set(gca, 'XLim', [-5 5]);
xlabel('x [x/wx0] (b1)');
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
