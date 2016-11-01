from models import Entity, OpSummary
from wiki_helper import get_wikipedia_image


def update_datastore(analyse, summary, url, when):
    entities = [Entity(photo_url=get_wikipedia_image(response['url']),
                       wikipedia_url=response['url'],
                       name=response['name'],
                       mention_type=response['mention_type'], salience=response['salience']) for response in
                analyse['entities']]
    ops = OpSummary(url=url, summary=summary, polarity=analyse['polarity'], entities=entities,
                    magnitude=analyse['magnitude'], when=when)
    ops.put()
