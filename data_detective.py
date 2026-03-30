# ============================================================
# data_detective.py
# Student: Akotet
# Course:  Introduction to Python Programming and Databases
# Lab:     Lab 2 — Social Media Data Detective
# ============================================================
#
# This program reads a Twitter CSV file and does 4 things:
#   Quest 1 — cleans the messy data (missing text, likes, retweets)
#   Quest 2 — finds the tweet with the most likes (no max() allowed)
#   Quest 3 — sorts tweets by likes using Selection Sort (no .sort() allowed)
#   Quest 4 — lets the user search tweets by a keyword
#
# How to run:
#   Make sure twitter_dataset.csv is in the same folder, then run:
#   python data_detective.py
# ============================================================

import csv  # used to read the CSV file row by row
import os   # used to check if the file exists before opening it


# HELPER FUNCTION — prints a nice section title so I know which quest is running
def show_section(title):
    print("\n" + "=" * 52)
    print(f"  {title}")
    print("=" * 52)


# LOAD FUNCTION — opens the CSV and loads all rows into a list of dicts
# Each row looks like: { 'Tweet_ID': '1', 'Username': 'john', 'Text': '...', ... }
# If the file is missing or empty I stop early with a clear message
def load_posts(file_path):

    # check the file exists before trying to open it
    # if not, raise a clear error message instead of crashing
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find '{file_path}'. Make sure the file is in the same folder.")

    # open the file and read every row into a list
    with open(file_path, newline='', encoding='utf-8') as csv_file:
        post_list = [row for row in csv.DictReader(csv_file)]

    # if the file opened but had no rows at all, stop here
    if len(post_list) == 0:
        raise ValueError("The CSV file is empty — there are no tweets to analyse.")

    return post_list


# ------------------------------------------------------------
# QUEST 1 — DATA AUDIT
# Goal: clean the raw data before we analyse anything
#
# Rules:
#   - If a tweet has no text at all → remove it completely
#   - If a tweet has no likes value → set it to 0
#   - If a tweet has no retweets value → set it to 0
#
# We also convert likes and retweets from strings to integers
# because CSV files store everything as text by default
# ------------------------------------------------------------
def clean_posts(post_list):

    # good_posts will hold only the tweets that pass our checks
    good_posts = []

    # problem_count tracks how many fields we fixed or removed
    problem_count = 0

    # go through every tweet one by one
    for post in post_list:

        # get the tweet text, strip removes extra spaces around it
        post_text = post.get('Text', '').strip()

        # if the tweet has no text it is useless — skip it entirely
        if post_text == '':
            problem_count += 1
            continue  # jump to the next tweet, don't add this one

        # if the likes field is blank, replace it with the string '0'
        # we keep it as a string here because the rest of the data is strings
        if post.get('Likes', '').strip() == '':
            post['Likes'] = '0'
            problem_count += 1

        # same fix for retweets
        if post.get('Retweets', '').strip() == '':
            post['Retweets'] = '0'
            problem_count += 1

        # now convert likes to a real integer to make sure it is a valid number
        # if it is something weird like 'abc', set it to 0 instead of crashing
        try:
            post['Likes'] = str(int(post['Likes']))
        except ValueError:
            post['Likes'] = '0'

        # same conversion check for retweets
        try:
            post['Retweets'] = str(int(post['Retweets']))
        except ValueError:
            post['Retweets'] = '0'

        # this tweet passed all checks — add it to the clean list
        good_posts.append(post)

    # print a summary of what we found and fixed
    print(f"  {problem_count} problem field(s) fixed or removed.")
    print(f"  {len(good_posts)} clean posts ready for analysis.")

    return good_posts


# ------------------------------------------------------------
# QUEST 2 — FIND THE VIRAL TWEET
# Goal: find the single tweet with the highest number of likes
#
# We are NOT allowed to use Python's built-in max() function
# Instead we loop through every tweet manually and keep track
# of the best one we have seen so far
#
# Think of it like going through a stack of cards and always
# keeping the highest number in your hand — replacing it
# whenever you find a bigger one
# ------------------------------------------------------------
def find_top_post(good_posts):

    # top_post will hold the winning tweet
    top_post = None

    # top_likes starts at -1 so even a tweet with 0 likes will beat it
    top_likes = -1

    # go through every tweet and compare its likes to our current best
    for post in good_posts:

        # convert likes from string to integer for proper number comparison
        # '100' as a string is not the same as 100 as a number
        try:
            like_count = int(post.get('Likes', '0'))
        except ValueError:
            like_count = 0  # if likes is invalid, treat it as 0

        # if this tweet has more likes than our current best, update the record
        if like_count > top_likes:
            top_likes = like_count
            top_post = post

    # if nothing was found (empty list), print a message and stop
    if top_post is None:
        print("  No posts available.")
        return

    # print the winning tweet's details
    print(f"  Username : {top_post.get('Username', 'Unknown')}")
    print(f"  Likes    : {top_likes}")
    print(f"  Text     : {top_post.get('Text', '')[:120]}")


