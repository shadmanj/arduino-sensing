#Import needed libraries
import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

    
# Class to plot data
class DigitalPlot:
  # constr
  def __init__(self, Port, maxLen):
      # open serial port
      self.ser = serial.Serial(Port, 9600)
      
      # define arrays to store display data
      self.ax = deque([0.0]*maxLen)

      # set maximum length of array
      self.maxLen = maxLen

  # Update buffer array with data coming in and data to be discarded
  def addToBuf(self, buf, val):
      if len(buf) < self.maxLen:
          buf.append(val)
      # If buffer array is full, drop the oldest value and move array left
      else:
          buf.pop()
          buf.appendleft(val)

  # Add data to buffer array
  def add(self, data):
      assert(len(data) == 1)
      self.addToBuf(self.ax, data[0])

  # update plot
  def update(self, frameNum, a0, a1, a2):
      try:
          line = self.ser.readline()
          data = [float(val) for val in line.split()]
          # print data
          if(len(data) == 1):
              self.add(data)
              a0.set_data(range(self.maxLen), self.ax)
      except KeyboardInterrupt:
          print('exiting')
      
      return a0, 

  # clean up
  def close(self):
      # close serial
      self.ser.flush()
      self.ser.close()    

# main() function
def main():
  # create parser
  parser = argparse.ArgumentParser(description="Serial")
  # add expected arguments
  parser.add_argument('--port', dest='port', required=True)

  # parse arguments
  args = parser.parse_args()
  
  #Port = '/dev/tty.usbserial-A7006Yqh'
  Port = args.port

  print('Reading from serial port %s' % Port)

  # plot parameters
  digitalPlot = DigitalPlot(Port, 100)

  print('Plotting data')

  # set up animation
  fig = plt.figure()
  ax = plt.axes(xlim=(0, 100), ylim=(-  10000, 50000))
  plt.ylabel('Absolute Acceleration (Gs)')
  a0, = ax.plot([], [])
  anim = animation.FuncAnimation(fig, digitalPlot.update, 
                                 fargs=(a0),interval=50)

  # show plot
  plt.show()
  
  # clean up
  digitalPlot.close()

  print('exiting.')
  

# call main
if __name__ == '__main__':
  main()