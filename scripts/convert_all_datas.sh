#!/bin/bash
for folder in simulation_experiments/experiments/*; do
    if [[ -d "$folder" && ! -L "$folder" ]]; then
        python convert_data.py "$folder"
    fi;
done