
import json

import openai

import hashlib
import redis
import numpy as np

import time
import tqdm

import datetime

from common import count_tokens, download, download_and_cache

from agent import * #make_paper, make_paper_first, make_paper_second, make_paper_third, ISSUE

r = redis.Redis(host='localhost', port=6379, db=0)

from api_keys import organisation, api_key
openai.organization = organisation
openai.api_key = api_key

idx = []

start_time = time.time() 

def pretty_time(ts):
    dt = datetime.datetime.fromtimestamp(ts)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def reset():
    global start_time
    start_time = time.time() 

def elapsed():
    elapsed_time = (time.time() - start_time) * 1000 # Get the elapsed time in milliseconds
    print(f"Time elapsed: {elapsed_time:.2f} ms")

print('Downloading new HN stories index...')
item_ids = json.loads(download_and_cache('https://hacker-news.firebaseio.com/v0/newstories.json', key_prefix=ISSUE))


# Define the base URL for the Hacker News API
API_BASE_URL = "https://hacker-news.firebaseio.com/v0"

# Define the endpoint for getting an item by ID
API_ITEM_ENDPOINT = "item/{}.json?print=pretty"
items = []

count = 0
error_count = 0
print('Downloading HN story details...')

for item_id in tqdm.tqdm(item_ids):
    count += 1
    item_url = f"{API_BASE_URL}/{API_ITEM_ENDPOINT.format(item_id)}"
#    print(f'downloading {item_id} [{count} of {len(item_ids)}]')
    item = download_and_cache(item_url)
    if json.loads(item) is None:
        continue

    item = json.loads(item)

    if 'url' not in item:
        continue

    for ignore_host in ['youtube.com', 'twitter.com']:
        if ignore_host in item['url']:
            break
    else:
        items.append(item)

count = 0
count_tokn = 0
stories_text = ''
stories_items = {}
for item in items:
    if 'kids' in item and len(item['kids'])>2:
#        print(json.dumps(item, indent=2))
        count += 1
        story = f'[{item["id"]}] {item["title"]}\n' # replace with id
        item['ai_text'] = story
        count_tokn += count_tokens(story)
        stories_items[str(item["id"])] = item
        stories_text += story
        oldest = item['time']

        if count_tokn > 4000:
            break

print(pretty_time(oldest))

print('Number of stories:',count)
print('token_count', count_tokn)

#make_pro_story(stories_items)
#exit()

make_paper_first(stories_items)
make_paper_second()
make_paper_third(stories_items)
make_paper_fourth()
make_paper_fifth()