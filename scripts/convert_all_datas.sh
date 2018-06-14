#!/bin/bash
the_folder=$1
cat $the_folder
for folder in $the_folder/*; do
    if [[ -d "$folder" && ! -L "$folder" ]]; then
        echo $folder;
        python conversion_scripts/convert_data.py "$folder"
    fi;
done