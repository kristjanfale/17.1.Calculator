#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

    def post(self):
        stevilka_ena = float(self.request.get("stevilka1"))
        stevilka_dva = float(self.request.get("stevilka2"))
        operacija = self.request.get("operacija")

        if operacija == "sestevanje":
            rezultat = stevilka_ena + stevilka_dva
        if operacija == "odstevanje":
            rezultat = stevilka_ena - stevilka_dva
        if operacija == "mnozenje":
            rezultat = stevilka_ena * stevilka_dva
        if operacija == "deljenje":
            rezultat = stevilka_ena / stevilka_dva

        return self.render_template("hello.html", params={"sporocilo": rezultat})
        #return self.write("Rezultat je: %s" % rezultat)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
