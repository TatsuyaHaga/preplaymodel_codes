#!/bin/bash

python3 create_Ymaze_network.py
python3 create_input_conf_Ymaze.py

date
python3 sim_input_Ymaze.py | python3 simRNN.py
date

python3 MIplace_Ytrack.py spike_som.csv position.csv
python3 plot_spike_2comp_Ymaze.py 2
