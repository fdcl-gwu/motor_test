import numpy as np
import matplotlib.pyplot as plt
import pdb

z = np.load('mat_240.npy')

# pdb.set_trace()
plt.subplot(2, 2, 1)
plt.plot(1./z[:,1]*30*1e6,'.-')
plt.ylabel('RPM')
plt.subplot(2, 2, 2)
plt.plot(z[:,2],'.-')
plt.ylabel('grams')
plt.subplot(2, 2, 3)
plt.plot(z[:,0],'.-')
plt.ylabel('cmd')
rpm = 1./z[:,1]*30*1e6
plt.subplot(2, 2, 4)
plt.plot(rpm,z[:,2],'.-')

z = np.polyfit(rpm,z[:,2],2)
rpm_fit = np.linspace(2000,5500,100)
p = np.poly1d(z)
print z
plt.plot(rpm_fit,p(rpm_fit),'--r')
plt.ylabel('Throttle')
plt.xlabel('rpm')
plt.show()
