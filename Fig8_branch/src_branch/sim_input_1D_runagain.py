#!/usr/bin/env python3

from shared_setting import *
import sys
import csv
import numpy

def placecell_func(X, Y, max_rate, width):
    return max_rate*numpy.exp(-0.5*(X-centerX)**2/width**2)

phi_input=80.0/1000.0
thr_sig=5.0
def sigmoid(x):
    return phi_input/(1.0+numpy.exp(-(x-thr_sig)))

out=csv.writer(sys.stdout, delimiter=",")
f_pos=open("position.csv", "w")
out_pos=csv.writer(f_pos, delimiter=",")
f_save=open("input.csv", "w")
out_save=csv.writer(f_save, delimiter=",")

sim_len=int(sim_len_sec*1000.0/time_pitch)
save_len=10

theta_amp=10.0
Inoise_amp=0.1
tau_Inoise=10.0
Inoise=numpy.zeros(NE+Ninput)

#place cell
input_conf1=numpy.loadtxt("input_conf1.csv", delimiter=",")
input_conf2=numpy.loadtxt("input_conf2.csv", delimiter=",")
centerX_cand=(input_conf1[:,0], input_conf2[:,0])
centerY_cand=(input_conf1[:,1], input_conf2[:,1])
max_rate_place_cand=(input_conf1[:,2], input_conf2[:,2])
width_place_cand=(input_conf1[:,3], input_conf2[:,3])

#motion param
x=0.0
y=0.0
run_start=60.0*1000.0 
run_end=80.0*1000.0
run2_start=140.0*1000.0
run2_end=160.0*1000.0
set_len=20.0*1000.0
time1=0.0*1000.0
time2=5.0*1000.0
time3=10.0*1000.0
time4=15.0*1000.0

#trigger
trig_input=5.0
trig_rate=1.0/1000.0
trig_time=10.0*time_pitch
trig_sw=0.0
Ntrig=10

inputconf_num=0
data=numpy.zeros(NE+Ninput+1)
for t in range(1, sim_len+1):
    time_ms=float(t)*time_pitch        
    
    #motion
    RUN1=(run_start<time_ms and time_ms<run_end)
    RUN2=(run2_start<time_ms and time_ms<run2_end)
    if RUN1:
        inputconf_num=0
    if RUN2:
        inputconf_num=1
    if RUN1 or RUN2:
        time_set=time_ms%set_len
        if time_set<=time1:
            x=0.0
            y=0.0
            moving=0
        elif time_set<=time2:
            x=1.0*(time_set-time1)/(time2-time1)
            y=0.0
            moving=1
        elif time_set<=time3:
            x=1.0
            y=0.0
            moving=0
        elif time_set<=time4:
            x=1.0-1.0*(time_set-time3)/(time4-time3)
            y=0.0
            moving=1
        else:
            x=0.0
            y=0.0
            moving=0
    else:
        x=0.0
        y=0.0
        moving=0

    centerX=centerX_cand[inputconf_num]
    centerY=centerY_cand[inputconf_num]
    max_rate_place=max_rate_place_cand[inputconf_num]
    width_place=width_place_cand[inputconf_num]
    Inoise+=time_pitch*(-Inoise/tau_Inoise+Inoise_amp*numpy.random.randn(NE+Ninput))
    #activity
    if moving:
        theta_osc=numpy.sin(2.0*numpy.pi*time_ms/1000.0*7.0)
        data[:NE]=theta_osc*theta_amp+Inoise[:NE]
        Iinput=theta_amp*(0.5*theta_osc-0.5)+placecell_func(x, y, max_rate_place, width_place)
        data[NE:NE+Ninput]=sigmoid(Iinput+Inoise[NE:NE+Ninput])
        #trigger sequence on first run
        if (run_start<=time_ms and time_ms<=run_start+500.0):
            data[:Ntrig]+=trig_input
            data[Ntrig:NE]-=trig_input
    else:
        data[:NE]=Inoise[:NE]
        data[NE:NE+Ninput]=sigmoid(Inoise[NE:NE+Ninput])
        if numpy.random.rand()<trig_rate*time_pitch:
            trig_sw=trig_time
        if trig_sw>0:
            data[:Ntrig]+=trig_input
            data[Ntrig:NE]-=trig_input
            trig_sw-=time_pitch

    data[-1]=moving
    out.writerow(data)
    if t%save_len==0:
        out_pos.writerow([x,y]); f_pos.flush();
        out_save.writerow(numpy.hstack([time_ms/1000.0, data[NE:NE+Ninput]])); f_save.flush();
