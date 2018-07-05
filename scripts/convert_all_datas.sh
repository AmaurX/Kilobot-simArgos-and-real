#!/bin/bash
the_folder=$1
sim_or_real=$2
for folder in $the_folder/*; do
    if [[ -d "$folder" && ! -L "$folder" ]]; then
        echo $folder;
        python conversion_scripts/convert_data.py "$folder" "$sim_or_real"
    fi;
done