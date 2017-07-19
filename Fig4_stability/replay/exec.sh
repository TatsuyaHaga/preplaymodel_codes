#!/bin/bash

NE=300
Ninput=300
samp_pitch=1.0
sim_len=600

date
python3 sim_input_spont.py $NE $Ninput $sim_len $samp_pitch | python3 simRNN_2comp.py $NE $Ninput $samp_pitch
date

python3 plot_spike_2comp_nopos.py
