#!/usr/bin/env python3

import csv
import numpy

thr_sig=5.0
def sigmoid(x):
    return 1.0/(1.0+numpy.exp(-(x-thr_sig)))

#parameters
time_pitch=1.0 #ms
save_pitch=10
save_pitch_weight=1000
simlen_sec=1800.0
simlen=int(simlen_sec*1000.0/time_pitch)
neuron_num=2

tauL=10.0 #ms
phi=80.0/1000.0
phi_input=80.0/1000.0
alpha_som=0.9
alpha_dnd=0.9
beta=2.5
gamma=1.0
r0=0.05
c0=1.0/(6.0*r0**2)
etaEsom=0.2
etaEdnd=0.2
etaIdnd=0.0 #0 or 0.2
taudeltaW=1.0*1000.0 #ms
tau_mean=60.0*1000.0
eta_Wdecay=1e-7
Wnoise_amp=1e-3/numpy.sqrt(time_pitch)

Winit=10.0
Winit_inh=20.0
Wmin=0.0

#input config.
input_src_num=2
cell_per_assembly=[0,10,20]
som_input_num=20
dnd_input_num=20
tau_input=10.0 #ms
input_amp=0.1/numpy.sqrt(time_pitch)
noise_amp=0.1/numpy.sqrt(time_pitch)

som_mix=numpy.ones([som_input_num, input_src_num])

dnd_mix=numpy.zeros([dnd_input_num, input_src_num])
for i in range(input_src_num):
    dnd_mix[cell_per_assembly[i]:cell_per_assembly[i+1],i]=1.0

#variables
PSC=numpy.zeros(neuron_num)
inh_input=0.0
Ex=r0*numpy.ones(neuron_num)
Ey=r0*numpy.ones(neuron_num)
input_src=numpy.zeros(input_src_num)
som_input_current=numpy.zeros(som_input_num)
dnd_input_current=numpy.zeros(dnd_input_num)
som_inputPSC=numpy.zeros(som_input_num)
dnd_inputPSC=numpy.zeros(dnd_input_num)
deltaWEsom=numpy.zeros([neuron_num, som_input_num])
deltaWEdnd=numpy.zeros([neuron_num, dnd_input_num])
deltaWIdnd=numpy.zeros(neuron_num)
WEsom=Winit*numpy.random.rand(neuron_num, som_input_num)
WEdnd=Winit*numpy.random.rand(neuron_num, dnd_input_num)
WIsom=Winit_inh*numpy.ones(neuron_num)
WIdnd=numpy.zeros(neuron_num)

#save
f_activity=open("activity.csv", "w")
csv_activity=csv.writer(f_activity, delimiter=",")

f_WEsom=open("WEsom.csv", "w")
csv_WEsom=csv.writer(f_WEsom, delimiter=",")
f_WEdnd=open("WEdnd.csv", "w")
csv_WEdnd=csv.writer(f_WEdnd, delimiter=",")
f_WIdnd=open("WIdnd.csv", "w")
csv_WIdnd=csv.writer(f_WIdnd, delimiter=",")

f_som_input=open("som_input.csv", "w")
csv_som_input=csv.writer(f_som_input, delimiter=",")
f_dnd_input=open("dnd_input.csv", "w")
csv_dnd_input=csv.writer(f_dnd_input, delimiter=",")

f_input_src=open("input_src.csv", "w")
csv_input_src=csv.writer(f_input_src, delimiter=",")

