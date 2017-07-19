#!/usr/bin/env python3

import sys
import csv
import numpy

def placecell_func(X, Y, max_rate, width):
    return max_rate*numpy.exp(-0.5*(X-centerX)**2/width**2)

out=csv.writer(sys.stdout, delimiter=",")
f_pos=open("position.csv", "w")
out_pos=csv.writer(f_pos, delimiter=",")
f_save=open("input.csv", "w")
out_save=csv.writer(f_save, delimiter=",")
f_DG=open("DGactivity.csv", "w")
out_DG=csv.writer(f_DG, delimiter=",")

NE=int(sys.argv[1])
sim_len_sec=float(sys.argv[2])
samp_pitch=float(sys.argv[3])
sim_len=int(sim_len_sec*1000.0/samp_pitch)
save_len=10

theta_amp=1.0
theta_amp_input=0.5
theta_bias_input=-0.5

#run
x=0.0
y=0.0
run_start=5.0*1000.0
run_end=10.0*1000.0

#DG
DGinput=0.5
DGspont_rate=1.0/1000.0
DGtime=10.0*samp_pitch
NDG=10
DGregion=0.05

DGsw=0.0
DGsave=0
data=numpy.zeros(NE+1)
for t in range(1, sim_len+1):
    time_ms=float(t)*samp_pitch
    
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

    #activity
    if moving:
        theta_osc=numpy.sin(2.0*numpy.pi*time_ms/1000.0*7.0)
        data[:NE]=theta_amp*theta_osc
        if x<DGregion:
            DGsave=1
            data[0:NDG]=data[0:NDG]+DGinput
            data[NDG:NE]=data[NDG:NE]-DGinput
    else:
        data[:NE]=0.0
        if x<DGregion and numpy.random.rand()<DGspont_rate*samp_pitch:
            DGsw=DGtime
        if DGsw>0:
            DGsave=1
            data[0:NDG]=data[0:NDG]+DGinput
            data[NDG:NE]=data[NDG:NE]-DGinput
            DGsw=DGsw-samp_pitch
    data[-1]=moving
    
    out.writerow(data)
    if t%save_len==0:
        out_pos.writerow([x,y]); f_pos.flush();
        out_save.writerow(data[:NE+1]); f_save.flush();
        out_DG.writerow([DGsave]); f_DG.flush();
        DGsave=0
