import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), '')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
	autoescape=True)

def get_posts(limit, offset):
	homepage_q = db.GqlQuery("SELECT * FROM Art WHERE created ASC")

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.write(*a, **kw)

	def render_str(self,template,**params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class Art(db.Model):
	title = db.StringProperty(required=True)
	art = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add = True)
	#art_id = db.

class ViewPostHandler(Handler):
	#def id(self):
	#	req.query_string()

	def render_front(self, id, title="", artwork="", error=""):
		#id = "4785074604081152"
		post = Art.get_by_id (int(id))
		#arts = db.GqlQuery("SELECT * FROM Art ORDER BY ID LIMIT 1")
		self.render("post.html", post=post)

	def get(self, id):
		self.render_front(id=id)

	def post(self):
		if posts:
			return Art.get_by_id(5733953138851840) #self.render('/blog/'+ id)
		else:
			return error(404)

class MainPage(Handler):
	def render_front(self, title="", artwork="", error=""):
		arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC LIMIT 5")
		self.render("main.html", title=title, artwork=artwork, error=error, arts=arts)

	def get(self):
		# self.render("front.html")
		self.render_front()

	def post(self):
		title = self.request.get('title')
		art = self.request.get('art')

		if title and art:
			# self.write('Thanks!')
			# Create an instance 'a' of art object
			a = Art(title=title, art=art)
			# Store new art object instance in the database
			a.put()
			self.redirect('/')
		else:
			error = "Enter title AND a post with text! Don't screw around!"
			self.render_front(title=title, artwork=art, error=error)

app = webapp2.WSGIApplication([
('/', MainPage),
webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
