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
data=numpy.loadtxt("sequence_count.csv", delimiter=",")

pylab.clf()
pylab.figure(figsize=(2,2))
for i in range(data.shape[0]):
    pylab.plot([data[i,0]/(data[i,0]+data[i,1]), data[i,2]/(data[i,2]+data[i,3])],".-")
pylab.xlim([-0.5, 1.5])
pylab.xticks([])
pylab.xlabel("before        after")
pylab.ylabel("ratio of sequences\nassociated with inputs")

pylab.tight_layout()
pylab.savefig("plot.pdf")