#simulation
for t in range(simlen):
    time_sec=float(t)*time_pitch/1000.0
        
    #source signal
    input_src=input_src+time_pitch*(-input_src/tau_input+input_amp*numpy.random.randn(input_src_num))
    
    #inputs
    som_input_current=som_input_current+time_pitch*(-som_input_current/tauL+som_mix@input_src+noise_amp*numpy.random.randn(som_input_num))
    dnd_induce=dnd_mix@input_src
    dnd_input_current=dnd_input_current+time_pitch*(-dnd_input_current/tauL+dnd_induce+noise_amp*numpy.random.randn(dnd_input_num))
    som_input=phi_input*sigmoid(som_input_current)
    dnd_input=phi_input*sigmoid(dnd_input_current)
    
    som_inputPSC=som_inputPSC+time_pitch*(-som_inputPSC/tauL+som_input)
    dnd_inputPSC=dnd_inputPSC+time_pitch*(-dnd_inputPSC/tauL+dnd_input)

    #neurons
    #dynamics
    Isom=WEsom@som_inputPSC-WIsom*inh_input
    Idnd=WEdnd@dnd_inputPSC-WIdnd*inh_input
    y=sigmoid(Idnd)
    x=sigmoid(Isom+beta*y)
    z=(1.0+gamma*y)*phi*x

    #plasticity
    #som
    WEsom=WEsom+time_pitch*(etaEsom*deltaWEsom-eta_Wdecay*WEsom+Wnoise_amp*numpy.random.randn(WEsom.shape[0],WEsom.shape[1]))
    thetaEsom=c0*Ex*Ex
    deltaWEsom=deltaWEsom+time_pitch*(-deltaWEsom+numpy.outer(((1.0-alpha_som)*x*(x-thetaEsom)+alpha_som*x*y)*(1.0-x),som_inputPSC))/taudeltaW

    #dnd
    WEdnd=WEdnd+time_pitch*(etaEdnd*deltaWEdnd-eta_Wdecay*WEdnd+Wnoise_amp*numpy.random.randn(WEdnd.shape[0],WEsom.shape[1]))
    thetaEdnd=c0*Ey*Ey
    deltaWEdnd=deltaWEdnd+time_pitch*(-deltaWEdnd+numpy.outer(((1.0-alpha_dnd)*y*(y-thetaEdnd)+alpha_dnd*x*y)*(1.0-y), dnd_inputPSC))/taudeltaW

    #dnd inh
    WIdnd=WIdnd+time_pitch*(etaIdnd*deltaWIdnd-eta_Wdecay*WIdnd)
    thetaIdnd=Ey
    deltaWIdnd=deltaWIdnd+time_pitch*(-deltaWIdnd+((1.0-alpha_dnd)*y*(y-thetaIdnd)+alpha_dnd*x*y)*(1.0-y)*inh_input)/taudeltaW

    #restrict weights
    WEsom[WEsom<Wmin]=Wmin
    WEdnd[WEdnd<Wmin]=Wmin
    WIdnd[WIdnd<Wmin]=Wmin
        
    #update output
    PSC=PSC+time_pitch*(-PSC/tauL+z)
    inh_input=numpy.sum(PSC)

    #update mean
    Ex=Ex+time_pitch*(-Ex+x)/tau_mean
    Ey=Ey+time_pitch*(-Ey+y)/tau_mean

    if time_sec==int(time_sec):
        print(time_sec,"sec")

    #save
    if t%save_pitch==0:
        csv_activity.writerow(numpy.hstack([time_sec, numpy.vstack([x,y,z]).T.reshape(neuron_num*3)])); f_activity.flush();
        csv_som_input.writerow(numpy.hstack([time_sec, som_input])); f_som_input.flush();
        csv_dnd_input.writerow(numpy.hstack([time_sec, dnd_input])); f_dnd_input.flush();
        csv_input_src.writerow(numpy.hstack([time_sec, input_src])); f_input_src.flush();
    
    if t%save_pitch_weight==0:
        csv_WEsom.writerow(numpy.hstack([time_sec, WEsom.reshape(neuron_num*som_input_num)])); f_WEsom.flush();
        csv_WEdnd.writerow(numpy.hstack([time_sec, WEdnd.reshape(neuron_num*dnd_input_num)])); f_WEdnd.flush();
        csv_WIdnd.writerow(numpy.hstack([time_sec, WIdnd])); f_WIdnd.flush();
