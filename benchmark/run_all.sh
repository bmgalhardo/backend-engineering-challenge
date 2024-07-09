#!/bin/bash

export PYTHONPATH=../src/
for d in $(ls data); do
  python ../src/app/main.py -i ../benchmark/data/$d -w 10 -t -o output/output_$d
done