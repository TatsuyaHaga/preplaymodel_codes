#!/bin/bash

python3 create_1Dtrack_network.py
python3 create_input_conf_1Dtrack.py

date
python3 sim_input_1D_distractor.py | python3 simRNN.py
date

python3 plot_spike_2comp.py 1
