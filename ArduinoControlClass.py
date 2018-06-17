import requests
def ArduinoMakePin(PinMode,PinValue=0): #just making tuple
    return list((PinMode,PinValue))
class ArduinoControl:

    def __init__(self,RobotAdress):
        self.PinDictionary = {}
        self.RobotAdress = RobotAdress

    def MakeSamplePinDictionary(self): #just for debugging
        for i in range(100):
            if i%4==0:
                self.PinDictionary[i] = ArduinoMakePin("DigitalOutput",1)
            if i%4==1:
                self.PinDictionary[i] = ArduinoMakePin("DigitalInput")
            if i%4==2:
                self.PinDictionary[i] = ArduinoMakePin("AnalogOutput", 1028)
            if i%4==3:
                self.PinDictionary[i] = ArduinoMakePin("AnalogInput")

    def PinMode(self,PinNumber,Mode):
        self.pinDictionary[PinNumber]=ArduinoMakePin(Mode) #changing mode -> changing value of pin to 0

    def DigitalWrite(self,PinNumber,Value):
        try:
            if self.PinDictionary[PinNumber][0]!="DigitalOutput":
                print("Pin "+str(PinNumber)+" is not DigitalOutput!")
                return
            if Value!=0 and Value!=1:
                print("Incorrect Value for DigitalOutput pin "+str(PinNumber)+"! Need to be 1 or 0.")
                return
            self.PinDictionary[PinNumber][1] = Value
        except:
            print("Something went wrong in DigitalWrite(" + str(PinNumber) + "," + str(Value) + ") ! Incorrect values.")

    def AnalogWrite(self,PinNumber,Value):
        try:
            if self.PinDictionary[PinNumber][0]!="AnalogOutput":
                print("Pin "+str(PinNumber)+" is not AnalogOutput!")
                return
            if Value>1027 or Value<0:
                print("Incorrect Value for AnalogOutput pin " + str(PinNumber) + "! Need to be [0,1027].")
                return
            self.PinDictionary[PinNumber][1] = Value
        except:
            print("Something went wrong in AnalogWrite("+str(PinNumber)+","+str(Value)+") ! Incorrect values.")

    def PinRead(self,PinNumber):
        try:
            return self.PinDictionary[PinNumber][1]
        except:
            print ("Something went wrong with PinRead!")

    def GetConfiguration(self): #will get config of pins from Raspberry and make PinDictionary like it is
            response = requests.post(self.RobotAdress,data={"Type":"GetConfiguration"})
            unformatted_dict = response.text
            unformatted_dict = unformatted_dict.replace('\n','')
            unformatted_dict = unformatted_dict.split("&")
            for i in range(0,len(unformatted_dict)):
                unformatted_dict[i]=unformatted_dict[i].split("=")
            for i in range(0,len(unformatted_dict),2):
                self.PinDictionary[int(unformatted_dict[i][0])]=ArduinoMakePin(str(unformatted_dict[i][1]),int(unformatted_dict[i+1][1]))
            return

    def SendConfiguration(self): #will send config of pins from this scratch and make PinDictionary on Raspberry like it is
            self.PinDictionary["Type"]="SendConfiguration"
            response = requests.post(self.RobotAdress,data=self.PinDictionary)
            return
