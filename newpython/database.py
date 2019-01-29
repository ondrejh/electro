#! /usr/bin/python3

import sqlite3

#db_name = 'tariff.sql'
db_name = '/home/pi/data/tariff.sql'

readings_table = 'readings'


def store_tariff_reading(header, body, timestamp=None):

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    query = "CREATE TABLE IF NOT EXISTS readings (id INTEGER PRIMARY KEY, header TEXT, body TEXT, " + \
            "timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)"
    c.execute(query)
    if timestamp is None:
        query = "INSERT INTO '{}' (header, body) VALUES ('{}', '{}')".format(readings_table, header, body)
    else:
        query = "INSERT INTO {} (header, body, timestamp) VALUES ('{}', '{}', '{}')".format(readings_table, header,
                                                                                            body, timestamp)
    c.execute(query)
    query = "SELECT last_insert_rowid()"
    c.execute(query)
    i = c.fetchone()[0]

    conn.commit()
    conn.close()

    return i


def dump_readings():

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    query = "SELECT * FROM readings"
    c.execute(query)
    print(c.fetchall())

    conn.close()


if __name__ == "__main__":

    #i = store_tariff_reading('ahoj', 'vole')
    #print(i)

    dump_readings()
