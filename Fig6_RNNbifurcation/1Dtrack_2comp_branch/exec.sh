#!/bin/bash

NE=400
Ninput=300
samp_pitch=1.0
sim_len=160

python3 create_1Dbranch_network.py $NE $Ninput
python3 create_input_conf.py $Ninput
mv input_conf.csv input_conf1.csv
python3 create_input_conf.py $Ninput
mv input_conf.csv input_conf2.csv

date
python3 sim_placecell_1D_runagain.py $NE $Ninput $sim_len $samp_pitch | python3 simRNN_2comp.py $NE $Ninput $samp_pitch
date

python3 plot_spike_2comp_branch.py
python3 get_max_synapse_change.py
