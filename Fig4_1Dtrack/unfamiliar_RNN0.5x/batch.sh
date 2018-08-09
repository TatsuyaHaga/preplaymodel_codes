#!/bin/bash

for SRC in 1comp_etalow 1comp_etamid 1comp_etahigh 2comp
do
    for N in `seq 3`
    do
        cp -r src_${SRC} ${SRC}_${N}
        cd ${SRC}_${N}
        qsub -cwd -q machine3.q exec.sh
        cd ../
    done
done
