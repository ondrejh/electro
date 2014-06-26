#! /var/bin/python3

''' this file contains functions calling gnuplot scripts '''

import config #workdir variable

import os, subprocess #filename functions and subprocess call

def gnuplot_day_file(filename):

    ''' it'll run gnuplot to create plot image from a day data file '''

    dstamp = os.path.basename(filename).split('_')[0]
    scall = ('gnuplot -e "datestamp=\'{}\'" -e "workdir=\'{}\'" one_day_wattage.gp'.format(dstamp,config.wdir))
    subprocess.call(scall,shell=True)
