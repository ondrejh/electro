#! /usr/bin/gnuplot

# this script plots one day wattage from data file according to input arg datestamp
# input file: YYYYMMDD_day_data.txt
# output file: YYYYMMDD_wattage.png
# usage: gnuplot -e "datestamp='YYYYMMDD'" -e "workdir='/root/data/'" one_day_wattage.gp

if (!exists("workdir")) workdir=""

if (exists("datestamp")) {
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
	set output workdir.datestamp.'_wattage.png'
	set datafile separator ";"
	set grid
	plot workdir.datestamp.'_day_data.txt' using 1:2 t datestamp[5:6].'.'.datestamp[7:8] w lines linewidth 2.5
}