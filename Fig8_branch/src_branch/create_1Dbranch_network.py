#!/usr/bin/env python3

from shared_setting import *
import sys
import numpy
import csv

#soma exc synapse
EEmax=18.0
EEwidth=5.0
EEmax_branch=14.0
EEwidth_branch=5.0
cell_branch1=250
connection_point=100

EEdistalmax=2.0

#som<-som
x=numpy.arange(NE)
y=numpy.arange(NE)
z=numpy.meshgrid(x,y)
WEE=EEmax*numpy.exp(-0.5*((z[1]-z[0])/EEwidth)**2)
for i in range(connection_point):
    for j in range(connection_point, cell_branch1):
        dist=numpy.abs(i-j)
        WEE[i,j]=EEmax_branch*numpy.exp(-0.5*(dist/EEwidth_branch)**2)
        WEE[j,i]=WEE[i,j]
    for j in range(cell_branch1, NE):
        dist=numpy.abs(i+1-connection_point)+(j+1-cell_branch1)
        WEE[i,j]=EEmax_branch*numpy.exp(-0.5*(dist/EEwidth_branch)**2)
        WEE[j,i]=WEE[i,j]
for i in range(connection_point, cell_branch1):
    for j in range(cell_branch1, NE):
        #dist=numpy.abs(i+1-connection_point)+(j+1-cell_branch1)
        #WEE[i,j]=EEmax_branch*numpy.exp(-0.5*(dist/EEwidth_branch)**2)
        WEE[i,j]=0.0
        WEE[j,i]=WEE[i,j]

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
