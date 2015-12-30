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

# For the drop-down select so we don't have to send the whole industry_data over.
industry_names = [
	{'id': 'consulting', 'display': 'Consulting'},
	{'id': 'industry2', 'display': 'Industry 2'}
]

# Contains all the info for the style guides > industry pages.
industry_data = [
	{
		'id': 'consulting',
		'display': 'Consulting',
		'style_data': [
			{
				'name': 'Business Formal',
				'image_src': '/images/businessformal.png',#TODO: FILLOUT
				'shop_link': 'about:blank',#TODO: FILLOUT
				'relevance': 'High',
				'activities': 'Client site activities',
				'attire': 'Dark suit, top'
			},
			{
				'name': 'Business Casual',
				'image_src': '/images/businesscasual.png',#TODO: FILLOUT
				'shop_link': 'about:blank',#TODO: FILLOUT
				'relevance': 'Medium',
				'activities': 'Casual fridays in office',
				'attire': 'Dress pant, shirt'
			},			
			{
				'name': 'Smart Casual',
				'image_src': '/images/smartcasual.png',#TODO: FILLOUT
				'shop_link': 'about:blank',#TODO: FILLOUT
				'relevance': 'Low',
				'activities': 'Happy hour, Social hangouts',
				'attire': 'Jeans, blazer'
			}
		]
	},
	{
		'id': 'industry2',
		'display': 'Industry 2',
		'style_data': [
			{
				'name': 'Business Formal',
				'image_src': '/images/businessformal.png',#TODO: FILLOUT
				'shop_link': 'about:blank',#TODO: FILLOUT
				'relevance': 'High',
				'activities': 'Nothing',
				'attire': 'Pants, shirt'
			},
			{
				'name': 'Smart Casual',
				'image_src': '/images/smartcasual.png',#TODO: FILLOUT
				'shop_link': 'about:blank',#TODO: FILLOUT
				'relevance': 'Medium',
				'activities': 'Something',
				'attire': 'Sandals, hat'
			},			
			{
				'name': 'Business Casual',
				'image_src': '/images/businesscasual.png',#TODO: FILLOUT
				'shop_link': 'about:blank',#TODO: FILLOUT
				'relevance': 'Low',
				'activities': 'Anything',
				'attire': 'Socks, gloves'
			}
		]
	}
]

coverflow_data = [
	{
		'caption': 'Bulbasaur',
		'image_src': '/images/bulbasaurllama.png'
	},
	{
		'caption': 'Ivysaur',
		'image_src': '/images/ivysaurllama.png'
	},
	{
		'caption': 'Venusaur',
		'image_src': '/images/venusaurllama.png'
	},
	{
		'caption': 'Charmander',
		'image_src': '/images/charmanderllama.png'
	},
	{
		'caption': 'Charmeleon',
		'image_src': '/images/charmeleonllama.png'
	},
	{
		'caption': 'Charizard',
		'image_src': '/images/charizardllama.png'
	},
	{
		'caption': 'Squirtle',
		'image_src': '/images/squirtlellama.png'
	},
	{
		'caption': 'Wartortle',
		'image_src': '/images/wartortlellama.png'
	},
	{
		'caption': 'Blastoise',
		'image_src': '/images/blastoisellama.png'
	},
]



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
		template_vars = {'coverflow_data': coverflow_data}

		who_wore_what_template = jinja_environment.get_template('templates/who_wore_what.html')
		logging.info('in who wore what handler logging')
		self.response.write(who_wore_what_template.render(template_vars))

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

class StyleGuidesIndustryHandler(webapp2.RequestHandler):
	def get(self):
		try: 
			selected_industry = self.request.get('industry')

			found_industry_data = {}

			for i in industry_data:
				if selected_industry == i['id']:
					found_industry_data = i
					break

			if found_industry_data == {}:
				logging.info('no industry data found for industry: ' + selected_industry)


			template_vars = {'industry_names': industry_names, 'industry_data': found_industry_data}

			# Check if it's a valid industry.
			if self.request.get('industry') == '':
				print "didn't get a valid industry value in get request."

			else:
				# Display normal style guides page.
				industry_template = jinja_environment.get_template('templates/industry.html')
				logging.info('in industry handler logging')
				self.response.write(industry_template.render(template_vars))

		except(TypeError, ValueError):
			self.response.write('<html><body><p>Invalid industry."</p></body></html>')


class StyleGuidesHandler(webapp2.RequestHandler):
	def get(self):
		logging.info('created industries list')

		style_guides_template = jinja_environment.get_template('templates/style_guides.html')
		logging.info('in style guides handler logging')
		self.response.write(style_guides_template.render({'industry_names': industry_names}))



app = webapp2.WSGIApplication([
    ('/shop.*', ShopHandler),
    ('/whoworewhat.*', WhoWoreWhatHandler),
    ('/styleguides/smartcasual.*', SmartCasualHandler),
    ('/styleguides/businesscasual.*', BusinessCasualHandler),
    ('/styleguides/businessformal.*', BusinessFormalHandler),
    ('/styleguides/industry.*', StyleGuidesIndustryHandler),
    ('/styleguides.*', StyleGuidesHandler),
    # ('/styleguides', StyleGuidesHandler),
    ('/.*', HomeHandler)
], debug=True)
