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
group_name=["A", "B", "C", "D"]

pylab.clf()
for count in range(neuron_num):
    Wdnd_plot=Wdnd[:,count*input_num:(count+1)*input_num]
    
    pylab.subplot(neuron_num,1,count+1)
    for n in range(group_num):
        mean1=numpy.mean(Wdnd_plot[:,n*cell_per_group:(n+1)*cell_per_group], axis=1)
        std1=numpy.std(Wdnd_plot[:,n*cell_per_group:(n+1)*cell_per_group], axis=1)
        pylab.plot(time, mean1, color=color_arr[n], label="Group "+group_name[n])
        pylab.fill_between(time, mean1-std1, mean1+std1, color=color_arr[n], alpha=0.5)
        pylab.ylabel("Neuron "+str(count+1)+"\nweight (dnd)")
        pylab.legend(loc="upper left")
        pylab.ylim([0.0, 40.0])
        pylab.yticks([0.0, 40.0])
        if count+1==neuron_num:
            pylab.xlabel("Time [s]")
            pylab.xticks([0, 600, 1200, 1800])
        else:
            pylab.xticks([])

pylab.tight_layout()
pylab.savefig("weight_mean_dnd.pdf")
