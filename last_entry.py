#! /usr/bin/env python3

from dbconn import return_last_entry, get_raw_data

#run main if this is stand alone module
if __name__ == "__main__":
    #print(return_last_entry())
    print(get_raw_data(return_last_entry()))
