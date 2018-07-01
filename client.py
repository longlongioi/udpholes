#!/usr/bin env python
# -*- coding:utf-8 -*-

import socket
import sys
import threading

type = sys.getfilesystemencoding()
def InitSocketToUDP():
    print "Please enter the port that you want to recv UDP msg :"
    port = raw_input()
    ip_port = ('127.0.0.1',int(port))
    try:
        sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    except socket.error, e:
        print  "Strange error creating socket: %s " % e
        return 0
    except Exception as e:
        print  e
        return 0
    try:
        sk.bind(ip_port)
    except Exception as e:
        print e
        return 0
    return sk

def SendHoleCmdGetHole(sk,ip_port):
    try:
        sk.sendto("Hole",ip_port)
    except Exception as e:
        print  str(e).decode()
        sys.exit(1)
    try:
        recvData,addrSrv = sk.recvfrom(sys.getsizeof(ip_port))
    except Exception as e:
        print  e
        sys.exit(1)
    print  recvData
    recvData = recvData.split(',')
    print "Other's IP : ",recvData[0]
    print "Port:",recvData[1]
    return recvData

def Hole(sk,ip_port):
    try:
        sk.sendto("I Believe you!",ip_port)
    except Exception as e:
        print  e
        sys.exit(1)

def RecvProc(sk):
    print "In socketClient is : %d %s" % (sk.fileno(),sk.getsockname())
    while 1:
        try:
            RecvBuf,client = sk.recvfrom(512)
        except Exception as e:
            print  e
            sys.exit(1)
        print client,RecvBuf





if __name__ == "__main__":
    sk = InitSocketToUDP()
    if sk == 0:
        exit(1)
    print "Please enter Hole Server's IP address :"
    strSrvIP = raw_input()
    print "Please enter Port :"
    uPort = int(raw_input())
    print "Sending Hole cmd to srv....."
    anotherIp_port = SendHoleCmdGetHole(sk,ip_port=(strSrvIP,uPort))
    if  anotherIp_port == 0:
        print "Get Hole Info from srv fails!"
        exit(1)
    print "Real socketClient is : %d" % sk.fileno(), sk.getsockname()
    try:                #udp无连接
        print sk.getpeername()
    except Exception as e:
        a = str(e)
        print a.decode(type)
    try:
        t = threading.Thread(target=RecvProc, args=(sk,),name="RecvProc")
    except Exception as e:
        print "Error: unable to start thread"

    if Hole(sk,(anotherIp_port[0],int(anotherIp_port[1]))) == 0:
        print "Hole fails!\n"
    print "Hole successful you can send msg to him !"
    t.start()
    while 1:
        me = sk.getsockname()
        SendBuf = raw_input()
        sk.sendto(str(SendBuf),(anotherIp_port[0],int(anotherIp_port[1])))
    print 'thread %s ended.' % threading.current_thread().name
    t.join()
    sk.close()