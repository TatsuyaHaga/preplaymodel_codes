#!/usr/bin/env python3

import csv
import numpy

thr_sig=5.0
def sigmoid(x):
    return 1.0/(1.0+numpy.exp(-(x-thr_sig)))

if __name__=="__main__":
    #parameters
    time_pitch=1.0 #ms
    save_pitch=10
    save_pitch_weight=1000
    simlen_sec=900.0
    simlen=int(simlen_sec*1000.0/time_pitch)

    tauL=10.0 #ms
    phi=80.0/1000.0
    phi_input=80.0/1000.0
    alpha_som=0.0
    alpha_dnd=0.0
    beta_som=0.0
    beta_dnd=0.0
    gamma=1.0
    c0=70.0
    eta_som=0.2
    eta_dnd=0.2
    taudeltaW=1.0*1000.0 #ms
    tau_mean=60.0*1000.0
    eta_Wdecay=1e-7
    Wnoise_amp=5e-3/numpy.sqrt(time_pitch)

    som_input_num=50
    dnd_input_num=som_input_num+0
    group1_num=10
    input_src_num=4
    tau_input=10.0 #ms
    input_amp=0.1/numpy.sqrt(time_pitch)
    noise_amp=0.1/numpy.sqrt(time_pitch)

    Winit=5.0
    Wmin=0.0
    E0=0.05

    #variables
    x=0.0
    y=0.0
    Ex=E0
    Ey=E0
    input_src=numpy.zeros(input_src_num)
    som_input_current=numpy.zeros(som_input_num)
    dnd_input_current=numpy.zeros(dnd_input_num)
    som_inputPSC=numpy.zeros(som_input_num)
    dnd_inputPSC=numpy.zeros(dnd_input_num)
    deltaWsom=numpy.zeros(som_input_num)
    deltaWdnd=numpy.zeros(dnd_input_num)
    Wsom=Winit*(numpy.random.rand(som_input_num))
    Wdnd=Winit*(numpy.random.rand(dnd_input_num))

    #save
    f_activity=open("activity.csv", "w")
    csv_activity=csv.writer(f_activity, delimiter=",")

    f_Wsom=open("Wsom.csv", "w")
    csv_Wsom=csv.writer(f_Wsom, delimiter=",")
    f_Wdnd=open("Wdnd.csv", "w")
    csv_Wdnd=csv.writer(f_Wdnd, delimiter=",")

    f_som_input=open("som_input.csv", "w")
    csv_som_input=csv.writer(f_som_input, delimiter=",")
    f_dnd_input=open("dnd_input.csv", "w")
    csv_dnd_input=csv.writer(f_dnd_input, delimiter=",")

    som_src=numpy.zeros([som_input_num, input_src_num])
    som_src[:group1_num, 0]=1.0
    som_src[group1_num:, 2]=1.0

    dnd_src=numpy.zeros([dnd_input_num, input_src_num])
    dnd_src[:group1_num,0]=1.0
    dnd_src[group1_num:,3]=1.0

    #simulation
    for t in range(simlen):
        time_sec=float(t)*time_pitch/1000.0
        if time_sec==int(time_sec):
            print(time_sec,"sec")

        #source signal
        input_src=input_src+time_pitch*(-input_src/tau_input+input_amp*numpy.random.randn(input_src_num))
        
        #inputs
        som_input_current+=time_pitch*(-som_input_current/tauL+som_src@input_src+noise_amp*numpy.random.randn(som_input_num))
        dnd_input_current+=time_pitch*(-dnd_input_current/tauL+dnd_src@input_src+noise_amp*numpy.random.randn(dnd_input_num))
        
        som_input=phi_input*sigmoid(som_input_current)
        dnd_input=phi_input*sigmoid(dnd_input_current)
        
        som_inputPSC+=time_pitch*(-som_inputPSC/tauL+som_input)
        dnd_inputPSC+=time_pitch*(-dnd_inputPSC/tauL+dnd_input)
        
        #dynamics
        xprev=x+0.0
        yprev=y+0.0
        Isom=Wsom@som_inputPSC
        Idnd=Wdnd@dnd_inputPSC
        x=sigmoid(Isom+beta_som*yprev)
        y=sigmoid(Idnd+beta_dnd*xprev)
        z=(1.0+gamma*y)*phi*x

        #plasticity
        #som
        Wsom+=time_pitch*(eta_som*deltaWsom+Wnoise_amp*numpy.random.randn(som_input_num)-eta_Wdecay*Wsom)
        Wsom[Wsom<Wmin]=Wmin

        theta_som=c0*Ex*Ex
        deltaWsom+=time_pitch*(-deltaWsom+((1.0-alpha_som)*x*(x-theta_som)+alpha_som*x*y)*(1.0-x)*som_inputPSC)/taudeltaW

        #dnd
        Wdnd+=time_pitch*(eta_dnd*deltaWdnd+Wnoise_amp*numpy.random.randn(dnd_input_num)-eta_Wdecay*Wdnd)
        Wdnd[Wdnd<Wmin]=Wmin

        theta_dnd=c0*Ey*Ey
        deltaWdnd+=time_pitch*(-deltaWdnd+((1.0-alpha_dnd)*y*(y-theta_dnd)+alpha_dnd*x*y)*(1.0-y)*dnd_inputPSC)/taudeltaW

        Ex+=time_pitch*(-Ex+x)/tau_mean
        Ey+=time_pitch*(-Ey+y)/tau_mean

        if t%save_pitch==0:
            csv_activity.writerow([time_sec, x, y, z]); f_activity.flush();
            csv_som_input.writerow(numpy.hstack([time_sec, som_input])); f_som_input.flush();
            csv_dnd_input.writerow(numpy.hstack([time_sec, dnd_input])); f_dnd_input.flush();
        if t%save_pitch_weight==0:
            csv_Wsom.writerow(numpy.hstack([time_sec, Wsom])); f_Wsom.flush();
            csv_Wdnd.writerow(numpy.hstack([time_sec, Wdnd])); f_Wdnd.flush();
