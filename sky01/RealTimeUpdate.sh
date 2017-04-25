#!/bin/bash

# Get the current day
_day=$(($(date -d "$(date +%DZ)" +%s)/86400))

# Find and synchronize most recent images (5 min)
_file=$(find ./Pictures/"$_day"/ -type f -cmin -5)
rsync $_file ./RealTime/

# Run the python script
/usr/local/miniconda2/bin/python RealTime.py

# Find and remove files older than 2 hours
expiration_DATE=$(date +%s -d "-2 hours")
for fn in ./RealTime/*; do ofn=("${fn##*/}") && [ "${ofn%.*}" -lt "$expiration_DATE" ] && rm "$fn"; done

# Add a security at 140 minutes
find ./RealTime/ -cmin +140 -exec rm -f {} \;
