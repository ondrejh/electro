#! /var/bin/python3

''' this file contains functions calling gnuplot scripts '''

import config #workdir variable

import os, subprocess #filename functions and subprocess call
import datetime

def gnuplot_day_file(filename):

    ''' it'll run gnuplot to create plot image from a day data file '''

    dstamp = os.path.basename(filename).split('_')[0]
    d = datetime.date(int(dstamp[0:4]),int(dstamp[4:6]),int(dstamp[6:8]))
    d -= datetime.timedelta(days=1)
    dfilename = '{}/{:04}{:02}{:02}{}'.format(os.path.dirname(filename),d.year,d.month,d.day,os.path.basename(filename)[8:])
    #print(dfilename)
    if os.path.isfile(dfilename):
        #print('{},{}'.format(dfilename,filename))
        dstamp2 = os.path.basename(dfilename).split('_')[0]
        scall = ('gnuplot -e "dstamp=\'{}\'" -e "pre_dstamp=\'{}\'" -e "workdir=\'{}\'" two_day_wattage.gp'.format(dstamp,dstamp2,config.wdir))
    else:
        #print('{}'.format(filename))
        scall = ('gnuplot -e "datestamp=\'{}\'" -e "workdir=\'{}\'" one_day_wattage.gp'.format(dstamp,config.wdir))
    subprocess.call(scall,shell=True)

if __name__ == '__main__':
    gnuplot_day_file('{}20140623_day_data.txt'.format(config.wdir))
    
