#!/usr/bin/python3





import json
import cgi
print("Content-type: text/html\n")

currentPinDictionary = {}
handledPinDictionary = {}
form = cgi.FieldStorage()
if(form["Type"].value=="SendConf"):
    handledPinDictionary = json.load(form["Dict"])
else:
    for i in range(70):
        if i%4==0:
            currentPinDictionary[i] = ["DigitalOutput",1]
        if i%4==1:
            currentPinDictionary[i] = ["DigitalInput",0]
        if i%4==2:
            currentPinDictionary[i] = ["AnalogOutput", 1028]
        if i%4==3:
            currentPinDictionary[i] = ["AnalogInput",0]
    print(json.dump(currentPinDictionary))
