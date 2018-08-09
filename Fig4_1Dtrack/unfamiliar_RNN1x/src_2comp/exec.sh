#!/bin/bash

python3 create_1Dtrack_network_shuffle.py
python3 create_input_conf_1Dtrack_preset.py

date
python3 sim_input_1D_distractor.py | python3 simRNN.py
date

python3 plot_spike_2comp.py
python3 plot_oneneuron.py
python3 plot_input.py input.csv position.csv
python3 MIplace.py spike_som.csv position.csv
