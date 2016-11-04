from nanpy import (ArduinoApi, SerialManager, Servo)
from time import sleep
import robot.device_info


try:
    connection = SerialManager()
    a = ArduinoApi(connection = connection)
except:
    print("Failed to connect to arduino")

for j in range(30,54, 1):
    a.digitalWrite(j, a.HIGH)


for i in range(30,54):
    a.pinMode(i, a.OUTPUT)
##
##
##for j in range(30,54, 1):
##    a.digitalWrite(j, a.LOW)
##
##    sleep(1)


oldrelay = 30
while(1):
    relay = int(input("Select a relay")) +29
    if(relay >= 30 and relay <= 54):
        a.digitalWrite(relay, a.LOW)
        if(relay != oldrelay):
            a.digitalWrite(oldrelay,a.HIGH)
        oldrelay = relay
        
        
    

