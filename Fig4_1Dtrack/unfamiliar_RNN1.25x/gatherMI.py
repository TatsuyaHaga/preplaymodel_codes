#/usr/bin/env python3

import numpy

N=3
namebase=["2comp", "1comp_etalow", "1comp_etamid", "1comp_etahigh"]
MI=numpy.zeros([N,len(namebase)])

for i in range(len(namebase)):
    for j in range(N):
        dirname=namebase[i]+"_"+str(j+1)
        MI[j,i]=numpy.loadtxt(dirname+"/MI.csv", delimiter=",")[0]

numpy.savetxt("MIall.csv", MI, delimiter=",")
