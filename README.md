# Lab 2 — Social Media Data Detective

A Python + Bash project that loads, cleans, and analyses a Twitter CSV dataset.
Built for BSE Year 1 — Introduction to Python Programming and Databases.

## Project Files

| File | What it does |

| `data_detective.py` | Main Python script — runs all 4 quests |
| `feed_analyzer.sh` | Bash script — finds the top 5 most active users |
| `twitter_dataset.csv` | The dataset used for testing |
| `README.md` | This file |

## How to Run

### Python Script

Make sure `twitter_dataset.csv` is in the same folder as `data_detective.py`, then run:

```bash
python data_detective.py
```

The script runs all 4 quests automatically one by one.
At Quest 4 it asks for a search keyword — type any word made of letters and press Enter.
After each search it asks if you want to search again — type `yes` to continue or `no` to stop.

Example:
```
  Enter a search keyword: father
  Found 357 tweet(s) matching 'father':

  #1   @ojordan (100 likes): West appear important not billion serve father...
  #2   @hjames (100 likes): Guy father gas allow...
  #3   @nwhite (100 likes): Audience lose do recently...

  Do you want to search again? (yes/no): no
  Okay, I am done searching.
```
### Bash Script

The bash script takes the CSV file as an argument:

```bash
bash feed_analyzer.sh twitter_dataset.csv
```

Expected output:
```
====================================
  Top 5 Most Active Users
====================================
  6 posts  @pjohnson
  5 posts  @nbrown
  5 posts  @awilliams
  4 posts  @fsmith
  4 posts  @jessicawilliams
====================================
```
## What Each Quest Does

### Quest 1 — Data Audit
Cleans the raw dataset before any analysis:
- Removes any tweet that has no text
- Replaces blank `Likes` or `Retweets` values with `0`
- Converts likes and retweets from strings to integers so comparisons work correctly
- Prints a summary of how many rows were fixed or removed

### Quest 2 — Viral Tweet
Finds the single tweet with the highest number of likes.
Uses a manual loop instead of Python's built-in `max()` function — starts by assuming
the first tweet is the best, then replaces it whenever a higher like count is found.
Prints the username, like count, and tweet text.

### Quest 3 — Top 10 Most Liked
Sorts all tweets from highest to lowest likes using **Selection Sort**.
Does not use `.sort()` or `sorted()` — the sorting logic is written from scratch.
After sorting, slices the first 10 results and prints them in a ranked list.

### Quest 4 — Content Filter
Asks the user to enter a search keyword (letters only — numbers and symbols are rejected
with a clear error message). Searches every tweet case-insensitively and displays all
matches ranked by likes from highest to lowest. After each search the program asks
if the user wants to search again — only `yes`, `y`, `no`, or `n` are accepted as answers,
anything else shows an error and asks again.

---

## How the Sorting Algorithm Works

Quest 3 uses "Selection Sort" in descending order.

The idea is simple: go through the list position by position. At each position, scan
everything after it to find the tweet with the most likes. Once found, swap it into
the current position. Repeat until the whole list is sorted.

```
Pass 1: find the highest liked tweet in the whole list → put it at position 0
Pass 2: find the highest in positions 1 to end        → put it at position 1
Pass 3: find the highest in positions 2 to end        → put it at position 2
...and so on until the list is fully sorted
```

The same sort function is also reused in Quest 4 to rank search results by likes.

---

## Error Handling

| Situation | What happens |
| CSV file not found | Clear message shown, program stops cleanly |
| CSV file is empty | Clear message shown, program stops cleanly |
| Blank search keyword | Program asks again until user types something |
| Numbers or symbols entered as keyword | Error message shown, asks again |
| Invalid answer to yes/no prompt | Error message shown, asks again |
| Blank or broken likes/retweets in CSV | Automatically replaced with `0` |

## How to Test the Bash Script Edge Cases

If you pass no file:
```bash
bash feed_analyzer.sh
# Output: Usage: feed_analyzer.sh twitter_dataset.csv
```

If the file does not exist:
```bash
bash feed_analyzer.sh wrong_name.csv
# Output: File not found: wrong_name.csv
```

If the file has no data rows:
```bash
bash feed_analyzer.sh empty.csv
# Output: No data rows found in empty.csv
```
## Requirements

- Python 3.x (no extra libraries needed — only `csv` and `os` which are built-in)
- Bash shell (Linux, macOS, or Git Bash on Windows)
- `twitter_dataset.csv` downloaded from Kaggle

## Dataset

The dataset is downloaded from Kaggle:
Twitter Dataset — `twitter_dataset.csv`

CSV columns used by this project:

| Column | Description |
|---|---|
| `Tweet_ID` | Unique ID for each tweet |
| `Username` | The Twitter handle of the poster |
| `Text` | The tweet content |
| `Retweets` | Number of retweets |
| `Likes` | Number of likes |
| `Timestamp` | Date and time the tweet was posted |

## Author

- Course: Introduction to Python Programming and Databases
- Year: BSE Year 1 — Trimester 2
- Institution: African Leadership University