#!/usr/bin/env python3

from shared_setting import *
import sys
import csv
import numpy

phi_input=80.0/1000.0
thr_sig=5.0
def sigmoid(x):
    return phi_input/(1.0+numpy.exp(-(x-thr_sig)))

#param
sim_len=int(sim_len_sec*1000.0/time_pitch)
save_len=10

#spont activity
Inoise_amp=0.1
tau_Inoise=10.0
Inoise=numpy.zeros(NE+Ninput)

#burst
burst_amp=0.1
tau_burst=100.0
burst_time=200.0
burst_rate=1.0/1000.0
burstsw=0.0
burst_input=numpy.zeros(Ninput)

#trigger
trig_input=10.0
trig_rate=1.0/1000.0
trig_time=10.0*time_pitch
trig_sw=0.0
Ntrig=10

#output
out=csv.writer(sys.stdout, delimiter=",")
f_save=open("input.csv", "w")
out_save=csv.writer(f_save, delimiter=",")

#simulation
moving=0
data=numpy.zeros(NE+Ninput+1)
for t in range(1, sim_len+1):
    time_ms=float(t)*time_pitch
    
    #spont_activity
    Inoise+=time_pitch*(-Inoise/tau_Inoise+Inoise_amp*numpy.random.randn(NE+Ninput))
    burst_input+=time_pitch*(-burst_input/tau_burst+burst_amp*numpy.random.randn(Ninput))

    #activity
    data[:NE]=Inoise[:NE]
    data[NE:NE+Ninput]=sigmoid((burstsw>0)*burst_input+Inoise[NE:NE+Ninput])
    if numpy.random.rand()<trig_rate*time_pitch:
        trig_sw=trig_time
    if trig_sw>0:
        data[:Ntrig]+=trig_input
        data[Ntrig:NE]-=trig_input
        trig_sw-=time_pitch

    #burst
    if numpy.random.rand()<burst_rate*time_pitch:
        burstsw=burst_time*time_pitch
    if burstsw>0:
        burstsw=burstsw-time_pitch

    data[-1]=moving

    out.writerow(data); sys.stdout.flush();
    if t%save_len==0:
        out_save.writerow(numpy.hstack([time_ms/1000.0, data[NE:NE+Ninput]])); f_save.flush();
