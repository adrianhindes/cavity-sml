%----------------------------------------------------------------
% function [x,y] = cavity1(noplot)
% Matlab function to plot Finesse output data
% Usage: 
%   [x,y] = cavity1    : plots and returns the data
%   [x,y] = cavity1(1) : just returns the data
%           cavity1    : just plots the data
% Created automatically Sat Mar  4 20:41:22 2017
% by Finesse 2.1 (2.1-4-g71575b0), 06.02.2017
%----------------------------------------------------------------
function [x,y] = cavity1(noplot)

data = load('cavity1.out');
[rows,cols]=size(data);
x=data(:,1);
y=data(:,2:cols);
mytitle='cavity1                Sat Mar  4 20:41:22 2017';
if (nargin==0)

figure('name','cavity1');

h1=subplot(2,1,1);
plot(x, y(:,1));
legend(' ');
set(gca, 'YScale', 'lin');
ylabel('Abs ');
set(gca, 'XLim', [-50000 50000]);
xlabel('f [Hz] (i1)');
grid on;

h2=subplot(2,1,2);
plot(x, y(:,2));
legend(' ');
ylabel('Phase [Deg] ');
set(gca, 'YScale', 'lin');
set(gca, 'XLim', [-50000 50000]);
xlabel('f [Hz] (i1)');
grid on;

subplot(2,1,1);
title(mytitle);
end

switch nargout
 case {0}
  clear x y;
 case {2}
 otherwise
  error('wrong number of outputs');
end
