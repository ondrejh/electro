#! /var/bin/python3

#local imports
import config
from utils import day_data_to_file, all_data_to_day_files

import os
import subprocess

#dstamp='20140623'
#wdir='C:\\GIT\\electro\\'
#scall = ('gnuplot -e "datestamp=\'{}\'" -e "workdir=\'{}\'" one_day_wattage.gp'.format(dstamp,wdir))
#print(scall)
#subprocess.call(scall,shell=True)

def gnuplot_day_file(filename):

    ''' it'll run gnuplot to create plot image from a day data file '''

    dstamp = os.path.basename(fname).split('_')[0]
    scall = ('gnuplot -e "datestamp=\'{}\'" -e "workdir=\'{}\'" one_day_wattage.gp'.format(dstamp,config.wdir))
    subprocess.call(scall,shell=True)

if os.path.isdir(config.wdir):

    #run again (last day data update only)
    fname = day_data_to_file(config.wdir)
    gnuplot_day_file(fname)

else:

    #run for the first time
    print('Energy monitor run for the first time:')

    #create workdir
    print('Create directory {} .. '.format(config.wdir),end='')
    os.mkdir(config.wdir)
    print(os.path.isdir(config.wdir))

    #generate all datafiles
    print('Generate day data files ..')
    fnames = all_data_to_day_files(config.wdir)
    print('Plot data into png files .. ',end='')
    for fname in fnames:
        gnuplot_day_file(fname)
    print('done')
