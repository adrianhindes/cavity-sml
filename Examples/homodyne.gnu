reset
set xrange[-90:90]
set xlabel "phase [deg] (l1)"
set ylabel "Abs "
set mxtics 2
set mytics 2
set zero 0.0
set title "homodyne                Mon Mar  6 11:38:19 2017" offset 0, 2
set nolog y
set format y "%g"
set term x11
set size ratio .5
set key below
set grid xtics ytics
 set title
plot\
'homodyne.out' using ($1):($2) axes x1y1 title "sqzd_noise nout1 :  " w l lt 1 lw 2, \
'homodyne.out' using ($1):($3) axes x1y1 title "shot_noise nout1 :  " w l lt 2 lw 2
