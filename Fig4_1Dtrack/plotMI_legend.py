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
pylab.figure(figsize=(2,2))
pylab.plot(0, 0, "+", color="blue", label="1-comp. ($\eta=0.1$)", markersize=marker_size)
pylab.plot(0, 1, "x", color="red", label="1-comp. ($\eta=0.5$)", markersize=marker_size)
pylab.plot(0, 2, "^", color="green", label="1-comp. ($\eta=1$)", markersize=marker_size)
pylab.plot(0, 3, "o", color="magenta", label="2-comp.", markersize=marker_size)
pylab.xticks([])
pylab.ylabel("Information per spike [bit]")
pylab.legend(numpoints=1)
pylab.tight_layout()
pylab.savefig("MIlegend.svg")
