import webapp2
from app.runners import index, all_articles, feed_index
import json

class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super(DatetimeEncoder, obj).default(obj)
        except TypeError:
            return str(obj)

class IndexPage(webapp2.RequestHandler):
    def get(self):
        feed_index()
        self.response.write("Articles indexed for today")

class GetSentiment(webapp2.RequestHandler):
    def get(self):
        self.response.write(json.dumps(all_articles(),cls=DatetimeEncoder))



app = webapp2.WSGIApplication([('/', GetSentiment), ('/index', IndexPage)],
                              debug=True)
