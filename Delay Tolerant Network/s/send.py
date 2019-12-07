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
from geopy.distance import geodesic

#keputih sukolilo
from pip._vendor.distlib.compat import raw_input



pesanDikirim = []
portDistance = []
portDistance_temp = []

def getLatLong():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = "0.0.0.0"
    port = 35
    server.bind((ip, port))
    server.listen(5)
    print ('menunggu mendapatkan posisi receiver')
    (client_socket, address) = server.accept()
    data = pickle.loads(client_socket.recv(1024))
    print ("========")
    print ("mendapatkan titik lat long dari receiver port " + str(data['port']))
    print ("isi data :")
    print (data['lat'])
    print (data['long'])
    print ("========")
    writeDistance(data['port'],getDistance(data['lat'],data['long']))
    server.close()

def sendDataInput():
    message = raw_input("input pesan > ")
    p = portDistance[0][0]
    del portDistance[0]

    pesanDikirim.insert(0,message)
    pesanDikirim.insert(1,portDistance)
    # hop
    pesanDikirim.insert(2,0)
    pesanDikirim.insert(3,time.time())
    # durasi kirim
    pesanDikirim.insert(4,0)

    print ('mengirimkan pesan ke port ' + str(p))
    hasil = send(pesanDikirim, p)
    while(hasil == 0):
        hasil = send(pesanDikirim, p)
    print ('pengiriman berhasil ke port ' + str(p))

def send(message,port):
    multicast_group = ('224.3.29.71', port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.2)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    print(json.dumps(message).encode('utf8'))
    sock.sendto(json.dumps(message).encode('utf8'), multicast_group)
    while True:
        try:
            sock.recvfrom(16)
        except:
            sock.close()
            return 0
        else:
            print ('pesan berhasil dikirim')
            sock.close()
            return 1


def getDistance(lat_to,long_to):
    coords_1 = (lat_from, long_from)
    coords_2 = (lat_to, long_to)
    return geodesic(coords_1, coords_2).km

def writeDistance(port,distance):
    file = open('log/'+str(port)+".txt","w") 
    file.writelines(str(distance))
    file.close()

def getUrutan():
    path = 'log/'
    for filename in glob.glob(os.path.join(path, '*.txt')):
        file_open = open(filename, 'r')
        nama_file_temp = int(filename[4:9])
        jarak_temp = float(file_open.read())
        portDistance_temp.append([nama_file_temp,jarak_temp])
    return sorted(portDistance_temp, key=operator.itemgetter(1), reverse=False)
    
if __name__ == '__main__':
    print ("sender multicast dtn")
    while 1:
        print ("1. mendapatkan semua lot lang dari semua receiver")
        print ("2. mengurutkan urutan pengiriman ke receiver")
        print ("3. menjalankan pengiriman data")
        print ("4. keluar")
        pilihan = raw_input("Pilihan > ")
        if(pilihan == '1'):
            getLatLong()
        elif(pilihan == '2'):
            portDistance = copy.deepcopy(getUrutan())
            print(portDistance)
        elif(pilihan == '3'):
            sendDataInput()
        elif(pilihan == '4'):
            exit()