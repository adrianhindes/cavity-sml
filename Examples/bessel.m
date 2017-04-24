%----------------------------------------------------------------
% function [x,y] = bessel(noplot)
% Matlab function to plot Finesse output data
% Usage: 
%   [x,y] = bessel    : plots and returns the data
%   [x,y] = bessel(1) : just returns the data
%           bessel    : just plots the data
% Created automatically Mon Mar  6 11:38:09 2017
% by Finesse 2.1 (2.1-4-g71575b0), 06.02.2017
%----------------------------------------------------------------
function [x,y] = bessel(noplot)

data = load('bessel.out');
[rows,cols]=size(data);
x=data(:,1);
y=data(:,2:cols);
mytitle='bessel                Mon Mar  6 11:38:09 2017';
if (nargin==0)

figure('name','bessel');
plot(x, y(:,1), x, y(:,2), x, y(:,3));
legend('bessel1 n1', 'bessel2 n1', 'bessel3 n1');
set(gca, 'YScale', 'lin');
ylabel('Abs ');
set(gca, 'XLim', [0 10]);
xlabel('midx  (eo1)');
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
