
import redis
import requests
import json


import random

r = redis.Redis(host='localhost', port=6379, db=0)

import time

import tiktoken
encoding = tiktoken.get_encoding("cl100k_base") # gpt2 for gpt3, and cl100k_base for gpt3turbo

def count_tokens(s):
    input_ids = encoding.encode(s)
    return len(input_ids)


def in_cache(url):
    return r.exists(url)

def download(url):
    response = requests.get(url)
    response.raise_for_status() # Check for any HTTP errors
    return response.content

def download_and_cache(url, cache_only=False):
    # Check if the content is already cached
    if cache_only:
        if r.exists(url):
            res = r.get(url)
            if res is not None:
                return res

        return None


    if r.exists(url):
        res = r.get(url)
        if res is not None:
            return res

    while True:
        try:
            # If not cached, download and cache the content
            response = requests.get(url)
            response.raise_for_status() # Check for any HTTP errors
            content = response.content
            r.set(url, content)
            return content
        except Exception as e:
            # Print the error message in red color
            print("\033[91m" + f"Error occurred: {str(e)}" + "\033[0m")
            # Sleep for some time before retrying
            time.sleep(random.randint(5, 60))

def json_fetch(kind, id, cache_only=False):
    url = f"https://hacker-news.firebaseio.com/v0/{kind}/{id}.json?print=pretty"

    result = download_and_cache(url, cache_only)
    if cache_only and result is None:
            return None

    return json.loads(result)
