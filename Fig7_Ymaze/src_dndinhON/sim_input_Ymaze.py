#!/usr/bin/env python3

from shared_setting import *
import sys
import csv
import numpy

def placecell_func(arm, X, Y, max_rate, width):
    return (centerY==arm)*max_rate*numpy.exp(-0.5*(X-centerX)**2/width**2)

phi_input=80.0/1000.0
thr_sig=5.0
def sigmoid(x):
    return phi_input/(1.0+numpy.exp(-(x-thr_sig)))

out=csv.writer(sys.stdout, delimiter=",")
f_pos=open("position.csv", "w")
out_pos=csv.writer(f_pos, delimiter=",")
f_save=open("input.csv", "w")
out_save=csv.writer(f_save, delimiter=",")

#param
sim_len=int(sim_len_sec*1000.0/time_pitch)
save_len=10

cell_per_arm=int(NE//3)
input_per_arm=int(Ninput//3)
arm_len=0.5

theta_amp=10.0
Inoise_amp=0.1
tau_Inoise=10.0
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

init_len=10.0*1000.0

set_len=10.0*1000.0
time1=2.5*1000.0
time2=5.0*1000.0
time3=7.5*1000.0

#trigger
trig_input=5.0
trig_rate=1.0/1000.0
trig_time=10.0*time_pitch
trig_sw=0.0
Ntrig=10

arm=0.0
data=numpy.zeros(NE+Ninput+1)
for t in range(1, sim_len+1):
    time_ms=float(t)*time_pitch
    
    #motion
    time_set=time_ms%set_len
    if time_ms<=init_len:
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

    Inoise+=time_pitch*(-Inoise/tau_Inoise+Inoise_amp*numpy.random.randn(NE+Ninput))
    #activity
    if moving:
        theta_osc=numpy.sin(2.0*numpy.pi*time_ms/1000.0*7.0)
        data[:NE]=theta_amp*theta_osc+Inoise[:NE]
        Iinput=theta_amp*(0.5*theta_osc-0.5)+placecell_func(int(arm), x, y, max_rate_place, width_place)
        data[NE:NE+Ninput]=sigmoid(Iinput+Inoise[NE:NE+Ninput])
        #trigger sequence
        if init_len<=time_ms and time_ms<=init_len+3*set_len and time1<=time_set and time_set<=time1+200.0:
            for i in [0, cell_per_arm, 2*cell_per_arm]:
                data[i:i+Ntrig]+=trig_input
                data[i+Ntrig:i+cell_per_arm]-=trig_input
    else:
        data[:NE]=Inoise[:NE]
        data[NE:NE+Ninput]=sigmoid(Inoise[NE:NE+Ninput])
        if numpy.random.rand()<trig_rate*time_pitch:
            trig_sw=trig_time
        if trig_sw>0:
            for i in [0, cell_per_arm, 2*cell_per_arm]:
                data[i:i+Ntrig]+=trig_input
                data[i+Ntrig:i+cell_per_arm]-=trig_input
            trig_sw-=time_pitch
    data[-1]=moving

    out.writerow(data)
    if t%save_len==0:
        out_pos.writerow([arm+x,y]); f_pos.flush();
        out_save.writerow(data[:NE+Ninput+1]); f_save.flush();
