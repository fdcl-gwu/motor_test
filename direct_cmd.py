#!/usr/bin/env python
import serial
import numpy as np
import time


ser = serial.Serial()
ser.baudrate = 9600
ser.port = '/dev/ttyACM0'
ser
ser.open()
time.sleep(2)

ser.write("000")
time.sleep(2)
t_ini = time.time()
while(True):
  str_in = ser.readline()
  # print str_in
  if str_in[0] == 'V':
    print 'v:'+str(str_in[8:])
  elif str_in[0] == 'c':
    print 'c:'+str(str_in[4:])
  elif len(str_in)>0:
    print 'd:'+str(str_in)
  if time.time()-t_ini > 1:
    ser.write("000")
    time.sleep(1)
    break

ser.close()
