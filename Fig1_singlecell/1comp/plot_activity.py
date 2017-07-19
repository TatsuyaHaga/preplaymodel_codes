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

#activity
activity=numpy.loadtxt("activity.csv", delimiter=",")

plot_start=-499

pylab.clf()
pylab.subplot(3,1,1)
pylab.plot(activity[plot_start:, 0], activity[plot_start:, 1])
pylab.ylabel("Soma")
pylab.xticks([])
#pylab.xlabel("time [s]")
pylab.ylim([0.0, 1.0])
pylab.yticks([0.0, 1.0])

pylab.subplot(3,1,2)
pylab.plot(activity[plot_start:, 0], activity[plot_start:, 2])
pylab.ylabel("Dendrite")
pylab.xticks([])
#pylab.xlabel("time [s]")
pylab.ylim([0.0, 1.0])
pylab.yticks([0.0, 1.0])

pylab.subplot(3,1,3)
pylab.plot(activity[plot_start:, 0], activity[plot_start:, 3])
pylab.xticks([round(activity[plot_start, 0]), round(activity[-1, 0])])
pylab.ylim([0.0, 0.16])
pylab.yticks([0.0, 0.16])
pylab.ylabel("Output [kHz]")
pylab.xlabel("Time [s]")

pylab.tight_layout()
pylab.savefig("activity.pdf")

#mean activity
mean_win=60.0 #[s]
mean_len=int(numpy.ceil(activity[-1,0]/mean_win))
time_mean=numpy.arange(0.0, mean_len*mean_win/60.0, mean_win/60.0)
mean_win=int(mean_win/(activity[1,0]-activity[0,0]))

pylab.clf()

mean=numpy.zeros(mean_len)
for i in range(mean_len):
    mean[i]=numpy.mean(activity[i*mean_win:(i+1)*mean_win,1])
pylab.subplot(2,1,1)
pylab.plot(time_mean, mean, color="black")
#pylab.plot(time_mean, [10.0/1000.0]*len(mean), "--", color="gray")
#pylab.xlabel("Time [m]")
pylab.xticks([])
pylab.ylabel("Distal [kHz]")
pylab.ylim([0.0, 1.0])

mean=numpy.zeros(mean_len)
for i in range(mean_len):
    mean[i]=numpy.mean(activity[i*mean_win:(i+1)*mean_win,2])
pylab.subplot(2,1,2)
pylab.plot(time_mean, mean, color="black")
#pylab.plot(time_mean, [10.0/1000.0]*len(mean), "--", color="gray")
#pylab.xlabel("Time [m]")
pylab.ylabel("Soma [kHz]")
pylab.ylim([0.0, 1.0])

pylab.tight_layout()
pylab.savefig("mean.pdf")
