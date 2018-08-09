#!/usr/bin/env python3

from shared_setting import *
import sys
import numpy

input_per_arm=int(Ninput//3)
x_max=0.55
x_min=-0.05

input_conf=numpy.zeros([Ninput,4])
input_conf[:,0]=(x_max-x_min)*numpy.random.rand(Ninput)+x_min #centerX
input_conf[:,2]=5.0 #max_rate_place
input_conf[:,3]=0.1 #width_place

#centerY
input_conf[0:input_per_arm,1]=0
input_conf[input_per_arm:2*input_per_arm,1]=1
input_conf[2*input_per_arm:3*input_per_arm,1]=2

numpy.savetxt("input_conf.csv", input_conf, delimiter=",")
