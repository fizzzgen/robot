import requests
import json

def arduinoMakePin(PinMode, PinValue=0):  # just making tuple
    return list((PinMode, PinValue))


class ArduinoControl:

    def __init__(self, RobotAdress):
        self.PinDictionary = {}
        self.RobotAdress = RobotAdress

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
        response = requests.post(self.RobotAdress, data={"Type":"GetConf"})
        self.PinDictionary = json.load(response.text)
        print(self.PinDictionary)
        return

    def sendConfiguration(self):  # will send config of pins from this scratch and make PinDictionary on Raspberry like it is
        data = {}
        data["Type"] = "SendConf"
        data["Dict"]=json.dump(self.PinDictionary)
        response = requests.post(self.RobotAdress, data=data)
        print(response.text)
        return