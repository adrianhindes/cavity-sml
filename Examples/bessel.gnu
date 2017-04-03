reset
set xrange[0:10]
set xlabel "midx  (eo1)"
set ylabel "Abs "
set mxtics 2
set mytics 2
set zero 0.0
set title "bessel                Mon Mar  6 11:38:09 2017" offset 0, 2
set nolog y
set term x11
set size ratio .5
set key below
set grid xtics ytics
 set title
plot\
'bessel.out' using ($1):($2) axes x1y1 title "bessel1 n1 :  " w l lt 1 lw 2, \
'bessel.out' using ($1):($3) axes x1y1 title "bessel2 n1 :  " w l lt 2 lw 2, \
'bessel.out' using ($1):($4) axes x1y1 title "bessel3 n1 :  " w l lt 3 lw 2
