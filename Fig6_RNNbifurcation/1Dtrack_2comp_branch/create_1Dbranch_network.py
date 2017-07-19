#!/usr/bin/env python3

import sys
import numpy
import csv

#neurons
exc_neuron_num=int(sys.argv[1])
input_neuron_num=int(sys.argv[2])
cell_branch1=250
connection_point=100

#soma exc synapse
EEmax=20.0
EEwidth=5.0
EEmax_branch=18.0
EEwidth_branch=5.0

EEdistalmax=2.0

AMPA_NMDA_ratio=0.05

#som<-som
x=numpy.arange(exc_neuron_num)
y=numpy.arange(exc_neuron_num)
z=numpy.meshgrid(x,y)
WEE=EEmax*numpy.exp(-0.5*((z[1]-z[0])/EEwidth)**2)
for i in range(connection_point):
    for j in range(connection_point, cell_branch1):
        dist=numpy.abs(i-j)
        WEE[i,j]=EEmax_branch*numpy.exp(-0.5*(dist/EEwidth_branch)**2)
        WEE[j,i]=WEE[i,j]
    for j in range(cell_branch1, exc_neuron_num):
        dist=numpy.abs(i+1-connection_point)+(j+1-cell_branch1)
        WEE[i,j]=EEmax_branch*numpy.exp(-0.5*(dist/EEwidth_branch)**2)
        WEE[j,i]=WEE[i,j]
for i in range(connection_point, cell_branch1):
    for j in range(cell_branch1, exc_neuron_num):
        #dist=numpy.abs(i+1-connection_point)+(j+1-cell_branch1)
        #WEE[i,j]=EEmax_branch*numpy.exp(-0.5*(dist/EEwidth_branch)**2)
        WEE[i,j]=0.0
        WEE[j,i]=WEE[i,j]

WEE[numpy.eye(exc_neuron_num, dtype=bool)]=0.0

WEENMDA=WEE*AMPA_NMDA_ratio
numpy.savetxt("WEEsom_init.csv", WEE, delimiter=",")
numpy.savetxt("WEEsomNMDA_init.csv", WEENMDA, delimiter=",")

#dnd<-input
WEE=EEdistalmax*numpy.random.rand(exc_neuron_num, input_neuron_num)
WEENMDA=WEE*AMPA_NMDA_ratio
#x=numpy.arange(input_neuron_num)
#y=numpy.arange(exc_neuron_num)
#z=numpy.meshgrid(x,y)
#WEE=EEdistalmax*numpy.exp(-0.5*((z[1]-z[0])/EEwidth)**2)
#WEENMDA=WEE*AMPA_NMDA_ratio
numpy.savetxt("WEEdnd_init.csv", WEE, delimiter=",")
numpy.savetxt("WEEdndNMDA_init.csv", WEENMDA, delimiter=",")


#inh synapse
WEIsom_init=4.0
WEIsomGABAB_init=WEIsom_init*0.05
WEIdnd_init=0.0
WEIdndGABAB_init=WEIdnd_init*0.05

WEIsom=WEIsom_init*numpy.ones(exc_neuron_num)
WEIsomGABAB=WEIsomGABAB_init*numpy.ones(exc_neuron_num)
numpy.savetxt("WEIsom_init.csv", WEIsom, delimiter=",")
numpy.savetxt("WEIsomGABAB_init.csv", WEIsomGABAB, delimiter=",")

WEIdnd=WEIdnd_init*numpy.ones(exc_neuron_num)
WEIdndGABAB=WEIdndGABAB_init*numpy.ones(exc_neuron_num)
numpy.savetxt("WEIdnd_init.csv", WEIdnd, delimiter=",")
numpy.savetxt("WEIdndGABAB_init.csv", WEIdndGABAB, delimiter=",")
