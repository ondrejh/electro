#! /usr/bin/env python3

from dbconn import last_entry_timestamp, first_entry_timestamp, return_data, get_raw_data

from datetime import datetime, timedelta, date, time


def print_raw_entry(entry):

    print('{}, '.format(str(entry[0])),end='')
    
    for c in entry[1:-1]:
        print('{}, '.format(str(c)),end='')

    print('{}'.format(str(entry[-1])))


def calculate_wattage(data):

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

        return [fname,len(data[1:])]

    return None

def all_data_to_day_files(workdir):

    fts = first_entry_timestamp()
    lts = last_entry_timestamp()

    dt00 = datetime(fts.year,fts.month,fts.day,0,0,0)

    while dt00<=lts:

        day = date(dt00.year,dt00.month,dt00.day)
        ret = day_data_to_file(workdir,day)

        if ret!=None:
            print('{} .. {} items'.format(ret[0],ret[1]))

        dt00 += timedelta(1,0,0)
        

#run main if this is stand alone module
if __name__ == "__main__":

    '''#last entry
    print('Last entry:')
    e = get_raw_data(return_last_entry())
    print_raw_entry(e)

    dt00=datetime(e[0].year,e[0].month,e[0].day,0,0,0)
    dt24=dt00+timedelta(1,0,0)

    # get data to with interval
    #data = get_raw_data(return_data(end=datetime(2014,6,19,19,0,0),interval=timedelta(0,3600*2,0)))
    # get data from with interval
    #data = get_raw_data(return_data(begin=datetime(2014,6,19,16,0,0),interval=timedelta(0,3600*3)))
    # get data from to
    data = get_raw_data(return_data(begin=dt00,end=dt24))
    # get last data in interval
    #data = get_raw_data(return_data(interval=timedelta(0,3600*24,0)))
    # all data
    #data = get_raw_data(return_data())
    print('Data:')
    calculate_wattage(data)
    for e in data:
        print_raw_entry(e)
        #print(e)

    fname = '{:04}{:02}{:02}_day_data.txt'.format(e[0].year,e[0].month,e[0].day)
    f = open(fname,'w')
    f.write('# time; p[kw]\n')
    for e in data[1:]:
        f.write('{:02}:{:02}; {:0.3f}\n'.format(e[0].hour,e[0].minute,e[2]))
    f.close()'''

    all_data_to_day_files('/root/electro/data/')
    #day_data_to_file('/root/electro/data/')
