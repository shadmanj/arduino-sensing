import serial
import numpy
import matplotlib.pyplot as plt
from drawnow import *

arduinoData = serial.Serial('/dev/ttyACM0',9600)
plt.ion()
cnt = 0

while True:
    while(arduinoData.inWaiting()==0):
        pass
    arduinoString = arduinoData.readline()
    dataArray = arduinoString.split(',')
    print(dataArray)
