#!/bin/bash

date
python3 sim_input_1D_distractor_test.py | python3 simRNN.py
date

python3 plot_spike_2comp.py

