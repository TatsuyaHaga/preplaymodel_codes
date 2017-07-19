#!/bin/bash

NE=450
Ninput=450
samp_pitch=1.0
sim_len=40.0

python3 create_Ymaze_network.py $NE $Ninput
python3 create_input_conf_Ymaze.py $Ninput

date
python3 sim_placecell_Ymaze.py $NE $Ninput $sim_len $samp_pitch | python3 simRNN_2comp_nodndinh.py $NE $Ninput $samp_pitch
date

python3 MIplace_Ytrack.py spike_som.csv position.csv
python3 plot_spike_2comp_Ymaze.py 1
