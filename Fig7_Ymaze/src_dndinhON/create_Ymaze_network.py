#!/usr/bin/env python3

from shared_setting import * 
import sys
import numpy
import csv

#neurons
arm_num=3
cell_per_arm=int(NE//arm_num)

#soma exc synapse
EEmax=20.0
EEwidth=5.0

EEdistalmax=2.0

#som<-som
x=numpy.arange(NE)
y=numpy.arange(NE)
z=numpy.meshgrid(x,y)
WEE=EEmax*numpy.exp(-0.5*((z[1]-z[0])/EEwidth)**2)
for i in range(arm_num):
    for j in range(arm_num):
        if i!=j:
            WEE[i*cell_per_arm:(i+1)*cell_per_arm, j*cell_per_arm:(j+1)*cell_per_arm]=0.0

WEE[numpy.eye(NE, dtype=bool)]=0.0
numpy.savetxt("WEEsom_init.csv", WEE, delimiter=",")

#dnd<-input
WEE=EEdistalmax*numpy.random.rand(NE, Ninput)
numpy.savetxt("WEEdnd_init.csv", WEE, delimiter=",")

#inh synapse
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

