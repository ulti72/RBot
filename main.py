# -*- coding: utf-8 -*-
import webapp2
import jinja2
import os
import os.path
import unirest
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from requests_toolbelt.adapters import appengine

appengine.monkeypatch()
# defining template directory....
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

# Acessing spread sheet
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('Watashi-9b0820a4c2bd.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open('multiply').sheet1
# end of acessing spread sheet


# similarity
response = unirest.get("https://text-similarity-calculator.p.rapidapi.com/stringcalculator.php?ftext=This+is+text+numer+one.&stext=This+is+text+number+two.",
                       headers={
                           "X-RapidAPI-Key": "63b39b17cdmsh425c3215c4760dap1e4b6cjsn9bd19292da28"
                       }
                       )

# endsimiliraty


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler):
    def get(self):
        self.render("shopping_list.html")

    def post(self):
        val1 = "15276615"
        val2 = wks.acell('C2').value
        ans = "Excel: incorrect"
        if(val1 == val2):
            ans = "Excel: correct"
        self.response.out.write(response.body['percentage'])



        # mapping webpages/.......
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)


# self.redirect("/excel")
