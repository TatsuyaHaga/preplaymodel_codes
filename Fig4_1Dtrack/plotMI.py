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

marker_size=4

pylab.clf()
pylab.figure(figsize=(2.5,2))

dirname=["familiar", "unfamiliar_RNN1x", "unfamiliar_RNN1.25x", "unfamiliar_RNN0.5x", "unfamiliar_nolearn", "unfamiliar_beta0_gamma2", "unfamiliar_beta4_gamma0"]

for i in range(7):
    yarr=[i]*3
    MI=numpy.loadtxt(dirname[i]+"/MIall.csv", delimiter=",")
    if MI.ndim==1:
        pylab.plot(MI, yarr, "o", color="magenta", label="2-comp", markersize=marker_size)
    else:
        pylab.plot(MI[:,0], yarr, "o", color="magenta", label="2-comp", markersize=marker_size)
        pylab.plot(MI[:,1], yarr, "+", color="blue", label="1-comp ($\eta=0.1$)", markersize=marker_size)
        pylab.plot(MI[:,2], yarr, "x", color="red", label="1-comp ($\eta=0.5$)", markersize=marker_size)
        pylab.plot(MI[:,3], yarr, "^", color="green", label="1-comp ($\eta=1$)", markersize=marker_size)

pylab.ylim([-0.5,6.5])
pylab.yticks(range(7), ["familiar", "unfamiliar", "RNN x1.25", "RNN x0.5", "no learning", r"$\beta=0, \gamma=2$", r"$\beta=4, \gamma=0$"])
pylab.xlim([0.0, 2.0])
pylab.xticks([0.0, 1.0, 2.0])
pylab.xlabel("Information per spike [bit]")
#pylab.ylabel("")
pylab.gca().invert_yaxis()
pylab.tight_layout()
pylab.savefig("MI.svg")
