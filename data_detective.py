# data-detective.py
# Twitter CSV data analysis — Lab 2
# Quests:
#   1) Clean messy data (missing text, likes, retweets)
#   2) Find the most liked tweet without max()
#   3) Sort top 10 by likes using selection sort — no .sort() allowed
#   4) Search tweets by keyword

import csv
import os


# ── helper: print a section header ──────────────────────────
def banner(title):
    print("\n" + "=" * 52)
    print(f"  {title}")
    print("=" * 52)


# ── load CSV into a list of dicts ────────────────────────────
def load_tweets(csv_file):
    """Read every row from the CSV and return as a list of dicts."""
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"Could not find '{csv_file}'. Check the file name.")

    with open(csv_file, newline='', encoding='utf-8') as f:
        tweets = [row for row in csv.DictReader(f)]

    # stop early if the file is empty
    if len(tweets) == 0:
        raise ValueError("The CSV file has no data rows.")

    return tweets


# ── Quest 1 — audit and clean ────────────────────────────────
def audit_tweets(tweets):
    """Remove rows with no text; replace blank likes/retweets with 0."""
    cleaned = []
    bad_count = 0

    for row in tweets:
        # skip the whole row if there is no tweet text
        if row.get('Text', '').strip() == '':
            bad_count += 1
            continue

        # fix blank likes
        if row.get('Likes', '').strip() == '':
            row['Likes'] = '0'
            bad_count += 1

        # fix blank retweets
        if row.get('Retweets', '').strip() == '':
            row['Retweets'] = '0'
            bad_count += 1

        # make sure likes and retweets are valid integers
        try:
            row['Likes'] = str(int(row['Likes']))
        except ValueError:
            row['Likes'] = '0'

        try:
            row['Retweets'] = str(int(row['Retweets']))
        except ValueError:
            row['Retweets'] = '0'

        cleaned.append(row)

    print(f"  {bad_count} bad field(s) fixed or removed.")
    print(f"  {len(cleaned)} clean tweets ready for analysis.")
    return cleaned


# ── Quest 2 — find the viral tweet ──────────────────────────
def find_most_liked_tweet(tweets):
    """Loop through all tweets and track the one with the highest likes.
    No max() used — just a manual comparison each step."""

    best = None
    best_likes = -1  # start below zero so any real value beats it

    for row in tweets:
        try:
            likes = int(row.get('Likes', '0'))
        except ValueError:
            likes = 0

        # replace current best if this tweet has more likes
        if likes > best_likes:
            best_likes = likes
            best = row

    if best is None:
        print("  No tweets found.")
        return

    print(f"  Username : {best.get('Username', 'Unknown')}")
    print(f"  Likes    : {best_likes}")
    print(f"  Text     : {best.get('Text', '')[:120]}")


# ── Quest 3 — selection sort + top 10 ────────────────────────
def selection_sort_by_likes(tweets):
    """Sort tweets from highest to lowest likes using Selection Sort.
    No .sort() or sorted() allowed.

    How it works:
      Each pass finds the tweet with the most likes in the unsorted
      part and swaps it into the current front position.
    """
    data = tweets.copy()
    n = len(data)

    for i in range(n):
        max_idx = i  # assume the current position is the best

        for j in range(i + 1, n):
            # compare likes as integers, not strings
            try:
                j_likes = int(data[j].get('Likes', '0'))
                max_likes = int(data[max_idx].get('Likes', '0'))
            except ValueError:
                j_likes = max_likes = 0

            if j_likes > max_likes:
                max_idx = j  # found a bigger value, remember its position

        # swap the best found into the front slot
        if max_idx != i:
            data[i], data[max_idx] = data[max_idx], data[i]

    return data


def show_top_10(tweets):
    """Print the top 10 tweets after sorting."""
    sorted_tweets = selection_sort_by_likes(tweets)
    top_n = min(10, len(sorted_tweets))  # handle datasets smaller than 10

    for rank, tweet in enumerate(sorted_tweets[:top_n], start=1):
        username = tweet.get('Username', 'Unknown')
        likes    = tweet.get('Likes', '0')
        text     = tweet.get('Text', '')[:80]
        print(f"  #{rank:<3} {username:<18} {likes:>5} likes  |  {text}...")


# ── Quest 4 — keyword search ─────────────────────────────────
def content_filter(tweets):
    """Ask user for a keyword, find all tweets that contain it."""

    # keep asking until the user actually types something
    search_word = input("\n  Enter a search keyword: ").strip()
    while search_word == '':
        print("  Please type a word to search for.")
        search_word = input("  Enter a search keyword: ").strip()

    # collect every tweet whose text contains the keyword
    matches = []
    for row in tweets:
        if search_word.lower() in row.get('Text', '').lower():
            matches.append(row)

    print(f"\n  Found {len(matches)} tweet(s) matching '{search_word}':\n")

    if len(matches) == 0:
        print("  No matches found. Try a different word.")
        return

    for row in matches:
        username = row.get('Username', 'Unknown')
        likes    = row.get('Likes', '0')
        text     = row.get('Text', '')[:100]
        print(f"  @{username} ({likes} likes): {text}")


# ── main ─────────────────────────────────────────────────────
def main():
    csv_file = 'twitter_dataset.csv'

    # load — stop cleanly if the file is missing or empty
    try:
        tweets = load_tweets(csv_file)
        print(f"\n  Loaded {len(tweets)} raw tweets from '{csv_file}'.")
    except (FileNotFoundError, ValueError) as e:
        print(f"\n  Error: {e}")
        return

    banner("Quest 1 — Data Audit")
    tweets = audit_tweets(tweets)

    banner("Quest 2 — Viral Tweet")
    find_most_liked_tweet(tweets)

    banner("Quest 3 — Top 10 Most Liked")
    show_top_10(tweets)

    banner("Quest 4 — Content Filter")
    content_filter(tweets)

    print("\n" + "=" * 52)
    print("  Analysis complete.")
    print("=" * 52 + "\n")


if __name__ == '__main__':
    main()