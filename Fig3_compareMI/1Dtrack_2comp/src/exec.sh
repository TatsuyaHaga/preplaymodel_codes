#!/bin/bash

NE=300
Ninput=500
Ndistractor=200
samp_pitch=1.0
sim_len=50.0
dnd_shuffle=${1}
som_shuffle=${2}

python3 create_1Dtrack_network_shuffle_partial.py $NE $Ninput $dnd_shuffle $som_shuffle
python3 create_input_conf_1Dtrack_preset.py $Ninput $Ndistractor

date
python3 sim_placecell_1D_distractor.py $NE $Ninput $sim_len $samp_pitch $Ndistractor | python3 simRNN_2comp.py $NE $Ninput $samp_pitch
date

python3 MIplace.py spike_som.csv position.csv
python3 plot_spike_2comp.py