# ------------------------------------------------------------
# QUEST 3 — CUSTOM SORT (SELECTION SORT)
# Goal: sort all tweets from most liked to least liked
#
# We are NOT allowed to use .sort() or sorted()
# So we write our own sorting algorithm called Selection Sort
#
# How Selection Sort works:
#   - Start at position 0
#   - Scan ALL tweets after position 0 to find the one with the most likes
#   - Swap that tweet into position 0
#   - Move to position 1, scan everything after it, swap the best in
#   - Keep going until the whole list is sorted
#
# Example with 5 tweets: [30, 10, 50, 20, 40]
#   Pass 1 → find 50 → swap to front → [50, 10, 30, 20, 40]
#   Pass 2 → find 40 → swap to pos 1 → [50, 40, 30, 20, 10]
#   ... and so on
# ------------------------------------------------------------
def sort_posts_by_likes(good_posts):

    # work on a copy so we do not change the original list
    sorted_list = good_posts.copy()

    # total number of tweets
    total = len(sorted_list)

    # outer loop — moves through each position in the list
    for current_pos in range(total):

        # assume the tweet at current_pos is already the best
        best_pos = current_pos

        # inner loop — scans everything after current_pos
        for scan_pos in range(current_pos + 1, total):

            # compare as integers — strings would sort wrong ('9' > '10' as text)
            try:
                scan_likes = int(sorted_list[scan_pos].get('Likes', '0'))
                best_likes = int(sorted_list[best_pos].get('Likes', '0'))
            except ValueError:
                scan_likes = best_likes = 0

            # if this tweet has more likes, remember its position
            if scan_likes > best_likes:
                best_pos = scan_pos

        # if we found something better than current_pos, swap them
        if best_pos != current_pos:
            sorted_list[current_pos], sorted_list[best_pos] = \
                sorted_list[best_pos], sorted_list[current_pos]

    return sorted_list


# this function calls sort_posts_by_likes and prints the top 10 results
def display_top_10(good_posts):

    sorted_posts = sort_posts_by_likes(good_posts)

    # use min() so we don't crash if there are fewer than 10 tweets
    how_many = min(10, len(sorted_posts))

    # print each tweet with its rank number
    for rank, post in enumerate(sorted_posts[:how_many], start=1):
        handle  = post.get('Username', 'Unknown')
        likes   = post.get('Likes', '0')
        preview = post.get('Text', '')[:80]  # only show first 80 characters
        print(f"  #{rank:<3} {handle:<18} {likes:>5} likes  |  {preview}...")


# ------------------------------------------------------------
# QUEST 4 — KEYWORD SEARCH
# Goal: let the user type a word and find all tweets that contain it
#
# The search is case-insensitive — searching 'music' also finds
# 'Music', 'MUSIC', 'MuSiC' etc.
#
# Matching tweets are added to a new list called matched_posts
# At the end we print how many we found using len()
# ------------------------------------------------------------
def search_posts(good_posts):

    # ask the user for a keyword
    # if they press Enter without typing anything, ask again
    search_term = input("\n  Enter a search keyword: ").strip()
    while search_term == '':
        print("  You did not type anything. Please enter a keyword.")
        search_term = input("  Enter a search keyword: ").strip()

    # matched_posts will collect every tweet that contains the keyword
    matched_posts = []

    # go through every tweet and check if the keyword is in the text
    for post in good_posts:
        post_text = post.get('Text', '')

        # .lower() on both sides makes the search case-insensitive
        if search_term.lower() in post_text.lower():
            matched_posts.append(post)  # add this tweet to our results

    # tell the user how many matches we found
    print(f"\n  Found {len(matched_posts)} tweet(s) matching '{search_term}':\n")

    # if nothing matched, suggest trying a different word
    if len(matched_posts) == 0:
        print("  No matches found. Try a different keyword.")
        return

    # print every matching tweet
    for post in matched_posts:
        handle   = post.get('Username', 'Unknown')
        likes    = post.get('Likes', '0')
        preview  = post.get('Text', '')[:100]
        print(f"  @{handle} ({likes} likes): {preview}")

# MAIN — this is where the program starts running
# It calls each quest function in order and passes results along
def main():

    # the name of the CSV file we want to analyse
    data_file = 'twitter_dataset.csv'

    # try to load the file — if it fails, print the error and stop
    try:
        post_list = load_posts(data_file)
        print(f"\n  Loaded {len(post_list)} raw tweets from '{data_file}'.")
    except (FileNotFoundError, ValueError) as load_error:
        print(f"\n  Error: {load_error}")
        return  # stop the program — no point continuing without data

    # Quest 1 — clean the data first before anything else
    show_section("Quest 1 — Data Audit")
    post_list = clean_posts(post_list)

    # Quest 2 — find the tweet with the most likes
    show_section("Quest 2 — Viral Tweet")
    find_top_post(post_list)

    # Quest 3 — sort and show the top 10 most liked tweets
    show_section("Quest 3 — Top 10 Most Liked")
    display_top_10(post_list)

    # Quest 4 — search tweets by keyword
    show_section("Quest 4 — Content Filter")
    search_posts(post_list)

    # final message when everything is done
    print("\n" + "=" * 52)
    print("  Analysis complete. All 4 quests finished.")
    print("=" * 52 + "\n")


# this line makes sure main() only runs when we execute this file directly
# it prevents main() from running if someone imports this file into another script
if __name__ == '__main__':
    main()