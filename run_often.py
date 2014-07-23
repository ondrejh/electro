#! /usr/bin/python3

#local imports
import config
from utils import day_data_to_file, all_data_to_day_files
import dbconn
from gnuplot_calls import gnuplot_day_file

#standard imports
import os
import subprocess



if __name__ == '__main__':

    #call dbconn to fetch data and store in into DB
    dbconn.make_new_entry()


    #test if working data directory exists
    if os.path.isdir(config.wdir):

        #exists: last day data update only
        
        fname = day_data_to_file(config.wdir)
        subprocess.call('echo "{}" >> log.txt'.format(fname))
        gnuplot_day_file(fname)

    else:

        #doesn't exist:
        
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


    #test if plot directory exists
    if os.path.isdir(config.pdir):

        #move all .png file into it

        subprocess.call('mv -f {}*.png {}'.format(config.wdir,config.pdir),shell=True)
