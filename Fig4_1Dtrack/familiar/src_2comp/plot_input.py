#!/usr/bin/env python3

import sys
import numpy
import pylab

pylab.rcParams["font.size"]=9
pylab.rcParams["legend.fontsize"]=9
pylab.rcParams["lines.linewidth"]=2
#pylab.rcParams["axes.linewidth"]=2
#pylab.rcParams["axes.labelsize"]="large"
pylab.rcParams["axes.labelweight"]="bold"
pylab.rcParams["xtick.major.size"]=0
pylab.rcParams["xtick.minor.size"]=0
pylab.rcParams["ytick.major.size"]=0
pylab.rcParams["ytick.minor.size"]=0
#pylab.rcParams["xtick.direction"]="out"
#pylab.rcParams["ytick.direction"]="out"
#pylab.rcParams["figure.figsize"]=(3, 3)

#activity
colormap="hot" #"jet", "bwr"

spike=numpy.loadtxt(sys.argv[1], delimiter=",")
time=spike[:,0]

pos=numpy.loadtxt(sys.argv[2], delimiter=",")
x_pos=pos[:,0]

pylab.clf()
pylab.figure(figsize=(3,3))
pylab.subplot2grid([3,1],[0,0])
pylab.plot(time, [0]*len(time), "--", color="black")
pylab.plot(time, [1]*len(time), "--", color="black")
pylab.plot(time, x_pos)#, ".")
pylab.ylim([numpy.min(x_pos)-0.1, numpy.max(x_pos)+0.1])
pylab.yticks([0.0, 0.5, 1.0])
pylab.xticks([])
#pylab.xlabel("time [s]")
pylab.ylabel("position")
pylab.gca().invert_yaxis()

pylab.subplot2grid([3,1],[1,0],rowspan=2)
pylab.imshow(spike[:, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spike[0,0], spike[-1,0], len(spike[0,1:]), 1])
#limit=numpy.max(numpy.abs(xE[:,1:]))
#pylab.clim([-limit, limit])
pylab.colorbar()
pylab.yticks([1, len(spike[0,1:])//2, len(spike[0,1:])])
pylab.xlabel("time [s]")
pylab.ylabel("neuron #")
pylab.tight_layout()
pylab.savefig("input.pdf")
