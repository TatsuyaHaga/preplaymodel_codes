#!/usr/bin/env python3

import numpy
import matplotlib
matplotlib.use("Agg")
import pylab
import seaborn
seaborn.set(context="paper", style="white", palette="deep")

alpha_som=numpy.loadtxt("alpha_som.csv", delimiter=",")
alpha_dnd=numpy.loadtxt("alpha_dnd.csv", delimiter=",")
wdif=numpy.loadtxt("wdif.csv", delimiter=",")

wdif2D_som=numpy.zeros([len(alpha_dnd),len(alpha_som)])
wdif2D_dnd=numpy.zeros([len(alpha_dnd),len(alpha_som)])
for x in wdif:
    wdif2D_som[int(x[1]),int(x[0])]=x[2]
    wdif2D_dnd[int(x[1]),int(x[0])]=x[3]

pylab.close()
pylab.figure(figsize=(6,3))

wdif_max=numpy.max(numpy.abs(wdif2D_som))
pylab.subplot(1,2,1)
pylab.title("Soma")
pylab.imshow(wdif2D_som,aspect="auto",interpolation="none",cmap="seismic",extent=[alpha_som[0],alpha_som[-1],alpha_dnd[-1],alpha_dnd[0]], vmax=wdif_max, vmin=-wdif_max)
pylab.gca().invert_yaxis()
pylab.xlabel(r"$\alpha_{som}$")
pylab.ylabel(r"$\alpha_{dnd}$")
pylab.colorbar()

wdif_max=numpy.max(numpy.abs(wdif2D_som))
pylab.subplot(1,2,2)
pylab.title("Dendrite")
pylab.imshow(wdif2D_dnd,aspect="auto",interpolation="none",cmap="seismic",extent=[alpha_som[0],alpha_som[-1],alpha_dnd[-1],alpha_dnd[0]], vmax=wdif_max, vmin=-wdif_max)
pylab.gca().invert_yaxis()
pylab.xlabel(r"$\alpha_{som}$")
pylab.ylabel(r"$\alpha_{dnd}$")
pylab.colorbar()

pylab.tight_layout()
pylab.savefig("wdif2D.pdf")
