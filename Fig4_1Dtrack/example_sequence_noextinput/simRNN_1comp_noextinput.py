#!/usr/bin/env python3

from shared_setting import *
import sys
import csv
import numpy

threshold=5.0
def sigmoid(x):
    return 1.0/(1.0+numpy.exp(-(x-threshold)))

#parameters
save_pitch=10.0 #ms
save_pitch_weight=60.0*1000.0 #ms

phi=100.0/1000.0 #kHz
tauL=10.0 #ms

tauSTD=500.0 #ms
tauSTF=200.0 #ms
USTF=[0.5, 0.03] #[no Ach, Ach]

#connections
WEEsom=numpy.loadtxt("WEEsom_init.csv", delimiter=",")
WEIsom=numpy.loadtxt("WEIsom_init.csv", delimiter=",")
WIEsom=numpy.loadtxt("WIEsom_init.csv", delimiter=",")

#variables
STDrecur=numpy.ones(NE); 
STFrecur=USTF[0]*numpy.ones(NE)
PSCrecur=numpy.zeros(NE)
Iext_som=numpy.zeros(NE)
Isominh=numpy.zeros(Nsominh)

#save
f_spike_som=open("spike_som.csv", "w")
csv_spike_som=csv.writer(f_spike_som, delimiter=",")

csv_ext=csv.reader(sys.stdin, delimiter=",")

#simulation
moving=0
moving_prev=0
t=0
for ext_input_str in csv_ext:
    #time
    t=t+1
    time_ms=float(t)*time_pitch
    time_sec=time_ms/1000.0
    if time_sec==int(time_sec):
        print(time_sec,"sec")

    #external inputs
    ext_input=numpy.array(list(map(float, ext_input_str)))
    moving_prev=moving
    moving=int(ext_input[NE])
    Iext_som=ext_input[:NE]
    
    #activity
    Isom=WEEsom@PSCrecur-WEIsom@Isominh
    x=sigmoid(Isom+Iext_som)
    z=phi*x
    
    #update output
    output=z*STDrecur*STFrecur
    STDrecur=STDrecur+time_pitch*((1.0-STDrecur)/tauSTD-output)
    STFrecur=STFrecur+time_pitch*((USTF[moving]-STFrecur)/tauSTF+USTF[moving]*z*(1.0-STFrecur))
    PSCrecur=PSCrecur+time_pitch*(-PSCrecur/tauL+output)
    #reset STF when Ach is induced
    if moving==1 and moving_prev==0:
        STFrecur=USTF[1]*numpy.ones(NE)

    #inhibitory inputs
    Isominh[:]=WIEsom@PSCrecur

    #save results
    if time_ms%save_pitch==0:
        temp=numpy.hstack([time_sec, z])
        csv_spike_som.writerow(temp); f_spike_som.flush();
        
