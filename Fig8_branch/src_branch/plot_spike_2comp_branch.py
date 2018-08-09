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

som_min=0.0
som_max=0.16
dnd_min=0.0
dnd_max=1.0
line1=100
line2=250

cellnum=spikeEsom.shape[1]-1

pylab.clf()
pylab.figure(figsize=(6,3))
pylab.subplot(2,1,1)
pylab.imshow(spikeEdnd[:, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spikeEdnd[0,0], spikeEdnd[-1,0], len(spikeEdnd[0,1:]), 1], vmax=dnd_max, vmin=dnd_min)
pylab.plot(spikeEsom[:,0], [line1]*len(spikeEsom[:,0]), "--", color="white")
pylab.plot(spikeEsom[:,0], [line2]*len(spikeEsom[:,0]), "--", color="white")
#limit=numpy.max(numpy.abs(xE[:,1:]))
#pylab.clim([-limit, limit])
pylab.colorbar()
pylab.xticks([])
#pylab.xlabel("Time [s]")
pylab.ylabel("Dendritic activity")

pylab.subplot(2,1,2)
pylab.imshow(spikeEsom[:, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spikeEsom[0,0], spikeEsom[-1,0], len(spikeEsom[0,1:]), 1], vmax=som_max, vmin=som_min)
pylab.plot(spikeEsom[:,0], [line1]*len(spikeEsom[:,0]), "--", color="white")
pylab.plot(spikeEsom[:,0], [line2]*len(spikeEsom[:,0]), "--", color="white")
#limit=numpy.max(numpy.abs(xE[:,1:]))
#pylab.clim([-limit, limit])
#pylab.xticks([])
pylab.colorbar()
pylab.xlabel("Time [s]")
pylab.ylabel("CA3 firing rate")

pylab.tight_layout()
pylab.savefig("spike_forpaper.pdf")

#part
for i in range(4):
    if i==0:
        start=0*100
        end=20*100
    elif i==1:
        start=60*100
        end=75*100
    elif i==2:
        start=80*100
        end=100*100
    elif i==3:
        start=140*100
        end=155*100
    spikeEsom_part=spikeEsom[start:end, :]
    spikeEdnd_part=spikeEdnd[start:end, :]

    pylab.clf()
    pylab.figure(figsize=(3.5,3))
    pylab.subplot(2,1,1)
    pylab.imshow(spikeEdnd_part[:,1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spikeEdnd_part[0,0], spikeEdnd_part[-1,0], len(spikeEdnd_part[0,1:]), 1], vmax=dnd_max, vmin=dnd_min)
    pylab.plot(spikeEdnd_part[:,0], [line1]*len(spikeEdnd_part[:,0]), "--", color="white")
    pylab.plot(spikeEdnd_part[:,0], [line2]*len(spikeEdnd_part[:,0]), "--", color="white")
    pylab.colorbar()
    pylab.yticks([1, len(spikeEdnd_part[0,1:])])
    pylab.xticks([])
    pylab.xlabel("Time [s]")
    pylab.ylabel("Dendritic\nactivity")
    
    pylab.subplot(2,1,2)
    pylab.imshow(spikeEsom_part[:,1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spikeEsom_part[0,0], spikeEsom_part[-1,0], len(spikeEsom_part[0,1:]), 1], vmax=som_max, vmin=som_min)
    pylab.plot(spikeEsom_part[:,0], [line1]*len(spikeEsom_part[:,0]), "--", color="white")
    pylab.plot(spikeEsom_part[:,0], [line2]*len(spikeEsom_part[:,0]), "--", color="white")
    pylab.colorbar()
    pylab.yticks([1, len(spikeEsom_part[0,1:])])
    #pylab.xticks([])
    pylab.xlabel("Time [s]")
    pylab.ylabel("CA3 firing rate")
    
    pylab.tight_layout()
    pylab.savefig("spike_part"+str(i)+".pdf")
