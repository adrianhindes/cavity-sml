%----------------------------------------------------------------
% function [x,y] = quantum_noise(noplot)
% Matlab function to plot Finesse output data
% Usage: 
%   [x,y] = quantum_noise    : plots and returns the data
%   [x,y] = quantum_noise(1) : just returns the data
%           quantum_noise    : just plots the data
% Created automatically Mon Mar  6 11:38:45 2017
% by Finesse 2.1 (2.1-4-g71575b0), 06.02.2017
%----------------------------------------------------------------
function [x,y] = quantum_noise(noplot)

data = load('quantum_noise.out');
[rows,cols]=size(data);
x=data(:,1);
y=data(:,2:cols);
mytitle='quantum\_noise                Mon Mar  6 11:38:45 2017';
if (nargin==0)

figure('name','quantum_noise');
plot(x, y(:,1), x, y(:,2));
legend('NSR\_with\_RP nsrc2', 'NSR\_without\_RP nsrc2');
set(gca, 'YScale', 'log');
ylabel('Abs ');
set(gca, 'XLim', [5 5000]);
set(gca, 'XScale', 'log');
xlabel('f [Hz] (darm)');
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
