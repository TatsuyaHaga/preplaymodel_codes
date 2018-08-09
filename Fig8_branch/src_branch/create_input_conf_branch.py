#!/usr/bin/env python3

from shared_setting import *
import sys
import numpy

input_conf=numpy.zeros([Ninput,4])
input_conf[:,0]=numpy.random.rand(Ninput) #centerX
input_conf[:,1]=0.0 #centerY
input_conf[:,2]=5.0 #max_rate_place
input_conf[:,3]=0.1 #width_place

numpy.savetxt("input_conf1.csv", input_conf, delimiter=",")

branch_point=0.2
centerX_resamp=branch_point+(1.0-branch_point)*numpy.random.rand(Ninput)
substitute=input_conf[:,0]>=branch_point
input_conf[substitute,0]=centerX_resamp[substitute]
numpy.savetxt("input_conf2.csv", input_conf, delimiter=",")
