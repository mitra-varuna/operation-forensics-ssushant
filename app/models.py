from google.appengine.ext import ndb

class Entity(ndb.Model):
    photo_url = ndb.StringProperty()
    wikipedia_url = ndb.StringProperty()
    name = ndb.StringProperty()
    mention_type = ndb.StringProperty()
    salience = ndb.FloatProperty()

class OpSummary(ndb.Model):
    summary = ndb.StringProperty()
    url = ndb.StringProperty()
    entities = ndb.StructuredProperty(Entity, repeated=True)
    polarity = ndb.FloatProperty()
    magnitude = ndb.FloatProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    when = ndb.DateProperty(auto_now_add=True)

    @classmethod
    def get_today_articles(cls):
        OpSummary.query(projection=[OpSummary.summary, OpSummary.url, OpSummary.polarity, OpSummary.magnitude]). \
            fetch()
