#! /usr/bin/env python3

''' Program for reading data out of the tariff device and writing it into the database:

Requirements:
It assumes there is MySQL database present on "localhost" with "root" user
and "1234" password (it can be changed in settings below).
The database "energy" with table "error" with columns "id","tstamp","errorlog"
and table "logdata" with columns "id","tstamp","logdata".
The module "pymysql" should be installed.
(https://github.com/PyMySQL/PyMySQL).

More details about database setting:

start mysql:

    #mysql -u root -p

create database and jump in it:

    mysql> create database energy;
    mysql> use energy;

create tables:

    mysql> create table error (id int, tstamp timestamp, errorstr text, PRIMARY KEY (id));
    mysql> create table logdata (id int, tstamp timestamp, ident text, data text, checksum text, PRIMARY KEY (id));

close mysql:

    exit
    
'''


import pymysql
from time import sleep
import electro

#tariff device settings
portname = '/dev/ttyAMA0'

#database settings
db_host  = 'localhost'
db_user  = 'root'
db_pass  = '1234'
db_name  = 'energy'
db_errortable = 'error'
db_logdatatable = 'logdata'

def main():

    ''' Open table '''
    #connect to db
    conn = pymysql.connect(host=db_host,user=db_user,passwd=db_pass)
    conn.autocommit(True)
    cur = conn.cursor()

    ''' Get data from tariff device '''
    try:
        answ = electro.get_data(portname)
        split_answ = electro.split_data_block(electro.join_listofbytes(answ))
        cur.execute('''insert into logdata (ident data checksum) values (split_answ[0],split_answ[1],split_answ[2]);''')
    except Exception as e:
        cur.execute('''insert into logdata (error) values ("{}")'''.format(str(e)))
    

    #first write
    cur.execute('''UPDATE {}.{} SET request='', status='STARTING', tstamp=current_timestamp;'''.format(db_name,db_table))

    while True:

        #read test table
        cur.execute('SELECT * FROM {}.{}'.format(db_name,db_table))
        testdb = cur.fetchall()[0]

        #check if stop request .. if not, update timestamp
        if testdb[0]=='STOP':
            #say 'stopped' and break the loop
            cur.execute('''UPDATE {}.{} SET request='', status='STOPPED';'''.format(db_name,db_table))
            break
        else:
            #say 'running' and update timestamp
            cur.execute('''UPDATE {}.{} SET status='RUNNING', tstamp=current_timestamp;'''.format(db_name,db_table))

        #wait a while
        sleep(5)

    #close db
    cur.close()
    conn.close()

#run main if this is stand alone module
if __name__ == "__main__":
    main()