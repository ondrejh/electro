#! /usr/bin/python3

import sqlite3
from utils import get_kwh_values

#db_name = 'tariff.sql'
db_name = '/home/pi/data/tariff.sql'

readings_table = 'readings'


def store_tariff_reading(header, body, timestamp=None):

    """ save one reading into database
    :arg header .. reading header
    :arg body .. reading body
    :arg timestamp .. timestamp of reading, if None current timestamp used (recommended)
    :return id of just added db row """

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


def dump_readings(db=db_name):

    """ read whole readings table
    :arg db, if not set default db used
    :return list of readings """

    conn = sqlite3.connect(db)
    c = conn.cursor()

    query = "SELECT * FROM readings"
    c.execute(query)
    data = c.fetchall()

    conn.close()
    return data


def update_id(idn, header=None, body=None, timestamp=None, db=db_name, conn_name=None):

    """ update column in reading table
    :arg idn .. row id
    :arg header .. header data to update, if not set keep current value
    :arg body .. body data to update, if not set keep current value
    :arg timestamp .. timestamp data do update, if not set keep current value
    :arg db .. database name to write to, if not set default database is used
    :arg conn_name .. open connector name, if not set open new with db_name """

    conn = conn_name
    if conn is None:
        conn = sqlite3.connect(db)

    c = conn.cursor()

    upd = []
    if header is not None:
        upd.append("header = '{}'".format(header))
    if body is not None:
        upd.append("body = '{}'".format(body))
    if timestamp is not None:
        upd.append("timestamp = '{}'".format(timestamp))
    if len(upd) > 0:
        query = "UPDATE {} SET {}".format(readings_table, upd[0])
        if len(upd) > 1:
            for u in upd[1:]:
                query += ', {}'.format(u)
        query += " WHERE id={}".format(idn)
        print(query)
        c.execute(query)
        if conn_name is None:
            conn.commit()

    if conn_name is None:
        conn.close()


if __name__ == "__main__":

    db = db_name
    update = False
    import sys
    if len(sys.argv) > 1:
        db = sys.argv[1]

    data = dump_readings(db=db)

    for d in data:
        v = get_kwh_values(d[2])
        print('{} {} {}'.format(d[0], d[3], '{:.03f} {:.03f} {:.03f}'.format(v[0], v[1], v[2])))
