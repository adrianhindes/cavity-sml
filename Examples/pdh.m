%----------------------------------------------------------------
% function [x,y] = pdh(noplot)
% Matlab function to plot Finesse output data
% Usage: 
%   [x,y] = pdh    : plots and returns the data
%   [x,y] = pdh(1) : just returns the data
%           pdh    : just plots the data
% Created automatically Mon Mar  6 11:38:34 2017
% by Finesse 2.1 (2.1-4-g71575b0), 06.02.2017
%----------------------------------------------------------------
function [x,y] = pdh(noplot)

data = load('pdh.out');
[rows,cols]=size(data);
x=data(:,1);
y=data(:,2:cols);
mytitle='pdh                Mon Mar  6 11:38:34 2017';
if (nargin==0)

figure('name','pdh');

h1=subplot(2,1,1);
plot(x, y(:,1));
legend(' n3');
set(gca, 'YScale', 'lin');
ylabel('dB ');
set(gca, 'XLim', [0.01 100]);
set(gca, 'XScale', 'log');
xlabel('f [Hz] (sig1)');
grid on;

h2=subplot(2,1,2);
plot(x, y(:,2));
legend(' n3');
ylabel('Phase [Deg] ');
set(gca, 'YScale', 'lin');
set(gca, 'XLim', [0.01 100]);
set(gca, 'XScale', 'log');
xlabel('f [Hz] (sig1)');
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
