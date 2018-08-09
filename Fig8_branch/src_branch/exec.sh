#!/bin/bash

python3 create_1Dbranch_network.py 
python3 create_input_conf_branch.py

date
python3 sim_input_1D_runagain.py | python3 simRNN_movingOFF.py 
date

python3 plot_spike_2comp_branch.py
python3 plot_input.py input.csv position.csv
