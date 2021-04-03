import time
import os
import argparse
from datetime import datetime
from csv import writer
from math import radians, cos, sin, asin, sqrt

import speedtest as sp


def haversine(lat1, lon1, lat2, lon2):

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956 #6371 Radius of earth in kilometers. Use 3956 for miles.
    distance = c * r

    return round(distance, 3)

def test():

    test = sp.Speedtest()

    ds = test.download()/1E6 # download speed
    us = test.upload()/1E6  # upload speed
    serv = test.get_best_server().get('id') # server id number
    s_lon = test.get_best_server().get('lon') # server longitude
    s_lat = test.get_best_server().get('lat') # server latitude
    name = test.get_best_server().get('name') # server municipal location

    return ds, us, serv, s_lon, s_lat, name

def append_test(src):

    try:
        # input client lon and lat .. default here is the White House lol
        h_lat = 38.897957
        h_lon = -77.036560
        ds, us, serv, s_lon, s_lat, name = test()
        hour = datetime.now().strftime('%H:%M')
        day = datetime.now().strftime('%Y%m%d')
        distance = haversine(h_lat, h_lon, float(s_lat), float(s_lon))

        row = [hour,day,f'{ds:0.2f}',f'{us:0.2f}',serv,name,s_lon,s_lat,distance]

        with open(src, 'a+') as f:
            csv_writer = writer(f)
            csv_writer.writerow(row)


    except Exception as e:
        print(e) # print exception for trouble shooting in case no connection

        ds = 0
        us = 0
        serv = 'None'
        hour = datetime.now().strftime('%H:%M')
        day = datetime.now().strftime('%Y%m%d')


        row = [hour,day,f'{ds:0.2f}',f'{us:0.2f}',serv]

        with open(src, 'a+') as f:
            csv_writer = writer(f)
            csv_writer.writerow(row)

def execute():
    print(opts)

    if opts.src is None:
        print('Data sheet not found or none specified please try again.')

    else:
        append_test(opts.src)

################################################################################

parser = argparse.ArgumentParser(description='Basic network speed monitor. Data exported to csv.')
parser.add_argument('--src', type=str, default=None, metavar='source', help='path to csv')
opts = parser.parse_args()


if __name__ == '__main__':

    today = datetime.now().strftime('%Y%m%d')
    begin = time.time()

    execute()

    fin = time.time() - begin
    print(f'Code completed in {fin:0.4f} seconds on {today}')
