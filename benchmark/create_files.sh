#!/bin/bash

# keep in mind these stats when choosing the files
# less than 10**5 will lead to negligible compute times
# 10**8 will have a size of around 23GB
for size in $(seq 5 8); do
  power=$((10**size))
  for days in 1 2 5; do
    echo creating file data_s${power}_d${days} ...
    python create_test_data.py -l $power -d $days
  done
done
