# -*- coding: utf-8 -*-
import socket
import struct
import sys
import pickle
import json
import ast
import time
import os
from geopy.distance import geodesic

from pip._vendor.distlib.compat import raw_input

lat_to = -7.155029
long_to = 112.572189


port = 15000
nodeid='s3'
pesanDikirim = []

def getDistance(lat_from,long_from):
    coords_1 = (lat_from, long_from)
    coords_2 = (lat_to, long_to)
    return geodesic(coords_1, coords_2).km

def compareDistance(distance,distance_limit):
    if distance<distance_limit:
        return 1
    return 0

def multicast():
    multicast_group = '224.3.29.71'
    server_address = ('', port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(server_address)
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    while True:
        print('\nWaiting for messages')
        data, address = sock.recvfrom(1024)
        data = json.loads(data.decode('utf-8'))
        print('Received %s bytes from %s' % (len(data), address))
        pesan = data[0]
        destination = data[1]
        hop = data[2] + 1
        getSecond = time.time() - data[3]
        sock.sendto(b'ack', address)
        distance = getDistance(data[5],data[6])
        if(compareDistance(distance,data[9])==0):
            print('Pesan tidak dapat dikirim, jarak melebihi batas')
            break
        elif(hop > data[9]):
            print('Hop count: ' + str(hop))
            print('Hop count limit reached')
            break
        elif(data[1] == nodeid):
            print('Message : ' + pesan)
            print ('Last DTN node in the route')
            print ('Time elapsed: ' + str(data[4]))
            print ('Hop count: ' + str(hop))
            sock.sendto(b'ack', address)
            break
        send = sendMsg(pesan,destination,hop,data[3],data[4],data[5],data[6],data[7],data[8],data[9])
        if send==1:
            break


def sendMsg(message,dest,hop,timestamp, source, lat_from,long_from,hop_limit,time_limit,distance_limit):
    settime = timestamp
    timecek = 0
    pesanDikirim = [message, dest, hop, time.time(), source, lat_from, long_from, hop_limit, time_limit,distance_limit]
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
    return 1

def send(message,port):
    multicast_group = ('224.3.29.71', port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
            print ('Message has been sent')
            sock.close()
            return 1

if __name__ == '__main__':
    print("[Node ID " + str(nodeid) + "]")
    print("--------------------")
    print("1. Receive and deliver message to next node")
    print("2. Exit")
    while 1:
        print("\nYour choice?")
        pilihan = raw_input('>> ')
        if (pilihan == '1'):
            multicast()
        elif (pilihan == '2'):
            exit()