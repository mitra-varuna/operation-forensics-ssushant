import logging
from time import mktime

from datetime import datetime
from google.appengine.api import urlfetch

import sentiments
from datastore_helper import update_datastore
from editorial_helper import get_editorial_content

FEEDS = ['http://www.thehindu.com/opinion/?service=rss']

def feed_index():
    """Get all the articles' content using the feeds and analyze them"""
    import feedparser
    for feed in FEEDS:
        parsed_feed = feedparser.parse(feed)
        for entry in parsed_feed.entries:
            parse_single_url(entry.link, entry.description, datetime.fromtimestamp(mktime(entry.published_parsed)))


def parse_single_url(url, summary, when):
    try:
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            content = process_editorial(url, result, summary, when)
        else:
            return {}
    except urlfetch.Error as e:
        logging.exception('Caught exception fetching url')


def process_editorial(url, result, summary, when):
    html_doc = result.content
    content = get_editorial_content(html_doc)
    analyse = sentiments.get_sentiment(content)
    update_datastore(analyse, summary, url, when)
