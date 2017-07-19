#!/usr/bin/env python3

import sys
import numpy
#import matplotlib
#matplotlib.use("SVG")
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
spikeEdnd=numpy.loadtxt("spike_dnd.csv", delimiter=",")

som_max=0.1
som_min=0.0
#dnd_max=1.0
dnd_min=0.0

pos=numpy.loadtxt("position.csv", delimiter=",")
x_pos=pos[:,0]
time=spikeEsom[:,0]

pylab.clf()
pylab.figure(figsize=(3.5,3))
pylab.subplot2grid([5,1],[0,0])
pylab.plot(time, [0]*len(time), "--", color="black")
pylab.plot(time, [1]*len(time), "--", color="black")
pylab.plot(time, x_pos)
pylab.ylim([numpy.min(x_pos)-0.1, numpy.max(x_pos)+0.1])
pylab.xticks([])
pylab.yticks([0.0, 1.0])
pylab.ylabel("Position")
pylab.gca().invert_yaxis()

pylab.subplot2grid([5,1],[1,0], rowspan=2)
pylab.imshow(spikeEsom[:, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spikeEsom[0,0], spikeEsom[-1,0], len(spikeEsom[0,1:]), 1], vmax=som_max, vmin=som_min)
#pylab.colorbar()
pylab.xticks([])
pylab.yticks([1, len(spikeEsom[0,1:])])
pylab.ylabel("CA3 firing rate")

pylab.subplot2grid([5,1],[3,0], rowspan=2)
pylab.imshow(spikeEdnd[:, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spikeEdnd[0,0], spikeEdnd[-1,0], len(spikeEdnd[0,1:]), 1], vmin=dnd_min)
#pylab.colorbar()
pylab.yticks([1, len(spikeEsom[0,1:])])
pylab.xlabel("Time [s]")
pylab.ylabel("Dendritic activity")

pylab.tight_layout()
pylab.savefig("spike.pdf")
