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
Ninput=int(sys.argv[2])
sim_len_sec=float(sys.argv[3])
samp_pitch=float(sys.argv[4])
sim_len=int(sim_len_sec*1000.0/samp_pitch)
save_len=10

theta_amp=1.0
theta_amp_input=0.5
theta_bias_input=-0.5

#spont activity
input_noise_amp=0.05
tau_spont=10.0 #ms
spont_input=numpy.zeros(Ninput)

#place cell
input_conf=numpy.loadtxt("input_conf.csv", delimiter=",")
centerX=input_conf[:,0]
centerY=input_conf[:,1]
max_rate_place=input_conf[:,2]
width_place=input_conf[:,3]

#motion param
x=0.0
y=0.0
run_start=10.0*1000.0
run_end=25.0*1000.0

set_len=15.0*1000.0
time1=5.0*1000.0
time2=7.5*1000.0
time3=12.5*1000.0

test_len=10.0*1000.0
time1_test=3.0*1000.0
time2_test=6.0*1000.0

#DG
DGinput=0.5
DGspont_rate=1.0/1000.0
DGtime=10.0*samp_pitch
NDG=10
DGregion=0.05

DGsw=0.0
DGsave=0
data=numpy.zeros(NE+Ninput+1)
for t in range(1, sim_len+1):
    time_ms=float(t)*samp_pitch        
    
    #motion
    if time_ms<=run_start:
        x=0.0
        y=0.0
        moving=0
    elif time_ms<=run_end:
        time_set=(time_ms-run_start)%set_len
        if time_set<=time1:
            x=1.0*time_set/time1
            y=0.0
            moving=1
        elif time_set<=time2:
            x=1.0
            y=0.0
            moving=0
        elif time_set<=time3:
            x=1.0-1.0*(time_set-time2)/(time3-time2)
            y=0.0
            moving=1
        else:
            x=0.0
            y=0.0
            moving=0
    else:
        time_set=(time_ms-run_end)%test_len
        if time_set<=time1_test:
            x=0.8*time_set/time1_test
            y=0.0
            moving=1
        elif time_set<=time2_test:
            x=0.8-0.4*(time_set-time1_test)/(time2_test-time1_test)
            y=0.0
            moving=1
        else:
            x=0.4+0.6*(time_set-time2_test)/(test_len-time2_test)
            y=0.0
            moving=1

    #spont_activity
    spont_input=spont_input+samp_pitch*(-spont_input/tau_spont+input_noise_amp*numpy.random.randn(Ninput))
    
    #activity
    if moving:
        theta_osc=numpy.sin(2.0*numpy.pi*time_ms/1000.0*7.0)
        data[:NE]=theta_amp*theta_osc
        data[NE:NE+Ninput]=theta_amp_input*theta_osc+theta_bias_input+placecell_func(x, y, max_rate_place, width_place)
        if x<DGregion:
            DGsave=1
            data[0:NDG]=data[0:NDG]+DGinput
            data[NDG:NE]=data[NDG:NE]-DGinput
    else:
        data[:NE]=0.0
        data[NE:NE+Ninput]=spont_input
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
        out_save.writerow(data[:NE+Ninput+1]); f_save.flush();
        out_DG.writerow([DGsave]); f_DG.flush();
        DGsave=0
