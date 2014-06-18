#! /usr/bin/env python3

''' Program for reading data out of the tariff device and writing it into the database:

Requirements:
It assumes there is MySQL database present on "localhost" with "root" user
and "1234" password (it can be changed in settings below).
The database "energy" with table "error" with columns "id","tstamp","errorlog"
and table "logdata" with columns "id","tstamp","logdata".
The module "pymysql" should be installed.
(https://github.com/PyMySQL/PyMySQL).

Raspberry Pi database install:

sudo apt-get install mysql-server mysql-client

More details about database setting:

start mysql:

    #mysql -u root -p

create database and jump in it:

    mysql> create database energy;
    mysql> use energy;

create tables:

    mysql> create table error (tstamp timestamp, errorstr text);
    mysql> create table logdata (tstamp timestamp, ident text, data text, checksum text);

close mysql:

    exit


using rpi cron table to run scrip every 5 minutes:

sudo crontab -e

add to the last line: */5 * * * * python3 /home/pi/electro/dbconn.py
    
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

def make_new_entry():

    ''' Open table '''
    #connect to db
    conn = pymysql.connect(host=db_host,user=db_user,passwd=db_pass)
    conn.autocommit(True)
    cur = conn.cursor()

    ''' Get data from tariff device '''
    try:
        answ = electro.get_data_silent(portname)
        split_answ = electro.split_data_block(electro.join_listofbytes(answ))
        cur.execute('''insert into {}.{} (ident,data,checksum) values ("{}","{}","{}");'''.format(db_name,db_logdatatable,split_answ[0],split_answ[1],split_answ[2]))
    except Exception as e:
        cur.execute('''insert into {}.{} (error) value ("{}")'''.format(db_name,db_errortable,str(e)))

    #close db
    cur.close()
    conn.close()

def return_last_entry():

    ''' Open table '''
    #connect to db
    conn = pymysql.connect(host=db_host,user=db_user,passwd=db_pass)
    conn.autocommit(True)
    cur = conn.cursor()

    ''' Get last entry timestamp '''
    cur.execute('''select max(tstamp) from {}.{}'''.format(db_name,db_logdatatable))
    lts = cur.fetchall()[0][0]
    cur.execute('''select * from {}.{} where tstamp = "{}"'''.format(db_name,db_logdatatable,lts))
    lts = cur.fetchall()[0]
    return(lts)

#run main if this is stand alone module
if __name__ == "__main__":
    make_new_entry()
