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
				'shop_page': 'about:blank',#TODO: FILLOUT
				'relevance': 'High',
				'activities': ['Client site activities'],
				'attire': ['Dark suit', 'Top']
			},
			{
				'name': 'Business Casual',
				'image_src': '/images/businesscasual.png',#TODO: FILLOUT
				'shop_page': 'about:blank',#TODO: FILLOUT
				'relevance': 'Medium',
				'activities': ['Casual fridays in office'],
				'attire': ['Dress pant', 'Shirt']
			},			
			{
				'name': 'Smart Casual',
				'image_src': '/images/smartcasual.png',#TODO: FILLOUT
				'shop_page': 'about:blank',#TODO: FILLOUT
				'relevance': 'Low',
				'activities': ['Happy hour', 'Social hangouts'],
				'attire': ['Jeans', 'Blazer']
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
				'shop_page': 'about:blank',#TODO: FILLOUT
				'relevance': 'High',
				'activities': ['Nothing'],
				'attire': ['Pants', 'Shirt']
			},
			{
				'name': 'Smart Casual',
				'image_src': '/images/smartcasual.png',#TODO: FILLOUT
				'shop_page': 'about:blank',#TODO: FILLOUT
				'relevance': 'Medium',
				'activities': ['Something'],
				'attire': ['Sandals', 'Hat']
			},			
			{
				'name': 'Business Casual',
				'image_src': '/images/businesscasual.png',#TODO: FILLOUT
				'shop_page': 'about:blank',#TODO: FILLOUT
				'relevance': 'Low',
				'activities': ['Anything'],
				'attire': ['Socks', 'Gloves']
			}
		]
	}
]

## NOTE: images must be same width x height. otherwise becomes really distorted.
coverflow_data = [
	{
		'caption': 'Bulbasaur',
		'id': 'bulbasaur',
		'image_src': '/images/bulbasaurllama.png'
	},
	{
		'caption': 'Ivysaur',
		'id': 'ivysaur',
		'image_src': '/images/ivysaurllama.png'
	},
	{
		'caption': 'Venusaur',
		'id': 'venusaur',
		'image_src': '/images/venusaurllama.png'
	},
	{
		'caption': 'Charmander',
		'id': 'charmander',
		'image_src': '/images/charmanderllama.png'
	},
	{
		'caption': 'Charmeleon',
		'id': 'charmeleon',
		'image_src': '/images/charmeleonllama.png'
	},
	{
		'caption': 'Charizard',
		'id': 'charizard',
		'image_src': '/images/charizardllama.png'
	},
	{
		'caption': 'Squirtle',
		'id': 'squirtle',
		'image_src': '/images/squirtlellama.png'
	},
	{
		'caption': 'Wartortle',
		'id': 'wartortle',
		'image_src': '/images/wartortlellama.png'
	},
	{
		'caption': 'Blastoise',
		'id': 'blastoise',
		'image_src': '/images/blastoisellama.png'
	}
]

person_data = [
	{
		'id': 'charmander',
		'display': 'Charmander',
		'bio': "Charmander is a bipedal, reptilian Pokemon with an orange body, though its underside and soles are cream-colored. It has two small fangs visible in its upper and lower jaws and blue eyes. Its arms and legs are short with four fingers and three clawed toes. A fire burns at the tip of this Pokemon's slender tail, and has blazed there since Charmander's birth. The flame can be used as an indication of Charmander's health and mood, burning brightly when the Pokemon is strong, weakly when it is exhausted, wavering when it is happy, and blazing when it is enraged. It is said that Charmander dies if its flame goes out. Charmander can be found in hot, mountainous areas. However, it is found far more often in the ownership of Trainers. Charmander exhibits pack behavior, calling others of its species if it finds food.",
		'postings': [
			{
				'image_src': '/images/gentlemoncharmander.png',
				'date': '2015-12-30',
				'description': 'Spotted in downtown balw awoiejf laiwjf a oifjaefoi jaeof ijewfoija ifjei oeawif id oieaa oeaijfaoeif efi jeaofi jefi jewaoifj oiewafj Cerulean City with a new top hat and monocle.',
				'similar_styles': [
					{
						'image_src': '/images/tophat.png',
						'brand': 'Ann Taylor',
						'price': '29.99',
						'description': 'Top hat from club penguin.'
					},
					{
						'image_src': '/images/monocleandmustache.png',
						'brand': 'JCrew',
						'price': '19.99',
						'description': 'Comes with a free mustache.'
					}
				]
			},
			{
				'image_src': '/images/charmanderascharizard.jpg',
				'date': '2015-09-07',
				'description': 'Dressed as Charizard.',
				'similar_styles': [
					{
						'image_src': '/images/charmanderonesie.jpg',
						'brand': 'Ann Taylor',
						'price': '29.99',
						'description': 'Onesies!'
					},
					{
						'image_src': '/images/familyofcharmanders.jpg',
						'brand': 'JCrew',
						'price': '19.99',
						'description': 'Because why not.'
					}
				]
			}
		]
	}
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

class WhoWoreWhatPersonHandler(webapp2.RequestHandler):
	def get(self):
		try: 
			person_arg = self.request.get('person')

			template_vars = {}

			found_person_data = {}

			for i in person_data:
				if person_arg == i['id']:
					found_person_data = i
					break

			if found_person_data == {}:
				logging.info('no person data found for person: ' + person_arg)


			template_vars = {'person_data': found_person_data}

			# Check if it's a valid person.
			if self.request.get('person') == '':
				print "didn't get a valid person value in get request."

			else:
				# Display normal style guides page.
				person_template = jinja_environment.get_template('templates/person.html')
				logging.info('in person handler logging')
				self.response.write(person_template.render(template_vars))

		except(TypeError, ValueError):
			self.response.write('<html><body><p>Invalid person."</p></body></html>')

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
			industry_arg = self.request.get('industry')

			found_industry_data = {}

			for i in industry_data:
				if industry_arg == i['id']:
					found_industry_data = i
					break

			if found_industry_data == {}:
				logging.info('no industry data found for industry: ' + industry_arg)


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
    ('/whoworewhat/person.*', WhoWoreWhatPersonHandler),
    ('/whoworewhat.*', WhoWoreWhatHandler),
    ('/styleguides/smartcasual.*', SmartCasualHandler),
    ('/styleguides/businesscasual.*', BusinessCasualHandler),
    ('/styleguides/businessformal.*', BusinessFormalHandler),
    ('/styleguides/industry.*', StyleGuidesIndustryHandler),
    ('/styleguides.*', StyleGuidesHandler),
    # ('/styleguides', StyleGuidesHandler),
    ('/.*', HomeHandler)
], debug=True)
