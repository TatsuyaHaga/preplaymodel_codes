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
pylab.rcParams["figure.figsize"]=(2, 2.5)

#weight
Winh=numpy.loadtxt("WIdnd.csv", delimiter=",")

pylab.clf()
pylab.subplot(2,1,1)
pylab.plot(Winh[:,0], Winh[:,1], color="blue")
pylab.ylabel("Inhibitory weight")
pylab.xlabel("Time [s]")
pylab.xticks([0, 300, 600, 900, 1200])
pylab.ylim([0.0, 80.0])
pylab.yticks([0.0, 80.0])
#pylab.legend(loc="upper left")

#pylab.xticks([])
#pylab.ylim([0.0, 1.1])
#pylab.yticks([0.0, 1.0])

pylab.tight_layout()
pylab.savefig("weight_inh.pdf")
