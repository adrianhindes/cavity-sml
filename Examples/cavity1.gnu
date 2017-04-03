reset
set xrange[-50000:50000]
set xlabel "f [Hz] (i1)"
set ylabel "Abs "
set y2label "Phase [Deg] "
set y2tics nomirror
set my2tics 3
set ytics nomirror
set mxtics 2
set mytics 2
set zero 0.0
set title "cavity1                Sat Mar  4 20:41:22 2017" offset 0, 2
set nolog y
set nolog y2
set term x11
set size ratio .5
set key below
set grid xtics ytics
 set title
plot\
'cavity1.out' using ($1):($2) axes x1y1 title "  : Abs  " w l lt 1 lw 2, \
'cavity1.out' using ($1):($3) axes x1y2 title "  : Phase [Deg]  " w l lt 2 lw 2
