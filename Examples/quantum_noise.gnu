reset
set xrange[5:5000]
set logscale x
set xlabel "f [Hz] (darm)"
set ylabel "Abs "
set mxtics 2
set mytics 2
set zero 0.0
set title "quantum_noise                Mon Mar  6 11:38:45 2017" offset 0, 2
set log y
set format y "%g"
set term x11
set size ratio .5
set key below
set grid xtics ytics
 set title
plot\
'quantum_noise.out' using ($1):($2) axes x1y1 title "NSR_with_RP nsrc2 :  " w l lt 1 lw 2, \
'quantum_noise.out' using ($1):($3) axes x1y1 title "NSR_without_RP nsrc2 :  " w l lt 2 lw 2
