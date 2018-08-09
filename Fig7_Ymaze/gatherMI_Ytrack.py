#/usr/bin/env python3

import numpy

N=5
namebase=["dndinhON", "dndinhOFF"]
MI=numpy.zeros([N,len(namebase)])

for i in range(len(namebase)):
    for j in range(N):
        dirname=namebase[i]+"_"+str(j+1)
        MI[j,i]=numpy.loadtxt(dirname+"/MI.csv", delimiter=",")[0]

numpy.savetxt("MIall.csv", MI, delimiter=",")
