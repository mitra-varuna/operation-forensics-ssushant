from google.appengine.ext import ndb

class OpSummary(ndb.Model):
    summary = ndb.StringProperty()
    score = ndb.FloatProperty()
    url = ndb.StringProperty()
    positive_comment = ndb.StringProperty()
    negative_comment = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
