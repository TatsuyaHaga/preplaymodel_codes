#!/usr/bin/env python3

import sys
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
spikeEdnd=numpy.loadtxt("spike_dnd.csv", delimiter=",")
inhinput=numpy.loadtxt("inhinput_dnd.csv", delimiter=",")

som_max=0.16
som_min=0.0
dnd_max=1.0
dnd_min=0.0
time=spikeEsom[:,0]

pylab.clf()
pylab.figure(figsize=(6,3))

pylab.subplot2grid([4,1],[0,0], rowspan=2)
pylab.imshow(spikeEsom[:, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spikeEsom[0,0], spikeEsom[-1,0], len(spikeEsom[0,1:]), 1], vmax=som_max, vmin=som_min)
#limit=numpy.max(numpy.abs(xE[:,1:]))
#pylab.clim([-limit, limit])
#pylab.colorbar()
pylab.xticks([])
#pylab.xlabel("time [s]")
pylab.ylabel("neuron #")

pylab.subplot2grid([4,1],[2,0], rowspan=2)
pylab.imshow(spikeEdnd[:, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spikeEdnd[0,0], spikeEdnd[-1,0], len(spikeEdnd[0,1:]), 1], vmax=dnd_max, vmin=dnd_min)
#limit=numpy.max(numpy.abs(xE[:,1:]))
#pylab.clim([-limit, limit])
#pylab.colorbar()
pylab.xlabel("time [s]")
pylab.ylabel("neuron #")

pylab.tight_layout()
pylab.savefig("spike.pdf")

#part
part_len=10*100
part_num=int(len(spikeEsom[:,0])//part_len)
for i in range(part_num):
    pylab.clf()
    pylab.figure(figsize=(3.5,3))
    pylab.subplot(3,1,1)
    pylab.imshow(spikeEsom[i*part_len:(i+1)*part_len, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spikeEsom[i*part_len,0], spikeEsom[(i+1)*part_len-1,0], len(spikeEsom[0,1:]), 1], vmax=som_max, vmin=som_min)
    pylab.colorbar()
    pylab.xticks([])
    pylab.yticks([1, len(spikeEsom[0,1:])])
    #pylab.xlabel("time [s]")
    pylab.ylabel("CA3 firing rate")
    
    pylab.subplot(3,1,2)
    pylab.imshow(spikeEdnd[i*part_len:(i+1)*part_len, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spikeEdnd[i*part_len,0], spikeEdnd[(i+1)*part_len-1,0], len(spikeEdnd[0,1:]), 1], vmax=dnd_max, vmin=dnd_min)
    pylab.colorbar()
    pylab.xticks([])
    pylab.yticks([1, len(spikeEsom[0,1:])])
    #pylab.xlabel("time [s]")
    pylab.ylabel("dendritic\nactivity")

    pylab.subplot(3,1,3)
    pylab.imshow(inhinput[i*part_len:(i+1)*part_len, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[inhinput[i*part_len,0], inhinput[(i+1)*part_len-1,0], len(inhinput[0,1:]), 1], vmin=0.0)
    pylab.colorbar()
    pylab.yticks([1, len(spikeEsom[0,1:])])
    pylab.xlabel("time [s]")
    pylab.ylabel("inhibitory inputs\nto dendrites")
    
    pylab.tight_layout()
    pylab.savefig("spike_part"+str(i)+".pdf")
