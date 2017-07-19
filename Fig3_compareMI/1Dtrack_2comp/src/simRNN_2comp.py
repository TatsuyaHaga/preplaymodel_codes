#!/usr/bin/env python3

import sys
import csv
import numpy

threshold=5.0
def sigmoid(x):
    return 1.0/(1.0+numpy.exp(-(x-threshold)))

#parameters
NE=int(sys.argv[1])
Ninput=int(sys.argv[2])
time_pitch=float(sys.argv[3])
save_pitch=10.0 #ms
save_pitch_weight=60.0*1000.0 #ms

etaEsom=1.0
etaEdnd=1.0
etaIdnd=1.0e-2
alpha=0.9
beta=2.5
gamma=1.0
phi=80.0/1000.0 #kHz

tauL=10.0 #ms
tauNMDA=150.0 #ms
phi_input=80.0/1000.0
taudeltaW=1.0*1000.0 #ms
tauM=60.0*1000.0 #ms
Wmin=0.0
Wnoise_amp=1e-3/numpy.sqrt(time_pitch)
eta_Wdecay=1e-7
r0=0.05
c0=1.0/(6.0*r0**2)
theta_inh=0.5
Inoise_amp=0.1/numpy.sqrt(time_pitch)

tauSTD=500.0 #ms
tauSTF=150.0 #ms
USTF=[0.5, 0.03] #[no Ach, Ach]

#connections
WEsom=numpy.loadtxt("WEEsom_init.csv", delimiter=",")
WEsomNMDA=numpy.loadtxt("WEEsomNMDA_init.csv", delimiter=",")
deltaWEsom=numpy.zeros_like(WEsom)

WEdnd=numpy.loadtxt("WEEdnd_init.csv", delimiter=",")
WEdndNMDA=numpy.loadtxt("WEEdndNMDA_init.csv", delimiter=",")
deltaWEdnd=numpy.zeros_like(WEdnd)

WIsom=numpy.loadtxt("WEIsom_init.csv", delimiter=",")
WIsomGABAB=numpy.loadtxt("WEIsomGABAB_init.csv", delimiter=",")

WIdnd=numpy.loadtxt("WEIdnd_init.csv", delimiter=",")
WIdndGABAB=numpy.loadtxt("WEIdndGABAB_init.csv", delimiter=",")
deltaWIdnd=numpy.zeros_like(WIdnd)

#variables
Ex=r0*numpy.ones(NE); Ey=r0*numpy.ones(NE);
STDrecur=numpy.ones(NE); 
STFrecur=USTF[0]*numpy.ones(NE)
PSCrecur=numpy.zeros(NE)
PSCrecurNMDA=numpy.zeros(NE)
Iext_som=numpy.zeros(NE)
Iext_dnd=numpy.zeros(NE)

Iinh=0.0
IinhGABAB=0.0

