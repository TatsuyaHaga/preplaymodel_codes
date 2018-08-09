#!/usr/bin/env python3

import sys
import numpy
import matplotlib
matplotlib.use("Agg")
import pylab

pylab.rcParams["font.size"]=7
pylab.rcParams["legend.fontsize"]=7
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
N=100
threshold=5.0
beta=2.5
gamma=1.0
phi=80.0/1000.0

spikeEsom=numpy.loadtxt("spike_som.csv", delimiter=",")
spikeEdnd=numpy.loadtxt("spike_dnd.csv", delimiter=",")
time=spikeEdnd[:,0]
spikeEdnd=spikeEdnd[:,N]
spikeEsom=spikeEsom[:,N]

pylab.clf()
pylab.figure(figsize=(3,2.5))

pylab.subplot(4,1,1)
pylab.plot(time, spikeEsom/(1.0+gamma*spikeEdnd)/phi)
pylab.yticks([0.0, 1.0])
pylab.ylabel("Somatic\nactivity")
pylab.xticks([])

pylab.subplot(4,1,2)
pylab.plot(time, spikeEdnd)
pylab.yticks([0.0, 1.0])
pylab.ylabel("Dendritic\nactivity")
pylab.xticks([])

pylab.subplot(4,1,3)
pylab.plot(time, threshold-beta*spikeEdnd)
pylab.yticks([threshold-beta, threshold])
pylab.ylabel("Threshold")
pylab.xticks([])

pylab.subplot(4,1,4)
pylab.plot(time, (1.0+gamma*spikeEdnd)*phi)
pylab.yticks([phi, (1.0+gamma)*phi])
pylab.ylabel("Maximum\nfiring rate")
pylab.xticks([0.0, numpy.max(time)])
pylab.xlabel("Time [s]")

pylab.tight_layout()
pylab.savefig("plot_oneneuron.pdf")
