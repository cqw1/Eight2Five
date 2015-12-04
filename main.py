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
import webapp2
import logging
import jinja2
import os

# Sets jinja's relative directory to match the directory name (dirname) of the current __file__, in this case, main.py
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class HomeHandler(webapp2.RequestHandler):
	def get(self):
		home_template = jinja_environment.get_template('templates/home.html')
		logging.info('in main handler logging')
		self.response.write(home_template.render())

class ShopHandler(webapp2.RequestHandler):
	def get(self):
		print "hello"
		shop_template = jinja_environment.get_template('templates/shop.html')
		logging.info('in shop handler logging')
		self.response.write(shop_template.render())

class WhoWoreWhatHandler(webapp2.RequestHandler):
	def get(self):
		whoworewhat_template = jinja_environment.get_template('templates/whoworewhat.html')
		logging.info('in who wore what handler logging')
		self.response.write(whoworewhat_template.render())

class StyleGuidesHandler(webapp2.RequestHandler):
	def get(self):
		styleguides_template = jinja_environment.get_template('templates/styleguides.html')
		logging.info('in style guides handler logging')
		self.response.write(styleguides_template.render())

app = webapp2.WSGIApplication([
    ('/shop', ShopHandler),
    ('/whoworewhat', WhoWoreWhatHandler),
    ('/styleguides', StyleGuidesHandler),
    ('/.*', HomeHandler)
], debug=True)
