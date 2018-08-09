#!/bin/bash

for SRC in branch
do
    for N in `seq 5`
    do
        cp -r src_${SRC} ${SRC}_${N}
        cd ${SRC}_${N}
        qsub -cwd -q machine3.q exec.sh
        cd ../
    done
done
