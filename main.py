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

class SimilarStyle(ndb.Model):
    img_src = ndb.TextProperty(required=True)
    item_page = ndb.TextProperty(required=True)
    description = ndb.TextProperty(required=False)
    brand = ndb.TextProperty(required=False)
    price = ndb.FloatProperty(required=False)

class Posting(ndb.Model):
    img_src = ndb.TextProperty(required=True)
    description = ndb.TextProperty(required=True)
    date = ndb.DateProperty(required=True)
    similar_style_keys = ndb.KeyProperty(kind='SimilarStyle', repeated=True)

class Person(ndb.Model):
    name = ndb.StringProperty(required=True)
    bio = ndb.TextProperty(required=True)
    postings = ndb.LocalStructuredProperty(Posting, repeated=True)

class Coverflow(ndb.Model):
    name = ndb.StringProperty(required=True)

    # NOTE: images must be same width x height. otherwise becomes really distorted.
    img_src = ndb.TextProperty(required=True)

    # Default added to beginning of the coverflow.
    order_id = ndb.IntegerProperty(required=False, default=0)

class DropdownSection(ndb.Model):
    dropdown = ndb.StringProperty(required=True) # Which dropdown is it in.
    heading = ndb.StringProperty(required=False, default='')
    items = ndb.TextProperty(repeated=True)
    order_id = ndb.IntegerProperty(required=False, default=0)

class LookOccasion(ndb.Model):
    style = ndb.StringProperty(required=True)
    look_img_src = ndb.TextProperty(required=True)
    look_descriptions = ndb.TextProperty(repeated=True)
    occasion_img_src = ndb.TextProperty(required=True)
    occasion_descriptions = ndb.TextProperty(repeated=True)
    order_id = ndb.IntegerProperty(required=False, default=0)
    shop_page = ndb.TextProperty(required=True)

class IndustryStyle(ndb.Model):
    industry = ndb.StringProperty(required=True)
    style = ndb.StringProperty(required=True)
    img_src = ndb.TextProperty(required=True)
    relevance = ndb.TextProperty(required=True)
    activities = ndb.TextProperty(repeated=True)
    attire = ndb.TextProperty(repeated=True)
    shop_page = ndb.TextProperty(required=True)

    




