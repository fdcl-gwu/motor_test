#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import pdb
from matplotlib.backends.backend_pdf import PdfPages

z = np.load('mat_240.npy')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
# mat_240 is 50Hz
fig, ax1 = plt.subplots()
# pdb.set_trace()
t = np.linspace(0,z.shape[0]/100,z.shape[0])
ax1.plot(t, 1./z[:,1]*30*1e6,'.')
plt.ylabel('RPM')
plt.xlabel('Time [s]')
plt.grid()
ax2 = ax1.twinx()
ax2.plot(t, z[:,0],'r.-')
plt.ylabel('cmd')
plt.xlim([0, 68])
# z = np.polyfit(rpm,z[:,2],2)
# rpm_fit = np.linspace(2000,5500,100)
# p = np.poly1d(z)
# print z
# plt.plot(rpm_fit,p(rpm_fit),'--r')
plt.tight_layout()
pp = PdfPages('response.pdf')
pp.savefig(fig)
fig.savefig('response.png')
pp.close()
plt.show()
