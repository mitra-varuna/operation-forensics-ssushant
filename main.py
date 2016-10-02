import webapp2
from app.runners import index
import json

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("hello sushant first gae app")

class GetSentiment(webapp2.RequestHandler):
    def get(self):
        self.response.write(json.dumps(index()))


app = webapp2.WSGIApplication([('/', GetSentiment),],
                              debug=True)
