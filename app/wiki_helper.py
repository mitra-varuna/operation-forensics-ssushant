import json
import logging

from google.appengine.api import urlfetch


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
    url = "https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles={0}".format(
        title)
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
