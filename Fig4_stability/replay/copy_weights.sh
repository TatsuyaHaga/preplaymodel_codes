#!/bin/bash

DIR=../firstrun

cp ${DIR}/*_end.csv ./
for FILE in *_end.csv
do
    mv $FILE ${FILE%_end.csv}_init.csv
done
