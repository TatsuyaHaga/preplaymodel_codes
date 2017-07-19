#!/usr/bin/env python3

import sys
import numpy

Ninput=int(sys.argv[1])

input_conf=numpy.zeros([Ninput,4])
input_conf[:,0]=numpy.random.rand(Ninput) #centerX
input_conf[:,1]=0.0 #centerY
input_conf[:,2]=0.5 #max_rate_place
input_conf[:,3]=0.1 #width_place

numpy.savetxt("input_conf.csv", input_conf, delimiter=",")
