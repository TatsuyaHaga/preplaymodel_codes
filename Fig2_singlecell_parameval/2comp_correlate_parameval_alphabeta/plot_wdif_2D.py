#!/usr/bin/env python3

import numpy
import matplotlib
matplotlib.use("Agg")
import pylab
import seaborn
seaborn.set(context="paper", style="white", palette="deep")

alpha=numpy.loadtxt("alpha.csv", delimiter=",")
beta=numpy.loadtxt("beta.csv", delimiter=",")
wdif=numpy.loadtxt("wdif.csv", delimiter=",")

wdif2D_som=numpy.zeros([len(beta),len(alpha)])
wdif2D_dnd=numpy.zeros([len(beta),len(alpha)])
for x in wdif:
    wdif2D_som[int(x[1]),int(x[0])]=x[2]
    wdif2D_dnd[int(x[1]),int(x[0])]=x[3]

pylab.close()
pylab.figure(figsize=(6,3))

wdif_max=numpy.max(numpy.abs(wdif2D_som))
pylab.subplot(1,2,1)
pylab.title("Soma")
pylab.imshow(wdif2D_som,aspect="auto",interpolation="none",cmap="seismic",extent=[alpha[0],alpha[-1],beta[-1],beta[0]], vmax=wdif_max, vmin=-wdif_max)
pylab.gca().invert_yaxis()
pylab.xlabel(r"$\alpha$")
pylab.ylabel(r"$\beta$")
pylab.colorbar()

wdif_max=numpy.max(numpy.abs(wdif2D_som))
pylab.subplot(1,2,2)
pylab.title("Dendrite")
pylab.imshow(wdif2D_dnd,aspect="auto",interpolation="none",cmap="seismic",extent=[alpha[0],alpha[-1],beta[-1],beta[0]], vmax=wdif_max, vmin=-wdif_max)
pylab.gca().invert_yaxis()
pylab.xlabel(r"$\alpha$")
pylab.ylabel(r"$\beta$")
pylab.colorbar()

pylab.tight_layout()
pylab.savefig("wdif2D.pdf")
