#!/bin/bash

DIR1=../firstrun
DIR2=../replay

cp ${DIR1}/input_conf.csv ./
cp ${DIR2}/*_end.csv ./
for FILE in *_end.csv
do
    mv $FILE ${FILE%_end.csv}_init.csv
done
