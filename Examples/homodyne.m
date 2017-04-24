%----------------------------------------------------------------
% function [x,y] = homodyne(noplot)
% Matlab function to plot Finesse output data
% Usage: 
%   [x,y] = homodyne    : plots and returns the data
%   [x,y] = homodyne(1) : just returns the data
%           homodyne    : just plots the data
% Created automatically Mon Mar  6 11:38:19 2017
% by Finesse 2.1 (2.1-4-g71575b0), 06.02.2017
%----------------------------------------------------------------
function [x,y] = homodyne(noplot)

data = load('homodyne.out');
[rows,cols]=size(data);
x=data(:,1);
y=data(:,2:cols);
mytitle='homodyne                Mon Mar  6 11:38:19 2017';
if (nargin==0)

figure('name','homodyne');
plot(x, y(:,1), x, y(:,2));
legend('sqzd\_noise nout1', 'shot\_noise nout1');
set(gca, 'YScale', 'lin');
ylabel('Abs ');
set(gca, 'XLim', [-90 90]);
xlabel('phase [deg] (l1)');
grid on;
title(mytitle);
end

switch nargout
 case {0}
  clear x y;
 case {2}
 otherwise
  error('wrong number of outputs');
end
