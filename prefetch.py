

import json
import threading
import os
import requests
import time

import random

import requests

from common import in_cache, download_and_cache, download


# Define the base URL for the Hacker News API
API_BASE_URL = "https://hacker-news.firebaseio.com/v0"

# Define the endpoint for getting an item by ID
API_ITEM_ENDPOINT = "item/{}.json?print=pretty"

# Define the number of threads to use
NUM_THREADS = 20

# Define a lock to synchronize access to the item IDs list
ids_lock = threading.Lock()

# Define a list of item IDs to download comments for
item_ids = list(range(1, 500000))

absolute_total_comments = 0
total_comments = 0
start_time = time.time()

def download_comments_recursive(item_id):
    # Download the item with the given ID
    item_url = f"{API_BASE_URL}/{API_ITEM_ENDPOINT.format(item_id)}"
#    if not in_cache(item_url): print(item_id)

    res = download_and_cache(item_url)

    global total_comments
    global start_time
    global absolute_total_comments

    total_comments += 1

    end_time = time.time()
    elapsed_time_minutes = (end_time - start_time) / 60
    comments_per_minute = total_comments / elapsed_time_minutes
    if total_comments % 100 == 0:
        print(f"[{item_id}] Downloaded {total_comments} ({absolute_total_comments}) comments in {elapsed_time_minutes:.2f} minutes ({comments_per_minute:.2f} comments per minute)")

    if elapsed_time_minutes > 1:
        absolute_total_comments += total_comments
        start_time = time.time()
        total_comments = 0

def download_comments_thread():
    # Download comments for items until the item IDs list is empty
    while True:
        with ids_lock:
            if len(item_ids) == 0:
                # All item IDs have been processed, so exit the thread
                return
            item_id = item_ids.pop()
        try:
            download_comments_recursive(item_id)
        except Exception as e: 
            print(e)


# Populate the item IDs list with the most recent item IDs
response = download(f"{API_BASE_URL}/maxitem.json")
max_item_id = int(response)
item_ids = list(range(1, max_item_id))##18000000+1))

# Create and start the threads
threads = []
for i in range(NUM_THREADS):
    thread = threading.Thread(target=download_comments_thread)
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()