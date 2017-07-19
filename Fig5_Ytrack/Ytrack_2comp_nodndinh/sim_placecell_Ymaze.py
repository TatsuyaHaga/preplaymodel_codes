#!/usr/bin/env python3

import sys
import csv
import numpy

def placecell_func(arm, X, Y, max_rate, width):
    return (centerY==arm)*max_rate*numpy.exp(-0.5*(X-centerX)**2/width**2)

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

theta_amp=1.0
theta_amp_input=0.5
theta_bias_input=-0.5

arm_len=0.5

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

init_len=int(10.0*1000.0/samp_pitch)

set_len=10.0*1000.0
time1=2.5*1000.0
time2=5.0*1000.0
time3=7.5*1000.0

#DG
DGinput=1.0
DGspont_rate=1.0/1000.0
DGtime=10.0*samp_pitch
NDG=10
DGregion=0.05

DGsw=0.0
DGsave=0
arm=0.0
data=numpy.zeros(NE+Ninput+1)
for t in range(1, sim_len+1):
    time_ms=float(t)*samp_pitch
    
    #motion
    time_set=time_ms%set_len
    if t<init_len+1:
        x=0.0
        y=0.0
        moving=0
    else:
        if time_set==0:
            arm=arm+1.0 #change arm
            if arm>=3:
                arm=0.0
        if time_set<=time1:
            x=0.0
            y=0.0
            moving=0
        elif time_set<=time2:
            x=arm_len*(time_set-time1)/(time2-time1)
            y=0.0
            moving=1
        elif time_set<=time3:
            x=arm_len
            y=0.0
            moving=0
        elif time_set<set_len:
            x=arm_len*(set_len-time_set)/(set_len-time3)
            y=0.0
            moving=1

    #spont_activity
    spont_input=spont_input+samp_pitch*(-spont_input/tau_spont+input_noise_amp*numpy.random.randn(Ninput))
    
    #activity
    if moving:
        theta_osc=numpy.sin(2.0*numpy.pi*time_ms/1000.0*7.0)
        data[:NE]=theta_amp*theta_osc
        data[NE:NE+Ninput]=theta_amp_input*theta_osc+theta_bias_input+placecell_func(int(arm), x, y, max_rate_place, width_place)
        if x<DGregion:
            DGsave=1
            for i in [0, cell_per_arm, 2*cell_per_arm]:
                data[i:i+NDG]=data[i:i+NDG]+DGinput
                data[i+NDG:i+cell_per_arm]=data[i+NDG:i+cell_per_arm]-DGinput
    else:
        data[:NE]=0.0
        data[NE:NE+Ninput]=spont_input
        if x<DGregion and numpy.random.rand()<DGspont_rate*samp_pitch:
            DGsw=DGtime
        if DGsw>0:
            DGsave=1
            for i in [0, cell_per_arm, 2*cell_per_arm]:
                data[i:i+NDG]=data[i:i+NDG]+DGinput
                data[i+NDG:i+cell_per_arm]=data[i+NDG:i+cell_per_arm]-DGinput
            DGsw=DGsw-samp_pitch
    data[-1]=moving
    
    out.writerow(data)
    if t%save_len==0:
        out_pos.writerow([arm+x,y]); f_pos.flush();
        out_save.writerow(data[:NE+Ninput+1]); f_save.flush();
        out_DG.writerow([DGsave]); f_DG.flush();
        DGsave=0
