#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import db
import datetime

import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+"/templates"))

class Message(db.Model):
	content = db.StringProperty(multiline = True,required = True)
	Name = db.StringProperty(required = False)
	year = db.StringProperty(required = True)

class max_inserted(db.Model):
	maximum=db.IntegerProperty(required = True)
	
class MainHandler(webapp2.RequestHandler):
    def get(self):
		user = users.get_current_user()
		self.response.out.write('''
<!DOCTYPE html>
<html>
<title>DHS P&P</title>
	<head>
		<link type="text/css" rel="stylesheet" href="../stylesheets/main.css" />
		<header>
			<ul>
				<li><a href = ".">Main Page</a></li>
				<li><a href = "./appinfo/">App Info</a></li>
				<li style = "padding: 14px 16px;border-right:none;">Welcome to DHS Past & Present</li> 
				<ul style = "float:right;list-style-type:none;">''')
		if user:
			self.response.out.write('''
					<li style = "display:block;padding: 14px 16px;text-align:centre;">Welcome, {0}</li>
					<li><a href="./signout/">Log out</a></li>'''.format(user.nickname()))
		else:
			self.response.out.write('''
					<li style = "display:block;padding: 14px 16px;text-align:centre;"></li>
					<li><a href="./signin/">Log in</a></li>''')
		self.response.out.write('''
			</ul>
			</ul>
		</header>
	</head
	<body>
		<section id = "post">
			<h3>Post Your Past Experience: </h3>
			<form method= "post">''')
		if user:
			self.response.out.write('''
				<textarea name = "Message" placeholder = "Post Your Past Experiences Here" rows = "7" cols = "100"required></textarea></br>
				<!--input type="file" name="image"/></br-->
				<label>Year of Experience: </label><select name = "year"></br>''')
			for i in range(1956,datetime.datetime.now().year + 1):
				self.response.out.write('''<option value ="{0}">{0}</option>'''.format(i))
			self.response.out.write('''</select></br>
				<input type = "submit"/>
			</form>
		</section>
		<section id = "posts">
		<h2 style="text-decoration:underline;">Past Experiences</h2>''')
		else:
			self.response.out.write('''<h4>Please <a href="./signin/">log in</a> to post</h4>
			</form>
		</section>
		<section id = "posts">
		<h2 style="text-decoration:underline;">Past Experiences: </h2>''')
		self.query=max_inserted.all()
		inserted = []
		for self.max_inserted in self.query:
			inserted.append(self.max_inserted.maximum)
		if inserted == []:
			maximum_inserted=0
		else:
			maximum_inserted = max(inserted)+1
		for i in range(maximum_inserted):
			current_message=Message.get_or_insert(str(maximum_inserted-i-1))
			self.response.write('<p><strong>Written by {0}</br>Year of Experience: {2}</br></strong>{1}</p>'.format(current_message.Name,current_message.content,current_message.year))
		self.response.out.write('''
		</section>
	</body>
	<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-74526689-1', 'auto');
  ga('send', 'pageview');

</script>
</html>''')
    def post(self):
		self.query=max_inserted.all()
		inserted = []
		for self.max_inserted in self.query:
			inserted.append(self.max_inserted.maximum)
		if inserted == []:
			maximum_inserted=0
		else:
			maximum_inserted = max(inserted)+1
		self.message=Message(key_name=str(maximum_inserted),Name=users.get_current_user().email(),content=self.request.get("Message"),year=self.request.get("year"))
		self.max_inserted=max_inserted(maximum=maximum_inserted)
		self.message.put()
		self.max_inserted.put()
		self.redirect("/")
class AppInfoHandler(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('appinfo.html')
		self.response.out.write(template.render())

class LoginHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			self.redirect("/")
		else:
			self.redirect(users.create_login_url(self.request.uri))
			
class LogoutHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			self.redirect(users.create_logout_url(self.request.uri))
		else:
			self.redirect("/")

app = webapp2.WSGIApplication([('/', MainHandler),
								('/signin/',LoginHandler),('/signout/',LogoutHandler),('/appinfo/',AppInfoHandler)], debug=True)
