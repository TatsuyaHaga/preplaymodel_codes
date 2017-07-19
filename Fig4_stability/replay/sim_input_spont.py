#!/usr/bin/env python3

import sys
import csv
import numpy

out=csv.writer(sys.stdout, delimiter=",")
f_pos=open("position.csv", "w")
out_pos=csv.writer(f_pos, delimiter=",")
f_save=open("input.csv", "w")
out_save=csv.writer(f_save, delimiter=",")
f_DG=open("DGactivity.csv", "w")
out_DG=csv.writer(f_DG, delimiter=",")

NE=int(sys.argv[1])
Ninput=int(sys.argv[2])
cell_per_arm=int(NE//3)
input_per_arm=int(Ninput//3)
sim_len_sec=float(sys.argv[3])
samp_pitch=float(sys.argv[4])
sim_len=int(sim_len_sec*1000.0/samp_pitch)
save_len=10

#spont activity
RNN_noise_amp=0.0
input_noise_amp=0.05
tau_spont=10.0 #ms
spont_input=numpy.zeros(Ninput)
spont_RNN=numpy.zeros(NE)

#burst
input_burst_amp=0.1
burst_time=200.0
burst_rate=1.0/1000.0
burstsw=0.0

#DG
DGinput=0.5
DGspont_rate=1.0/1000.0
DGtime=10.0*samp_pitch
NDG=10
DGsw=0.0

data=numpy.zeros(NE+Ninput+1)
moving=0
DGsave=0
for t in range(1, sim_len+1):
    time_ms=float(t)*samp_pitch

    #spont_activity
    spont_RNN=spont_RNN+samp_pitch*(-spont_RNN/tau_spont+RNN_noise_amp*numpy.random.randn(NE))
    if burstsw>0:
        spont_input=spont_input+samp_pitch*(-spont_input/tau_spont+input_burst_amp*numpy.random.randn(Ninput))
    else:
        spont_input=spont_input+samp_pitch*(-spont_input/tau_spont+input_noise_amp*numpy.random.randn(Ninput))
        
    #activity
    data[:NE]=spont_RNN
    data[NE:NE+Ninput]=spont_input
    #burst
    if numpy.random.rand()<burst_rate*samp_pitch:
        burstsw=burst_time*samp_pitch
    if burstsw>0:
        burstsw=burstsw-samp_pitch
    #DG
    if numpy.random.rand()<DGspont_rate*samp_pitch:
        DGsw=DGtime
    if DGsw>0:
        DGsave=1
        data[0:NDG]=data[0:NDG]+DGinput
        data[NDG:NE]=data[NDG:NE]-DGinput
        DGsw=DGsw-samp_pitch
    data[-1]=moving
   
    out.writerow(data)
    if t%save_len==0:
        out_save.writerow(data[:NE+Ninput+1]); f_save.flush();
        out_DG.writerow([DGsave]); f_DG.flush();
        DGsave=0
