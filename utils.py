#! /usr/bin/env python3

from dbconn import last_entry_timestamp, first_entry_timestamp, return_data, get_raw_data

from datetime import datetime, timedelta, date, time

import sys


def print_raw_entry(entry):

    ''' print table item '''

    print('{}, '.format(str(entry[0])),end='')
    
    for c in entry[1:-1]:
        print('{}, '.format(str(c)),end='')

    print('{}'.format(str(entry[-1])))


def calculate_wattage(data):

    ''' calculate wattage form data list and append it to the data '''

    last_kwh = None
    last_dtm = None

    try:
        for e in data:
            if last_kwh == None:
                last_dtm = e[0]
                last_kwh = e[1]
            else:
                ddtm = e[0]-last_dtm
                dkwh = e[1]-last_kwh
                last_dtm = e[0]
                last_kwh = e[1]
                w = dkwh/(ddtm.total_seconds()/3600)
                e.append(w)
    except:
        pass


def day_data_to_file(workdir,day=None):

    ''' generate one day wattage text file '''

    # get datetime limits
    dt00 = datetime(2010,1,1,0,0,0)
    if day==None:
        lts = last_entry_timestamp()
        dt00 = datetime(lts.year,lts.month,lts.day,0,0,0)

    else:
        dt00 = datetime(day.year,day.month,day.day,0,0,0)
    dt24 = dt00 + timedelta(1,0,0)

    # get data from to
    data = get_raw_data(return_data(begin=dt00,end=dt24))
    calculate_wattage(data)

    if type(data)==list:
        fname = '{}{:04}{:02}{:02}_day_data.txt'.format(workdir,dt00.year,dt00.month,dt00.day)
        f = open(fname,'w')
        f.write('# time; p[kw]\n')
        for e in data[1:]:
            f.write('{:02}:{:02}; {:0.3f}\n'.format(e[0].hour,e[0].minute,e[2]))
        f.close()

        return fname

    return None


def all_data_to_day_files(workdir):

    ''' generate day wattage files from all data in db '''

    fts = first_entry_timestamp()
    lts = last_entry_timestamp()

    dt00 = datetime(fts.year,fts.month,fts.day,0,0,0)

    ret = []

    while dt00<=lts:

        day = date(dt00.year,dt00.month,dt00.day)
        r = day_data_to_file(workdir,day)

        if r!=None:
            print('{}'.format(r))
            ret.append(r)

        dt00 += timedelta(1,0,0)

    return ret
        

#run main if this is stand alone module
if __name__ == "__main__":

    ''' when running this file as standalone:
    it creates last day wattage data file or if --all
    argument found it creates wattage datafiles form all data'''

    workdir = '/root/electro/data/'

    files = []

    if (len(sys.argv)>1) and (sys.argv[1]=='--all'):
        files = all_data_to_day_files(workdir)
            
    else:
        files = day_data_to_file(workdir)
