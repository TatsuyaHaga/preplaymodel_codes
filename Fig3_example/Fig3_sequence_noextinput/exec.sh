#!/bin/bash

NE=300
samp_pitch=1.0
sim_len=10.0

python3 create_1Dtrack_network_onlysom.py $NE

date
python3 sim_noextinput.py $NE $sim_len $samp_pitch | python3 simRNN_1comp_noextinput.py $NE $samp_pitch
date

python3 plot_spike_1comp.py 1
