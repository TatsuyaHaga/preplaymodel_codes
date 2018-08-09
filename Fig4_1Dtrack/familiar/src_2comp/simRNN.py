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

etaEsom=1.0
etaEdnd=1.0
etaIdnd=1.0e-2*Ndndinh
thetainh=0.5

alpha=0.9
beta_som=2.5
beta_dnd=2.5
gamma=1.0
phi=80.0/1000.0 #kHz

tauL=10.0 #ms
taudeltaW=1.0*1000.0 #ms
tauM=60.0*1000.0 #ms
Wmin=0.0
r0=0.05
c0=70.0
eta_Wdecay=1e-7

tauSTD=500.0 #ms
tauSTF=200.0 #ms
USTF=[0.5, 0.03] #[no Ach, Ach]

#connections
WEEsom=numpy.loadtxt("WEEsom_init.csv", delimiter=",")
deltaWEEsom=numpy.zeros_like(WEEsom)

WEEdnd=numpy.loadtxt("WEEdnd_init.csv", delimiter=",")
deltaWEEdnd=numpy.zeros_like(WEEdnd)

WEIsom=numpy.loadtxt("WEIsom_init.csv", delimiter=",")

WEIdnd=numpy.loadtxt("WEIdnd_init.csv", delimiter=",")
deltaWEIdnd=numpy.zeros_like(WEIdnd)

WIEsom=numpy.loadtxt("WIEsom_init.csv", delimiter=",")
WIEdnd=numpy.loadtxt("WIEdnd_init.csv", delimiter=",")

#variables
x=numpy.zeros(NE)
y=numpy.zeros(NE)
Ex=r0*numpy.ones(NE)
Ey=r0*numpy.ones(NE)
STDrecur=numpy.ones(NE) 
STFrecur=USTF[0]*numpy.ones(NE)
PSCrecur=numpy.zeros(NE)
Iext_som=numpy.zeros(NE)
Iext_dnd=numpy.zeros(NE)

Isominh=numpy.zeros(Nsominh)
Idndinh=numpy.zeros(Ndndinh)

Iinput=numpy.zeros(Ninput)
STDinput=numpy.ones(Ninput)
STFinput=USTF[0]*numpy.ones(Ninput)
PSCinput=numpy.zeros(Ninput)

#save
f_spike_som=open("spike_som.csv", "w")
csv_spike_som=csv.writer(f_spike_som, delimiter=",")
f_spike_dnd=open("spike_dnd.csv", "w")
csv_spike_dnd=csv.writer(f_spike_dnd, delimiter=",")
f_spike_input=open("spike_input.csv", "w")
csv_spike_input=csv.writer(f_spike_input, delimiter=",")
f_inhinput_dnd=open("inhinput_dnd.csv", "w")
csv_inhinput_dnd=csv.writer(f_inhinput_dnd, delimiter=",")

csv_ext=csv.reader(sys.stdin, delimiter=",")

