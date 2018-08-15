import requests
import json
import time
import socket
def arduinoMakePin(PinMode, PinValue=0):  # just making tuple
    return list((PinMode, PinValue))


class ArduinoControl:

    def __init__(self, RobotAdress):
        self.PinDictionary = {}
        self.RobotAdress = RobotAdress
        self.sockGet = socket.socket()
        self.sockGet.connect((RobotAdress, 11117))
        self.sockSend = socket.socket()
        self.sockSend.connect((RobotAdress, 11118))

    def makeSamplePinDictionary(self):  # just for debugging
        for i in range(70):
            if i % 4 == 0:
                self.PinDictionary[i] = arduinoMakePin("DigitalOutput", 1)
            if i % 4 == 1:
                self.PinDictionary[i] = arduinoMakePin("DigitalInput")
            if i % 4 == 2:
                self.PinDictionary[i] = arduinoMakePin("AnalogOutput", 1028)
            if i % 4 == 3:
                self.PinDictionary[i] = arduinoMakePin("AnalogInput")

    def pinMode(self, PinNumber, Mode):
        self.pinDictionary[PinNumber] = arduinoMakePin(Mode)  # changing mode -> changing value of pin to 0

    def digitalWrite(self, PinNumber, Value):
        try:
            if self.PinDictionary[PinNumber][0] != "DigitalOutput":
                print("Pin " + str(PinNumber) + " is not DigitalOutput!")
                return
            if Value != 0 and Value != 1:
                print("Incorrect Value for DigitalOutput pin " + str(PinNumber) + "! Need to be 1 or 0.")
                return
            self.PinDictionary[PinNumber][1] = Value
        except:
            print("Something went wrong in DigitalWrite(" + str(PinNumber) + "," + str(Value) + ") ! Incorrect values.")

    def analogWrite(self, PinNumber, Value):
        try:
            if self.PinDictionary[PinNumber][0] != "AnalogOutput":
                print("Pin " + str(PinNumber) + " is not AnalogOutput!")
                return
            if Value > 1027 or Value < 0:
                print("Incorrect Value for AnalogOutput pin " + str(PinNumber) + "! Need to be [0,1027].")
                return
            self.PinDictionary[PinNumber][1] = Value
        except:
            print("Something went wrong in AnalogWrite(" + str(PinNumber) + "," + str(Value) + ") ! Incorrect values.")

    def pinRead(self, PinNumber):
        try:
            return self.PinDictionary[PinNumber][1]
        except:
            print("Something went wrong with PinRead!")

    def getConfiguration(self):  # will get config of pins from Raspberry and make PinDictionary like it is
        #time_to_get = time.time()
        msg = "getConf"
        totalsent = 0
        while(len(msg)<2048):
            msg+=" "
        msg = msg.encode()
        while totalsent < 2048:
            sent = self.sockGet.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
        data = self.myreceive()
        if not data:
            print("Connection lost")
            exit(0)
        string = data
        while string[-1]!="}":
            string = string[:-1]
        #print("get:"+str(time.time()-time_to_get))
        data = str(string)
        self.PinDictionary = json.loads(data)
        #print(self.PinDictionary)
        return

    def sendConfiguration(self):  # will send config of pins from this scratch and make PinDictionary on Raspberry like it is
        #time_to_send = time.time()
        totalsent = 0
        msg = json.dumps(self.PinDictionary)
        while(len(msg)<2048):
            msg+=" "
        msg = msg.encode()
        while totalsent < 2048:
            sent = self.sockSend.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
        
        #print("send:"+str(time.time()-time_to_send))
        
        return
    def myreceive(self):
        chunks = ""
        bytes_recd = 0
        while bytes_recd < 2048:
            chunk = self.sockGet.recv(min(2048 - bytes_recd, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunk = chunk.decode()
            chunks+=(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return chunks
AC = ArduinoControl("localhost")
AC.makeSamplePinDictionary()
time0 = time.time()
AC.sendConfiguration()
for i in range(100):
    AC.getConfiguration()
    AC.sendConfiguration()
time1 = time.time()
print((time1-time0)/200.0)


