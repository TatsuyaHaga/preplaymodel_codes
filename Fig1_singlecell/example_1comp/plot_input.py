#!/usr/bin/python

import numpy
import pylab

pylab.rcParams["font.size"]=8
pylab.rcParams["legend.fontsize"]=6
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
pylab.rcParams["figure.figsize"]=(2, 2.5)

#inputs
som_input=numpy.loadtxt("som_input.csv", delimiter=",")
dnd_input=numpy.loadtxt("dnd_input.csv", delimiter=",")

plot_end=500

pylab.clf()
pylab.subplot(2,1,1)
for i in range(1,som_input.shape[1]):
    pylab.plot(som_input[:plot_end,0], som_input[:plot_end,i])
pylab.ylim([0.0, 0.05])
pylab.yticks([0.0, 0.05])
pylab.xticks([round(som_input[0,0]), round(som_input[plot_end,0])])
pylab.ylabel("Input (soma)")
pylab.xlabel("Time [s]")

pylab.subplot(2,1,2)
for i in range(1,dnd_input.shape[1]):
    pylab.plot(dnd_input[:plot_end,0], dnd_input[:plot_end,i])
pylab.ylim([0.0, 0.05])
pylab.yticks([0.0, 0.05])
pylab.xticks([round(dnd_input[0,0]), round(dnd_input[plot_end,0])])
pylab.ylabel("Input (dendrite)")
pylab.xlabel("Time [s]")

#pylab.xticks([])
#pylab.ylim([0.0, 1.1])
#pylab.yticks([0.0, 1.0])

pylab.tight_layout()
pylab.savefig("input.pdf")
