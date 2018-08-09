#!/usr/bin/env python3

from shared_setting import *
import numpy
import csv

#soma exc synapse
EEmax=18.0
EEwidth=5.0

#som<-som
x=numpy.arange(NE)
y=numpy.arange(NE)
z=numpy.meshgrid(x,y)
dif=numpy.abs(z[1]-z[0])
WEE=EEmax*numpy.exp(-0.5*(dif/EEwidth)**2)
WEE[WEE<0.0]=0.0
WEE[numpy.eye(NE, dtype=bool)]=0.0

numpy.savetxt("WEEsom_init.csv", WEE, delimiter=",")

#inh connection
WEIsom_init=4.0

WEIsom=numpy.random.rand(NE, Nsominh)
WEIsom=WEIsom_init*WEIsom/numpy.mean(WEIsom, axis=1, keepdims=True)
numpy.savetxt("WEIsom_init.csv", WEIsom, delimiter=",")

WIEsom_init=1.0/Nsominh

WIEsom=numpy.random.rand(Nsominh, NE)
WIEsom=WIEsom_init*WIEsom/numpy.mean(WIEsom, axis=0, keepdims=True)
numpy.savetxt("WIEsom_init.csv", WIEsom, delimiter=",")

