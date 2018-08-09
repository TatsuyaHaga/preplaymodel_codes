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
pylab.rcParams["figure.figsize"]=(3, 3)

#weight
Wsom=numpy.loadtxt("WEsom.csv", delimiter=",")
Wdnd=numpy.loadtxt("WEdnd.csv", delimiter=",")

time=Wsom[:,0]
Wsom=Wsom[:,1:]
Wdnd=Wdnd[:,1:]

neuron_num=2
input_num=int(len(Wsom[0,:])//neuron_num)

color_arr=["b", "r", "y", "g", "k", "c", "m"]

for count in range(neuron_num):
    Wsom_plot=Wsom[:,count*input_num:(count+1)*input_num]
    Wdnd_plot=Wdnd[:,count*input_num:(count+1)*input_num]
    
    pylab.clf()
    pylab.subplot(2,1,1)
    for i in range(Wsom_plot.shape[1]):
        #n=int(i//cell_per_group)
        pylab.plot(time, Wsom_plot[:,i])#, color=color_arr[n])
    pylab.ylabel("Weight (soma)")
    pylab.xlabel("Time [s]")
    #pylab.legend(loc="upper left")

    pylab.subplot(2,1,2)
    for i in range(Wdnd_plot.shape[1]):
        #n=int(i//cell_per_group)
        pylab.plot(time, Wdnd_plot[:,i])#, color=color_arr[n])
    pylab.ylabel("Weight (dendrite)")
    pylab.xlabel("Time [s]")
    #pylab.legend(loc="upper left")

    pylab.tight_layout()
    pylab.savefig("weight"+str(count)+".pdf")
