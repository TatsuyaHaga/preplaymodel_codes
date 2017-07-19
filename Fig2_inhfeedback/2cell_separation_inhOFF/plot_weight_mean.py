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

#weight
Wsom=numpy.loadtxt("WEsom.csv", delimiter=",")
Wdnd=numpy.loadtxt("WEdnd.csv", delimiter=",")

time=Wsom[:,0]
Wsom=Wsom[:,1:]
Wdnd=Wdnd[:,1:]

neuron_num=2
group_num=2
cell_per_group=10
input_num=int(len(Wsom[0,:])//neuron_num)

color_arr=["b", "r", "y", "g", "k", "c", "m"]

for count in range(neuron_num):
    Wsom_plot=Wsom[:,count*input_num:(count+1)*input_num]
    Wdnd_plot=Wdnd[:,count*input_num:(count+1)*input_num]
    
    #som
    pylab.clf()
    pylab.subplot(2,1,1)
    for n in range(group_num):
        mean1=numpy.mean(Wsom_plot[:,n*cell_per_group:(n+1)*cell_per_group], axis=1)
        std1=numpy.std(Wsom_plot[:,n*cell_per_group:(n+1)*cell_per_group], axis=1)
        pylab.plot(time, mean1, color=color_arr[n], label="Group "+str(n))
        pylab.fill_between(time, mean1-std1, mean1+std1, color=color_arr[n], alpha=0.5)
        pylab.ylabel("Weight (som)")
        #pylab.xlabel("Time [s]")
        pylab.legend(loc="upper left")
        pylab.xticks([])

    #dnd
    pylab.subplot(2,1,2)
    for n in range(group_num):
        mean1=numpy.mean(Wdnd_plot[:,n*cell_per_group:(n+1)*cell_per_group], axis=1)
        std1=numpy.std(Wdnd_plot[:,n*cell_per_group:(n+1)*cell_per_group], axis=1)
        pylab.plot(time, mean1, color=color_arr[n], label="Group "+str(n))
        pylab.fill_between(time, mean1-std1, mean1+std1, color=color_arr[n], alpha=0.5)
        pylab.ylabel("Weight (dnd)")
        pylab.xlabel("Time [s]")
        pylab.legend(loc="upper left")
        pylab.ylim([0.0, 30.0])
        pylab.yticks([0.0, 30.0])
        pylab.xticks([0, 600, 1200, 1800])

    pylab.tight_layout()
    pylab.savefig("weight_mean"+str(count)+".pdf")
