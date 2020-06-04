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
#plt.plot(x,y, 'x','go', label="points") #x,y, 'go', x, fit_fn(x), '--k', label="test0"

# plt.hist(x)
# https://jakevdp.github.io/PythonDataScienceHandbook/04.02-simple-scatter-plots.html
# plt.scatter(x,y, marker='*',c='b', label='Pythia8')
plt.plot(x,y, '-^k', c='b', label='Pythia8')
plt.xlabel(r"Cos $\theta^{*}$")
# plt.ylabel(r"$\dot{\Theta}$[deg/s]")
plt.ylabel("Events")
plt.legend(loc=2)
#plt.show()
plt.savefig("theta_tc.pdf")
