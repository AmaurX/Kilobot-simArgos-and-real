#!/bin/bash
for folder in simulation_experiments/experiments/*; do
    if [[ -d "$folder" && ! -L "$folder" ]]; then
        echo $folder;
        python conversion_scripts/convert_data.py "$folder"
    fi;
done