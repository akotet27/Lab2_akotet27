#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 twitter_dataset.csv"
  exit 1
fi

csv_file="$1"

if [ ! -f "$csv_file" ]; then
  echo "File not found: $csv_file"
  exit 1
fi

# Extract username column (2nd field assuming CSV has columns: id,Username,...) and output top 5 active users
# This pipeline matches the lab requirement with cut, sort, uniq -c, sort -nr, head.

tail -n +2 "$csv_file" | cut -d',' -f2 | sed '/^$/d' | sort | uniq -c | sort -nr | head -n 5
