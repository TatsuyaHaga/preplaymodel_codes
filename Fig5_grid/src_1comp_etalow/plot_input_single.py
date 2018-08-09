#!/usr/bin/env python3

import numpy
import pylab

def smooth_spike(x):
    tau=10.0
    m=100
    ret=x/tau/numpy.sqrt(2.0*numpy.pi)
    for t in range(1,m+1):
        ret[:-t,:]=ret[:-t,:]+x[t:,:]*numpy.exp(-0.5*(t/tau)**2)/tau/numpy.sqrt(2.0*numpy.pi)
        ret[t:,:]=ret[t:,:]+x[:-t,:]*numpy.exp(-0.5*(t/tau)**2)/tau/numpy.sqrt(2.0*numpy.pi)
    return ret

pylab.rcParams["font.size"]=8
pylab.rcParams["legend.fontsize"]=8
#pylab.rcParams["lines.linewidth"]=2
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

spike=numpy.loadtxt("input.csv", delimiter=",")
time=spike[:,0]
spike=smooth_spike(spike[:,1:])

pos=numpy.loadtxt("position.csv", delimiter=",")
x_pos=pos[:,0]

plot_arr=(time>=10.0)*(time<=15.0)
time=time[plot_arr]
x_pos=x_pos[plot_arr]
spike=spike[plot_arr,:]

pylab.clf()
pylab.figure(figsize=(2,2))
pylab.subplot(2,1,1)
pylab.plot(time, [0]*len(time), "--", color="black")
pylab.plot(time, [1]*len(time), "--", color="black")
pylab.plot(time, x_pos)#, ".")
pylab.ylim([numpy.min(x_pos)-0.1, numpy.max(x_pos)+0.1])
pylab.yticks([0.0, 0.5, 1.0])
pylab.xticks([])
#pylab.xlabel("time [s]")
pylab.ylabel("Position")
pylab.gca().invert_yaxis()

pylab.subplot(2,1,2)
for i in range(4):
    pylab.plot(time, spike[:,i])
pylab.yticks([])
pylab.xlabel("Time [s]")
pylab.ylabel("Input")

pylab.tight_layout()
pylab.savefig("input_single.pdf")
