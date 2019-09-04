import numpy as np
import warnings
from numpy import *
import matplotlib.pyplot as plt
x, y = loadtxt('../hist.dat',unpack=True, usecols=[0,1])
#z = np.polyfit(x, y, 1)
#print ("z",z)


#fit = np.polyfit(x,y,1)
#fit_fn = np.poly1d(fit) 
# fit_fn is now a function which takes in x and returns an estimate for y

#plt.plot(x,y, 'go', label="points") #x,y, 'go', x, fit_fn(x), '--k', label="test0"

plt.scatter(x,y, c='r', label='the data')
plt.xlabel("x values")
plt.ylabel("y values")
plt.legend(loc=2)
#plt.show()
plt.savefig("theta_tc.png")
