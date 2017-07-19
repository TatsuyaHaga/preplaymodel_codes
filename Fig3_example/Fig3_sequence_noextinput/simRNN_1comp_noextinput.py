#!/usr/bin/env python3

import sys
import csv
import numpy

threshold=5.0
def sigmoid(x):
    return 1.0/(1.0+numpy.exp(-(x-threshold)))

#parameters
NE=int(sys.argv[1])
time_pitch=float(sys.argv[2])
save_pitch=10.0 #ms
save_pitch_weight=60.0*1000.0 #ms

phi=90.0/1000.0 #kHz

tauL=10.0 #ms
tauNMDA=150.0 #ms
Inoise_amp=0.1/numpy.sqrt(time_pitch)

tauSTD=500.0 #ms
tauSTF=150.0 #ms
USTF=[0.5, 0.03] #[no Ach, Ach]

#connections
WEsom=numpy.loadtxt("WEEsom_init.csv", delimiter=",")
WEsomNMDA=numpy.loadtxt("WEEsomNMDA_init.csv", delimiter=",")

WIsom=numpy.loadtxt("WEIsom_init.csv", delimiter=",")
WIsomGABAB=numpy.loadtxt("WEIsomGABAB_init.csv", delimiter=",")

#variables
STDrecur=numpy.ones(NE); 
STFrecur=USTF[0]*numpy.ones(NE)
PSCrecur=numpy.zeros(NE)
PSCrecurNMDA=numpy.zeros(NE)
Iext_som=numpy.zeros(NE)

Iinh=0.0
IinhGABAB=0.0

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
    ext_input=list(map(float, ext_input_str))
    moving_prev=moving
    moving=int(ext_input[NE])
    Iext_som=Iext_som+time_pitch*(-Iext_som/tauL+ext_input[:NE]+Inoise_amp*numpy.random.randn(NE))
    
    #activity
    Isom=WEsom@PSCrecur+WEsomNMDA@PSCrecurNMDA-WIsom*Iinh-WIsomGABAB*IinhGABAB+Iext_som
    x=sigmoid(Isom)
    z=phi*x
    
    #update output
    output=z*STDrecur*STFrecur
    STDrecur=STDrecur+time_pitch*((1.0-STDrecur)/tauSTD-output)
    STFrecur=STFrecur+time_pitch*((USTF[moving]-STFrecur)/tauSTF+USTF[moving]*z*(1.0-STFrecur))
    PSCrecur=PSCrecur+time_pitch*(-PSCrecur/tauL+output)
    PSCrecurNMDA=PSCrecurNMDA+time_pitch*(-PSCrecurNMDA/tauNMDA+output)
    #reset STF when Ach is induced
    if moving==1 and moving_prev==0:
        STFrecur=USTF[1]*numpy.ones(NE)

    #inhibitory inputs
    Iinh=numpy.sum(PSCrecur)
    IinhGABAB=numpy.sum(PSCrecurNMDA)

    #save results
    if time_ms%save_pitch==0:
        temp=numpy.hstack([time_sec, z])
        csv_spike_som.writerow(temp); f_spike_som.flush();
        
