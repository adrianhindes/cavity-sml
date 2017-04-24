reset
set xrange[0.01:100]
set logscale x
set xlabel "f [Hz] (sig1)"
set ylabel "dB "
set y2label "Phase [Deg] "
set y2tics nomirror
set my2tics 3
set ytics nomirror
set mxtics 2
set mytics 2
set zero 0.0
set title "pdh                Mon Mar  6 11:38:34 2017" offset 0, 2
set nolog y
set nolog y2
set term x11
set size ratio .5
set key below
set grid xtics ytics
 set title
plot\
'pdh.out' using ($1):($2) axes x1y1 title " n3 : dB  " w l lt 1 lw 2, \
'pdh.out' using ($1):($3) axes x1y2 title " n3 : Phase [Deg]  " w l lt 2 lw 2