class HomeHandler(webapp2.RequestHandler):
    def get(self):
        self.datastore()

        template_vars = {
                'styleguide_sections': self.app.config.get('styleguide_sections')}
        logging.info(self.app.config.get('styleguide_sections'))

        home_template = jinja_environment.get_template('templates/home.html')
        logging.info('in main handler logging')
        self.response.write(home_template.render(template_vars))

    def datastore(self):
        ############################################################# BEGIN DATASTORE ####
        logging.info('hello from datastore')

        #===================================================================== PERSON === 
        monocle= SimilarStyle(
                img_src='/images/monocleandmustache.png', 
                item_page='TODO', 
                description='Comes with a free mustache.',
                brand='JCrew',
                price=19.99)
        monocle_key = monocle.put()
        
        tophat = SimilarStyle(
                img_src='/images/tophat.png', 
                item_page='TODO', 
                description='Top hat from club penguin.',
                brand='Ann Taylor',
                price=29.99)
        tophat_key = tophat.put()

        posting_one = Posting(
                img_src='/images/gentlemoncharmander.png', 
                description='Spotted in downtown aiwefj awoeifj awefjoifj afio jefoief ojifaoi jafljeafkj fdsl jawefoi fjifdsoi jweafeoi jwefi f ej aefoij awefij Cerulean City with a new top hat and monocle.', 
                date=datetime.date(2016, 1, 4))

        posting_one.similar_style_keys.append(tophat_key)
        posting_one.similar_style_keys.append(monocle_key)

        onesie = SimilarStyle(
                img_src='/images/charmanderonesie.jpg', 
                item_page='TODO', 
                description='Onesies!',
                brand='JCrew',
                price=19.99)
        onesie_key = onesie.put()

        familyofonesies= SimilarStyle(
                img_src='/images/familyofcharmanders.jpg', 
                item_page='TODO', 
                description='Because why not.',
                brand='Ann Taylor',
                price=29.99)
        familyofonesies_key = familyofonesies.put()

        posting_two = Posting(
                img_src='/images/charmanderascharizard.jpg', 
                description='Dressed as Charizard.', 
                date=datetime.date(2015, 9, 16))

        posting_two.similar_style_keys.append(onesie_key)
        posting_two.similar_style_keys.append(familyofonesies_key)

        charmander = Person(
                name='Charmander', 
                bio="Charmander is a bipedal, reptilian Pokemon with an orange body, though its underside and soles are cream colored. It has two small fangs visible in its upper and lower jaws and blue eyes. Its arms and legs are short with four fingers and three clawed toes. A fire burns at the tip of this Pokemon's slender tail, and has blazed there since Charmander's birth. The flame can be used as an indication of Charmander's health and mood, burning brightly when the Pokemon is strong, weakly when it is exhausted, wavering when it is happy, and blazing when it is enraged. It is said that Charmander dies if its flame goes out. Charmander can be found in hot, mountainous areas. However, it is found far more often in the ownership of Trainers. Charmander exhibits pack behavior, calling others of its species if it finds food.",
                postings=[posting_one, posting_two])
        charmander.put()

        #================================================================ COVERFLOW === 

        bulbasaur = Coverflow(
                name='Bulbasaur', 
                img_src='/images/bulbasaurllama.png', 
                order_id=0)
        bulbasaur.put()

        ivysaur = Coverflow(
                name='Ivysaur', 
                img_src='/images/ivysaurllama.png',
                order_id=1)
        ivysaur.put()

        venusaur = Coverflow(
                name='Venasaur', 
                img_src='/images/venusaurllama.png',
                order_id=2)
        venusaur.put()

        charmander = Coverflow(
                name='Charmander', 
                img_src='/images/charmanderllama.png',
                order_id=3)
        charmander.put()

        charmeleon = Coverflow(
                name='Charmeleon', 
                img_src='/images/charmeleonllama.png',
                order_id=4)
        charmeleon.put()

        charizard = Coverflow(
                name='Charizard', 
                img_src='/images/charizardllama.png',
                order_id=5)
        charizard.put()

        squirtle = Coverflow(
                name='Squirtle', 
                img_src='/images/squirtlellama.png',
                order_id=6)
        squirtle.put()

        wartortle = Coverflow(
                name='Wartortle', 
                img_src='/images/wartortlellama.png',
                order_id=7)
        wartortle.put()

        blastoise = Coverflow(
                name='Blastoise', 
                img_src='/images/blastoisellama.png',
                order_id=8)
        blastoise.put()

        #================================================================== DROPDOWNS === 
        """
        general_styles = DropdownSection(
                heading='General', 
                items=['Smart Casual', 'Business Casual', 'Business Formal'], 
                dropdown='Style Guides',
                order_id=0)
        general_styles.put()

        industry_styles = DropdownSection(
                heading='Industry', 
                items=['Consulting', 'Industry 2'], 
                dropdown='Style Guides',
                order_id=1)
        industry_styles.put()

        men_shop_filters = DropdownSection(
                heading='Men', 
                items=['Tops', 'Bottoms', 'Suits', 'Outerwear'], 
                dropdown='Shop',
                order_id=0)
        men_shop_filters.put()

        women_shop_filters = DropdownSection(
                heading='Women', 
                items=['Tops', 'Bottoms', 'Dresses', 'Suits', 'Outerwear'], 
                dropdown='Shop',
                order_id=1)
        women_shop_filters.put()
        """

        #=============================================================== LOOKOCCASION === 
        
        smartcasual_one = LookOccasion(
                style='Smart Casual',
                look_img_src='/images/smartcasual.png',
                look_descriptions=['White jeans and top', 'Beige blazer'],
                occasion_img_src='/images/smartcasual.png',
                occasion_descriptions=['Casual Fridays'],
                order_id=0,
                shop_page='TODO')
        smartcasual_one.put()

        smartcasual_two = LookOccasion(
                style='Smart Casual',
                look_img_src='/images/smartcasual.png',
                look_descriptions=['Something', 'Or another'],
                occasion_img_src='/images/smartcasual.png',
                occasion_descriptions=['The Happy Hour'],
                order_id=1,
                shop_page='TODO')
        smartcasual_two.put()

        businesscasual_one = LookOccasion(
                style='Business Casual',
                look_img_src='/images/businesscasual.png',
                look_descriptions=['White jeans and top', 'Beige blazer'],
                occasion_img_src='/images/businesscasual.png',
                occasion_descriptions=['Casual Fridays'],
                order_id=0,
                shop_page='TODO')
        businesscasual_one.put()

        businesscasual_two = LookOccasion(
                style='Business Casual',
                look_img_src='/images/businesscasual.png',
                look_descriptions=['Something', 'Or another'],
                occasion_img_src='/images/businesscasual.png',
                occasion_descriptions=['The Happy Hour'],
                order_id=1,
                shop_page='TODO')
        businesscasual_two.put()

        businessformal_one = LookOccasion(
                style='Business Formal',
                look_img_src='/images/businessformal.png',
                look_descriptions=['White jeans and top', 'Beige blazer'],
                occasion_img_src='/images/businessformal.png',
                occasion_descriptions=['Casual Fridays'],
                order_id=0,
                shop_page='TODO')
        businessformal_one.put()

        businessformal_two= LookOccasion(
                style='Business Formal',
                look_img_src='/images/businessformal.png',
                look_descriptions=['Something', 'Or another'],
                occasion_img_src='/images/businessformal.png',
                occasion_descriptions=['The Happy Hour'],
                order_id=1,
                shop_page='TODO')
        businessformal_two.put()

        #=========================================================== INDUSTRYSTYLE === 

        consulting_sc = IndustryStyle(
                industry='Consulting',
                style='Smart Casual',
                img_src='/images/smartcasual.png',
                relevance='Low',
                activities=['Happy hour', 'Social hangouts'],
                attire=['Jeans', 'Blazer'],
                shop_page='TODO')
        consulting_sc.put()

        consulting_bc = IndustryStyle(
                industry='Consulting',
                style='Business Casual',
                img_src='/images/businesscasual.png',
                relevance='Medium',
                activities=['Casual fridays in office'],
                attire=['Dress pant', 'Shirt'],
                shop_page='TODO')
        consulting_bc.put()

        consulting_bf = IndustryStyle(
                industry='Consulting',
                style='Business Formal',
                img_src='/images/businessformal.png',
                relevance='High',
                activities=['Client site activities'],
                attire=['Dark suit', 'Top', 'etc.'],
                shop_page='TODO')
        consulting_bf.put()

        industry_sc = IndustryStyle(
                industry='Industry 2',
                style='Smart Casual',
                img_src='/images/smartcasual.png',
                relevance='High',
                activities=['Happy hour', 'Social hangouts'],
                attire=['Jeans', 'Blazer'],
                shop_page='TODO')
        industry_sc.put()

        industry_bc = IndustryStyle(
                industry='Industry 2',
                style='Business Casual',
                img_src='/images/businesscasual.png',
                relevance='Low',
                activities=['Casual fridays in office'],
                attire=['Dress pant', 'Shirt'],
                shop_page='TODO')
        industry_bc.put()

        industry_bf = IndustryStyle(
                industry='Industry 2',
                style='Business Formal',
                img_src='/images/businessformal.png',
                relevance='Medium',
                activities=['Client site activities'],
                attire=['Dark suit', 'Top', 'etc.'],
                shop_page='TODO')
        industry_bf.put()


        ############################################################### END DATASTORE ####

