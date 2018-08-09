#!/usr/bin/env python3

import sys
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
#pylab.rcParams["figure.figsize"]=(3, 3)

#activity
marker_size=4

pylab.clf()
pylab.figure(figsize=(3,1))

MI=numpy.loadtxt("MIall.csv", delimiter=",")
pylab.plot(MI[:,1], [0]*5, "o", color="magenta", label="inhibition OFF", markersize=marker_size)
pylab.plot(MI[:,0], [1]*5, "o", color="magenta", label="inhibition ON", markersize=marker_size)

pylab.ylim([-0.5,1.5])
pylab.yticks(range(2), ["inhibition OFF", "inhibition ON"])
pylab.xlim([0.0, 2.0])
pylab.xticks([0.0, 1.0, 2.0])
pylab.xlabel("Information per spike [bit]")
pylab.tight_layout()
pylab.savefig("MI.svg")
