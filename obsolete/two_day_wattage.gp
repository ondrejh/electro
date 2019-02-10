#! /usr/bin/gnuplot

# this script plots one day wattage from data file according to input arg datestamp
# input file (today data): YYYYMMDD_day_data.txt
# input file (yesterday data): YYYYMMDD_day_data.txt
# output file: YYYYMMDD_wattage.png
# usage: gnuplot -e "dstamp='YYYYMMDD'" -e "pre_dstamp='YYYYMMDD'" -e "workdir='/root/data/'" two_day_wattage.gp

if (!exists("workdir")) workdir=""

set xdata time
set style data lines
unset multiplot
# set title "Wattage over the 24 hours"
set term png size 800,400
set timefmt "%H:%M"
set format x "%H:%M"
# set xlabel "time"
set ylabel "p [ kW ]"
set autoscale y
set autoscale x
set output workdir.dstamp.'_wattage.png'
set datafile separator ";"
set grid
set style line 1 linecolor rgb 'red' linewidth 2.5
set style line 2 linecolor rgb 'dark-gray' linewidth 2.5
plot workdir.pre_dstamp.'_day_data.txt' using 1:2 t pre_dstamp[5:6].'.'.pre_dstamp[7:8] w lines linestyle 2, \
workdir.dstamp.'_day_data.txt' using 1:2 t dstamp[5:6].'.'.dstamp[7:8] w lines linestyle 1
