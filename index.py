
import json

import openai

import hashlib
import redis
import numpy as np

import time

import datetime

from common import count_tokens

from agent import make_paper

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

with open('index.json', 'r') as f:
    items = json.loads(f.read())

count = 0
count_tokn = 0
stories_text = ''
stories_items = {}
for item in items:
    if item['score']>5:
        count += 1
        story = f'[{item["score"]}] {item["title"]}\n' # replace with id
        count_tokn += count_tokens(story)
        stories_items[str(item["id"])] = item
        stories_text += story
        oldest = item['time']
        
        if count_tokn > 4000:
            break

print(pretty_time(oldest))

print('num stories:',count)

#print(stories_text)
exit()
make_paper(stories_items)

