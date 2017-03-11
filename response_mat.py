#!/usr/bin/env python
import serial, sys
import numpy as np
import time
import progressbar
from time import sleep

ser = serial.Serial()
ser.baudrate = 9600
ser.port = '/dev/ttyACM1'
ser
ser.open()

time_init = time.time()
t_cmd, t_interval = 0., 0.

cycle = 2.
cmd_min = 80
cmd_max = 240

ser.write(str(cmd_min).zfill(3))
z = []

cmd = 0
dt_f = 0.
v_in = 0

cmd_seq = []
for i in range(cmd_min,cmd_max,10):
  for j in range(i+10,cmd_max+1,10):
    cmd_seq.append(i)
    cmd_seq.append(j)

cmd_seq = np.array(cmd_seq)
print cmd_seq
t_f = cmd_seq.shape[0]*cycle
print "time total: " + str(t_f)

bar = progressbar.ProgressBar(maxval=t_f, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()

ser.write("020")
print "motor warmup started wait 2 sec"
time.sleep(3)

# while(True):
#   cond = ser.read()
#   if cond == '\n':
ser.readline()
#     break
v_in_i, cmd_in_i, dt_in_i = 0, 0 ,0
k = 0
while(True):
  save_flag = 1;
  dt = ser.readline()
  t_now = time.time()-time_init
  t_cmd = t_now - t_interval
  # print dt
  if dt[0] == 'V':
    v_in = dt[8:]
    try:
      v_in_i = int(v_in)
    except ValueError:
      save_flag = 0
      print 'voltage value error: ' + str(dt)
      pass
    # print dt
    # print v_in
  elif dt[0] == 'c':
    cmd_in = dt[4:]
    try:
      cmd_in_i = int(cmd_in)
    except ValueError:
      save_flag = 0
      print 'cmd value error: ' + str(dt)
      pass
    # print cmd_in
  elif len(dt)>0:
    dt_in = dt
    try:
      dt_in_i = int(dt_in)
    except ValueError:
      save_flag = 0
      print 'dt value error: ' + str(dt)
      pass
  if t_now>4 and save_flag:
    z.append([cmd_in_i,dt_in_i,v_in_i])

  if t_now > 1 and t_cmd > cycle:
    mot_cmd = cmd_seq[k]
    cmd =  int(mot_cmd)
    cmd_str = str(cmd).zfill(3)
    ser.write(cmd_str)
    t_interval = time.time() - time_init
    k+=1
  elif t_now < 1:
    cmd = cmd_min
    ser.write(str(cmd).zfill(3))

  if t_now > t_f + 1.5:
    ser.write('000')
    time.sleep(1)
    break
  # print int(100.*(cmd-cmd_min)/(cmd_max-cmd_min))
  bar.update(k*cycle)

ser.write('000')
bar.finish()
ser.close()
z = np.array(z)
np.save('mat_240.npy',z)
