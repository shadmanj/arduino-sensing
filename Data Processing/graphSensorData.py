#Import needed libraries
import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

scale = .0078
# Class to plot data
class DigitalPlot:
  # constr
  def __init__(self, Port, maxLen):
      # open serial port
      self.ser = serial.Serial(Port, 9600)
      # define arrays to store display data
      self.ax = deque([0.0]*maxLen)
      self.ay = deque([0.0]*maxLen)
      self.az = deque([0.0]*maxLen)
      self.abs = deque([0.0]*maxLen)
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
      assert(len(data) == 3)
      x = data[0]*scale
      y = data[1]*scale
      z = data[2]*scale
      absolute = np.sqrt(x**(2)+y**(2)+z**(2))
      self.addToBuf(self.ax, x)
      self.addToBuf(self.ay, y)
      self.addToBuf(self.az, z)
      print( data[0]*scale, data[1]*scale, data[2]*scale)
      self.addToBuf(self.abs, absolute)

  # update plot
  def update(self, frameNum, a0, a1, a2, a3):
      try:
          line = self.ser.readline()
          data = [float(val) for val in line.split()]
          # print data
          if(len(data) == 3):
              self.add(data)
              a0.set_data(range(self.maxLen), self.ax)
              a1.set_data(range(self.maxLen), self.ay)
              a2.set_data(range(self.maxLen), self.az)
              a3.set_data(range(self.maxLen), self.abs)
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
  ax = plt.axes(xlim=(0, 100), ylim=(-8,8))
  plt.title('ADXL345 Data')
  plt.ylabel('Acceleration (G)')
  a0, = ax.plot([], [])
  a1, = ax.plot([], [])
  a2, = ax.plot([], [])
  a3, = ax.plot([], [])
  anim = animation.FuncAnimation(fig, digitalPlot.update, 
                                 fargs=(a0, a1, a2, a3), 
                                 interval=50)

  # show plot
  plt.show()
  
  # clean up
  digitalPlot.close()

  print('exiting.')
  

# call main
if __name__ == '__main__':
  main()
