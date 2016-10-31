from .models import OpSummary, Entity
from google.appengine.api import urlfetch
import json
from bs4 import BeautifulSoup
import logging
import sentiments

FEEDS = ['http://www.thehindu.com/opinion/?service=rss']

def feed_index():
    import feedparser
    for feed in FEEDS:
        d = feedparser.parse(feed)
        for entry in d.entries:
            parse_single_url(entry.link)


def index():
    response = []
    for url in URLS:
        try:
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                content = hindu_strategy(url, result)
                #response.append(get_sentiment(content))
            else:
                return {}
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')
    return response
    # return hindu_strategy(None, None)

def parse_single_url(url):
    try:
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            content = hindu_strategy(url, result)
            #response.append(get_sentiment(content))
        else:
            return {}
    except urlfetch.Error:
        logging.exception('Caught exception fetching url')

def all_articles():
    return [f.to_dict(exclude=['date']) for f in OpSummary.query().fetch()]


def hindu_strategy(url, result):
    html_doc = result.content
    bs = BeautifulSoup(html_doc)
    content = ''.join((p.text for p in bs.findAll('p',{'class':'body'})))
    summary = bs.findAll('h1', {'class':'detail-title'})[0].text
    analyse = sentiments.get_sentiment(content.replace('\n',''))
    entities = [Entity(photo_url=None, wikipedia_url=r['url'], name=r['name'],mention_type=r['mention_type'],salience=r['salience']) for r in analyse['entities']]
    ops = OpSummary(url=url, summary=summary, polarity=analyse['polarity'], entities=entities,magnitude=analyse['magnitude'])
    ops.put()
