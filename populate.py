import threading
import os
import requests
import time

import random

import json

import requests

from common import in_cache, download_and_cache, download, json_fetch, count_tokens

from helpers import get_embedding, cosine_similarity


import datetime

# Define the base URL for the Hacker News API
API_BASE_URL = "https://hacker-news.firebaseio.com/v0"

# Define the endpoint for getting an item by ID
API_ITEM_ENDPOINT = "item/{}.json?print=pretty"

# Define the number of threads to use
NUM_THREADS = 50

# Define a lock to synchronize access to the item IDs list
ids_lock = threading.Lock()

# Define a list of item IDs to download comments for
item_ids = list(range(1, 500000))

absolute_total_comments = 0
total_comments = 0
start_time = time.time()



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

item_count = 0
token_count = 0

def populate():
    global item_count
    global token_count

    # Populate the item IDs list with the most recent item IDs
    response = download(f"{API_BASE_URL}/maxitem.json")
    max_item_id = int(response)
    item_ids = list(range(1, max_item_id))##18000000+1))

    items = []
    while True:
        item_id = item_ids.pop()
#        print(item_id)

        item = json_fetch('item', item_id, cache_only=False)

        if item is None:
            continue

        if item_id % 100 == 0:
            print(item_id)

        if item['type'] == 'story' and 'title' in item:# and 'url' in item and item['score']>3:
            print(f'[{item["score"]}] {item["title"]}')
            emb = get_embedding(item['title'])

            print(json.dumps(item, indent=2))

            dt = datetime.datetime.fromtimestamp(item["time"])
            pretty_time = dt.strftime("%Y-%m-%d %H:%M:%S")

            item['pretty_time'] = pretty_time

            new_item = {
                    'id': item['id'],
                    'score': item['score'],
                    'title': item['title'],
                    'time': item['time'],
                    'source': item['url'] if 'url' in item else '',
                }

            items.append(new_item)

            if item['score'] > 3:
                item_count += 1
                token_count += count_tokens(item['title'])

                delta_time =  datetime.datetime.now() - datetime.datetime.fromtimestamp(item['time'])

            if delta_time > datetime.timedelta(days=1):
                break

            print(item_count, token_count, pretty_time)

#        if len(items)>200:
#            break # archive not updated that far back yet



    with open('index.json', 'w') as f:
        f.write(json.dumps(items, indent=2))

populate()
