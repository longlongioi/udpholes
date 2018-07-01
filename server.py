#!/usr/bin env python
# -*- coding:utf-8 -*-
import socket
import sys
import os
type = sys.getfilesystemencoding()
def InitSocketToUDP():
    try:
        sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    except Exception as e:
        print e
        return 0
    return sk

def Bind(sk,ip_port):
    try:
        sk.bind(ip_port)
    except Exception as e:
        print(e)
        return 0
    return 1

def HoleSrv(sk,ip_port):
    while 1:
        try:
            recvData, addr = sk.recvfrom(512)
        except Exception as e:
            print(e)
            return 0
        print addr,recvData
        if recvData == "Hole":
            try:
                recvData, addrtemp = sk.recvfrom(512)
            except Exception as e:
                print(e)
                return 0
            print addrtemp, recvData
            if recvData == "Hole":
                try:
                    sk.sendto(("%s,%d" % (addrtemp[0],addrtemp[1])),addr)
                except Exception as e:
                    print(str(e).decode(type))
                    return 0
                try:
                    sk.sendto(("%s,%d" % (addr[0],addr[1])),addrtemp)
                except Exception as e:
                    print(str(e).decode(type))
                    return 0
                print addr,"and",addrtemp,"Hole successful!"

    return 1

if __name__ == "__main__":
    sk = InitSocketToUDP()
    ip_port = ('127.0.0.1',5174)
    if sk == 0:
        exit(1)
    if Bind(sk,ip_port) == 0:
        exit(1)
    HoleSrv(sk,ip_port)
    os.system("pause")
