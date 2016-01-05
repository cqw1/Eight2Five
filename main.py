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
import jinja2
import logging
import os
import webapp2

import datetime
from datetime import date
from google.appengine.ext import ndb

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

style_data = [
	{
		'id': 'smartcasual',
		'display': 'Smart Casual',
		'image_src': '/images/smartcasual.png',
		'styles': [
			{
				'look': {
					'image_src': '/images/smartcasual.png',
					'descriptions': ['White jeans and top aofeij ef awejf ewafio jawef aewf ijweof ijewf oijewaof jwae', 'Beige blazer']
				},
				'occasion': {
					'image_src': '/images/smartcasual.png',
					'descriptions': ['Casual fridays']
				}
			},
			{
				'look': {
					'image_src': '/images/smartcasual.png',
					'descriptions': ['Blank']
				},
				'occasion': {
					'image_src': '/images/smartcasual.png',
					'descriptions': ['The happy hour']
				}
			}
		]
	},
	{
		'id': 'businesscasual',
		'display': 'Business Casual',
		'image_src': '/images/businesscasual.png',
		'styles': [
			{
				'look': {
					'image_src': '/images/businesscasual.png',
					'descriptions': ['blah']
				},
				'occasion': {
					'image_src': '/images/businesscasual.png',
					'descriptions': ['Casual fridays']
				}
			},
			{
				'look': {
					'image_src': '/images/businesscasual.png',
					'descriptions': ['Blank', 'Blank']
				},
				'occasion': {
					'image_src': '/images/businesscasual.png',
					'descriptions': ['The happy hour']
				}
			}
		]
	},
	{
		'id': 'businessformal',
		'display': 'Business Formal',
		'image_src': '/images/businessformal.png',
		'styles': [
			{
				'look': {
					'image_src': '/images/businessformal.png',
					'descriptions': ['blah']
				},
				'occasion': {
					'image_src': '/images/businessformal.png',
					'descriptions': ['Casual fridays']
				}
			},
			{
				'look': {
					'image_src': '/images/businessformal.png',
					'descriptions': ['Blank', 'Blank']
				},
				'occasion': {
					'image_src': '/images/businessformal.png',
					'descriptions': ['The happy hour']
				}
			}
		]
	}
]

class Person(ndb.Model):
    name = ndb.StringProperty(required=True)
    bio = ndb.TextProperty(required=True)
    posting_keys = ndb.KeyProperty(kind='Posting', repeated=True)

class Posting(ndb.Model):
    img_src = ndb.TextProperty(required=True)
    description = ndb.TextProperty(required=True)
    date = ndb.DateProperty(required=True)
    similar_style_keys = ndb.KeyProperty(kind='SimilarStyle', repeated=True)

class SimilarStyle(ndb.Model):
    img_src = ndb.TextProperty(required=True)
    item_page = ndb.TextProperty(required=True)
    description = ndb.TextProperty(required=True)

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        self.datastore()

        home_template = jinja_environment.get_template('templates/home.html')
        logging.info('in main handler logging')
        self.response.write(home_template.render())

    def datastore(self):
        ############################################################# BEGIN DATASTORE ####
        logging.info('hello from datastore')

        monocle= SimilarStyle(img_src='/images/monocleandmustache.png', item_page='TODO', description='Comes with a free mustache.')
        monocle_key = monocle.put()
        
        tophat = SimilarStyle(img_src='/images/tophat.png', item_page='TODO', description='Top hat from club penguin.')
        tophat_key = tophat.put()

        posting_one = Posting(img_src='/images/gentlemoncharmaner.png', description='Spotted in downtown aiwefj awoeifj awefjoifj afio jefoief ojifaoi jafljeafkj fdsl jawefoi fjifdsoi jweafeoi jwefi f ej aefoij awefij Cerulean City with a new top hat and monocle.', date=datetime.date(2016, 1, 4))

        posting_one.similar_style_keys.append(tophat_key)
        posting_one.similar_style_keys.append(monocle_key)
        posting_one_key = posting_one.put()

        onesie = SimilarStyle(img_src='/images/charmanderonesie.jpg', item_page='TODO', description='Onesies!')
        onesie_key = onesie.put()
        familyofonesies= SimilarStyle(img_src='/images/familyofcharmanders.jpg', item_page='TODO', description='Because why not.')
        familyofonesies_key = familyofonesies.put()

        posting_two = Posting(img_src='/images/charmanderascharizard.png', description='Dressed as Charizard.', date=datetime.date(2015, 9, 16))

        posting_two.similar_style_keys.append(onesie_key)
        posting_two.similar_style_keys.append(familyofonesies_key)
        posting_two_key = posting_two.put()

        charmander = Person(name='Charmander', bio="Charmander is a bipedal, reptilian Pokemon with an orange body, though its underside and soles are cream colored. It has two small fangs visible in its upper and lower jaws and blue eyes. Its arms and legs are short with four fingers and three clawed toes. A fire burns at the tip of this Pokemon's slender tail, and has blazed there since Charmander's birth. The flame can be used as an indication of Charmander's health and mood, burning brightly when the Pokemon is strong, weakly when it is exhausted, wavering when it is happy, and blazing when it is enraged. It is said that Charmander dies if its flame goes out. Charmander can be found in hot, mountainous areas. Howver, it is found far more often in the ownership of Trainers. Charmander exhibits pack behavior, calling others of its species if it finds food.")
        charmander.posting_keys.append(posting_one_key)
        charmander.posting_keys.append(posting_two_key)
        charmander.put()

        ############################################################### END DATASTORE ####

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

class StyleGuidesStyleHandler(webapp2.RequestHandler):
	def get(self):
		try: 
			style_arg = self.request.get('style')

			found_style_data = {}

			for i in style_data:
				if style_arg == i['id']:
					found_style_data = i
					break

			if found_style_data == {}:
				logging.info('no style data found for style: ' + style_arg)


			template_vars = {'industry_names': industry_names, 'style_data': found_style_data}

			# Check if it's a valid industry.
			if style_arg == '':
				print "didn't get a valid style value in get request."

			else:
				# Display normal industry page.
				style_template = jinja_environment.get_template('templates/style.html')
				logging.info('in style handler logging')
				self.response.write(style_template.render(template_vars))

		except(TypeError, ValueError):
			self.response.write('<html><body><p>Invalid style."</p></body></html>')


class StyleGuidesHandler(webapp2.RequestHandler):
	def get(self):
		logging.info('created industries list')

		style_guides_template = jinja_environment.get_template('templates/style_guides.html')
		logging.info('in style guides handler logging')
		self.response.write(style_guides_template.render({'industry_names': industry_names, 'style_data': style_data}))


app = webapp2.WSGIApplication([
    ('/shop.*', ShopHandler),
    ('/whoworewhat/person.*', WhoWoreWhatPersonHandler),
    ('/whoworewhat.*', WhoWoreWhatHandler),
    ('/styleguides/smartcasual.*', SmartCasualHandler),
    ('/styleguides/businesscasual.*', BusinessCasualHandler),
    ('/styleguides/businessformal.*', BusinessFormalHandler),
    ('/styleguides/industry.*', StyleGuidesIndustryHandler),
    ('/styleguides/style.*', StyleGuidesStyleHandler),
    ('/styleguides.*', StyleGuidesHandler),
    ('/.*', HomeHandler)
], debug=True)
