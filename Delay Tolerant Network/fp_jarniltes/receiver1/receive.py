# -*- coding: utf-8 -*-
import socket
import struct
import sys
import json
import pickle
import ast
import time
import os
from geopy.distance import geodesic
from pip._vendor.distlib.compat import raw_input

lat_to = -7.228549
long_to = 112.731391
ip_addr = '192.168.1.1'
port = 10000
time_limit = 30
hop_limit = 4
pesanDikirim = []

def getDistance(lat_from,long_from):
    coords_1 = (lat_from, long_from)
    coords_2 = (lat_to, long_to)
    return geodesic(coords_1, coords_2).km

def multicast():
    MCAST_GRP = '224.3.29.71'
    IS_ALL_GROUPS = True

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if IS_ALL_GROUPS:
        # on this port, receives ALL multicast groups
        sock.bind(('', port))
    else:
        # on this port, listen ONLY to MCAST_GRP
        sock.bind((MCAST_GRP, port))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    while True:
        print('\nwaiting to receive message')
        data = sock.recv(1024)
        data = json.loads(data.decode('utf-8'))
        pesan = data[0]
        print('message : ' + pesan)
        jarak = getDistance(data[1], data[5])
        print('jarak dari Source :' + str(jarak))
        hop = data[2] + 1
        getSecond = time.time() - data[3]
        duration = data[4] + getSecond
        if(jarak>30):
            print("Pesan tidak bisa dikirim karena terlalu jauh");
            exit()
        elif(data[2] > hop_limit):
            print('jumlah hop : ' + str(hop))
            print('hop telah melebihi limit')
            exit()
        elif(data[6]==ip_addr):
            print("Pesan sampai")
            print("Message : " + pesan)
            print("Source : " + data[7])
            print("Destination : " + data[6])
            print("Hop : " + str(data[2]))
            exit()
        else:
            sendMsg(pesan,data[1],hop,data[3],duration,data[5],data[6],data[7])

def sendMsg(pesan,lat_from,hop,timestamp,duration,long_from,dest,source):
    pesanDikirim.insert(0, pesan)
    pesanDikirim.insert(1, lat_from)
    # hop
    pesanDikirim.insert(2, hop+1)
    pesanDikirim.insert(3, timestamp)
    # durasi kirim
    pesanDikirim.insert(4, 0)
    pesanDikirim.insert(5, long_from)
    pesanDikirim.insert(6, dest)
    pesanDikirim.insert(7, source)
    print('mengirimkan pesan')
    send(pesanDikirim)

def send(message):
    multicast_group = ('224.3.29.71', port)
    # regarding socket.IP_MULTICAST_TTL
    # ---------------------------------
    # for all packets sent, after two hops on the network the packet will not
    # be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
    MULTICAST_TTL = 2

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
    sock.sendto(json.dumps(message).encode('utf8'), multicast_group)
    print('send')
    time.sleep(1)

if __name__ == '__main__':
    print("receiver port " + str(port) + ": ")
    print("==============")
    while 1:
        print("1. menerima pesan dan mengirimkan ke node selanjutnya")
        print("2. keluar")
        pilihan = raw_input('Pilihan > ')
        if (pilihan == '1'):
            multicast()
        elif (pilihan == '2'):
            exit()
        elif (pilihan == 'help'):
            print("Pilihan yang tersedia:")
            print("1. Terima dan lanjutkan pengiriman pesan")
            print("2. Keluar")
        else:
            print("Silahkan masukkan pilihan yang tersedia")
            print("gunakan 'help' untuk melihat daftar pilihan")