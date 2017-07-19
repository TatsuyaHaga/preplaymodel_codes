#!/usr/bin/env python3

import csv
import numpy
import scipy.linalg

thr_sig=5.0
def sigmoid(x):
    return 1.0/(1.0+numpy.exp(-(x-thr_sig)))

#parameters
time_pitch=1.0 #ms
save_pitch=10
simlen_sec=60.0
simlen=int(simlen_sec*1000.0/time_pitch)

tauL=10.0 #ms
phi_input=80.0/1000.0

som_input_num=50
dnd_input_num=50
group1_num=10
input_src_num=4
tau_input=10.0 #ms
input_amp=0.1/numpy.sqrt(time_pitch)
noise_amp=0.1/numpy.sqrt(time_pitch)

#variables
input_src=numpy.zeros(input_src_num)
som_input=numpy.zeros(som_input_num)
dnd_input=numpy.zeros(dnd_input_num)
som_input_current=numpy.zeros(som_input_num)
dnd_input_current=numpy.zeros(dnd_input_num)
som_inputLPF=numpy.zeros(som_input_num)
dnd_inputLPF=numpy.zeros(dnd_input_num)

time_vec=numpy.zeros([simlen,1])
signal_som=numpy.zeros([simlen, som_input_num])
signal_dnd=numpy.zeros([simlen, dnd_input_num])

#simulation
som_src=numpy.zeros([som_input_num, input_src_num])
som_src[:group1_num, 0]=1.0
som_src[group1_num:, 2]=1.0

dnd_src=numpy.zeros([dnd_input_num, input_src_num])
dnd_src[:group1_num,0]=1.0
dnd_src[group1_num:,3]=1.0

for t in range(simlen):
    time_ms=float(t)*time_pitch
    if time_ms%1000==0:
        print(time_ms/1000,"sec")

    #source signal
    input_src=input_src+time_pitch*(-input_src/tau_input+input_amp*numpy.random.randn(input_src_num))
    
    #inputs
    som_input_current=som_input_current+time_pitch*(-som_input_current/tauL+som_src@input_src+noise_amp*numpy.random.randn(som_input_num))
    dnd_input_current=dnd_input_current+time_pitch*(-dnd_input_current/tauL+dnd_src@input_src+noise_amp*numpy.random.randn(dnd_input_num))
    
    som_input=phi_input*sigmoid(som_input_current)
    dnd_input=phi_input*sigmoid(dnd_input_current)
    
    som_inputLPF=som_inputLPF+time_pitch*(-som_inputLPF/tauL+som_input)
    dnd_inputLPF=dnd_inputLPF+time_pitch*(-dnd_inputLPF/tauL+dnd_input)

    time_vec[t,0]=time_ms/1000.0
    signal_som[t,:]=som_inputLPF
    signal_dnd[t,:]=dnd_inputLPF
    

#PCA
PCval1, PCcoef1=scipy.linalg.eig(numpy.cov(signal_som.T))
PCval2, PCcoef2=scipy.linalg.eig(numpy.cov(signal_dnd.T))

PCscore1=numpy.dot(signal_som, PCcoef1)
PCscore2=numpy.dot(signal_dnd, PCcoef2)

numpy.savetxt("PCcoef_som.csv", PCcoef1, delimiter=",")
numpy.savetxt("PCcoef_dnd.csv", PCcoef2, delimiter=",")
numpy.savetxt("PCscore_som.csv", numpy.hstack([time_vec, PCscore1]), delimiter=",")
numpy.savetxt("PCscore_dnd.csv", numpy.hstack([time_vec, PCscore2]), delimiter=",")

#CCA
signal_all=numpy.hstack((signal_som, signal_dnd))
cov_all=numpy.cov(signal_all.T)
cov11=cov_all[0:som_input_num, 0:som_input_num]
cov12=cov_all[0:som_input_num, som_input_num:]
cov21=cov_all[som_input_num:, 0:som_input_num]
cov22=cov_all[som_input_num:, som_input_num:]

CCval1, CCcoef1=scipy.linalg.eig(numpy.dot(cov12, numpy.dot(numpy.linalg.inv(cov22),cov12.T)), b=cov11)
CCval2, CCcoef2=scipy.linalg.eig(numpy.dot(cov12.T, numpy.dot(numpy.linalg.inv(cov11),cov12)), b=cov22)

CCscore1=numpy.dot(signal_som, CCcoef1)
CCscore2=numpy.dot(signal_dnd, CCcoef2)

numpy.savetxt("CCcoef_som.csv", CCcoef1, delimiter=",")
numpy.savetxt("CCcoef_dnd.csv", CCcoef2, delimiter=",")
numpy.savetxt("CCscore_som.csv", numpy.hstack([time_vec, CCscore1]), delimiter=",")
numpy.savetxt("CCscore_dnd.csv", numpy.hstack([time_vec, CCscore2]), delimiter=",")
