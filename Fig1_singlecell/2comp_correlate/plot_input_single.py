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
pylab.rcParams["figure.figsize"]=(1.5, 2)

#inputs
som_input=numpy.loadtxt("som_input.csv", delimiter=",")
dnd_input=numpy.loadtxt("dnd_input.csv", delimiter=",")

plot_end=1000
y_max=0.08

pylab.clf()

pylab.subplot(4,1,1)
pylab.plot(som_input[:plot_end,0], som_input[:plot_end,1], color="blue")
pylab.ylim([0.0, y_max])
#pylab.yticks([0.0, y_max])
pylab.yticks([])
pylab.xticks([])
pylab.ylabel("A")

pylab.subplot(4,1,2)
pylab.plot(som_input[:plot_end,0], som_input[:plot_end,11], color="red")
pylab.ylim([0.0, y_max])
#pylab.yticks([0.0, y_max])
pylab.yticks([])
pylab.xticks([])
pylab.ylabel("B")

pylab.subplot(4,1,3)
pylab.plot(dnd_input[:plot_end,0], dnd_input[:plot_end,1], color="blue")
pylab.ylim([0.0, y_max])
#pylab.yticks([0.0, y_max])
pylab.yticks([])
pylab.xticks([])
pylab.ylabel("A'")

pylab.subplot(4,1,4)
pylab.plot(dnd_input[:plot_end,0], dnd_input[:plot_end,11], color="red")
pylab.ylim([0.0, y_max])
#pylab.yticks([0.0, y_max])
pylab.yticks([])
pylab.xticks([round(dnd_input[0,0]), round(dnd_input[plot_end,0])])
pylab.ylabel("B'")
pylab.xlabel("Time [s]")

pylab.tight_layout()
pylab.savefig("input_single.pdf")
