#!/usr/bin/python

import numpy
import pylab

pylab.rcParams["font.size"]=8
pylab.rcParams["legend.fontsize"]=6
#pylab.rcParams["lines.linewidth"]=1
#pylab.rcParams["axes.linewidth"]=2
#pylab.rcParams["axes.labelsize"]="large"
#pylab.rcParams["axes.labelweight"]="bold"
pylab.rcParams["xtick.major.size"]=0
pylab.rcParams["xtick.minor.size"]=0
pylab.rcParams["ytick.major.size"]=0
pylab.rcParams["ytick.minor.size"]=0
#pylab.rcParams["xtick.direction"]="out"
#pylab.rcParams["ytick.direction"]="out"
pylab.rcParams["figure.figsize"]=(3, 3)

#weight
Wsom=numpy.loadtxt("Wsom.csv", delimiter=",")
Wdnd=numpy.loadtxt("Wdnd.csv", delimiter=",")
group1_num=10

pylab.clf()
pylab.subplot(2,1,1)
for i in range(1,Wsom.shape[1]):
    if i<=group1_num:
        pylab.plot(Wsom[:,0], Wsom[:,i], color="blue")
    else:
        pylab.plot(Wsom[:,0], Wsom[:,i], color="red")
pylab.ylabel("Weight (soma)")
pylab.xlabel("Time [s]")
#pylab.legend(loc="upper left")
"""
pylab.subplot(2,1,2)
for i in range(1,Wdnd.shape[1]):
    if i<=group1_num:
        pylab.plot(Wdnd[:,0], Wdnd[:,i], color="blue")
    else:
        pylab.plot(Wdnd[:,0], Wdnd[:,i], color="red")
pylab.ylabel("weight (dendrite)")
pylab.xlabel("time [s]")
#pylab.legend(loc="upper left")
"""
#pylab.xticks([])
#pylab.ylim([0.0, 1.1])
#pylab.yticks([0.0, 1.0])

pylab.tight_layout()
pylab.savefig("weight.pdf")
