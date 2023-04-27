
import json

import openai

import hashlib
import redis
import numpy as np

import time

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

r = redis.Redis(host='localhost', port=6379, db=0)

from api_keys import organisation, api_key
openai.organization = organisation
openai.api_key = api_key

def md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

def make_embeddings():
    pass

def get_embedding(text, model="text-embedding-ada-002"):
    h = 'embed:' + md5(text)

    if r.exists(h):
        res = json.loads(r.get(h))
        if res is not None:
            return res

    text = text.replace("\n", " ")
    res = openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']
#    print(res[:10])

    r.set(h, json.dumps(res))
    return res