class ShopHandler(webapp2.RequestHandler):
    def get(self):

        filters = [
            {
                'name': 'Gender',
                'selections': ['Men', 'Women']
            },
            {
                'name': 'Type',
                'selections': ['Tops', 'Bottoms', 'Dresses', 'Suits', 'Overwear']
            }
        ]

        template_vars = {
                'styleguide_sections': self.app.config.get('styleguide_sections'),
                'filters': filters}

        shop_template = jinja_environment.get_template('templates/shop.html')
        logging.info('in shop handler logging')
        self.response.write(shop_template.render(template_vars))

class WhoWoreWhatHandler(webapp2.RequestHandler):
    def get(self):
        coverflow_data = Coverflow.query().order(Coverflow.order_id).fetch()

        template_vars = {
                'coverflow_data': coverflow_data,
                'styleguide_sections': self.app.config.get('styleguide_sections')}

        who_wore_what_template = jinja_environment.get_template('templates/who_wore_what.html')
        logging.info('in who wore what handler logging')
        self.response.write(who_wore_what_template.render(template_vars))

class WhoWoreWhatPersonHandler(webapp2.RequestHandler):
    def get(self):
        try: 
            person_arg = self.request.get('person') 

            query = Person.query(getattr(Person, 'name') == person_arg)
            results = query.fetch()
            logging.info('results')
            logging.info(results)

            # Calling get() on similar styles and saving in a dictionary.
            posting_to_similar_style_dict = {}

            for p in results[0].postings:
                similar_styles = []
                for key in p.similar_style_keys:
                    similar_styles.append(key.get())
                # Using posting img_src as a unique ID. TODO: define an actual UID.
                posting_to_similar_style_dict[p.img_src] = similar_styles

            template_vars = {
                    'person': results[0], 
                    'posting_to_similar_styles_dict': posting_to_similar_style_dict, 
                    'styleguide_sections': self.app.config.get('styleguide_sections')}

            # Check if it's a valid person.
            if self.request.get('person') == '':
                print "didn't get a valid person value in get request."

            else:
                # Display normal style guides page.
                person_template = jinja_environment.get_template('templates/person.html')
                logging.info('in person handler logging')
                self.response.write(person_template.render(template_vars))

        except(TypeError, ValueError):
            self.response.write('<html><body><p>Invalid person.</p></body></html>')