#simulation
moving=0
moving_prev=0
t=0
WEEsom_diagonal=numpy.eye(NE, dtype=bool)
for ext_input_str in csv_ext:
    #time
    t=t+1
    time_ms=float(t)*time_pitch
    time_sec=time_ms/1000.0
    if time_sec==int(time_sec):
        print(time_sec,"sec", numpy.mean(Ex), numpy.mean(Ey), file=sys.stderr)

    #external inputs
    ext_input=numpy.array(list(map(float, ext_input_str)))
    moving_prev=moving
    moving=int(ext_input[NE+Ninput])
    Iext_som=ext_input[:NE]
    input_rate=ext_input[NE:NE+Ninput]

    #activity
    inhinput_dnd=WEIdnd@Idndinh
    Idnd=WEEdnd@PSCinput-inhinput_dnd
    Isom=WEEsom@PSCrecur-WEIsom@Isominh
    xprev=x+0.0
    yprev=y+0.0
    y=sigmoid(Idnd+beta_dnd*xprev)
    x=sigmoid(Isom+beta_som*yprev+Iext_som)
    z=(1.0+gamma*y)*phi*x

    #WEEsom plasticity
    WEEsom+=time_pitch*(etaEsom*deltaWEEsom-eta_Wdecay*WEEsom)
    WEEsom[WEEsom<Wmin]=Wmin
    WEEsom[WEEsom_diagonal]=0.0
    thetaEsom=c0*Ex*Ex
    deltaWEEsom+=time_pitch*(-deltaWEEsom+numpy.outer(((1.0-alpha)*x*(x-thetaEsom)+alpha*x*y)*(1.0-x), PSCrecur))/taudeltaW

    #WEEdnd plasticity
    WEEdnd+=time_pitch*(etaEdnd*deltaWEEdnd-eta_Wdecay*WEEdnd)
    WEEdnd[WEEdnd<Wmin]=Wmin
    thetaEdnd=c0*Ey*Ey
    deltaWEEdnd+=time_pitch*(-deltaWEEdnd+numpy.outer(((1.0-alpha)*y*(y-thetaEdnd)+alpha*x*y)*(1.0-y), PSCinput))/taudeltaW

    #WEIdnd plasticity
    WEIdnd+=time_pitch*(etaIdnd*deltaWEIdnd-eta_Wdecay*WEIdnd)
    WEIdnd[WEIdnd<Wmin]=Wmin
    deltaWEIdnd+=time_pitch*(-deltaWEIdnd+numpy.outer(((1.0-alpha)*y*(y-thetainh)+alpha*x*y)*(1.0-y), Idndinh))/taudeltaW
    
    #update mean
    Ex=Ex+time_pitch*(-Ex+x)/tauM
    Ey=Ey+time_pitch*(-Ey+y)/tauM

    #update input
    input_rate_out=input_rate*STDinput*STFinput
    STDinput+=time_pitch*((1.0-STDinput)/tauSTD-input_rate_out)
    STFinput+=time_pitch*((USTF[0]-STFinput)/tauSTF+USTF[0]*input_rate*(1.0-STFinput))
    PSCinput+=time_pitch*(-PSCinput/tauL+input_rate_out)
    
    #update output
    output=z*STDrecur*STFrecur
    STDrecur+=time_pitch*((1.0-STDrecur)/tauSTD-output)
    STFrecur+=time_pitch*((USTF[moving]-STFrecur)/tauSTF+USTF[moving]*z*(1.0-STFrecur))
    PSCrecur+=time_pitch*(-PSCrecur/tauL+output)

    #reset STF when Ach is induced
    if moving==1 and moving_prev==0:
        STFrecur=USTF[1]*numpy.ones(NE)
    
    #inhibitory inputs
    Isominh[:]=WIEsom@PSCrecur
    Idndinh[:]=WIEdnd@PSCrecur

    #save results
    if time_ms%save_pitch==0:
        temp=numpy.hstack([time_sec, z])
        csv_spike_som.writerow(temp); f_spike_som.flush();
        temp=numpy.hstack([time_sec, input_rate])
        csv_spike_input.writerow(temp); f_spike_input.flush();
        temp=numpy.hstack([time_sec, y])
        csv_spike_dnd.writerow(temp); f_spike_dnd.flush();
        temp=numpy.hstack([time_sec, inhinput_dnd])
        csv_inhinput_dnd.writerow(temp); f_inhinput_dnd.flush();
        
    if t!=0 and time_ms%save_pitch_weight==0:
        numpy.savetxt("WEEsom_"+str(int(time_sec))+"s.csv", WEEsom, delimiter=",")
        numpy.savetxt("WEEdnd_"+str(int(time_sec))+"s.csv", WEEdnd, delimiter=",")

numpy.savetxt("WEEsom_end.csv", WEEsom, delimiter=",")
numpy.savetxt("WEEdnd_end.csv", WEEdnd, delimiter=",")
numpy.savetxt("WEIsom_end.csv", WEIsom, delimiter=",")
numpy.savetxt("WEIdnd_end.csv", WEIdnd, delimiter=",")
