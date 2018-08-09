#!/bin/bash

python3 create_1Dtrack_network_onlysom.py

date
python3 sim_noextinput.py | python3 simRNN_1comp_noextinput.py
date

python3 plot_spike_1comp.py 1
