from .models import OpSummary
from google.appengine.api import urlfetch
from googleapiclient import discovery
import httplib2
import json
from oauth2client.client import GoogleCredentials
from bs4 import BeautifulSoup
import logging

DISCOVERY_URL = ('https://{api}.googleapis.com/'
                 '$discovery/rest?version={apiVersion}')
URLS = ['http://www.thehindu.com/opinion/editorial/a-nobel-push-for-peace-in-colombia/article9198670.ece']
http = httplib2.Http()
credentials = GoogleCredentials.get_application_default().create_scoped(
['https://www.googleapis.com/auth/cloud-platform']
)
credentials.authorize(http)
service = discovery.build('language', 'v1beta1', http=http, discoveryServiceUrl=DISCOVERY_URL, developerKey='AIzaSyC91OWR65l9h8Wi9YX1ULQ7SFhhO65ZSsg')

def get_sentiment(doc):
    service_request = service.documents().annotateText(body={
         'document':{
             'type':'PLAIN_TEXT',
             'content':doc
         },
         'features': {
             "extractSyntax": False,
             "extractEntities": True,
             "extractDocumentSentiment": True,
          },
          'encodingType':'UTF32'
    })
    response = service_request.execute()
    logging.error("Response from api {0}".format(response))
    polarity = response['documentSentiment']['polarity']
    magnitude = response['documentSentiment']['magnitude']
    entities = []
    for r in response['entities']:
        wikipedia_url = None
        if 'wikipedia_url'in r['metadata']:
            wikipedia_url = r['metadata']['wikipedia_url']
        entities.append(dict(salience=r['salience'], mention_type=r['type'],url=wikipedia_url, name=r['name']))
    return dict(polarity=polarity, magnitude=magnitude, entities=entities)


def index():
    response = []
    for url in URLS:
        try:
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                content = hindu_strategy(result.content)
                response.append(get_sentiment(content))
            else:
                return {}
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')
    return response

def hindu_strategy(html_doc):
    content = ''.join((p.text for p in BeautifulSoup(html_doc).findAll('p',{'class':'body'})))
    return content.replace('\n','')
