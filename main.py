#!/usr/bin/env python
import serial
import numpy as np
import time
import progressbar
from time import sleep


ser = serial.Serial()
ser.baudrate = 9600
ser.port = '/dev/ttyACM0'
ser
ser.open()
time.sleep(2)

ser.write("030")
time.sleep(2)


time_init = time.time()
t_cmd, t_interval = 0., 0.
t_f = 120
cycle = 1.
cmd_min = 80
cmd_max = 244
p_max = 83.
p_min = 10.

ser.write(str(cmd_min).zfill(3))
z = []

cmd = 0
dt_f = 0.
v_in = 0

coef =np.array([-1.12e-9,   2.91e-7,  -2.76e-5  , 1.05e-3  ,-1.34e-3 , -9.94e-1, 2.69e1  ,-1.23e2])
coef = np.array([2.14,  69.83])

p2cmd = np.poly1d(coef)
print 'min power: '+ str(p2cmd(p_min)) +' max power: '+ str(p2cmd(p_max))


bar = progressbar.ProgressBar(maxval=100, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()
i = 1

# while(True):
#   cond = ser.read()
#   if cond == '\n':
ser.readline()
#     break
v_in_i, cmd_in_i, dt_in_i = 0, 0 ,0
x = []

while(True):
  save_flag = 1;
  serial_in = ser.readline()
  t_now = time.time()-time_init
  t_cmd = t_now - t_interval
  # print dt
  if serial_in[0] == 'V':
    v_in = serial_in[8:]
    try:
      v_in_i = int(v_in)
    except ValueError:
      save_flag = 0
      print( 'voltage value error: ' + str(serial_in))
      pass
    # print dt
    # print v_in
  elif serial_in[0] == 'c':
    cmd_in = serial_in[4:]
    try:
      cmd_in_i = int(cmd_in)
    except ValueError:
      save_flag = 0
      print( 'cmd value error: ' + str(serial_in))
      pass
    # print cmd_in
  elif serial_in[0] == 'I':
    dt_str = serial_in[4:]
    try:
      x = [int(i) for i in dt_str.split()]
      # current =
      # voltage =
      # rpm =
    except ValueError:
      save_flag = 0
      print( 'I2C read value error: ' + str(serial_in))

  elif len(serial_in)>0:
    dt_in = serial_in
    try:
      dt_in_i = int(dt_in)
    except ValueError:
      save_flag = 0
      print( 'dt value error: ' + str(serial_in))
      pass
  if t_now>4 and save_flag:
    z.append([cmd_in_i,dt_in_i,v_in_i,x[0],x[3],x[-1]])

  if t_now > 1. and t_cmd > 0.01:
    p_d = p_min + (p_max-p_min)/t_f*t_now #
    mot_cmd = p2cmd(p_d)
    # mot_cmd = cmd_min + (cmd_max-cmd_min)/t_f*t_now #
    # mot_cmd = cmd_min + 1./2*(cmd_max-cmd_min)*(1.+np.sin(-np.pi/2+2.*np.pi*t_now/t_f*cycle))
    cmd =  int(mot_cmd)
    cmd_str = str(cmd).zfill(3)
    ser.write(cmd_str)
    t_interval = time.time() - time_init
  # elif t_now < 1:
  #   cmd = cmd_min
  #   ser.write(str(cmd).zfill(3))

  if cmd > cmd_max and t_now > t_f:
    ser.write('000')
    time.sleep(1)
    break
  # print int(100.*(cmd-cmd_min)/(cmd_max-cmd_min))
  # bar.update(int(100.*t_now/t_f))

ser.write('000')
bar.finish()
ser.close()
z = np.array(z)
np.save('power_command_3.npy',z)
