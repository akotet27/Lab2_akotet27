# data-detective.py
# A simple data analysis script for Twitter CSV data.
# It covers:
# 1) auditing/cleaning tweets (missing text, likes, retweets)
# 2) finding the viral tweet by max likes (without max())
# 3) sorting by likes via custom selection sort (without sort()/sorted())
# 4) filtering tweets by a user search term

import csv
import os


def load_tweets(csv_file):
    """Load tweets from CSV into a list of dictionaries."""
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"{csv_file} not found")

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        tweets = [row for row in reader]
    return tweets


def audit_tweets(tweets):
    """Quest 1: Clean missing data.

    - Remove rows with missing Text.
    - Convert empty Likes/Retweets to 0.
    - Keep counter of fixed/removed rows.
    """
    cleaned = []
    bad_count = 0

    for row in tweets:
        text = row.get('Text', '').strip()
        if text == '':
            bad_count += 1
            continue

        likes_raw = row.get('Likes', '').strip()
        retweets_raw = row.get('Retweets', '').strip()

        if likes_raw == '':
            likes_raw = '0'
            bad_count += 1

        if retweets_raw == '':
            retweets_raw = '0'
            bad_count += 1

        try:
            likes = int(likes_raw)
        except ValueError:
            likes = 0

        try:
            retweets = int(retweets_raw)
        except ValueError:
            retweets = 0

        row['Text'] = text
        row['Likes'] = str(likes)
        row['Retweets'] = str(retweets)

        cleaned.append(row)

    print(f"Quest 1: Cleaned data -> {bad_count} bad rows fixed or removed")
    return cleaned


def find_most_liked_tweet(tweets):
    """Quest 2: Identify the tweet with maximum likes without max()."""
    best = None
    best_likes = -1

    for row in tweets:
        try:
            likes = int(row.get('Likes', '0'))
        except ValueError:
            likes = 0

        if likes > best_likes:
            best_likes = likes
            best = row

    if best is None:
        print('Quest 2: No tweets available after cleaning.')
        return

    print('Quest 2: Viral Tweet')
    print(f"Username: {best.get('Username', 'Unknown')}")
    print(f"Likes: {best_likes}")
    print(f"Text: {best.get('Text', '')}")


def selection_sort_by_likes(tweets):
    """Quest 3: Custom sort by likes in descending order using Selection Sort."""
    sorted_tweets = tweets.copy()
    n = len(sorted_tweets)

    for i in range(n):
        max_idx = i
        try:
            max_likes = int(sorted_tweets[i].get('Likes', '0'))
        except ValueError:
            max_likes = 0

        for j in range(i + 1, n):
            try:
                current_likes = int(sorted_tweets[j].get('Likes', '0'))
            except ValueError:
                current_likes = 0

            if current_likes > max_likes:
                max_likes = current_likes
                max_idx = j

        if max_idx != i:
            sorted_tweets[i], sorted_tweets[max_idx] = sorted_tweets[max_idx], sorted_tweets[i]

    return sorted_tweets


def show_top_10_most_liked(tweets):
    print('Quest 3: Top 10 Most Liked Tweets')
    sorted_tweets = selection_sort_by_likes(tweets)
    top_10 = sorted_tweets[:10]

    for idx, tweet in enumerate(top_10, start=1):
        print(f"{idx}. {tweet.get('Username', 'Unknown')} - {tweet.get('Likes', '0')} likes - {tweet.get('Text', '')}")


def content_filter(tweets):
    """Quest 4: Filter tweets by user-supplied keyword and show matches."""
    search_word = input('Quest 4 - Enter a search word: ').strip()
    if search_word == '':
        print('No search word provided. Skipping content filter.')
        return

    search_lower = search_word.lower()
    matches = []

    for row in tweets:
        text = row.get('Text', '')
        if search_lower in text.lower():
            matches.append(row)

    print(f"Found {len(matches)} tweets matching '{search_word}'")
    for row in matches:
        print(
            f"{row.get('Username', 'Unknown')} ({row.get('Likes', '0')} likes): {row.get('Text', '')}")


def main():
    csv_file = 'twitter_dataset.csv'

    try:
        tweets = load_tweets(csv_file)
    except FileNotFoundError as e:
        print(e)
        return

    tweets = audit_tweets(tweets)
    find_most_liked_tweet(tweets)
    show_top_10_most_liked(tweets)
    content_filter(tweets)


if __name__ == '__main__':
    main()
