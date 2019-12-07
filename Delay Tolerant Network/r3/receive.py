# -*- coding: utf-8 -*-
import socket
import struct
import sys
import pickle
import ast


#gresik
port = 10003
lat_to = -7.155029
long_to = 112.572189

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
    print ('sukses mengirim lokasi !')
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
        print ('\nwaiting to receive message', file = sys.stderr)
        data, address = sock.recvfrom(1024)
        
        print ('received %s bytes from %s' % (len(data), address), file = sys.stderr)
        data = ast.literal_eval(data)

        pesan = data[0]
        print ('isi pesan : ' + pesan)

        if not data[1]:
            endReceiver()
        
        rute = data[1]

        sock.sendto('ack', address)

        print ('pengiriman selanjutnya ke port ' + str(rute[0][0]))
        sendData(pesan,rute)

def endReceiver():
    print ('ini adalah rute DTN terakhir')
    exit()

def sendData(pesan,rute):
    p = rute[0][0]
    del rute[0]
    pesanDikirim.insert(0,pesan)
    pesanDikirim.insert(1,rute)
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

if __name__ == '__main__':
    print ("receiver port " + str(port) + ": ")
    print ("==============")
    while 1:
        print ("1. mengirimkan posisi ke sender")
        print ("2. menerima data dan mengirimkan ke alamat selanjutnya")
        print ("3. keluar")
        inputan = input('Pilihan > ')
        if(inputan == '1'):
            sendPosition()
        elif(inputan == '2'):
            multicast()
        elif(inputan == '3'):
            exit()
        else :
            print ('inputan salah')