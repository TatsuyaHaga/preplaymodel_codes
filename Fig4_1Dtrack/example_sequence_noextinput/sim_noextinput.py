#!/usr/bin/env python3

from shared_setting import *
import sys
import csv
import numpy

#param
sim_len=int(sim_len_sec*1000.0/time_pitch)
save_len=10

theta_amp=10.0
Inoise_amp=0.1
tau_Inoise=10.0
Inoise=numpy.zeros(NE)

#run
x=0.0
y=0.0
run_start=5.0*1000.0
run_end=10.0*1000.0

#DG
trig_input=10.0
trig_rate=1.0/1000.0
trig_time=10.0*time_pitch
trig_sw=0.0
Ntrig=10

out=csv.writer(sys.stdout, delimiter=",")
f_pos=open("position.csv", "w")
out_pos=csv.writer(f_pos, delimiter=",")

data=numpy.zeros(NE+1)
for t in range(1, sim_len+1):
    time_ms=float(t)*time_pitch
    
    #motion
    if time_ms<=run_start:
        x=0.0
        y=0.0
        moving=0
    elif time_ms<=run_end:
        x=1.0*(time_ms-run_start)/(run_end-run_start)
        y=0.0
        moving=1
    else:
        x=1.0
        y=0.0
        moving=0

    Inoise+=time_pitch*(-Inoise/tau_Inoise+Inoise_amp*numpy.random.randn(NE))
    #activity
    if moving:
        theta_osc=numpy.sin(2.0*numpy.pi*time_ms/1000.0*7.0)
        data[:NE]=theta_amp*theta_osc+Inoise
        if run_start<=time_ms and time_ms<=run_start+50.0:
            data[0:Ntrig]+=trig_input
            data[Ntrig:NE]-=trig_input
    else:
        data[:NE]=Inoise
        if numpy.random.rand()<trig_rate*time_pitch:
            trig_sw=trig_time
        if trig_sw>0:
            data[0:Ntrig]+=trig_input
            data[Ntrig:NE]-=trig_input
            trig_sw-=time_pitch
    data[-1]=moving
    
    out.writerow(data)
    if t%save_len==0:
        out_pos.writerow([x,y]); f_pos.flush();
