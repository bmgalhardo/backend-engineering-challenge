#!/bin/bash

folder=$(dirname $0)

for d in $(ls ${folder}/data); do
  poetry run unbabel -i ${folder}/data/$d -w 10 -o ${folder}/output/output_$d
done