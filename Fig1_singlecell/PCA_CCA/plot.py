#!/usr/bin/python

import numpy
import pylab

pylab.rcParams["font.size"]=8
pylab.rcParams["legend.fontsize"]=6
#pylab.rcParams["lines.linewidth"]=1
#pylab.rcParams["axes.linewidth"]=2
#pylab.rcParams["axes.labelsize"]="large"
#pylab.rcParams["axes.labelweight"]="bold"
#pylab.rcParams["axes.titleweight"]="bold"
pylab.rcParams["xtick.major.size"]=0
pylab.rcParams["xtick.minor.size"]=0
pylab.rcParams["ytick.major.size"]=0
pylab.rcParams["ytick.minor.size"]=0
#pylab.rcParams["xtick.direction"]="out"
#pylab.rcParams["ytick.direction"]="out"
pylab.rcParams["figure.figsize"]=(3, 3)

#plot
coef_som=numpy.loadtxt("PCcoef_som.csv", delimiter=",")
coef_dnd=numpy.loadtxt("PCcoef_dnd.csv", delimiter=",")
score_som=numpy.loadtxt("PCscore_som.csv", delimiter=",")
score_dnd=numpy.loadtxt("PCscore_dnd.csv", delimiter=",")

plot_end=4999

max_eig=0.2
max_score=1.5

pylab.clf()
pylab.subplot(4,2,1)
pylab.plot(numpy.abs(coef_som[:,0]), ".")
pylab.ylabel("PCA\nsoma")
pylab.title("Eigenvector")
pylab.xticks([])
#pylab.xlabel("Time [s]")
pylab.ylim([0.0, max_eig])
pylab.yticks([0.0, max_eig])

pylab.subplot(4,2,2)
pylab.plot(score_som[:plot_end, 0], numpy.abs(score_som[:plot_end, 1]))
pylab.title("Score")
#pylab.ylabel("Score")
pylab.xticks([])
#pylab.xlabel("Time [s]")
pylab.ylim([0.0, max_score])
pylab.yticks([0.0, max_score])

pylab.subplot(4,2,3)
pylab.plot(numpy.abs(coef_dnd[:,0]), ".")
pylab.ylabel("PCA\ndendrite")
pylab.xticks([])
#pylab.xlabel("Neuron #")
pylab.ylim([0.0, max_eig])
pylab.yticks([0.0, max_eig])

pylab.subplot(4,2,4)
pylab.plot(score_dnd[:plot_end, 0], numpy.abs(score_dnd[:plot_end, 1]))
#pylab.ylabel("Score")
pylab.xticks([])
#pylab.xlabel("Time [s]")
pylab.ylim([0.0, max_score])
pylab.yticks([0.0, max_score])

coef_som=numpy.loadtxt("CCcoef_som.csv", delimiter=",")
coef_dnd=numpy.loadtxt("CCcoef_dnd.csv", delimiter=",")
score_som=numpy.loadtxt("CCscore_som.csv", delimiter=",")
score_dnd=numpy.loadtxt("CCscore_dnd.csv", delimiter=",")

max_eig=0.5
max_score=0.8

pylab.subplot(4,2,5)
pylab.plot(numpy.abs(coef_som[:,0]), ".")
pylab.ylabel("CCA\nsoma")
#pylab.title("Eigenvector")
pylab.xticks([])
#pylab.xlabel("Time [s]")
pylab.ylim([0.0, max_eig])
pylab.yticks([0.0, max_eig])

pylab.subplot(4,2,6)
pylab.plot(score_som[:plot_end, 0], numpy.abs(score_som[:plot_end, 1]))
#pylab.title("Score")
#pylab.ylabel("Score")
pylab.xticks([])
#pylab.xlabel("Time [s]")
pylab.ylim([0.0, max_score])
pylab.yticks([0.0, max_score])

pylab.subplot(4,2,7)
pylab.plot(numpy.abs(coef_dnd[:,0]), ".")
pylab.ylabel("CCA\ndendrite")
pylab.xticks([])
#pylab.xlabel("Neuron #")
pylab.ylim([0.0, max_eig])
pylab.yticks([0.0, max_eig])

pylab.subplot(4,2,8)
pylab.plot(score_dnd[:plot_end, 0], numpy.abs(score_dnd[:plot_end, 1]))
#pylab.ylabel("Score")
pylab.xlabel("Time [s]")
pylab.ylim([0.0, max_score])
pylab.yticks([0.0, max_score])

pylab.tight_layout()
pylab.savefig("plot.pdf")
