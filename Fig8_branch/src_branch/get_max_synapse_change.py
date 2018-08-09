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
before=numpy.loadtxt("WEEsom_init.csv", delimiter=",")
after=numpy.loadtxt("WEEsom_120s.csv", delimiter=",")

dif=after-before
maxdif=numpy.max(dif)
maxbefore=numpy.max(before)
meandif=numpy.mean(numpy.abs(dif))
argmaxdif=numpy.where(dif==maxdif)
maxdif_ratio=maxdif/maxbefore
meandif_ratio=meandif/maxbefore
numpy.savetxt("WEEsom_init_120s_dif.csv", dif, delimiter=",")
numpy.savetxt("WEEsom_init_120s_dif_max.csv", [maxdif, maxdif_ratio, meandif, meandif_ratio], delimiter=",")

