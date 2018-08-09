#!/usr/bin/env python3

from shared_setting import *
import numpy
import csv

#soma exc synapse
EEmax=18.0
EEwidth=5.0
EEbias=0.0

EEdistalmax=2.0

w_rand=0.5

#som<-som
x=numpy.arange(NE)
y=numpy.arange(NE)
z=numpy.meshgrid(x,y)
WEE=EEmax*numpy.exp(-0.5*((z[1]-z[0]-EEbias)/EEwidth)**2)+w_rand*numpy.random.randn(NE, NE)
WEE[WEE<0.0]=0.0
WEE[numpy.eye(NE, dtype=bool)]=0.0

numpy.savetxt("WEEsom_init.csv", WEE, delimiter=",")

#dnd<-input
WEE=EEdistalmax*numpy.random.rand(NE, Ninput)
numpy.savetxt("WEEdnd_init.csv", WEE, delimiter=",")

#inh connection
WEIsom_init=4.0
WEIdnd_init=0.0

WEIsom=WEIsom_init*2.0*numpy.random.rand(NE, Nsominh)
numpy.savetxt("WEIsom_init.csv", WEIsom, delimiter=",")

WEIdnd=WEIdnd_init*2.0*numpy.random.rand(NE, Ndndinh)
numpy.savetxt("WEIdnd_init.csv", WEIdnd, delimiter=",")

WIEsom_init=1.0/Nsominh
WIEdnd_init=1.0/Ndndinh

WIEsom=WIEsom_init*2.0*numpy.random.rand(Nsominh, NE)
numpy.savetxt("WIEsom_init.csv", WIEsom, delimiter=",")

WIEdnd=WIEsom_init*2.0*numpy.random.rand(Ndndinh, NE)
numpy.savetxt("WIEdnd_init.csv", WIEdnd, delimiter=",")
