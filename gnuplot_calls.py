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

def run():
    #list data files in work directory
    files = os.listdir(config.wdir)

    #find highest index
    last_data_file = None
    for file in files:
        if file[8:]=='_day_data.txt':
            if last_data_file == None:
                last_data_file = file
            else:
                if int(file[:8])>int(last_data_file[:8]):
                    last_data_file = file

    #plot it
    if last_data_file!=None:
        gnuplot_day_file('{}{}'.format(config.wdir,last_data_file))
        #subprocess.call('mv -f {}*.png {}'.format(config.wdir,config.pdir),shell=True)
    else:
        print('No data file found!')

if __name__ == '__main__':
    run()
