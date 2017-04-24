reset
set xrange[-80:80]
set xlabel "phi [deg] (m1)"
set yrange[0.5:0.9]
set ylabel "r  (m2)"
set zlabel "Abs "
set mztics 10
set mxtics 2
set mytics 2
set zero 0.0
set title "3D                Mon Mar  6 14:57:55 2017" offset 0, 2
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
set view 70, 220, ,         # the 3D plot ...
set hidden3d
set pm3d at s hidden3d 100 solid
splot\
'3D.out' using ($1):($2):($3) title "inphase :  "  w l
