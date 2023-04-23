
import json

import openai

import hashlib
import redis
import numpy as np

import time

r = redis.Redis(host='localhost', port=6379, db=0)

from api_keys import organisation, api_key
openai.organization = organisation
openai.api_key = api_key

idx = []

start_time = time.time() 

def reset():
    global start_time
    start_time = time.time() 

def elapsed():
    elapsed_time = (time.time() - start_time) * 1000 # Get the elapsed time in milliseconds
    print(f"Time elapsed: {elapsed_time:.2f} ms")

with open('index.json', 'r') as f:
    items = json.loads(f.read())

count = 0

for item in items:
    if item['score']>5:
        count += 1
        print(f'[{item["id"]}] {item["title"]}')


