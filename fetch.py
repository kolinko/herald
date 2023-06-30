#
# a tool for scraping websites for articles
# 
# fetch_text(url) - fetches URL with a help of scraperAPI
# fetch_article(url) - fetch_text + clean it up using GPT
#

from newspaper import Article

from bs4 import BeautifulSoup
import requests
import api_keys
import json

from common import ai, download_and_cache, count_tokens, ai16k

def fetch_article(url):
    if api_keys.scrape_key is not None:
        url = f"http://api.scraperapi.com?api_key={api_keys.scrape_key}&url={url}"

    article = Article(url)
    article.download()
    try:
        article.parse()
        if count_tokens(article.text) < 5000:
            return f'''
===title
{article.title}
===text
{article.text}
            '''
        elif count_tokens(article.text) < 12000:
            ai16k('Summarise this article into five paragraphs', article.title)
        else:
            new_text = article.text
            out_text = ''
            while len(new_text)>0:

                clipped = ''
                while count_tokens(clipped) < 10000 and len(new_text)>0:
                    clipped += new_text[:10]
                    new_text = new_text[10:]
                out_text += ai16k('Summarise this into three paragraphs', clipped) + '\n\n'

            return f'''
===title
{article.title}
===text
{article.text}
'''

    except:
        return article.html


def fetch_text(url):
    if api_keys.scrape_key is not None:
        url = f"http://api.scraperapi.com?api_key={api_keys.scrape_key}&url={url}"

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
    # splits text returned by gpt via fetch_article into parts
    # we use this formatting instead of JSON because GPT is more consistent
    # in producing a well formatted output this way - no issues with json escaping

    lines = s.split('\n')
    section = ''
    res = {'':''}
    for l in lines:
        if l[:3] == '===':
            section = l[3:]
            res[section] = ''
        else:
            res[section] += l+'\n'

    return res
