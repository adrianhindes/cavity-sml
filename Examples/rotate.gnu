reset
set xrange[-5:5]
set xlabel "x [x/wx0] (b1)"
set yrange[-4e-05:4e-05]
set ylabel "xbeta [rad] (bs1)"
set zlabel "Abs "
set mztics 10
set mxtics 2
set mytics 2
set zero 0.0
set title "rotate                Sat Mar  4 20:41:36 2017" offset 0, 2
set nolog z
set term x11
set size ratio .5
set key below
set grid xtics ytics
 set title
set pm3d
set pm3d map
set pm3d interpolate 2,2
set hidden3d
set size square
set view 0, 0, ,
set nosurface
unset hidden3d
set colorbox v
set colorbox user origin .95,.1 size .04,.8
set style line 100 lt -1 lw 0	
set pm3d at b
#-----------------------Colors--------------------------------
# -- traditional pm3d (black-blue-red-yellow)
set palette rgbformulae 7,5,15
# -- green-red-violet
#set palette rgbformulae 3,11,6
# -- ocean (green-blue-white)  try also all other permutations
#set palette rgbformulae 23,28,3
# -- hot  (black-red-yellow-white)
#set palette rgbformulae 21,22,23
# --  colour printable on gray (black-blue-violet-yellow-white)
#set palette rgbformulae 30,31,32
# -- rainbow (blue-green-yellow-red)
#set palette rgbformulae 33,13,10
# -- AFM hot (black-red-yellow-white)
#set palette rgbformulae 34,35,36
#-------------------------------------------------------------
unset grid
splot\
'rotate.out' using ($1):($2):($3) title "b1 (wx0=10m, wy0=10m) :  "  w l
