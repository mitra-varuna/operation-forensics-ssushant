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
URLS = ['http://www.thehindu.com/opinion/lead/rakesh-sood-writes-on-the-aftermath-of-uri-terror-attacks-uri-as-inflection-point/article9169396.ece']
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
          }
    })
    response = service_request.execute()
    logging.error("Response from api {0}".format(response))
    polarity = response['documentSentiment']['polarity']
    magnitude = response['documentSentiment']['magnitude']
    return response


def index():
    response = []
    for url in URLS:
        try:
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                content = ''.join((p.text for p in BeautifulSoup(result.content).findAll('p',{'class':'body'})))
                content = content.replace('\n','')
                response.append(get_sentiment(content))
            else:
                return {}
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')
    return response
