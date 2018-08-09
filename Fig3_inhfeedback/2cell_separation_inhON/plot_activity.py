#!/usr/bin/python

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
pylab.rcParams["figure.figsize"]=(2, 2.5)

#activity
activity=numpy.loadtxt("activity.csv", delimiter=",")
time=activity[:,0]
activity=activity[:,1:]

neuron_num=int(activity.shape[1]//3)
plot_start=-499

for count in range(neuron_num):
    activity_plot=activity[:,3*count:3*(count+1)]
    
    pylab.clf()
    pylab.subplot(3,1,1)
    pylab.plot(time[plot_start:], activity_plot[plot_start:, 0])
    pylab.ylabel("Soma")
    pylab.xticks([])
    #pylab.xlabel("time [s]")
    pylab.ylim([0.0, 1.0])
    pylab.yticks([0.0, 1.0])

    pylab.subplot(3,1,2)
    pylab.plot(time[plot_start:], activity_plot[plot_start:, 1])
    pylab.ylabel("Dendrite")
    pylab.xticks([])
    #pylab.xlabel("Time [s]")
    pylab.ylim([0.0, 1.0])
    pylab.yticks([0.0, 1.0])

    pylab.subplot(3,1,3)
    pylab.plot(time[plot_start:], activity_plot[plot_start:, 2])
    pylab.xticks([round(time[plot_start]), round(time[-1])])
    pylab.ylim([0.0, 0.16])
    pylab.yticks([0.0, 0.16])
    pylab.ylabel("Output [kHz]")
    pylab.xlabel("Time [s]")

    pylab.tight_layout()
    pylab.savefig("activity"+str(count)+".pdf")
    
