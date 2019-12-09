# -*- coding: utf-8 -*-
import socket
import struct
import sys
import pickle
import json
import ast
import time
import os

from pip._vendor.distlib.compat import raw_input

lat_to = -7.265441
long_to = 112.797661


port = 12003
time_limit = 30
hop_limit = 2
pesanDikirim = []

def sendLocation():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(20)
    client.connect(('10.151.254.214', 35))
    data = {
        'port' : port,
        'lat' : lat_to,
        'long' : long_to
    }
    client.send(pickle.dumps(data))
    print('Location has been sent')
    return client.close()

def multicast():
    multicast_group = '224.3.29.71'
    server_address = ('', port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
        
        rute = data[1]
        hop = data[2] + 1
        getSecond = time.time() - data[3]
        timestamp = time.time()
        duration = data[4] + getSecond
        sock.sendto(b'ack', address)
        if(hop > hop_limit):
            print('Hop count: ' + str(hop))
            print('Hop count limit reached')
            exit()
        print('Message : ' + pesan)
        if not data[1]:
            sock.sendto(b'ack', address)
            print ('Last DTN node in the route')
            print ('Time elapsed: ' + str(data[4]))
            print ('Hop count: ' + str(hop))
            exit()

        sendMsg(pesan,rute,hop,data[3],duration)

def sendMsg(pesan,rute,hop,timestamp,duration):
    p = rute[0][0]
    del rute[0]
    pesanDikirim.insert(0,pesan)
    pesanDikirim.insert(1,rute)
    pesanDikirim.insert(2,hop)
    pesanDikirim.insert(3,timestamp)
    settime = timestamp
    timecek = 0
    pesanDikirim.insert(4, timecek)
    print('Sending message to port ' + str(p))
    hasil = send(pesanDikirim, p)
    while (timecek < time_limit):
        if hasil == 0:
            pesanDikirim.insert(4,timecek)
            hasil = send(pesanDikirim, p)
        else:
            print('Message sent to port ' + str(p))
            break
        timecek = time.time() - settime
    if hasil == 0:
        print('Message lifetime limit reached, message will be deleted\n')
        exit()
    else:
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
            print ('Message has been sent')
            sock.close()
            return 1

if __name__ == '__main__':
    print("[Receiver port " + str(port) + "]")
    print("--------------------")
    print("1. Send node location")
    print("2. Receive and deliver message to next node")
    print("3. Exit")
    while 1:
        print("\nYour choice?")
        pilihan = raw_input('>> ')
        if (pilihan == '1'):
            sendLocation()
        elif (pilihan == '2'):
            multicast()
        elif (pilihan == '3'):
            exit()