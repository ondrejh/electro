#! /usr/bin/env python3

''' Program for reading data out of the tariff device and writing it into the database:

Requirements:
It assumes there is MySQL database present on "localhost" with "root" user
and "1234" password (it can be changed in settings below).
The database "energy" with table "error" with columns "id","tstamp","errorlog"
and table "logdata" with columns "id","tstamp","logdata".
The module "pymysql" should be installed.
(https://github.com/PyMySQL/PyMySQL).


1) Raspberry Pi database install:

sudo apt-get install mysql-server mysql-client


2) More details about database settings:

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


3) Install PyMySQL to rpi:

... need to try again ...


4) Using rpi cron table to run scrip every 5 minutes:

run crontab editor (root user):

    sudo crontab -e

insert into the last line:

    */5 * * * * python3 /home/pi/electro/dbconn.py

    CTRL+O to save, CTRL+X to exit


5) Backup and restore database:

backup into file:

    mysqldump -u root -p1234 --add-drop-database energy backup_file.sql

restore from file:

    mysql -u root -p1234 energy < backup_file.sql
    
'''


import pymysql
from time import sleep
import electro
import datetime

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
    ret = cur.fetchall()[0]
    return(ret)

def return_data():

    ''' Open table '''
    #connect to db
    conn = pymysql.connect(host=db_host,user=db_user,passwd=db_pass)
    conn.autocommit(True)
    cur = conn.cursor()

    ''' Get last entry timestamp '''
    cur.execute('''select * from {}.{}'''.format(db_name,db_logdatatable))
    ret = cur.fetchall()
    return(ret)

def get_raw_data(entry):

    ''' return [datetime,value] if one entry input
    or list [[dtm0,val0],[dtm1,val1]..[dtmN,valN]] if more entries in list input '''

    if type(entry[0])!=datetime.datetime:

        #it's probably not an entry'
        if type(entry[0][0])==datetime.datetime:
            ret = []
            for e in entry:
                dtm = e[0]
                kwh = electro.get_total_kwh(e[2])
                ret.append([dtm,kwh])
            return(ret)

        #not even one entry or list of it
        return([])

    #one entry conversion
    dtm = entry[0]
    kwh = electro.get_total_kwh(entry[2])
    return([dtm,kwh])

#run main if this is stand alone module
if __name__ == "__main__":
    make_new_entry()
