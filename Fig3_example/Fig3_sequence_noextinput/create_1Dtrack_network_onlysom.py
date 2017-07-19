#!/usr/bin/env python3

import sys
import numpy
import csv

#neurons
exc_neuron_num=int(sys.argv[1])

#soma exc synapse
EEmax=18.0
EEwidth=5.0
EEbias=0.0

w_rand=0.5

AMPA_NMDA_ratio=0.05

#som<-som
x=numpy.arange(exc_neuron_num)
y=numpy.arange(exc_neuron_num)
z=numpy.meshgrid(x,y)
WEE=EEmax*numpy.exp(-0.5*((z[1]-z[0]-EEbias)/EEwidth)**2)+w_rand*numpy.random.randn(exc_neuron_num, exc_neuron_num)
WEE[WEE<0.0]=0.0
WEE[numpy.eye(exc_neuron_num, dtype=bool)]=0.0

WEENMDA=WEE*AMPA_NMDA_ratio
numpy.savetxt("WEEsom_init.csv", WEE, delimiter=",")
numpy.savetxt("WEEsomNMDA_init.csv", WEENMDA, delimiter=",")

#inh connection
WEIsom_init=4.0
WEIsomGABAB_init=WEIsom_init*0.05

WEIsom=WEIsom_init*numpy.ones(exc_neuron_num)
WEIsomGABAB=WEIsomGABAB_init*numpy.ones(exc_neuron_num)
numpy.savetxt("WEIsom_init.csv", WEIsom, delimiter=",")
numpy.savetxt("WEIsomGABAB_init.csv", WEIsomGABAB, delimiter=",")
