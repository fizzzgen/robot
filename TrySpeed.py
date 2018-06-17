import ArduinoControlClass

A = ArduinoControlClass.ArduinoControl("http://192.168.1.44/cgi-bin/RequestHandler.py")
A.makeSamplePinDictionary()
for i in range(100):
    print(i)
    A.sendConfiguration()
for i in range(100):
    print(i)
    A.getConfiguration()
