#This code graphs data from the ADXL345 accelerometer in real time

#Import libraries
import serial 	#import Serial library
import numpy	#imports numpy library
import matplotlib.pyplot as plt 	#imports matplotlib for plotting
from drawnow import *	#allows live plotting of data

#Initialize output arrays
xPosition = []
yPosition = []
zPosition = []
time = []

#Serial object arduinoData
arduinoData = serial.Serial('com11', 115200)
plt.ion()	#Enable interactive mode in matplotlib to plot live data
cnt = 0

#Function to plot data
def makeFig():	
	plt.ylim(-100,100)					#Min and Max y values
	plt.title('Sensor Data Stream')		#Plot title
	plt.grid(True)						#Turn on grid
	plt.ylabel('Value')					#Y label
	plt.plot(xPosition,'ro-',label='X-Position')	#Plot X-position
	plt.legend(loc='upper left')		#Legend

	plt2 = plt.twinx()					#Second plot for x values
	plt2.ylim(-100,100)					
	plt2.plot(yPosition, 'b^-',label='Y-Position')
	
	plt3 = plt.twinx()					#Third plot for z values
	plt3.ylim(-100,100)
	plt3.plot(zPosition, 'g', label='Z-Position')

while True:	#While loop to run forever
	while(arduinoData.inWaiting()==0):	#Wait until data received
		pass 						
	arduinoString = arduinoData.readline()	#Read text data from serial port
	dataArray = arduinoString.splt(',')		#Split into dataArray
	t = int( dataArray[0])					#Store time value
	x = int( dataArray[1])			#Store x position value
	y = int( dataArray[2])			#Store y position value
	z = int( dataArray[3])			#Store z position value

	time.append(t)			#Build time array by appending time values
	xPosition.append(x)		#Append x position values
	yPosition.append(y)		#Append y position values
	zPosition.append(z)		#Append z position values

	drawnow(makeFig)		#Call drawnow to make live graph
	plt.pause(.000001)		#Pause plotting to prevent crash
	cnt = cnt + 1
	if(cnt > 50):		#For more than 50 data points, deletes first one from array
		time.pop(0)		#Allows us to see just the last 50 data points
		xPosition.pop(0)
		yPosition.pop(0)
		zPosition.pop(0)









