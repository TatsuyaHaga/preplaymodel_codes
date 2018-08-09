#!/usr/bin/env python3

from shared_setting import *
import sys
import numpy

input_conf=numpy.zeros([Ninput,4])
input_conf[:(Ninput-Ndistractor),0]=(1.1*numpy.arange(Ninput-Ndistractor)-0.05)/(Ninput-Ndistractor) #centerX
input_conf[:,1]=0.0 #centerY
input_conf[:,2]=5.0 #max_rate_place
input_conf[:,3]=0.1 #width_place

numpy.savetxt("input_conf.csv", input_conf, delimiter=",")
