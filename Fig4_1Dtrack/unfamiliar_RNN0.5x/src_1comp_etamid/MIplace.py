#!/usr/bin/env python3

import sys
import numpy

rate=numpy.loadtxt(sys.argv[1], delimiter=",")
rate=rate[:,1:]*1000.0 #kHz -> Hz
pos=numpy.loadtxt(sys.argv[2], delimiter=",")
pos=pos[:,0]

data_len, neuron_num=rate.shape
bin_num=50
rate_threshold=5.0

moving=numpy.zeros_like(pos, dtype=bool)
for t in range(1,data_len):
    if pos[t]!=pos[t-1]:
        moving[t]=True

mean_rate=numpy.mean(rate[moving], axis=0).reshape([1,neuron_num])

pos_max=numpy.max(pos)
pos_min=numpy.min(pos)
pos_bins=numpy.arange(pos_min, pos_max, (pos_max-pos_min)/bin_num)
pos_prob=numpy.zeros([bin_num,1])
mean_rate_pos=numpy.zeros([bin_num, neuron_num])

for n in range(bin_num):
    if n==bin_num-1:
        filt=(pos_bins[n]<=pos)*moving
    else:
        filt=(pos_bins[n]<=pos)*(pos<pos_bins[n+1])*moving
    pos_prob[n,0]=numpy.sum(filt)/numpy.sum(moving)
    mean_rate_pos[n,:]=numpy.sum(rate[filt,:], axis=0)/numpy.sum(filt)

#information content per spike (bits per spike)
MI=numpy.sum(mean_rate_pos/mean_rate*pos_prob*numpy.log2(mean_rate_pos/mean_rate), axis=0)

numpy.savetxt("MI.csv", numpy.hstack([numpy.mean(MI[mean_rate[0,:]>rate_threshold]),MI]), delimiter=",")
