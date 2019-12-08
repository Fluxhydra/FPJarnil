# -*- coding: utf-8 -*-
import socket
import struct
import sys
import json
import pickle
import ast
import time
import os


from pip._vendor.distlib.compat import raw_input

lat_to = -7.228549
long_to = 112.731391

port = 10001
time_limit = 5
hop_limit = 1
pesanDikirim = []

def sendPosition():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(20)
    client.connect(('127.0.0.1', 35))
    data = {
        'port' : port,
        'lat' : lat_to,
        'long' : long_to
    }
    client.send(pickle.dumps(data))
    print('sukses mengirim lokasi !')
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
        print('\nwaiting to receive message')
        data, address = sock.recvfrom(1024)
        data = json.loads(data.decode('utf-8'))
        print('received %s bytes from %s' % (len(data), address))
        pesan = data[0]
        print('message : ' + pesan)
        rute = data[1]
        hop = data[2] + 1
        getSecond = time.time() - data[3]
        timestamp = time.time()
        duration = data[4] + getSecond
        print ('sending acknowledgement to', address)
        sock.sendto(b'ack', address)
        if(data[2] > hop_limit):
            print('jumlah hop : ' + str(hop))
            print('hop telah melebihi limit')
            exit()
        if not data[1]:
            sock.sendto(b'ack', address)
            print ('ini adalah rute DTN terakhir')
            print ('durasi pengiriman pesan : ' + str(data[4]))
            print ('jumlah hop : ' + str(data[2]))
            exit()

        sendData(pesan,rute,hop,timestamp,duration)

def sendData(pesan,rute,hop,timestamp,duration):
    p = rute[0][0]
    del rute[0]
    pesanDikirim.insert(0,pesan)
    pesanDikirim.insert(1,rute)
    pesanDikirim.insert(2,hop)
    pesanDikirim.insert(3,timestamp)
    pesanDikirim.insert(4,duration)
    pesanDikirim.insert(4, 0)
    settime = time.time()
    timecek = 0
    print('mengirimkan pesan ke port ' + str(p))
    hasil = send(pesanDikirim, p)
    while (timecek < time_limit):
        if hasil == 0:
            hasil = send(pesanDikirim, p)
        else:
            print('pengiriman berhasil ke port ' + str(p))
            break
        timecek = time.time() - settime
    if hasil==0:
        print('Umur pesan melebihi batas waktu, pesan akan dihapus\n')
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
            print ('pesan berhasil dikirim')
            sock.close()
            return 1

if __name__ == '__main__':
    print("receiver port " + str(port) + ": ")
    print("==============")
    path="../sender/log/"
    if not os.path.isfile(os.path.join(path,str(port)+".txt")):
        sendPosition()
    while 1:
        print("1. menerima pesan dan mengirimkan ke node selanjutnya")
        print("2. keluar")
        inputan = raw_input('Pilihan > ')
        if (inputan == '1'):
            multicast()
        elif (inputan == '2'):
            exit()
        else:
            print('inputan salah')