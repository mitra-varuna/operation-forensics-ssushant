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
            parse_single_url(entry.link, entry.description)


def parse_single_url(url, summary):
    try:
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            content = hindu_strategy(url, result, summary)
        else:
            return {}
    except urlfetch.Error:
        logging.exception('Caught exception fetching url')

def all_articles():
    return [f.to_dict(exclude=['date']) for f in OpSummary.query().fetch()]


def hindu_strategy(url, result, summary):
    html_doc = result.content
    bs = BeautifulSoup(html_doc)
    content = ''.join((p.text for p in bs.findAll('p',{'class':'body'})))
    #summary = bs.findAll('h1', {'class':'detail-title'})[0].text
    analyse = sentiments.get_sentiment(content.replace('\n',''))
    wikipedia_url = r['url']
    entities = [Entity(photo_url=get_wikipedia_image(wikipedia_url), wikipedia_url=r['url'], name=r['name'],mention_type=r['mention_type'],salience=r['salience']) for r in analyse['entities']]
    ops = OpSummary(url=url, summary=summary, polarity=analyse['polarity'], entities=entities,magnitude=analyse['magnitude'])
    ops.put()

    
def get_wikipedia_image(wikipedia_url):
    title = get_title(wikipedia_url)
    if title:
        images = get_image(title)
        if images:
            return images
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
        info = json.loads(json_info)
        for  i in info['query']['pages'].values():
            if 'thumbnail' in i:
                image_url = i['thumbnail']['original']
                return image_url
    except Exception:
        return None
