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

# tests
# https://github.com/aeon-toolkit/aeon - not a regular article
#  https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0291668  - timeouts with Article(url), but not with regular get

def fetch_article(main_url):
    if api_keys.scrape_key is not None:
        url = f"http://api.scraperapi.com?api_key={api_keys.scrape_key}&url={main_url}"

    try:
        article = Article(url)
        try:
            article.download()
            article.parse()
        except:
            article = None
        if article is None or count_tokens(article.text)<100:
            txt = fetch_text(main_url)
            out = ai("Summarise this article into five paragraphs. Output in a json format: {'title':'(title)', 'text':'(summary)'}", txt, json=True)
            return out
        elif count_tokens(article.text) < 5000:
            return json.dumps({'title': article.title, 'text': article.text})
        else:
            out = ai("Summarise this article into five paragraphs. Output in a json format: {'title':'(title)', 'text':'(summary)'}", article.text, json=True)
            return out
    except Exception as e:
        print(f'An error occurred: {e}')
        return json.dumps({'title': 'error', 'text': f'An error occurred while loading the article: {e}'})

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
