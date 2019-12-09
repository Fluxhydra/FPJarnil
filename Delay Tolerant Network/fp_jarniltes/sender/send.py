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
time_limit = 30
ip_addr = '192.168.1.0'
pesanDikirim = []
port = 10000

def sendMessage():
    message = raw_input("input pesan > ")
    pesanDikirim.insert(0,message)
    pesanDikirim.insert(1,lat_from)
    # hop
    pesanDikirim.insert(2,0)
    pesanDikirim.insert(3,time.time())
    # durasi kirim
    pesanDikirim.insert(4,0)
    pesanDikirim.insert(5,long_from)
    pesanDikirim.insert(6,tujuan)
    pesanDikirim.insert(7,ip_addr)
    settime = time.time()
    timecek = 0
    print(pesanDikirim)
    hasil = send(pesanDikirim, port)
    while (timecek < time_limit):
        if hasil == 0:
            hasil = send(pesanDikirim, port)
        else:
            print('pengiriman berhasil')
            break
        timecek = time.time() - settime
    if hasil == 0:
        print('Umur pesan melebihi batas waktu, pesan akan dihapus\n')


def send(message,port):
    multicast_group = ('224.3.29.71', port)
    # regarding socket.IP_MULTICAST_TTL
    # ---------------------------------
    # for all packets sent, after two hops on the network the packet will not
    # be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
    MULTICAST_TTL = 2

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
    sock.sendto(json.dumps(message).encode('utf8'), multicast_group)

if __name__ == '__main__':
        print("sender multicast dtn")
        path = 'location/'
        cek = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
        print("1. Jalankan pengiriman pesan")
        print("2. keluar")
        print("Masukkan pilihan")
        while 1:
            pilihan = raw_input(">> ")
            if (pilihan == '1'):
                tujuan = raw_input('IP Tujuan > ')
                sendMessage()
            elif (pilihan == '2'):
                exit()
            elif (pilihan == 'help'):
                print("Pilihan yang tersedia:")
                print("1. Jalankan pengiriman pesan")
                print("2. keluar")
            else:
                print("Silahkan masukkan pilihan yang tersedia")
                print("gunakan 'help' untuk melihat daftar pilihan")