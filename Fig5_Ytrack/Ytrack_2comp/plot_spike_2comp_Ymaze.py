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
colormap="hot" #"jet", "bwr"

spikeEsom=numpy.loadtxt("spike_som.csv", delimiter=",")
spikeEdnd=numpy.loadtxt("spike_dnd.csv", delimiter=",")
inhinput=numpy.loadtxt("inhinput_dnd.csv", delimiter=",")
DG=numpy.loadtxt("DGactivity.csv", delimiter=",")
time=spikeEsom[:,0]

som_min=0.0
som_max=0.16
dnd_min=0.0
dnd_max=1.0
inh_min=0.0
inh_max=numpy.max(inhinput[:,1:])

cellnum=spikeEsom.shape[1]-1

pre_len=10*100
part_len=30*100
part_num=int(sys.argv[1])

pylab.clf()
pylab.figure(figsize=(3,3))

pylab.subplot2grid([7,1],[0,0], rowspan=1)
pylab.plot(time[:pre_len], DG[:pre_len])
pylab.xticks([])
pylab.ylim([0,1])
pylab.yticks([])
pylab.ylabel("DG")

pylab.subplot2grid([7,1],[1,0], rowspan=2)
spike_part=spikeEdnd[:pre_len, :]
pylab.imshow(spike_part[:, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spike_part[0,0], spike_part[-1,0], len(spike_part[0,1:]), 1], vmax=dnd_max, vmin=dnd_min)
pylab.plot(spike_part[:,0], [cellnum/3]*len(spike_part[:,0]), "--", color="white")
pylab.plot(spike_part[:,0], [2*cellnum/3]*len(spike_part[:,0]), "--", color="white")
#pylab.colorbar()
pylab.xticks([])
pylab.yticks([1, len(spikeEdnd[0,1:])])
#pylab.xlabel("Time [s]")
pylab.ylabel("Dendritic\nactivity")

pylab.subplot2grid([7,1],[3,0], rowspan=2)
spike_part=spikeEsom[:pre_len, :]
pylab.imshow(spike_part[:, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spike_part[0,0], spike_part[-1,0], len(spike_part[0,1:]), 1], vmax=som_max, vmin=som_min)
pylab.plot(spike_part[:,0], [cellnum/3]*len(spike_part[:,0]), "--", color="white")
pylab.plot(spike_part[:,0], [2*cellnum/3]*len(spike_part[:,0]), "--", color="white")
#pylab.colorbar()
pylab.xticks([])
pylab.yticks([1, len(spikeEsom[0,1:])])
#pylab.xlabel("Time [s]")
pylab.ylabel("CA3 firing rate")

pylab.subplot2grid([7,1],[5,0], rowspan=2)
spike_part=inhinput[:pre_len, :]
pylab.imshow(spike_part[:, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spike_part[0,0], spike_part[-1,0], len(spike_part[0,1:]), 1], vmin=inh_min, vmax=inh_max)
#pylab.colorbar()
pylab.plot(spike_part[:,0], [cellnum/3]*len(spike_part[:,0]), "--", color="white")
pylab.plot(spike_part[:,0], [2*cellnum/3]*len(spike_part[:,0]), "--", color="white")
#pylab.xticks([])
pylab.yticks([1, len(inhinput[0,1:])])
pylab.xlabel("Time [s]")
pylab.ylabel("Inhibitory inputs\nto dendrites")

pylab.tight_layout()
pylab.savefig("spike_0.pdf")

#part
for i in range(part_num):
    pylab.clf()
    pylab.figure(figsize=(3,3))

    pylab.subplot2grid([7,1],[0,0], rowspan=1)
    pylab.plot(time[pre_len+i*part_len:pre_len+(i+1)*part_len], DG[pre_len+i*part_len:pre_len+(i+1)*part_len])
    pylab.xticks([])
    pylab.ylim([0,1])
    pylab.yticks([])
    pylab.ylabel("DG")

    pylab.subplot2grid([7,1],[1,0], rowspan=2)
    spike_part=spikeEdnd[pre_len+i*part_len:pre_len+(i+1)*part_len, :]
    pylab.imshow(spike_part[:, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spike_part[0,0], spike_part[-1,0], len(spike_part[0,1:]), 1], vmax=dnd_max, vmin=dnd_min)
    pylab.plot(spike_part[:,0], [cellnum/3]*len(spike_part[:,0]), "--", color="white")
    pylab.plot(spike_part[:,0], [2*cellnum/3]*len(spike_part[:,0]), "--", color="white")
    #pylab.colorbar()
    pylab.xticks([])
    pylab.yticks([1, len(spike_part[0,1:])])
    #pylab.xlabel("Time [s]")
    pylab.ylabel("Dendritic\nactivity")
        
    pylab.subplot2grid([7,1],[3,0], rowspan=2)
    spike_part=spikeEsom[pre_len+i*part_len:pre_len+(i+1)*part_len, :]
    pylab.imshow(spike_part[:,1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spike_part[0,0], spike_part[-1,0], len(spike_part[0,1:]), 1], vmax=som_max, vmin=som_min)
    pylab.plot(spike_part[:,0], [cellnum/3]*len(spike_part[:,0]), "--", color="white")
    pylab.plot(spike_part[:,0], [2*cellnum/3]*len(spike_part[:,0]), "--", color="white")
    #pylab.colorbar()
    pylab.yticks([1, len(spike_part[0,1:])])
    pylab.xticks([])
    #pylab.xlabel("Time [s]")
    pylab.ylabel("CA3 firing rate")

    pylab.subplot2grid([7,1],[5,0], rowspan=2)
    spike_part=inhinput[pre_len+i*part_len:pre_len+(i+1)*part_len, :]
    pylab.imshow(spike_part[:, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spike_part[0,0], spike_part[-1,0], len(spike_part[0,1:]), 1], vmin=inh_min, vmax=inh_max)
    #pylab.colorbar()
    pylab.plot(spike_part[:,0], [cellnum/3]*len(spike_part[:,0]), "--", color="white")
    pylab.plot(spike_part[:,0], [2*cellnum/3]*len(spike_part[:,0]), "--", color="white")
    #pylab.xticks([])
    pylab.yticks([1, len(spike_part[0,1:])])
    pylab.xlabel("Time [s]")
    pylab.ylabel("Inhibitory inputs\nto dendrites")
    
    pylab.tight_layout()
    pylab.savefig("spike_"+str(i+1)+".pdf")
