#!/usr/bin/env python3

import numpy
import matplotlib
matplotlib.use("Agg")
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
colormap="hot" #"jet", "bwr"

spikeEsom=numpy.loadtxt("spike_som.csv", delimiter=",")

som_max=0.1
som_min=0.0

time=spikeEsom[:,0]

pylab.clf()
pylab.figure(figsize=(2.5,1.5))
pylab.imshow(spikeEsom[:, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spikeEsom[0,0], spikeEsom[-1,0], len(spikeEsom[0,1:]), 1], vmax=som_max, vmin=som_min)
pylab.colorbar()
pylab.yticks([1, len(spikeEsom[0,1:])])
pylab.xlabel("Time [s]")
pylab.ylabel("CA3 firing rate")

pylab.tight_layout()
pylab.savefig("spike.pdf")
