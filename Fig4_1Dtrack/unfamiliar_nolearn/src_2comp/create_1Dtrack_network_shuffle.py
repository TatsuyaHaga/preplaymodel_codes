#!/usr/bin/env python3

from shared_setting import *
import numpy
import csv

#soma exc synapse
EEmax=18.0
EEwidth=5.0

EEdistalmax=5.0
EEdistalwidth=5.0

#som<-som
x=numpy.arange(NE)
y=numpy.arange(NE)
z=numpy.meshgrid(x,y)
dif=numpy.abs(z[1]-z[0])
WEE=EEmax*numpy.exp(-0.5*(dif/EEwidth)**2)
WEE[WEE<0.0]=0.0
WEE[numpy.eye(NE, dtype=bool)]=0.0

numpy.savetxt("WEEsom_init.csv", WEE, delimiter=",")

#dnd<-input
x=numpy.arange(Ninput)
y=numpy.arange(NE)
z=numpy.meshgrid(x,y)
WEE=EEdistalmax*numpy.exp(-0.5*((z[1]-z[0])/EEdistalwidth)**2)
WEE[WEE<0.0]=0.0
for i in range(NE):
    numpy.random.shuffle(WEE[i,:])

numpy.savetxt("WEEdnd_init.csv", WEE, delimiter=",")

#inh connection
WEIsom_init=4.0
WEIdnd_init=0.0

WEIsom=numpy.random.rand(NE, Nsominh)
WEIsom=WEIsom_init*WEIsom/numpy.mean(WEIsom, axis=1, keepdims=True)
numpy.savetxt("WEIsom_init.csv", WEIsom, delimiter=",")

WEIdnd=numpy.random.rand(NE, Ndndinh)
WEIdnd=WEIdnd_init*WEIdnd/numpy.mean(WEIdnd, axis=1, keepdims=True)
numpy.savetxt("WEIdnd_init.csv", WEIdnd, delimiter=",")

WIEsom_init=1.0/Nsominh
WIEdnd_init=1.0/Ndndinh

WIEsom=numpy.random.rand(Nsominh, NE)
WIEsom=WIEsom_init*WIEsom/numpy.mean(WIEsom, axis=0, keepdims=True)
numpy.savetxt("WIEsom_init.csv", WIEsom, delimiter=",")

WIEdnd=numpy.random.rand(Ndndinh, NE)
WIEdnd=WIEdnd_init*WIEdnd/numpy.mean(WIEdnd, axis=0, keepdims=True)
numpy.savetxt("WIEdnd_init.csv", WIEdnd, delimiter=",")

