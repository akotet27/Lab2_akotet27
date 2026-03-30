#!/bin/bash
# feed-analyzer.sh
# Shows the Top 5 most active users from twitter_dataset.csv

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 twitter_dataset.csv"
  exit 1
fi

csv_file="$1"

# make sure the file actually exists
if [ ! -f "$csv_file" ]; then
  echo "File not found: $csv_file"
  exit 1
fi

# stop if there are no data rows (only a header)
line_count=$(tail -n +2 "$csv_file" | wc -l)
if [ "$line_count" -eq 0 ]; then
  echo "No data rows found in $csv_file"
  exit 1
fi

echo ""
echo "===================================="
echo "  Top 5 Most Active Users"
echo "===================================="

# We use Python here instead of cut because tweet Text fields
# contain commas inside quotes — that breaks cut and shifts columns.
# Python's csv.DictReader handles quoted fields correctly.
python3 -c "
import csv, sys

counts = {}
with open(sys.argv[1], newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        name = row['Username'].strip()
        counts[name] = counts.get(name, 0) + 1

# sort by count descending and take top 5
top5 = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]
for name, count in top5:
    print(f'  {count} posts  @{name}')
" "$csv_file"

echo "===================================="
echo ""