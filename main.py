import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("hello sushant first gae app")


app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)
