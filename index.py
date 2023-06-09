import json

import time
import tqdm

import datetime

from common import count_tokens, download, download_and_cache, pretty_time, json_fetch

from agent import make_paper_first, make_paper_second, make_paper_third, make_paper_fourth, make_paper_fifth

import paper

print('Downloading new HN stories index...')
item_ids = json.loads(download_and_cache('https://hacker-news.firebaseio.com/v0/newstories.json', key_prefix=paper.issue))

items = []

print('Downloading HN story details...')

for item_id in tqdm.tqdm(item_ids):
    try:
        item = json_fetch('item', item_id)
    except:
        continue

    if 'url' not in item:
        continue

    ignore_hosts = ['youtube.com', 'twitter.com']
    if any(host in item['url'] for host in ignore_hosts):
        continue

    items.append(item)


# filter new stories
count_tokn = 0
stories_text = ''
stories_items = {}
for item in items:
    # criteria for story exclusion:
    if 'kids' not in item or len(item['kids'])<=2:
        continue
    # /criteria

    story = f'[{item["id"]}] {item["title"]}\n'
    item['ai_text'] = story
    count_tokn += count_tokens(story)
    stories_items[str(item["id"])] = item
    stories_text += story

    if count_tokn > 4000:
        break

print('Oldest post:', pretty_time(items[-1]['time']))
print('Number of stories:',len(items))
print('Token count:', count_tokn)

# Paper generation below

# prepare a list of article tites
make_paper_first(stories_items)

# prepare Editors' note
make_paper_second()

# write each article
make_paper_third(stories_items)

# add ads
make_paper_fourth()

# generate html
make_paper_fifth()
