#!/bin/bash
for folder in experiments_real/*; do
    if [[ -d "$folder" && ! -L "$folder" ]]; then
        python convert_data_real.py "$folder"
    fi;
done