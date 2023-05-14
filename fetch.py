from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import api_keys
import json

from common import ai, download_and_cache

USE_SCRAPERAPI = True
# scraperapi is extremely useful for going around websites protections for crawling
# if you switch to False, the websites will be downloaded directly, but in many situations
# it will result in no article contents fetched

def fetch_article(url):
    # Returns an article from a given URL that is stripped of all tags and split into title and text
    # The output can be easily parsed into a list by using split_parts defined below

    # Using gpt-4 here:
    # - gpt-3 tended to ommit and rewrite parts of the article
    # - gpt-4's context length is longer, so this will break on fewer articles
    #
    # Using this format instead of json, because it's hard to wrangle gpt-4 into producing a valid json in this case
    # (due to it not escaping quotes properly, and newlines either)
    #
    # Error should be produced if website contains no decent article - e.g. only a message that javascript is disabled etc

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

    result = ai(system_prompt, text)

    return result #split_parts(result)

def fetch_text(url):
    if USE_SCRAPERAPI:
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

    lines = s.split('\n')
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


