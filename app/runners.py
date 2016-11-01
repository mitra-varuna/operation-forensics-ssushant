import logging

from google.appengine.api import urlfetch

import sentiments
from bs4 import BeautifulSoup
from datastore_helper import update_datastore
from .models import OpSummary

FEEDS = ['http://www.thehindu.com/opinion/?service=rss']

def feed_index():
    """Get all the articles' content using the feeds and analyze them"""
    import feedparser
    for feed in FEEDS:
        parsed_feed = feedparser.parse(feed)
        for entry in parsed_feed.entries:
            parse_single_url(entry.link, entry.description)


def parse_single_url(url, summary):
    try:
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            content = hindu_strategy(url, result, summary)
        else:
            return {}
    except urlfetch.Error as e:
        logging.exception('Caught exception fetching url')


def all_articles():
    return [f.to_dict(exclude=['date']) for f in OpSummary.query().fetch()]


def hindu_strategy(url, result, summary):
    html_doc = result.content
    bs = BeautifulSoup(html_doc)
    content = ''.join((p.text for p in bs.findAll('p',{'class':'body'})))
    analyse = sentiments.get_sentiment(content.replace('\n',''))
    update_datastore(analyse, summary, url)
