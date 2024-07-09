#!/bin/bash

folder=$(dirname $0)

# keep in mind these stats when choosing the files
# less than 10**5 will lead to negligible compute times
# 10**8 will have a size of around 23GB
for size in $((10**5)) $((10**6)) $((10**7)) $((3*10**7)) $((5*10**7)) $((8*10**7)) $((10**8)); do
  for days in 1 2 5; do
    echo creating file data_s${size}_d${days} ...
    python $folder/create_test_data.py -l $size -d $days
  done
done
