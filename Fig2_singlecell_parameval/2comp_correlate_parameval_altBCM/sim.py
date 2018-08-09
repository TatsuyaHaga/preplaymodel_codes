#!/usr/bin/env python3

import csv
import numpy
import multiprocessing

def sigmoid(x):
    return 1.0/(1.0+numpy.exp(-(x-5.0)))

def sim_func(q,alpha1,alpha2,Nalpha1,Nalpha2):
    #parameters
    time_pitch=1.0 #ms
    save_pitch=10
    save_pitch_weight=1000
    simlen_sec=900.0
    simlen=int(simlen_sec*1000.0/time_pitch)

    tauL=10.0 #ms
    phi=80.0/1000.0
    phi_input=80.0/1000.0
    alpha_som=alpha1
    alpha_dnd=alpha2
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

    som_src=numpy.zeros([som_input_num, input_src_num])
    som_src[:group1_num, 0]=1.0
    som_src[group1_num:, 2]=1.0

    dnd_src=numpy.zeros([dnd_input_num, input_src_num])
    dnd_src[:group1_num,0]=1.0
    dnd_src[group1_num:,3]=1.0

    #simulation
    for t in range(simlen):
        time_sec=float(t)*time_pitch/1000.0
        #if time_sec==int(time_sec):
        #    print(time_sec,"sec")

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

        xamp=(1.0-alpha_som)*x+alpha_som*x*y
        theta_som=c0*Ex*Ex
        deltaWsom+=time_pitch*(-deltaWsom+(xamp*(xamp-theta_som))*(1.0-x)*som_inputPSC)/taudeltaW

        #dnd
        Wdnd+=time_pitch*(eta_dnd*deltaWdnd+Wnoise_amp*numpy.random.randn(dnd_input_num)-eta_Wdecay*Wdnd)
        Wdnd[Wdnd<Wmin]=Wmin

        yamp=(1.0-alpha_dnd)*y+alpha_dnd*x*y
        theta_dnd=c0*Ey*Ey
        deltaWdnd+=time_pitch*(-deltaWdnd+(yamp*(yamp-theta_dnd))*(1.0-y)*dnd_inputPSC)/taudeltaW

        Ex+=time_pitch*(-Ex+xamp)/tau_mean
        Ey+=time_pitch*(-Ey+yamp)/tau_mean

    wdif_som=numpy.sum(Wsom[:group1_num])-numpy.sum(Wsom[group1_num:])
    wdif_dnd=numpy.sum(Wdnd[:group1_num])-numpy.sum(Wdnd[group1_num:])
    q.put((Nalpha1,Nalpha2,wdif_som,wdif_dnd))


if __name__=="__main__":
    alpha1=numpy.arange(0.0,1.0,0.1)
    alpha2=numpy.arange(0.0,1.0,0.1)
    max_process=40

    que=multiprocessing.Queue()
    process_arr=[]
    results=[]
    process_num=0
    for i in range(len(alpha1)):
        for j in range(len(alpha2)):
            print(alpha1[i],alpha2[j])
            process_arr.append(multiprocessing.Process(target=sim_func, args=(que,alpha1[i],alpha2[j],i,j)))
            process_arr[-1].start()
            process_num+=1
            if process_num>=max_process:
                for k in range(process_num):
                    process_arr[k].join()
                for k in range(process_num):
                    tmp=que.get()
                    results.append(tmp)
                process_arr.clear()
                process_num=0

    for i in range(process_num):
        process_arr[i].join()
    for k in range(process_num):
        tmp=que.get()
        results.append(tmp)
    
    numpy.savetxt("alpha_som.csv", alpha1, delimiter=",")
    numpy.savetxt("alpha_dnd.csv", alpha2, delimiter=",")
    numpy.savetxt("wdif.csv", results, delimiter=",")
