# -*- coding: utf-8 -*-
import socket
import struct
import sys
import os
import json
import pickle
import glob
import numpy
import operator
import time
import copy
import array
from geopy.distance import geodesic

from pip._vendor.distlib.compat import raw_input

lat_from = -7.294080
long_from = 112.801598
nodeid = 's0'
port = 12346

def sendMessage():
    message = raw_input("Message > ")
    dest = raw_input("Destination > ")
    hop_limit = int(raw_input("Hop Limit > "))
    time_limit = int(raw_input("Time Limit(s) > "))
    distance_limit = int(raw_input("Distance limit(km) > "))
    pesanDikirim = [message, dest, 0, time.time(), nodeid, lat_from, long_from, hop_limit, time_limit, distance_limit]
    settime = time.time()
    timecek = 0
    print('Sending message to nodeid ' + str(dest))
    hasil = send(pesanDikirim, port)
    while (timecek < time_limit):
        if hasil == 0:
            hasil = send(pesanDikirim, port)
        else:
            print('Message sent to nodeid ' + str(dest))
            break
        timecek = time.time() - settime
    if hasil == 0:
        print('Message lifetime limit reached, message will be deleted\n')
        exit()
        


def send(message,port):
    multicast_group = ('224.3.29.71', port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.2)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    sock.sendto(json.dumps(message).encode('utf8'), multicast_group)
    while True:
        try:
            sock.recvfrom(16)
        except:
            sock.close()
            return 0
        else:
            sock.close()
            return 1


def getDistance(lat_to,long_to):
    coords_1 = (lat_from, long_from)
    coords_2 = (lat_to, long_to)
    return geodesic(coords_1, coords_2).km

if __name__ == '__main__':
        print("[DTN Multicast: Node S]")
        print("--------------------")
        print("1. Create a new message")
        print("2. Exit")
        while 1:
            print("\nYour choice?")
            pilihan = raw_input(">> ")
            if (pilihan == '1'):
                sendMessage()
            elif (pilihan == '2'):
                exit()