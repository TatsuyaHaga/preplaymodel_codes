#!/usr/bin/env python3

import sys
import csv
import numpy

def placecell_func(X, Y, max_rate, width):
    return max_rate*numpy.exp(-0.5*(X-centerX[inputconf_num])**2/width**2)

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
input_conf1=numpy.loadtxt("input_conf1.csv", delimiter=",")
input_conf2=numpy.loadtxt("input_conf2.csv", delimiter=",")
centerX=[input_conf1[:,0], input_conf2[:,0]]
centerY=[input_conf1[:,1], input_conf2[:,1]]
max_rate_place=[input_conf1[:,2], input_conf2[:,2]]
width_place=[input_conf1[:,3], input_conf2[:,3]]

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

#DG
DGinput=0.5
DGspont_rate=1.0/1000.0
DGtime=10.0*samp_pitch
NDG=10
DGregion=0.05

DGsw=0.0
DGsave=0
inputconf_num=0
data=numpy.zeros(NE+Ninput+1)
for t in range(1, sim_len+1):
    time_ms=float(t)*samp_pitch        
    
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

    #spont_activity
    spont_input=spont_input+samp_pitch*(-spont_input/tau_spont+input_noise_amp*numpy.random.randn(Ninput))
    
    #activity
    if moving:
        theta_osc=numpy.sin(2.0*numpy.pi*time_ms/1000.0*7.0)
        data[:NE]=theta_amp*theta_osc
        data[NE:NE+Ninput]=theta_amp_input*theta_osc+theta_bias_input+placecell_func(x, y, max_rate_place[inputconf_num], width_place[inputconf_num])
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
