from .models import OpSummary
from google.appengine.apu import urlfetch
URLS = []

def index():
    for url in URLS:
        result - urlfetch.fetch(url)
        if result.status_code == 200:
