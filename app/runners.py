import json
import logging

from google.appengine.api import urlfetch

import sentiments
from bs4 import BeautifulSoup
from .models import OpSummary, Entity

FEEDS = ['http://www.thehindu.com/opinion/?service=rss']

def feed_index():
    import feedparser
    for feed in FEEDS:
        d = feedparser.parse(feed)
        for entry in d.entries:
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
    entities = [Entity(photo_url=get_wikipedia_image(response['url']),
                       wikipedia_url=response['url'],
                       name=response['name'],
                       mention_type=response['mention_type'], salience=response['salience']) for response in
                analyse['entities']]
    ops = OpSummary(url=url, summary=summary, polarity=analyse['polarity'], entities=entities,
                    magnitude=analyse['magnitude'])
    ops.put()

    
def get_wikipedia_image(wikipedia_url):
    title = get_title(wikipedia_url)
    logging.info("Got the title {0}".format(title))
    if title:
        image_url = get_image(title)
        logging.info("Got the images {0}".format(image_url))
        if image_url:
            return image_url
        else:
            return None
    else:
        return None


def get_title(wikipedia_url):
    """Get the title given a wikipedia URL"""
    if wikipedia_url:
        (_, _, title) = wikipedia_url.partition("/wiki/")
        return title
    else:
        return None

def get_image(title):
    """Gets the list of images associated with the wikipedia title"""
    url = "https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles={0}".format(title)
    try:
        json_info = urlfetch.fetch(url)
        info = json.loads(json_info.content)
        for thumbnail_info in info['query']['pages'].values():
            if 'thumbnail' in thumbnail_info:
                image_url = thumbnail_info['thumbnail']['original']
                return image_url
    except Exception as e:
        logging.exception("Exception occured when getting wikipedia thumbanil for {0}".format(title))
        return None
