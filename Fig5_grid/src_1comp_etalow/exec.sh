#!/bin/bash

python3 create_1Dtrack_network_random.py

date
python3 sim_input_gridcell_1D_distractor.py | python3 simRNN_1comp.py
date

python3 plot_spike_2comp.py
python3 plot_oneneuron.py
python3 plot_input.py input.csv position.csv
python3 MIplace.py spike_som.csv position.csv
python3 plot_input_single.py
