#!/bin/bash

SHUF=1 #shuffling of input synaptic weights

for RNNweight in 0 0.25 0.5 0.75 1;do
    for NUM in 1 2 3;do
	DIR=RNN${RNNweight}_trial${NUM}
	cp -r src/ $DIR
	cd $DIR
	bash exec.sh $SHUF $RNNweight
	cd ../
    done
done
