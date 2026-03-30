# Lab 2: Social Media Data Detective

## Usage

1. Put `twitter_dataset.csv` in the same folder as `data-detective.py` and `feed-analyzer.sh`.
2. Run Python:

   ```bash
   python data-detective.py
   ```

3. Run Bash (Linux/MacWSL/Git Bash):

   ```bash
   bash feed-analyzer.sh twitter_dataset.csv
   ```

## Algorithm Explanation (2 sentences)

The custom sorting algorithm in `data-detective.py` is Selection Sort: it repeatedly finds the tweet with the largest Likes in the unsorted portion and swaps it into the current index, producing a descending list. This ensures no Python built-ins (`sort`, `sorted`, or `max`) are used for the key tasks.
