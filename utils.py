#! /usr/bin/python3

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
    last_t1_kwh = None
    last_t2_kwh = None

    try:
    #if True:
        for e in data:
            if last_kwh == None:
                last_dtm = e[0]
                last_kwh = e[1]
                last_t1_kwh = e[2]
                last_t2_kwh = e[3]
            else:
                ddtm = e[0]-last_dtm
                dkwh = e[1]-last_kwh
                dt1kwh = e[2]-last_t1_kwh
                dt2kwh = e[3]-last_t2_kwh
                last_dtm = e[0]
                last_kwh = e[1]
                last_t1_kwh = e[2]
                last_t2_kwh = e[3]
                w = dkwh/(ddtm.seconds/3600)#total_seconds()/3600)
                wt1 = dt1kwh/(ddtm.seconds/3600)#total_seconds()/3600)
                wt2 = dt2kwh/(ddtm.seconds/3600)#total_seconds()/3600)
                e.append(w)
                e.append(wt1)
                e.append(wt2)
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
    #print(data)	

    if type(data)==list:
        fname = '{}{:04}{:02}{:02}_day_data.txt'.format(workdir,dt00.year,dt00.month,dt00.day)
        f = open(fname,'w')
        f.write('# time; p[kw]; t1[kw]; t2[kw]\n')
        for e in data[1:]:
            f.write('{:02}:{:02}; {:0.3f}; {:0.3f}; {:0.3f}\n'.format(e[0].hour,e[0].minute,e[4],e[5],e[6]))
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

    day_data_to_file('/home/ondrej/',date(2015,12,2))
    #workdir = '/home/ondrej/energy_data/'

    #files = []

    #if (len(sys.argv)>1) and (sys.argv[1]=='--all'):
    #    files = all_data_to_day_files(workdir)
            
    #else:
    #    files = day_data_to_file(workdir)

