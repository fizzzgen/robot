#!/usr/bin/python3


import json
import socket
from multiprocessing import Process, Manager


manager = Manager()
currentPinDictionary = manager.dict()
handledPinDictionary = manager.dict()

def getConfHandler():
    sock = socket.socket()
    sock.bind(('', 11117))
    sock.listen(100)
    conn, addr = sock.accept()
    while True:
        data = conn.recv(2048)
        if not data:
            continue
        try:
            string = str(data.decode())
            #print("-----getConfHandler SUCCESS: decode success-----")
            while string[-1]==" ":
                    string = string[:-1]
        except:
            print("-----getConfHandler ERROR: Decode error-----")
            continue
        try:
            if string=="getConf":
                send_data = json.dumps(dict(currentPinDictionary))
                while len(send_data)<2048:
                    send_data+=" "
                conn.send(send_data.encode())
            #print("-----getConfHandler SUCCESS: Dictionary sent!-----")
        except:
            print("-----getConfHandler ERROR: Dictionary didn't send-----")

def sendConfHandler():
    sock = socket.socket()
    sock.bind(('', 11118))
    sock.listen(100)
    conn, addr = sock.accept()
    while True:
        data = conn.recv(2048)
        if not data:
            continue
        try:
            string = str(data.decode())
            #print("-----sendConfHandler SUCCESS: Decode success-----")
            while string[-1]==" ":
                    string = string[:-1]
        except:
            print("-----sendConfHandler ERROR: Decode error-----")
            continue
        try:
            if string[0]=="{":
                while string[-1]!="}":
                    string = string[:-1]
                handledPinDictionary.update(json.loads(string))
            #print("-----sendConfHandler SUCCESS: Dictionary handled!-----")
            currentPinDictionary = handledPinDictionary
        except:
            print("-----sendConfHandler ERROR:Dictionary couldn't be handeled!-----")
    
procs = [ Process(target=getConfHandler),Process(target=sendConfHandler) ]
for proc in procs:
    proc.start()
for proc in procs:
    proc.join()
