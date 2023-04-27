import json

from common import in_cache, download_and_cache, download, json_fetch, count_tokens

from helpers import get_embedding, cosine_similarity

with open('index.json', 'r') as f:
    idx = json.loads(f.read())


for item in idx:
#    print(item['title'])
    emb = get_embedding(item['title'])
    item['embedding'] = emb

def adv_in(idx, url):
    for i in idx:
        if i['source'] == url:
            return True

    return False

def dedupe(idx):
    res = []
    for i in range(len(idx)):
        if not adv_in(idx[i+1:], idx[i]['source']):
            res.append(idx[i])

    return res


def find(query, idx, indent=0):
    if type(query) is str:
        qemb = get_embedding(query)
    else:
        qemb = query

#    for item in idx:
#        item["similarity"] = cosine_similarity(item["embedding"], qemb)

    sorted_data = sorted(idx, key=lambda x: cosine_similarity(x["embedding"], qemb), reverse=True)

    res = []

    for row in sorted_data[:10]:
        if cosine_similarity(row['embedding'], qemb) < 0.9:
            continue

        res.append(row)
        if indent == 0:
            res += find(row['embedding'], idx, 2)
        '''
        if indent == 0:
            print()
        print(indent*' ', f"[{row['id']}] {cosine_similarity(row['embedding'], qemb):.2f} ", row['title'])     #{row['similarity']:.2f}
        print(indent*' ', row['source'])
        if indent==0:
            find(row['embedding'], idx, 2)
        '''

    return dedupe(res)

used_up = [] # list of urls that were already used up

count = 0
for item in idx:
    if item['source'] in used_up:
        print(count, 'skip', item['title'])
        continue
    count += 1
    print(count)
    res = find(item['title'], idx)
    if len(res)>1:
        for r in res:
            print(r['title'])
            print('    ', r['source'])
            used_up.append(r['source'])

        print('.')

find('Automakers are starting to admit that drivers hate touchscreens', idx)