#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import pdb, sys
from decimal import Decimal

z = np.load('calibration.npy')
z = np.load('power_command_3.npy')
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

N = 1 # number of p-magnet
t = np.linspace(0,120,z.shape[0])
power = z[:,-3]*z[:,-1]*0.01
cmd = z[:,0]
throttle = 9.81*1e-3*z[:,2]
rpm = 1./z[:,1]*60/N*1e6
cmd_power = np.poly1d(np.array([  0.44, -25.69]))

p_max = 85.
p_min = 10.
cmd_power_in = np.linspace(p_min,p_max,z.shape[0])

fig, ax1 = plt.subplots()
plt.grid()
lrpm = ax1.plot(t, rpm,'g.',label='RPM')
ax1.set_ylim([3000, 5600])
ax1.set_ylabel('RPM')
ax1.set_xlabel('time (s)')
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax2 = ax1.twinx()
lpow = ax2.plot(t,power,'r.',label='Power')
lpcmd = ax2.plot(t,cmd_power_in,'b.',label='Power$_{ref}$')
ax2.set_ylim([p_min,100])
plt.ylabel('Power (watt)')
plt.grid()
lns = lrpm+lpow+lpcmd
labs = [l.get_label() for l in lns]
plt.legend(lns, labs, loc=2)
plt.savefig('power_ramp.png')

plt.figure()
plt.plot(t,cmd)
plt.plot(t,power)





plt.figure()
plt.subplot(2, 2, 2)
plt.grid()
plt.plot(power,throttle,'.')
plt.ylabel('Throttle [N]')
plt.xlabel('Power [watt]')

plt.subplot(2, 2, 3)
plt.grid()
plt.plot(power,cmd,'.')
plt.ylabel('cmd')

z_fit = np.polyfit(cmd,power,1)
np.set_printoptions(precision=2)
print 'cmd to power: ' + str(z_fit)


z_fit = np.polyfit(power,cmd,1)
power_fit = np.linspace(power.min(),power.max(),100)
p = np.poly1d(z_fit)
np.set_printoptions(precision=2)
print z_fit
plt.plot(power_fit,p(power_fit),'--r')


plt.subplot(2, 2, 4)
plt.grid()
plt.plot(rpm,throttle,'.-')
plt.ylabel('Throttle [N]')
plt.xlabel('rpm')


z_fit = np.polyfit(rpm,throttle,2)
rpm_fit = np.linspace(2000,5500,100)
p = np.poly1d(z_fit)
np.set_printoptions(precision=2)
print z_fit
plt.plot(rpm_fit,p(rpm_fit),'--r')
plt.text(2400, 4, z_fit, fontsize=12)

plt.savefig('fit.png')
# pp.close()
plt.show()


fig, ax1 = plt.subplots()
# pdb.set_trace()
# t = np.linspace(0,z.shape[0]/100,z.shape[0])
ax1.plot(t, z[:,-1]*0.1,'.',label='Voltage')
plt.ylabel('Voltage [V]')
plt.xlabel('Time [s]')
plt.grid()
ax2 = ax1.twinx()
ax2.plot(t, z[:,-3]*0.1,'r.',label='Current')
plt.ylabel('Current [C]')
# plt.xlim([0, 68])
plt.tight_layout()
plt.show()
