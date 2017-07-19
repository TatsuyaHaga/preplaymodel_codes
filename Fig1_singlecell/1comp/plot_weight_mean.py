#!/usr/bin/python

import numpy
import pylab

pylab.rcParams["font.size"]=8
pylab.rcParams["legend.fontsize"]=6
#pylab.rcParams["lines.linewidth"]=1
#pylab.rcParams["axes.linewidth"]=2
#pylab.rcParams["axes.labelsize"]="small"
#pylab.rcParams["axes.labelweight"]="bold"
pylab.rcParams["xtick.major.size"]=0
pylab.rcParams["xtick.minor.size"]=0
pylab.rcParams["ytick.major.size"]=0
pylab.rcParams["ytick.minor.size"]=0
#pylab.rcParams["xtick.direction"]="out"
#pylab.rcParams["ytick.direction"]="out"
pylab.rcParams["figure.figsize"]=(2, 2.5)

#weight
Wsom=numpy.loadtxt("Wsom.csv", delimiter=",")
Wdnd=numpy.loadtxt("Wdnd.csv", delimiter=",")
group1_num=10
wmax=10.0

mean1=numpy.mean(Wsom[:,1:group1_num+1], axis=1)
mean2=numpy.mean(Wsom[:,group1_num+1:], axis=1)
std1=numpy.std(Wsom[:,1:group1_num+1], axis=1)
std2=numpy.std(Wsom[:,group1_num+1:], axis=1)

pylab.clf()
pylab.subplot(2,1,1)
pylab.plot(Wsom[:,0], mean1, color="blue", label="group A")
pylab.plot(Wsom[:,0], mean2, color="red", label="group B")
pylab.fill_between(Wsom[:,0], mean1-std1, mean1+std1, color="blue", alpha=0.5)
pylab.fill_between(Wsom[:,0], mean2-std2, mean2+std2, color="red", alpha=0.5)
pylab.ylabel("Weight (som)")
pylab.xlabel("Time [s]")
pylab.legend(loc="upper left")
pylab.xticks([0, 300, 600, 900])
pylab.ylim([0.0, wmax])
pylab.yticks([0.0, wmax])

pylab.tight_layout()
pylab.savefig("weight_mean.pdf")
