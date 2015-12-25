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
# jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))


class HomeHandler(webapp2.RequestHandler):
	def get(self):
		home_template = jinja_environment.get_template('templates/home.html')
		logging.info('in main handler logging')
		self.response.write(home_template.render())

class ShopHandler(webapp2.RequestHandler):
	def get(self):
		shop_template = jinja_environment.get_template('templates/shop.html')
		logging.info('in shop handler logging')
		self.response.write(shop_template.render())

class WhoWoreWhatHandler(webapp2.RequestHandler):
	def get(self):
		who_wore_what_template = jinja_environment.get_template('templates/who_wore_what.html')
		logging.info('in who wore what handler logging')
		self.response.write(who_wore_what_template.render())

class StyleGuidesHandler(webapp2.RequestHandler):
	def get(self):
		style_guides_template = jinja_environment.get_template('templates/style_guides.html')
		logging.info('in style guides handler logging')
		self.response.write(style_guides_template.render())

class SmartCasualHandler(webapp2.RequestHandler):
	def get(self):
		smart_casual_template = jinja_environment.get_template('templates/smart_casual.html')
		logging.info('in smart casual handler logging')
		self.response.write(smart_casual_template.render())

class BusinessCasualHandler(webapp2.RequestHandler):
	def get(self):
		business_casual_template = jinja_environment.get_template('templates/business_casual.html')
		logging.info('in business casual handler logging')
		self.response.write(business_casual_template.render())

class BusinessFormalHandler(webapp2.RequestHandler):
	def get(self):
		business_formal_template = jinja_environment.get_template('templates/business_formal.html')
		logging.info('in business formal handler logging')
		self.response.write(business_formal_template.render())

class StyleGuidesKeyWordsHandler(webapp2.RequestHandler):
	def get(self):
		# Dictionary of 'select value': 'display name' of an industry.
		industries = {'industry1': 'Industry 1', 'industry2': 'Industry 2', 'industry3': 'Industry 3'}
		logging.info('created industries list')
		try: 
			style = self.request.get('style')
			industry = self.request.get('industry')

			logging.info('url arg style: ' + style)
			logging.info('url arg industry: ' + industry)

			if style == 'businessformal':
				business_formal_template = jinja_environment.get_template('templates/business_formal.html')
				logging.info('in business formal handler logging')
				self.response.write(business_formal_template.render())

			else:
				# Display normal style guides page.
				style_guides_template = jinja_environment.get_template('templates/style_guides.html')
				logging.info('in style guides handler logging')
				self.response.write(style_guides_template.render({'industries': industries}))

		except(TypeError, ValueError):
			self.response.write('<html><body><p>Invalid Style Guides URL. Try something like "/styleguides?style=&industry="</p></body></html>')



app = webapp2.WSGIApplication([
    ('/shop', ShopHandler),
    ('/whoworewhat', WhoWoreWhatHandler),
    ('/styleguides.*', StyleGuidesKeyWordsHandler),
    # ('/styleguides/smartcasual', SmartCasualHandler),
    # ('/styleguides/businesscasual', BusinessCasualHandler),
    # ('/styleguides/businessformal', BusinessFormalHandler),
    ('/styleguides', StyleGuidesHandler),
    ('/.*', HomeHandler)
], debug=True)
