#! /usr/bin/python3

import sqlite3
from database import dump_readings, update_id, db_name


if __name__ == "__main__":

    db_name = db_name

    import sys

    if len(sys.argv) > 1:

        db_name = sys.argv[1]

    data = dump_readings(db_name)

    conn = None

    for d in data:
        header = None
        body = None
        d1strip = d[1].strip()
        if d1strip != d[1]:
            header = d1strip
        d2strip = d[2].strip()
        if d2strip != d[2]:
            body = d2strip
        if (header is not None) or (body is not None):
            if conn is None:
                print("Open database file {}".format(db_name))
                conn = sqlite3.connect(db_name)
            update_id(d[0], header=header, body=body, conn_name=conn)

    if conn is not None:
        print("Commit and close")
        conn.commit()
        conn.close()
