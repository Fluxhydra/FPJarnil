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
from geopy.distance import geodesic

#keputih sukolilo
lat_from = -7.294080
long_from = 112.801598

pesanDikirim = []
portDistance = []

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
    message = input("input pesan > ")
    p = portDistance[0][0]
    del portDistance[0]
    pesanDikirim.insert(0,message)
    pesanDikirim.insert(1,portDistance)
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
    print ('mengirimkan pesan ke port ' + str(port))
    sock.sendto(str(message), multicast_group)
    while True:
        try:
            sock.recvfrom(16)
        except:
            print ('tidak ada respon dari port %s' % port)
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
        portDistance.append([nama_file_temp,jarak_temp])
    return sorted(portDistance, key=operator.itemgetter(1), reverse=False)
    
if __name__ == '__main__':
    print ("sender multicast dtn")
    while 1:
        print ("1. mendapatkan semua lot lang dari semua receiver")
        print ("2. mengurutkan urutan pengiriman ke receiver")
        print ("3. menjalankan pengiriman data")
        print ("4. keluar")
        pilihan = input("Pilihan > ")
        if(pilihan == '1'):
            getLatLong()
        elif(pilihan == '2'):
            ngurut = getUrutan()
            print (ngurut)
        elif(pilihan == '3'):
            sendDataInput()
        elif(pilihan == '4'):
            exit()