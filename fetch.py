#
# a tool for scraping websites for articles
# 
# fetch_text(url) - fetches URL with a help of scraperAPI
# fetch_article(url) - fetch_text + clean it up using GPT
#

from bs4 import BeautifulSoup
import requests
import api_keys
import json

from common import ai, download_and_cache, count_tokens

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

    assert count_tokens(text) < 7000 # todo: for longer articles, chunk them and summarise, so that we can provide them as prompt later on
    

    if count_tokens(text) > 2000: # ideally it should be > 5000, but as of 19 May 2023, 
                                  # OpenAI keeps lagging with longer prompts
        return fetch_long_article(text)

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

#    if 'apnews' in url:
#        print(text)
#        print()

    try:

        result = ai(system_prompt, text, retry=False)
#        if 'apnews' in url:
#            print('done!', url)
    except:
        result = text

    return result #split_parts(result)

def fetch_long_article(text):
    system_prompt = """
You are a text-processor. You receive a webpage stripped from html tags, and your job is to reply with the following format:

===title
(article title)
===text-beginning
(first two sentences of the article, verbatim)
===text-ending
(last two sentences of the article, verbatim)

Or, if the article is unreadable:

===error
(reason, if given)

Make sure that the article is transcribed in full - from first sentence to the last.
    """

    try:
        result = ai(system_prompt, text, retry=False)
        parts = split_parts(result)
    except:
        return text # give up, return plain html and hope for the best

    if 'error' in parts:
        return result

    if 'title' not in parts or \
        'text-beginning' not in parts or \
        'text-ending' not in parts:
        return text

    beginning = parts['text-beginning']
    ending = parts['text-ending']

    while len(beginning) > 0:
        if text.find(beginning)>=0:
            text = text[text.find(beginning):]
            break
        else:
            beginning = beginning[:-1]

    while len(ending) > 0:
        if text.rfind(ending)>=0:
            text = text[:text.rfind(ending)+1]
            break
        else:
            ending = ending[:-1]


    return f"""===title
{parts['title']}
===text
{text}
"""


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
