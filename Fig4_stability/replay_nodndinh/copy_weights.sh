#!/bin/bash

DIR=../firstrun

cp ${DIR}/*_end.csv ./
for FILE in *_end.csv
do
    mv $FILE ${FILE%_end.csv}_init.csv
done
#cp ../WEIdnd_init_zero.csv WEIdnd_init.csv
#cp ../WEIdndGABAB_init_zero.csv WEIdndGABAB_init.csv
