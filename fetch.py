#url = 'https://www.politico.com/news/magazine/2023/04/22/elon-musk-the-barking-mad-publicity-hound-00093293'

from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests


def fetch_text(url):

#url = 'https://www.bloomberg.com/news/articles/2023-04-21/alphabet-ceo-s-pay-soars-to-226-million-on-massive-stock-award?leadSource=uverify%20wall'

    #url = "https://www.bloomberg.com/news/articles/2023-04-21/alphabet-ceo-s-pay-soars-to-226-million-on-massive-stock-award?leadSource=uverify%20wall"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    #html = urlopen(url).read()
    html = requests.get(url, headers=headers).text
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

#print(text)