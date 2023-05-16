import requests
import json
import random
import hashlib
import time

import tiktoken
encoding = tiktoken.get_encoding("cl100k_base") # gpt2 for gpt3, and cl100k_base for gpt3turbo

import openai
from api_keys import organisation, api_key
openai.organization = organisation
openai.api_key = api_key

import redis
r = redis.Redis(host='localhost', port=6379, db=0)

def md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

def ai3(system, prompt):
    return ai(system, prompt, "gpt-3.5-turbo")

def ai(system, prompt, model="gpt-4"):
    cache_key = f'ai-cache:{model}:' + md5(system+'***'+prompt)
    if r.exists(cache_key):
        return r.get(cache_key).decode('utf-8')

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt}
    ]

    while True:
        try:
            completion = openai.ChatCompletion.create(model=model, messages=messages)
            result = completion.choices[0].message.content
            r.set(cache_key, result)
            return result

        except Exception as e:
            # Print the error message in red color
            print("\033[91m" + f"Error occurred: {str(e)}" + "\033[0m")
            time.sleep(1)

def count_tokens(s):
    input_ids = encoding.encode(s)
    return len(input_ids)

def in_cache(url):
    return r.exists(url)

def download(url):
    response = requests.get(url)
    response.raise_for_status() # Check for any HTTP errors
    return response.content

def download_and_cache(url, cache_only=False, key_prefix=''):
    # Check if the content is already cached
    if r.exists(key_prefix+url):
        res = r.get(key_prefix+url)
        if res is not None:
            return res
    elif cache_only:
        return None

    while True:
        try:
            # If not cached, download and cache the content
            response = requests.get(url)
            response.raise_for_status() # Check for any HTTP errors
            content = response.content
            r.set(key_prefix+url, content)
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
