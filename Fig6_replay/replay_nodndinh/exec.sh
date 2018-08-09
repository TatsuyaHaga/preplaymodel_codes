#!/bin/bash

date
python3 sim_input_spont.py | python3 simRNN_nodndinh.py
date

python3 plot_spike_2comp_nopos.py
