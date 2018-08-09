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

#param
sim_len=int(sim_len_sec*1000.0/time_pitch)
save_len=10

isdistractor=numpy.arange(Ninput)>=Ninput-Ndistractor
isinput=numpy.arange(Ninput)<Ninput-Ndistractor

theta_amp=10.0

#spont activity
Inoise_amp=0.1
tau_Inoise=10.0
distractor_noise_amp=0.2
tau_distractor=500.0
spont_distractor=numpy.zeros(Ninput)
Inoise=numpy.zeros(NE+Ninput)

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

set_len=15.0*1000.0
time1=5.0*1000.0
time2=7.5*1000.0
time3=12.5*1000.0

time1_2=10.0*1000.0
time2_2=12.5*1000.0

run_end=run_start+2*set_len

test_len=10.0*1000.0
time1_test=3.0*1000.0
time2_test=6.0*1000.0

#trigger
trig_input=10.0
trig_rate=1.0/1000.0
trig_time=10.0*time_pitch
trig_sw=0.0
Ntrig=10

#output
out=csv.writer(sys.stdout, delimiter=",")
f_pos=open("position.csv", "w")
out_pos=csv.writer(f_pos, delimiter=",")
f_save=open("input.csv", "w")
out_save=csv.writer(f_save, delimiter=",")

#simulation
data=numpy.zeros(NE+Ninput+1)
for t in range(1, sim_len+1):
    time_ms=float(t)*time_pitch
    
    #motion
    if time_ms<=run_start:
        x=0.0
        y=0.0
        moving=0
    elif time_ms<=run_start+set_len:
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
    elif time_ms<=run_start+2*set_len:
        time_set=(time_ms-run_start+set_len)%set_len
        if time_set<=time1_2:
            x=1.0*time_set/time1_2
            y=0.0
            moving=1
        elif time_set<=time2_2:
            x=1.0-1.0*(time_set-time1_2)/(time2_2-time1_2)
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
    spont_distractor+=time_pitch*(-spont_distractor/tau_distractor+distractor_noise_amp*numpy.random.randn(Ninput))
    Inoise+=time_pitch*(-Inoise/tau_Inoise+Inoise_amp*numpy.random.randn(NE+Ninput))

    #activity
    if moving:
        theta_osc=numpy.sin(2.0*numpy.pi*time_ms/1000.0*7.0)
        data[:NE]=theta_osc*theta_amp+Inoise[:NE]
        Iinput=theta_amp*(0.5*theta_osc-0.5)+isinput*placecell_func(x, y, max_rate_place, width_place)+isdistractor*spont_distractor
        data[NE:NE+Ninput]=sigmoid(Iinput+Inoise[NE:NE+Ninput])
        #trigger sequence on first run
        if run_start<=time_ms and time_ms<=run_start+100.0:
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

    out.writerow(data); sys.stdout.flush();
    if t%save_len==0:
        out_pos.writerow([x,y]); f_pos.flush();
        out_save.writerow(numpy.hstack([time_ms/1000.0, data[NE:NE+Ninput]])); f_save.flush();
