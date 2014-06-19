#! /usr/bin/env python3

from dbconn import return_last_entry, return_data, get_raw_data

from datetime import datetime, timedelta


def print_raw_entry(entry):

    print('{}, '.format(str(entry[0])),end='')
    
    for c in entry[1:-1]:
        print('{}, '.format(str(c)),end='')

    print('{}'.format(str(entry[-1])))


def calculate_wattage(data):

    last_kwh = None
    last_dtm = None
    
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
        

#run main if this is stand alone module
if __name__ == "__main__":

    #last entry
    print('Last entry:')
    e = get_raw_data(return_last_entry())
    print_raw_entry(e)

    # get data to with interval
    #data = get_raw_data(return_data(end=datetime(2014,6,19,19,0,0),interval=timedelta(0,3600*2,0)))
    # get data from with interval
    #data = get_raw_data(return_data(begin=datetime(2014,6,19,16,0,0),interval=timedelta(0,3600*3)))
    # get data from to
    #data = get_raw_data(return_data(begin='2014-06-18 16:00:00',end='2014-06-18 17:30:00'))
    # get last data in interval
    data = get_raw_data(return_data(interval=timedelta(0,3600*24,0)))
    # all data
    #data = get_raw_data(return_data())
    print('Data:')
    calculate_wattage(data)
    for e in data:
        print_raw_entry(e)
        #print(e)

    f = open('dump.txt','w')
    f.write('# time; p[kw]\n')
    for e in data[1:]:
        f.write('{}; {:0.3f}\n'.format(e[0],e[2]))
    f.close
