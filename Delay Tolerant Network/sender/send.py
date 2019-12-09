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
pesanDikirim = []
portDistance = []
portDistance_temp = []

def getLocation():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = "0.0.0.0"
    port = 35
    server.bind((ip, port))
    server.listen(5)
    print('Waiting for receiver position data')
    (client_socket, address) = server.accept()
    data = pickle.loads(client_socket.recv(1024))
    if cekLokasi(str(data['port'])) == "0":
        print ("========")
        print ("Getting lang lat points from receiver" + str(data['port']))
        print ("Data: ")
        print (data['lat'])
        print (data['long'])
        print ("========")
        file = open('location/' + str(data['port']) + ".txt", "w")
        file.writelines(str(getDistance(data['lat'],data['long'])))
        file.close()
        server.close()
    elif cek:
        server.close()

def cekLokasi(lok):
    if os.path.isfile(os.path.join(path, str(lok) + ".txt")):
        return "1"
    else:
        return "0"


def sendMessage():
    message = raw_input("Input > ")
    p = portDistance[0][0]
    del portDistance[0]
    pesanDikirim.insert(0,message)
    pesanDikirim.insert(1,portDistance)
    pesanDikirim.insert(2,0)
    pesanDikirim.insert(3,time.time())
    pesanDikirim.insert(4,0)
    settime = time.time()
    timecek = 0
    print('Sending message to port ' + str(p))
    hasil = send(pesanDikirim, p)
    while (timecek < time_limit):
        if hasil == 0:
            hasil = send(pesanDikirim, p)
        else:
            print('Message sent to port ' + str(p))
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

def Sort():
    path = 'location/'
    name = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
    for filename in glob.glob(os.path.join(path, '*.txt')):
        file_open = open(filename, 'r')
        nama_file_temp = int(filename[9:14])
        jarak_temp = float(file_open.read())
        if (len(portDistance) != 3):
            portDistance.append([nama_file_temp, jarak_temp])
    return sorted(portDistance, key=operator.itemgetter(1), reverse=False)

if __name__ == '__main__':
        print("[DTN Multicast: Node S]")
        print("--------------------")
        path = 'location/'
        cek = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
        print("1. Get receiver location")
        print("2. Create a new message")
        print("3. Exit")
        while 1:
            print("\nYour choice?")
            pilihan = raw_input(">> ")
            if (pilihan == '1'):
                if cek != 3:
                    getLocation()
                else:
                    print("Location obtained")
            elif (pilihan == '2'):
                portDistance = []
                portDistance = copy.deepcopy(Sort())
                print(portDistance)
                sendMessage()
            elif (pilihan == '3'):
                exit()