Iinput=numpy.zeros(Ninput)
STDinput=numpy.ones(Ninput)
STFinput=USTF[0]*numpy.ones(Ninput)
PSCinput=numpy.zeros(Ninput)
PSCinputNMDA=numpy.zeros(Ninput)

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
WEsom_diagonal=numpy.eye(NE, dtype=bool)
for ext_input_str in csv_ext:
    #time
    t=t+1
    time_ms=float(t)*time_pitch
    time_sec=time_ms/1000.0
    if time_sec==int(time_sec):
        print(time_sec,"sec", numpy.mean(Ex), numpy.mean(Ey))

    #external inputs
    ext_input=list(map(float, ext_input_str))
    moving_prev=moving
    moving=int(ext_input[NE+Ninput])
    Iext_som=Iext_som+time_pitch*(-Iext_som/tauL+ext_input[:NE]+Inoise_amp*numpy.random.randn(NE))
    Iext_dnd=Iext_dnd+time_pitch*(-Iext_dnd/tauL+Inoise_amp*numpy.random.randn(NE))
    Iinput=Iinput+time_pitch*(-Iinput/tauL+ext_input[NE:NE+Ninput]+Inoise_amp*numpy.random.randn(Ninput))
    
    #activity
    inhinput_dnd=WIdnd*Iinh+WIdndGABAB*IinhGABAB
    Idnd=WEdnd@PSCinput+WEdndNMDA@PSCinputNMDA-inhinput_dnd+Iext_dnd
    Isom=WEsom@PSCrecur+WEsomNMDA@PSCrecurNMDA-WIsom*Iinh-WIsomGABAB*IinhGABAB+Iext_som
    y=sigmoid(Idnd)
    x=sigmoid(Isom+beta*y)
    z=(1.0+gamma*y)*phi*x

    #WEsom plasticity
    WEsom=WEsom+time_pitch*(etaEsom*deltaWEsom-eta_Wdecay*WEsom+Wnoise_amp*numpy.random.randn(WEsom.shape[0], WEsom.shape[1]))
    WEsom[WEsom<Wmin]=Wmin
    WEsom[WEsom_diagonal]=0.0
    thetaEsom=c0*Ex*Ex
    deltaWEsom=deltaWEsom+time_pitch*(-deltaWEsom+numpy.outer(((1.0-alpha)*x*(x-thetaEsom)+alpha*x*y)*(1.0-x), PSCrecur))/taudeltaW

    #WEdnd plasticity
    WEdnd=WEdnd+time_pitch*(etaEdnd*deltaWEdnd-eta_Wdecay*WEdnd+Wnoise_amp*numpy.random.randn(WEdnd.shape[0], WEdnd.shape[1]))
    WEdnd[WEdnd<Wmin]=Wmin
    thetaEdnd=c0*Ey*Ey
    deltaWEdnd=deltaWEdnd+time_pitch*(-deltaWEdnd+numpy.outer(((1.0-alpha)*y*(y-thetaEdnd)+alpha*x*y)*(1.0-y), PSCinput))/taudeltaW
    WEdnd[WEdnd<Wmin]=Wmin

    #WIdnd plasticity
    WIdnd=WIdnd+time_pitch*(etaIdnd*deltaWIdnd-eta_Wdecay*WIdnd)
    deltaWIdnd=deltaWIdnd+time_pitch*(-deltaWIdnd+((1.0-alpha)*y*(y-theta_inh)+alpha*x*y)*(1.0-y)*Iinh)/taudeltaW
    WIdnd[WIdnd<Wmin]=Wmin
    
    #update mean
    Ex=Ex+time_pitch*(-Ex+x)/tauM
    Ey=Ey+time_pitch*(-Ey+y)/tauM

    #update input
    input_rate=phi_input*sigmoid(Iinput)
    input_rate_out=input_rate*STDinput*STFinput
    STDinput=STDinput+time_pitch*((1.0-STDinput)/tauSTD-input_rate_out)
    STFinput=STFinput+time_pitch*((USTF[0]-STFinput)/tauSTF+USTF[0]*input_rate*(1.0-STFinput))
    PSCinput=PSCinput+time_pitch*(-PSCinput/tauL+input_rate_out)
    PSCinputNMDA=PSCinputNMDA+time_pitch*(-PSCinputNMDA/tauNMDA+input_rate_out)
    
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
        temp=numpy.hstack([time_sec, input_rate])
        csv_spike_input.writerow(temp); f_spike_input.flush();
        temp=numpy.hstack([time_sec, y])
        csv_spike_dnd.writerow(temp); f_spike_dnd.flush();
        temp=numpy.hstack([time_sec, inhinput_dnd])
        csv_inhinput_dnd.writerow(temp); f_inhinput_dnd.flush();
        
    if t!=0 and time_ms%save_pitch_weight==0:
        numpy.savetxt("WEsom_"+str(int(time_sec))+"s.csv", WEsom, delimiter=",")
        numpy.savetxt("WEdnd_"+str(int(time_sec))+"s.csv", WEdnd, delimiter=",")

numpy.savetxt("WEEsom_end.csv", WEsom, delimiter=",")
numpy.savetxt("WEEsomNMDA_end.csv", WEsomNMDA, delimiter=",")
numpy.savetxt("WEEdnd_end.csv", WEdnd, delimiter=",")
numpy.savetxt("WEEdndNMDA_end.csv", WEdndNMDA, delimiter=",")
numpy.savetxt("WEIsom_end.csv", WIsom, delimiter=",")
numpy.savetxt("WEIsomGABAB_end.csv", WIsomGABAB, delimiter=",")
numpy.savetxt("WEIdnd_end.csv", WIdnd, delimiter=",")
numpy.savetxt("WEIdndGABAB_end.csv", WIdndGABAB, delimiter=",")
