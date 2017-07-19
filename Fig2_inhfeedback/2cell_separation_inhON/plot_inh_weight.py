#!/usr/bin/python

import numpy
import pylab

pylab.rcParams["font.size"]=8
pylab.rcParams["legend.fontsize"]=8
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
Wdnd=numpy.loadtxt("WIdnd.csv", delimiter=",")

time=Wdnd[:,0]
Wdnd=Wdnd[:,1:]

color_arr=["b", "r", "y", "g", "k", "c", "m"]

pylab.clf()
pylab.subplot(2,1,1)
for i in range(Wdnd.shape[1]):
    pylab.plot(time, Wdnd[:,i], color=color_arr[i])
pylab.ylabel("Inh. weight (dendrite)")
pylab.xlabel("Time [s]")
#pylab.legend(loc="upper left")

pylab.tight_layout()
pylab.savefig("inh_weight.pdf")