class StyleGuidesIndustryHandler(webapp2.RequestHandler):
    def get(self):
        try: 
            industry_arg = self.request.get('industry')

            industry_results= IndustryStyle.query(getattr(IndustryStyle, 'industry') == industry_arg).fetch()

            logging.info(industry_results)

            industry_dict = {}

            for r in industry_results:
                industry_dict[r.relevance] = r

            logging.info(industry_dict)

            industry_data = [
                    industry_dict['High'], 
                    industry_dict['Medium'], 
                    industry_dict['Low']]

            logging.info(industry_data)

            template_vars = {
                    'industry_names': industry_names, 
                    'industry_data': industry_data, 
                    'industry': industry_arg,
                    'styleguide_sections': self.app.config.get('styleguide_sections')}

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

            style_data = LookOccasion.query(getattr(LookOccasion, 'style') == style_arg).order(LookOccasion.order_id).fetch()

            template_vars = {
                    'industry_names': industry_names, 
                    'style_data': style_data, 
                    'style': style_arg,
                    'styleguide_sections': self.app.config.get('styleguide_sections')}

            # Check if it's a valid industry.
            if style_arg == '':
                print "didn't get a valid style value in get request."

            else:
                # Display normal industry page.
                style_template = jinja_environment.get_template('templates/style.html')
                logging.info('in style handler logging')
                self.response.write(style_template.render(template_vars))

        except(TypeError, ValueError):
            self.response.write('<html><body><p>Invalid style.</p></body></html>')


class StyleGuidesHandler(webapp2.RequestHandler):
    def get(self):

        style_data = [
                {'name': 'Smart Casual', 'img_src': '/images/smartcasual.png'},
                {'name': 'Business Casual', 'img_src': '/images/businesscasual.png'},
                {'name': 'Business Formal', 'img_src': '/images/businessformal.png'}]

        template_vars = {
                'industry_names': industry_names, 
                'style_data': style_data, 
                'styleguide_sections': self.app.config.get('styleguide_sections')}

        style_guides_template = jinja_environment.get_template('templates/style_guides.html')
        logging.info('in style guides handler logging')
        self.response.write(style_guides_template.render(template_vars))


app = webapp2.WSGIApplication(routes=[
    ('/shop.*', ShopHandler),
    ('/whoworewhat/person.*', WhoWoreWhatPersonHandler),
    ('/whoworewhat.*', WhoWoreWhatHandler),
    ('/styleguides/industry.*', StyleGuidesIndustryHandler),
    ('/styleguides/style.*', StyleGuidesStyleHandler),
    ('/styleguides.*', StyleGuidesHandler),
    ('/.*', HomeHandler)
], debug=True, config={
    'styleguide_sections': DropdownSection.query(getattr(DropdownSection, 'dropdown') == 'Style Guides').order(DropdownSection.order_id).fetch() 
})
