import numpy as np
import matplotlib.pyplot as plt
import pdb

z = np.load('mat_240.npy')
# mat_240 is 50Hz
fig, ax1 = plt.subplots()
# pdb.set_trace()
t = np.linspace(0,z.shape[0]/100,z.shape[0])
ax1.plot(t, 1./z[:,1]*30*1e6,'.-')
plt.ylabel('RPM')

ax2 = ax1.twinx()
ax2.plot(t, z[:,0],'r.-')
plt.ylabel('cmd')

# z = np.polyfit(rpm,z[:,2],2)
# rpm_fit = np.linspace(2000,5500,100)
# p = np.poly1d(z)
# print z
# plt.plot(rpm_fit,p(rpm_fit),'--r')
plt.xlabel('Time')
plt.show()
