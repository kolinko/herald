#url = 'https://www.politico.com/news/magazine/2023/04/22/elon-musk-the-barking-mad-publicity-hound-00093293'

from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import api_keys
import json
# 53624cc2159a98ce7de73799d3a02bff

from common import ai, md5, download_and_cache

def fetch_text(url):

#url = 'https://www.bloomberg.com/news/articles/2023-04-21/alphabet-ceo-s-pay-soars-to-226-million-on-massive-stock-award?leadSource=uverify%20wall'

    url = f"http://api.scraperapi.com?api_key={api_keys.scrape_key}&url={url}"

    #url = "https://www.bloomberg.com/news/articles/2023-04-21/alphabet-ceo-s-pay-soars-to-226-million-on-massive-stock-award?leadSource=uverify%20wall"
#    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    #html = urlopen(url).read()
#    html = requests.get(url, headers=headers).text

    html = download_and_cache(url)
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text


def split_parts(s):
    lines = s.split('\n')
#    print(len(lines))
    section = ''
    res = {'':''}
    for l in lines:
        if l[:3] == '===':
            section = l[3:]
#            print(section)
            res[section] = ''
        else:
            res[section] += l+'\n'

    return res

def fetch_article(url):
    text = fetch_text(url)

    system_prompt = """
You are a text-processor. You receive a webpage stripped from html tags, and your job is to reply with the following format:

===title
(article title)
===text
(full article text)

Or, if the article is unreadable:

===error
(reason, if given)

Make sure that the article is transcribed in full - from first sentence to the last.
    """

#    print(text)
#    print('\n\n===\n\n')

    result = ai(system_prompt, text)
    
    return result #split_parts(result)

#    print(res['text'])
#    print(json.dumps(res, indent=2))
#    exit()


#url = "http://api.scraperapi.com?api_key=53624cc2159a98ce7de73799d3a02bff&url=https://www.cnn.com/2023/04/26/tech/south-korea-samsung-q1-profits-plunge-intl-hnk/index.html"

#url = "https://twitter.com/mysk_co/status/1651021165727477763"
'''
url = "https://www.cnn.com/2023/04/26/tech/south-korea-samsung-q1-profits-plunge-intl-hnk/index.html"
url = "https://www.afr.com/world/north-america/ray-dalio-says-china-us-on-brink-of-war-20230427-p5d3k8"
url = "https://www.theregister.com/2023/04/27/ntt_network_sharing_blockchain/"
url = "https://twitter.com/mysk_co/status/1651021165727477763"
art = fetch_article(url)

res = art
for r in res:
    print('---', r)
    print(res[r])
    '''
#print(text)