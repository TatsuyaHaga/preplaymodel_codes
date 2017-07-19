#!/bin/bash

cd firstrun/
bash exec.sh
cd ../

cd replay/
bash copy_weights.sh
bash exec.sh
cd ../

cd secondrun/
bash copy_weights.sh
bash exec.sh
cd ../

cd replay_nodndinh/
bash copy_weights.sh
bash exec.sh
cd ../

cd secondrun_nodndinh/
bash copy_weights.sh
bash exec.sh
cd ../
