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
import csv
import datetime
import jinja2
import logging
import os
import time
import webapp2
import webapp2_extras.appengine.auth.models

from datetime import date
from google.appengine.ext import ndb
from webapp2_extras import security
from webapp2_extras import sessions
from webapp2_extras import auth


# Sets jinja's relative directory to match the directory name (dirname) of the current __file__, in this case, main.py
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

APPARELS = [
    'top', 
    'bottom', 
    'dress', 
    'suits', 
    'outerwear'
]

BRANDS = [
    'J. Crew', 
    'Ann Taylor',
    'Zara',
    'Banana Republic'
]

DRESS_CODES = [
    'smart casual', 
    'biz casual', 
    'biz formal',
    'tech casual'
]

# Alpha sorted.
INDUSTRIES = [
    'consulting'
]

# Alpha sorted.
OCCASIONS = [
    'client meeting',
    'interview'
]

SHOP_SORTS = [
    'name [a - z]', 
    'name [z - a]', 
    'price [low - high]', 
    'price [high - low]', 
    'date [new - old]', 
    'date [old - new]'
]

SHOP_SORT_DEFAULT = SHOP_SORTS[4]

ITEMS_PER_PAGE = [
        30, 
        60,
        90, 
        'all'
]

ITEMS_PER_PAGE_DEFAULT = ITEMS_PER_PAGE[1]

PAGE_DEFAULT = 1

RELEVANCE = [
    'high',
    'medium',
    'low'
]

populated = False

with open('categories.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        values = row[1: len(row)]
        values = [v for v in values if v] # Remove empty strings from list.

        if row[0] == 'apparel':
            APPARELS = values #Take everything except first element which is the key
        elif row[0] == 'occasion':
            OCCASIONS = values
        elif row[0] == 'dress_code':
            DRESS_CODES = values
        elif row[0] == 'brand':
            logging.info(values)
            BRANDS = values
        elif row[0] == 'industry':
            INDUSTRIES = values
        logging.info(row)

# Taken from blog.abahgat.com/2013/01/07/user-authentication-with-webapp2-on-google-app-engine/
class User(webapp2_extras.appengine.auth.models.User):
    def set_password(self, raw_password):
        """Sets the password for the current User
        :param raw_password:
            The raw password which will be hashed and stored.
        """
        self.password = security.generate_password_hash(raw_password, length=12)

    def get_by_auth_token(cls, user_id, token, subject='auth'):
        """Returns a user object based on a user ID and token.

        :param user_id:
            The user_id of the requesting user.
        :param token:
            The token string to be verified.
        :returns:
            A tuple (User, timestamp), with a user object and the token 
            timestamp, or (None, None) if both were not found.
        """
        token_key = cls.token_model.get_key(user_id, subject, token)
        user_key = ndb.Key(cls, user_id)
        # Use get_multi() to save a RPC call
        valid_token, user = ndb.get_multi([token_key, user_key])
        if valid_token and user:
            timestamp = int(time.mktime(valid_token.created.timetuple()))
            return user, timestamp

        return None, None

class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def auth(self):
        """Shortcut to access the auth instance as a property."""
        return auth.get_auth()

    @webapp2.cached_property
    def user_info(self):
        """Shortcut to access a subset of the user attributes that are stored
        in the session.

        The list of attributes to store in the session is specified in 
        config['webapp2_extras.auth']['user_attributes'].

        :returns
            A dictionary with most user information.
        """
        return self.auth.get_user_by_session()

    @webapp2.cached_property
    def user(self):
        """Shortcut to access the current logged in user.

        Unlike user_info, it fetches information from the persistence layer and
        returns an instance of the underlying model.

        :returns
            The instance of the user model associated to the logged in user.
        """
        u = self.user_info
        return self.user_model.get_by_id(u['user_id']) if u else None

    @webapp2.cached_property
    def user_model(self):
        """Returns the implementation of the user model.

        It is consistent with config['webapp2_extras.auth']['user_model'], if set.
        """
        return self.auth.store.user_model

    @webapp2.cached_property
    def session(self):
        """Shortcut to access the current session."""
        return self.session_store.get_session(backend="datastore")

    def render_template(self, view_filename, params={}):
        user = self.user_info
        params['user'] = user

        template = jinja_environment.get_template(view_filename)
        self.response.write(template.render(params))

    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions
            self.session_store.save_sessions(self.response)

##################################################################################


class SimilarStyle(ndb.Model):
    img_src = ndb.TextProperty(required=True)
    item_page = ndb.TextProperty(required=True)
    description = ndb.TextProperty(required=False)
    brand = ndb.TextProperty(required=False, choices=BRANDS)
    price = ndb.FloatProperty(required=False)

"""
class Posting(ndb.Model):
    img_src = ndb.TextProperty(required=True)
    description = ndb.TextProperty(required=True)
    date = ndb.DateProperty(required=True)
    similar_style_keys = ndb.KeyProperty(kind='SimilarStyle', repeated=True)
"""

class Posting(ndb.Model):
    id = ndb.IntegerProperty(required=True) # Unique id
    date = ndb.DateProperty(required=True)
    title = ndb.TextProperty(required=True)
    imgs = ndb.TextProperty(repeated=True)
    links = ndb.TextProperty(repeated=True) # Format: 'text: url'
    description = ndb.TextProperty(required=True)
    dress_code = ndb.TextProperty(required=True, choices=DRESS_CODES)

class Person(ndb.Model):
    # Name must match coverflow name.
    name = ndb.StringProperty(required=True)
    bio = ndb.TextProperty(required=True)
    # postings = ndb.LocalStructuredProperty(Posting, repeated=True)

class Look(ndb.Model):
    img_src = ndb.TextProperty(required=True)
    description = ndb.TextProperty(required=True)
    date = ndb.DateProperty(required=True)
    similar_style_keys=ndb.KeyProperty(kind='SimilarStyle', repeated=True)
    person = ndb.LocalStructuredProperty(Person)

    # Unique id for each look.
    id = ndb.IntegerProperty(required=True)

class Coverflow(ndb.Model):
    # Name must match person name.
    name = ndb.StringProperty(required=True)

    # NOTE: images must be same width x height. otherwise becomes really distorted. Or flows out of div.
    img_src = ndb.TextProperty(required=True)

    # Default added to beginning of the coverflow.
    order_id = ndb.IntegerProperty(required=False, default=0)

class DropdownSection(ndb.Model):
    dropdown = ndb.StringProperty(required=True) # Which dropdown is it in.
    heading = ndb.StringProperty(required=False, default='')
    items = ndb.TextProperty(repeated=True)
    order_id = ndb.IntegerProperty(required=False, default=0)

class StyleInfo(ndb.Model):
    name = ndb.StringProperty(required=True)
    # Really need to find a better way to do this if it grows too large.
    look_1_img = ndb.StringProperty(required=True)
    look_1_name = ndb.StringProperty(required=True)
    look_1_brand = ndb.StringProperty(required=True)
    look_1_tip = ndb.StringProperty(required=True)
    look_2_img = ndb.StringProperty(required=True)
    look_2_name = ndb.StringProperty(required=True)
    look_2_brand = ndb.StringProperty(required=True)
    look_2_tip = ndb.StringProperty(required=True)
    look_3_img = ndb.StringProperty(required=True)
    look_3_name = ndb.StringProperty(required=True)
    look_3_brand = ndb.StringProperty(required=True)
    look_3_tip = ndb.StringProperty(required=True)
    occasion_1_img = ndb.StringProperty(required=True)
    occasion_1_text = ndb.StringProperty(required=True)
    occasion_2_img = ndb.StringProperty(required=True)
    occasion_2_text = ndb.StringProperty(required=True)
    occasion_3_img = ndb.StringProperty(required=True)
    occasion_3_text = ndb.StringProperty(required=True)
    tip = ndb.StringProperty(required=True)



class LookOccasion(ndb.Model):
    dress_code = ndb.StringProperty(required=True, choices=DRESS_CODES)
    look_img_src = ndb.TextProperty(required=True)
    look_descriptions = ndb.TextProperty(repeated=True)
    occasion_img_src = ndb.TextProperty(required=True)
    occasion_descriptions = ndb.TextProperty(repeated=True)
    order_id = ndb.IntegerProperty(required=False, default=0)
    shop_page = ndb.TextProperty(required=True)

class IndustryStyle(ndb.Model):
    industry = ndb.StringProperty(required=True, choices=INDUSTRIES)
    dress_code = ndb.StringProperty(required=True, choices=DRESS_CODES)
    img_src = ndb.TextProperty(required=True)
    relevance = ndb.TextProperty(required=True, choices=RELEVANCE)
    activities = ndb.TextProperty(repeated=True)
    attire = ndb.TextProperty(repeated=True)
    shop_page = ndb.TextProperty(required=True)

class Item(ndb.Model):
    # Must be unique.
    sku_id = ndb.IntegerProperty(required=True)

    name = ndb.StringProperty(required=True)
    brand = ndb.StringProperty(required=True, choices=BRANDS)
    apparels = ndb.StringProperty(repeated=True, choices=APPARELS)
    price = ndb.FloatProperty(required=True)
    industries = ndb.StringProperty(repeated=True, choices=INDUSTRIES)
    dress_codes = ndb.StringProperty(repeated=True, choices=DRESS_CODES)
    occasions = ndb.StringProperty(repeated=True, choices=OCCASIONS)

    # Description (product info) on item page.
    description = ndb.TextProperty(required=False, default='Description currently unavailable.')

    # Main image on shopping grid page.
    img_1_src = ndb.TextProperty(required=True)
    img_2_src = ndb.TextProperty(required=True)

    # Link to outside website.
    external_src = ndb.TextProperty(required=True)

    # Smaller images shown on item page of different perspectives.
    smaller_imgs = ndb.TextProperty(repeated=True)

    # Date added to database
    date = ndb.DateProperty(required=True)

    # Whether current item is out of stock at parent website. 
    #out_of_stock = ndb.BooleanProperty(required=True)

class DatastoreHandler(webapp2.RequestHandler):

    def get(self):
        global populated

        ############################################################# BEGIN DATASTORE ####
        logging.info('hello from the datastore')
        logging.info('populated: ')
        logging.info(populated)

        if not populated:
            populated = True
            logging.info(populated)

            """
            marissa_mayer_person = Person(
                name='Marissa Mayer',
                bio='CEO and President, Yahoo')
            marissa_mayer_person.put()

            one_a_marissa_mayer = SimilarStyle(
                    img_src='/images/who_wore_what/marissa_mayer/Marissa_1_a.jpg', 
                    item_page='https://www.jcrew.com/womens_category/dresses/weartowork/PRDOVR~E4684/E4684.jsp?color_name=black', 
                    description='Insert description.',
                    brand='J. Crew',
                    price=228)
            one_a_key_marissa_mayer = one_a_marissa_mayer.put()

            one_b_marissa_mayer = SimilarStyle(
                    img_src='/images/who_wore_what/marissa_mayer/Marissa_1_b.jpg', 
                    item_page='http://www.zara.com/us/en/sale/woman/dresses/view-all/long-tube-dress-c732061p2922083.html', 
                    description='Insert description.',
                    brand='Zara',
                    price=22.99)
            one_b_key_marissa_mayer = one_b_marissa_mayer.put()

            look_one_marissa_mayer = Look(
                img_src='/images/who_wore_what/marissa_mayer/Marissa_1.jpg',
                description='Marissa wearing a knee-length navy dress and blue short cardigan.',
                date=datetime.date(2016, 1, 18),
                person=marissa_mayer_person,
                id=0)
            look_one_marissa_mayer.similar_style_keys.append(one_a_key_marissa_mayer)
            look_one_marissa_mayer.similar_style_keys.append(one_b_key_marissa_mayer)
            look_one_marissa_mayer.put()

            two_a_marissa_mayer = SimilarStyle(
                    img_src='/images/who_wore_what/marissa_mayer/Marissa_2_a.jpg', 
                    item_page='http://www.anntaylor.com/tropical-wool-sheath-dress/391849?skuId=20147327&defaultColor=6600&colorExplode=false&catid=cata000012', 
                    description='Insert description.',
                    brand='Ann Taylor',
                    price=169)
            two_a_key_marissa_mayer = two_a_marissa_mayer.put()

            two_b_marissa_mayer = SimilarStyle(
                    img_src='/images/who_wore_what/marissa_mayer/Marissa_2_b.jpg', 
                    item_page='http://www.anntaylor.com/wrap-flare-dress/392036?skuId=19992945&defaultColor=1246&colorExplode=false&catid=cata000012', 
                    description='Insert description.',
                    brand='Ann Taylor',
                    price=129)
            two_b_key_marissa_mayer = two_b_marissa_mayer.put()

            look_two_marissa_mayer = Look(
                img_src='/images/who_wore_what/marissa_mayer/Marissa_2.jpg',
                description='Marissa wearing a short-sleeve, black dress.',
                date=datetime.date(2016, 1, 18),
                person=marissa_mayer_person,
                id=1)
            look_two_marissa_mayer.similar_style_keys.append(two_a_key_marissa_mayer)
            look_two_marissa_mayer.similar_style_keys.append(two_b_key_marissa_mayer)
            look_two_marissa_mayer.put()

            three_a_marissa_mayer = SimilarStyle(
                    img_src='/images/who_wore_what/marissa_mayer/Marissa_3_a.jpg', 
                    item_page='http://www.anntaylor.com/long-sleeve-dress-shrug/391465?skuId=19924830&defaultColor=6600&colorExplode=false&catid=cata000011', 
                    description='Insert description.',
                    brand='Ann Taylor',
                    price=64.99)
            three_a_key_marissa_mayer = three_a_marissa_mayer.put()

            look_three_marissa_mayer = Look(
                img_src='/images/who_wore_what/marissa_mayer/Marissa_3.jpg',
                description='Marissa sporting a black short cardigan over a green dress.',
                date=datetime.date(2016, 1, 18),
                person=marissa_mayer_person,
                id=2)
            look_three_marissa_mayer.similar_style_keys.append(three_a_key_marissa_mayer)
            look_three_marissa_mayer.put()

            #---------------------

            indra_nooyi_person = Person(
                name='Indra Nooyi',
                bio='CEO and Chairman, PepsiCo')
            indra_nooyi_person.put()

            one_a_indra_nooyi = SimilarStyle(
                    img_src='/images/who_wore_what/indra_nooyi/Indra_1_a.jpg', 
                    item_page='https://www.jcrew.com/womens_category/outerwear_sm/wool/PRDOVR~C8552/C8552.jsp', 
                    description='Insert description.',
                    brand='J. Crew',
                    price=350)
            one_a_key_indra_nooyi = one_a_indra_nooyi.put()

            look_one_indra_nooyi = Look(
                img_src='/images/who_wore_what/indra_nooyi/Indra_1.jpg',
                description='Indra posing in a sky blue coat.',
                date=datetime.date(2016, 1, 18),
                person=indra_nooyi_person,
                id=3)
            look_one_indra_nooyi.similar_style_keys.append(one_a_key_indra_nooyi)
            look_one_indra_nooyi.put()

            two_a_indra_nooyi = SimilarStyle(
                    img_src='/images/who_wore_what/indra_nooyi/Indra_2_a.jpg', 
                    item_page='https://www.jcrew.com/womens_category/blazers/regent/PRDOVR~B0323/B0323.jsp?color_name=BOHEMIAN%20RED&styles=B0323-RD6013', 
                    description='Insert description.',
                    brand='J. Crew',
                    price=198)
            two_a_key_indra_nooyi = two_a_indra_nooyi.put()

            look_two_indra_nooyi = Look(
                img_src='/images/who_wore_what/indra_nooyi/Indra_2.jpg',
                description='Indra outside wearing a grapefruit-red jacket.',
                date=datetime.date(2016, 1, 18),
                person=indra_nooyi_person,
                id=4)
            look_two_indra_nooyi.similar_style_keys.append(two_a_key_indra_nooyi)
            look_two_indra_nooyi.put()

            #-----------------------------------------

            sheryl_sandberg_person = Person(
                name='Sheryl Sandberg',
                bio='COO, Facebook')
            sheryl_sandberg_person.put()

            one_a_sheryl_sandberg = SimilarStyle(
                    img_src='/images/who_wore_what/sheryl_sandberg/Sheryl_1_a.jpg', 
                    item_page='https://www.jcrew.com/womens_category/sweaters/cardigans/PRDOVR~E2078/E2078.jsp', 
                    description='Insert description.',
                    brand='J. Crew',
                    price=198)
            one_a_key_sheryl_sandberg = one_a_sheryl_sandberg.put()

            look_one_sheryl_sandberg = Look(
                img_src='/images/who_wore_what/sheryl_sandberg/Sheryl_1.jpg',
                description='Insert description.',
                date=datetime.date(2016, 1, 18),
                person=sheryl_sandberg_person,
                id=5)
            look_one_sheryl_sandberg.similar_style_keys.append(one_a_key_sheryl_sandberg)
            look_one_sheryl_sandberg.put()

            two_a_sheryl_sandberg = SimilarStyle(
                    img_src='/images/who_wore_what/sheryl_sandberg/Sheryl_2_a.jpg', 
                    item_page='http://www.anntaylor.com/all-season-stretch-one-button-jacket/379001?skuId=19195995&defaultColor=1878&colorExplode=false&catid=cata000013', 
                    description='Insert description.',
                    brand='Ann Taylor',
                    price=169)
            two_a_key_sheryl_sandberg = two_a_sheryl_sandberg.put()

            look_two_sheryl_sandberg = Look(
                img_src='/images/who_wore_what/sheryl_sandberg/Sheryl_2.jpg',
                description='Insert description.',
                date=datetime.date(2016, 1, 18),
                person=sheryl_sandberg_person,
                id=6)
            look_two_sheryl_sandberg.similar_style_keys.append(two_a_key_sheryl_sandberg)
            look_two_sheryl_sandberg.put()
            """

            with open('www_database.csv', 'rb') as csvfile:
                reader = csv.reader(csvfile)
                first = True
                keys = []
                prefix = '/images/who_wore_what/'
                for row in reader:
                    logging.info('row: ')
                    logging.info(row)
                    if (first):
                        keys = row
                        first = False

                    elif any(row):
                        # Make dictionary first
                        d = {}
                        for r in range(len(row)):
                            if keys[r] == 'date':
                                date_split = row[r].split('/')
                                logging.info(date_split)
                                d['month'] = int(date_split[0])
                                d['day'] = int(date_split[1])
                                d['year'] = int(date_split[2])
                            elif keys[r] == 'imgs':
                                d[keys[r]] = row[r].split(', ')

                                for i in range(len(d[keys[r]])):
                                    # Need to add prefix to all pictures
                                    d[keys[r]][i] = prefix + d[keys[r]][i]
                            elif keys[r] == 'links':
                                d[keys[r]] = row[r].split(', ')
                            else:
                                d[keys[r]] = row[r]

                        posting = Posting(
                            id=int(d['id']),
                            date=datetime.date(d['year'], d['month'], d['day']),
                            title=d['title'],
                            imgs=d['imgs'],
                            links=d['links'],
                            description=d['description'],
                            dress_code = d['dress_code']
                        )
                        posting.put()

                    else:
                        logging.info('row caught: ')
                        logging.info(row)




            """
            one_a_marissa_mayer = SimilarStyle(
                    img_src='/images/who_wore_what/marissa_mayer/Marissa_1_a.jpg', 
                    item_page='https://www.jcrew.com/womens_category/dresses/weartowork/PRDOVR~E4684/E4684.jsp?color_name=black', 
                    description='Insert description.',
                    brand='J. Crew',
                    price=228)
            one_a_key_marissa_mayer = one_a_marissa_mayer.put()

            one_b_marissa_mayer = SimilarStyle(
                    img_src='/images/who_wore_what/marissa_mayer/Marissa_1_b.jpg', 
                    item_page='http://www.zara.com/us/en/sale/woman/dresses/view-all/long-tube-dress-c732061p2922083.html', 
                    description='Insert description.',
                    brand='Zara',
                    price=22.99)
            one_b_key_marissa_mayer = one_b_marissa_mayer.put()

            posting_one_marissa_mayer = Posting(
                img_src='/images/who_wore_what/marissa_mayer/Marissa_1.jpg',
                description='Marissa wearing a knee-length navy dress and blue short cardigan.',
                date=datetime.date(2016, 1, 18))
            posting_one_marissa_mayer.similar_style_keys.append(one_a_key_marissa_mayer)
            posting_one_marissa_mayer.similar_style_keys.append(one_b_key_marissa_mayer)

            two_a_marissa_mayer = SimilarStyle(
                    img_src='/images/who_wore_what/marissa_mayer/Marissa_2_a.jpg', 
                    item_page='http://www.anntaylor.com/tropical-wool-sheath-dress/391849?skuId=20147327&defaultColor=6600&colorExplode=false&catid=cata000012', 
                    description='Insert description.',
                    brand='Ann Taylor',
                    price=169)
            two_a_key_marissa_mayer = two_a_marissa_mayer.put()

            two_b_marissa_mayer = SimilarStyle(
                    img_src='/images/who_wore_what/marissa_mayer/Marissa_2_b.jpg', 
                    item_page='http://www.anntaylor.com/wrap-flare-dress/392036?skuId=19992945&defaultColor=1246&colorExplode=false&catid=cata000012', 
                    description='Insert description.',
                    brand='Ann Taylor',
                    price=129)
            two_b_key_marissa_mayer = two_b_marissa_mayer.put()

            posting_two_marissa_mayer = Posting(
                img_src='/images/who_wore_what/marissa_mayer/Marissa_2.jpg',
                description='Marissa wearing a short-sleeve, black dress.',
                date=datetime.date(2016, 1, 18))
            posting_two_marissa_mayer.similar_style_keys.append(two_a_key_marissa_mayer)
            posting_two_marissa_mayer.similar_style_keys.append(two_b_key_marissa_mayer)

            three_a_marissa_mayer = SimilarStyle(
                    img_src='/images/who_wore_what/marissa_mayer/Marissa_3_a.jpg', 
                    item_page='http://www.anntaylor.com/long-sleeve-dress-shrug/391465?skuId=19924830&defaultColor=6600&colorExplode=false&catid=cata000011', 
                    description='Insert description.',
                    brand='Ann Taylor',
                    price=64.99)
            three_a_key_marissa_mayer = three_a_marissa_mayer.put()

            posting_three_marissa_mayer = Posting(
                img_src='/images/who_wore_what/marissa_mayer/Marissa_3.jpg',
                description='Marissa sporting a black short cardigan over a green dress.',
                date=datetime.date(2016, 1, 18))
            posting_three_marissa_mayer.similar_style_keys.append(three_a_key_marissa_mayer)

            marissa_mayer_person = Person(
                name='Marissa Mayer',
                bio='CEO and President, Yahoo',
                postings=[posting_one_marissa_mayer, posting_two_marissa_mayer, posting_three_marissa_mayer])
            marissa_mayer_person.put()

            #---------------------

            one_a_indra_nooyi = SimilarStyle(
                    img_src='/images/who_wore_what/indra_nooyi/Indra_1_a.jpg', 
                    item_page='https://www.jcrew.com/womens_category/outerwear_sm/wool/PRDOVR~C8552/C8552.jsp', 
                    description='Insert description.',
                    brand='J. Crew',
                    price=350)
            one_a_key_indra_nooyi = one_a_indra_nooyi.put()

            posting_one_indra_nooyi = Posting(
                img_src='/images/who_wore_what/indra_nooyi/Indra_1.jpg',
                description='Indra posing in a sky blue coat.',
                date=datetime.date(2016, 1, 18))
            posting_one_indra_nooyi.similar_style_keys.append(one_a_key_indra_nooyi)

            two_a_indra_nooyi = SimilarStyle(
                    img_src='/images/who_wore_what/indra_nooyi/Indra_2_a.jpg', 
                    item_page='https://www.jcrew.com/womens_category/blazers/regent/PRDOVR~B0323/B0323.jsp?color_name=BOHEMIAN%20RED&styles=B0323-RD6013', 
                    description='Insert description.',
                    brand='J. Crew',
                    price=198)
            two_a_key_indra_nooyi = two_a_indra_nooyi.put()

            posting_two_indra_nooyi = Posting(
                img_src='/images/who_wore_what/indra_nooyi/Indra_2.jpg',
                description='Indra outside wearing a grapefruit-red jacket.',
                date=datetime.date(2016, 1, 18))
            posting_two_indra_nooyi.similar_style_keys.append(two_a_key_indra_nooyi)

            indra_nooyi_person = Person(
                name='Indra Nooyi',
                bio='CEO and Chairman, PepsiCo',
                postings=[posting_one_indra_nooyi, posting_two_indra_nooyi])
            indra_nooyi_person.put()

            #-----------------------------------------

            one_a_sheryl_sandberg = SimilarStyle(
                    img_src='/images/who_wore_what/sheryl_sandberg/Sheryl_1_a.jpg', 
                    item_page='https://www.jcrew.com/womens_category/sweaters/cardigans/PRDOVR~E2078/E2078.jsp', 
                    description='Insert description.',
                    brand='J. Crew',
                    price=198)
            one_a_key_sheryl_sandberg = one_a_sheryl_sandberg.put()

            posting_one_sheryl_sandberg = Posting(
                img_src='/images/who_wore_what/sheryl_sandberg/Sheryl_1.jpg',
                description='Insert description.',
                date=datetime.date(2016, 1, 18))
            posting_one_sheryl_sandberg.similar_style_keys.append(one_a_key_sheryl_sandberg)

            two_a_sheryl_sandberg = SimilarStyle(
                    img_src='/images/who_wore_what/sheryl_sandberg/Sheryl_2_a.jpg', 
                    item_page='http://www.anntaylor.com/all-season-stretch-one-button-jacket/379001?skuId=19195995&defaultColor=1878&colorExplode=false&catid=cata000013', 
                    description='Insert description.',
                    brand='Ann Taylor',
                    price=169)
            two_a_key_sheryl_sandberg = two_a_sheryl_sandberg.put()

            posting_two_sheryl_sandberg = Posting(
                img_src='/images/who_wore_what/sheryl_sandberg/Sheryl_2.jpg',
                description='Insert description.',
                date=datetime.date(2016, 1, 18))
            posting_two_sheryl_sandberg.similar_style_keys.append(two_a_key_sheryl_sandberg)

            sheryl_sandberg_person = Person(
                name='Sheryl Sandberg',
                bio='COO, Facebook',
                postings=[posting_one_sheryl_sandberg, posting_two_sheryl_sandberg])
            sheryl_sandberg_person.put()
            """

            #================================================================ COVERFLOW === 

            marissa_mayer_coverflow = Coverflow(
                name='Marissa Mayer',
                img_src='/images/who_wore_what/marissa_mayer/Marissa.png',
                order_id=0)
            marissa_mayer_coverflow.put()

            indra_nooyi_coverflow = Coverflow(
                name='Indra Nooyi',
                img_src='/images/who_wore_what/indra_nooyi/Indra.png',
                order_id=1)
            indra_nooyi_coverflow.put()

            sheryl_sandberg_coverflow = Coverflow(
                name='Sheryl Sandberg',
                img_src='/images/who_wore_what/sheryl_sandberg/Sheryl.png',
                order_id=2)
            sheryl_sandberg_coverflow.put()

            #================================================================== DROPDOWNS === 
            general_styles = DropdownSection(
                    heading='style', 
                    items=['smart casual', 'biz casual', 'biz formal'], 
                    dropdown='style guides',
                    order_id=0)
            general_styles.put()

            industry_styles = DropdownSection(
                    heading='industry', 
                    items=['consulting', 'industry 2'], 
                    dropdown='style guides',
                    order_id=1)
            industry_styles.put()

            shop_filters = DropdownSection(
                    items=['top', 'bottom', 'dress', 'suit', 'outerwear'], 
                    dropdown='shop',
                    order_id=1)
            shop_filters.put()

            #=============================================================== LOOKOCCASION === 
            """
            smartcasual_one = LookOccasion(
                    dress_code='smart casual',
                    look_img_src='/images/smartcasual.png',
                    look_descriptions=['White and blue stripe fit and flare dress'],
                    occasion_img_src='/images/smartcasual.png',
                    occasion_descriptions=['This dress is perfect for casual Fridays, a summer happy hour, or an outdoor work BBQ!'],
                    order_id=0,
                    shop_page='TODO')
            smartcasual_one.put()

            smartcasual_two = LookOccasion(
                    dress_code='smart casual',
                    look_img_src='/images/casual_friday.jpg',
                    look_descriptions=['Dark wash jeans with striped tank top and black cotton blazer'],
                    occasion_img_src='/images/casual_friday.jpg',
                    occasion_descriptions=['Go from casual Friday in the office to after work drinks.  This outfit does it all!'],
                    order_id=1,
                    shop_page='TODO')
            smartcasual_two.put()

            businesscasual_one = LookOccasion(
                    dress_code='biz casual',
                    look_img_src='/images/businesscasual.png',
                    look_descriptions=['Tan slacks with silk white top and a decorative neck tie'],
                    occasion_img_src='/images/businesscasual.png',
                    occasion_descriptions=['Wear this outfit for everyday meetings or traveling to and from client site.'],
                    order_id=0,
                    shop_page='TODO')
            businesscasual_one.put()

            businesscasual_two = LookOccasion(
                    dress_code='biz casual',
                    look_img_src='/images/biz_casual_skirt.jpg',
                    look_descriptions=['Beige pencil skirt with navy long sleeve button down shirt'],
                    occasion_img_src='/images/biz_casual_skirt.jpg',
                    occasion_descriptions=['Great outfit for the office, presenting to the team, and going out for lunch meetings.'],
                    order_id=1,
                    shop_page='TODO')
            businesscasual_two.put()

            businessformal_one = LookOccasion(
                    dress_code='biz formal',
                    look_img_src='/images/businessformal.png',
                    look_descriptions=['Black suit jacket with matching pant and a white silk top'],
                    occasion_img_src='/images/businessformal.png',
                    occasion_descriptions=['Wear this suit for big presentations, executive meetings, or any time you need to make a great impression!'],
                    order_id=0,
                    shop_page='TODO')
            businessformal_one.put()

            businessformal_two= LookOccasion(
                    dress_code='biz formal',
                    look_img_src='/images/biz_formal_skirtsuit.jpg',
                    look_descriptions=['Grey suit jacket with matching skirt and a navy top'],
                    occasion_img_src='/images/biz_formal_skirtsuit.jpg',
                    occasion_descriptions=['This skirt suit is great for big meetings, first day on a important job, or sales presentations.'],
                    order_id=1,
                    shop_page='TODO')
            businessformal_two.put()
            """

            with open('style_guides_database.csv', 'rb') as csvfile:
                reader = csv.reader(csvfile)
                first = True
                keys = []
                prefix = '/images/style_guides/'
                for row in reader:
                    if (first):
                        keys = row
                        first = False
                    else:
                        # Make dictionary first
                        d = {}
                        for r in range(len(row)):
                            d[keys[r]] = row[r]

                        info = StyleInfo(
                            name = d['name'],
                            look_1_img = prefix + d['look_1_img'],
                            look_1_name = d['look_1_name'],
                            look_1_brand = d['look_1_brand'],
                            look_1_tip = d['look_1_tip'],
                            look_2_img = prefix + d['look_2_img'],
                            look_2_name = d['look_2_name'],
                            look_2_brand = d['look_2_brand'],
                            look_2_tip = d['look_2_tip'],
                            look_3_img = prefix + d['look_3_img'],
                            look_3_name = d['look_3_name'],
                            look_3_brand = d['look_3_brand'],
                            look_3_tip = d['look_3_tip'],
                            occasion_1_img = prefix + d['occasion_1_img'],
                            occasion_1_text = d['occasion_1_text'],
                            occasion_2_img = prefix + d['occasion_2_img'],
                            occasion_2_text = d['occasion_2_text'],
                            occasion_3_img = prefix + d['occasion_3_img'],
                            occasion_3_text = d['occasion_3_text'],
                            tip = d['tip'])
                        info.put()

            #======================================================= INDUSTRYSTYLE === 

            consulting_sc = IndustryStyle(
                    industry='consulting',
                    dress_code='smart casual',
                    img_src='/images/smartcasual.png',
                    relevance='low',
                    activities=['Happy hour', 'Social hangouts'],
                    attire=['Jeans', 'Blazer'],
                    shop_page='TODO')
            consulting_sc.put()

            consulting_bc = IndustryStyle(
                    industry='consulting',
                    dress_code='biz casual',
                    img_src='/images/businesscasual.png',
                    relevance='medium',
                    activities=['Casual fridays in office'],
                    attire=['Dress pant', 'Shirt'],
                    shop_page='TODO')
            consulting_bc.put()

            consulting_bf = IndustryStyle(
                    industry='consulting',
                    dress_code='biz formal',
                    img_src='/images/businessformal.png',
                    relevance='high',
                    activities=['Client site activities'],
                    attire=['Dark suit', 'Top', 'etc.'],
                    shop_page='TODO')
            consulting_bf.put()


            #================================================================== ITEM === 

            with open('sku_database_v1.csv', 'rb') as csvfile:
                reader = csv.reader(csvfile)
                first = True
                keys = []
                for row in reader:
                    if (first):
                        keys = row
                        first = False
                    else:
                        # Make dictionary first
                        d = {}
                        for r in range(len(row)):
                            # Brands are case sensitive. but others aren't.
                            if keys[r] != 'brand' and keys[r] != 'image_1' and keys[r] != 'image_2' and keys[r] != 'url':
                                row[r] = row[r].lower()

                            # List of properties
                            if keys[r] == 'occasion' or keys[r] == 'dress_code' or keys[r] == 'apparel':
                                d[keys[r]] = row[r].split(', ')
                            else:
                                d[keys[r]] = row[r]

                        logging.info(row)
                        # Reading in empty rows now? Temporary patch.
                        if d['sku_id'] != '' :
                            item = Item(
                                sku_id=int(d['sku_id']),
                                name=d['name'],
                                brand=d['brand'],
                                apparels=d['apparel'],
                                price=float(d['price']),
                                industries=['consulting'],
                                dress_codes=d['dress_code'],
                                occasions=d['occasion'],
                                description='Insert description.',
                                img_1_src='/images/items/' + d['image_1'],
                                img_2_src='/images/items/' + d['image_2'],
                                external_src=d['url'],
                                smaller_imgs=['/images/charmanderllama.png', '/images/charmeleonllama.png', '/images/charizardllama.png'],
                                date=datetime.date(2016, 1, 10))
                            item.put()
            ############################################################### END DATASTORE ####


class HomeHandler(BaseHandler):
    def get(self):
        logging.info('in main handler logging')
        self.render_template('templates/home.html')
        #self.render_template('templates/leka/index7.html')

class ShopHandler(BaseHandler):
    def get(self):
        logging.info('arguments:')
        logging.info(self.request.arguments())

        args = self.request.arguments()
        argDict = {}

        for key in args:
            argDict[key] = self.request.get_all(key)

        logging.info('argDict')
        logging.info(argDict)

        if 'sort' in argDict:
            selected_shop_sort = argDict['sort'][0]
        else:
            selected_shop_sort = SHOP_SORT_DEFAULT

        if 'items' in argDict:
            selected_items_per_page = argDict['items'][0]
        else:
            selected_items_per_page = ITEMS_PER_PAGE_DEFAULT

        if 'page' in argDict:
            selected_page = argDict['page'][0]
        else:
            selected_page = PAGE_DEFAULT


        # Check shop.js filters.
        filters = [
            {
                'property_name': 'occasions',
                'display_name': 'occasion',
                'selections': OCCASIONS 
            },
            {
                'property_name': 'apparels',
                'display_name': 'apparel',
                'selections': APPARELS
            },
            {
                'property_name': 'brand',
                'display_name': 'brand',
                'selections': BRANDS 
            },
            {
                'property_name': 'dress_codes',
                'display_name': 'dress code',
                'selections': DRESS_CODES 
            },
            {
                'property_name': 'industries',
                'display_name': 'industry',
                'selections': INDUSTRIES 
            }
        ]

        # create query filters.
        query = Item.query()
        query = self.applySort(query, argDict)
        query = self.applyCheckboxes(query, filters, argDict)
        

        logging.info(query)


        all_results = query.fetch()
        num_results = len(all_results)

        showing_from = 1
        showing_to = num_results

        # calculating offset for results.
        if selected_items_per_page == 'all':
            selected_page = 1
            num_pages = [1]
            results = all_results
        elif num_results < int(selected_items_per_page):
            # Not enough results to offset or have multiple pages.
            selected_page = 1
            num_pages = [1]
            results = all_results
        else:
            selected_items_per_page = int(selected_items_per_page)
            start = (int(selected_page) - 1) * selected_items_per_page
            stop = start + selected_items_per_page
            offset_results = all_results[start:stop]
            results = offset_results

            # calculating pages.
            if num_results % selected_items_per_page == 0:
                pages = num_results / selected_items_per_page
            else:
                pages = num_results / selected_items_per_page + 1

            num_pages = [i for i in range(1, pages + 1)]

            showing_from = start + 1
            showing_to = stop
    
        logging.info('================= RESULTS =====================')
        for r in results:
            logging.info(r)
            logging.info('----------------------')

        logging.info('======================================')

        # Manually filter out by price because gae required inequality filters 
        # to have a sort on the query, and that would require sacrificing sorts 
        # and maybe need more indexes.
        if 'price-min' in argDict and 'price-max' in argDict:
            results = self.filterByPrice(results, int(argDict['price-min'][0]), int(argDict['price-max'][0]))

        template_vars = {
                'filters': filters,
                'shop_sorts': SHOP_SORTS,
                'selected_shop_sort': selected_shop_sort,
                'default_shop_sort': SHOP_SORT_DEFAULT,
                'items_per_page': ITEMS_PER_PAGE,
                'selected_items_per_page': selected_items_per_page,
                'default_items_per_page': ITEMS_PER_PAGE_DEFAULT,
                'selected_page': selected_page,
                'default_page': PAGE_DEFAULT,
                'num_pages': num_pages,
                'results': results,
                'showing_from': showing_from,
                'showing_to': showing_to,
                'showing_total': num_results
        }

        self.render_template('templates/shop.html', template_vars)
        #self.render_template('templates/leka/shop-left-sidebar.html', template_vars)

    def applySort(self, query, argDict):
        if 'sort' in argDict:
            sortType = argDict['sort'][0]

            if sortType ==  'name [a - z]':
                query = query.order(Item.name)
            elif sortType == 'name [z - a]':
                query = query.order(-Item.name)
            elif sortType == 'price [low - high]':
                query = query.order(Item.price)
            elif sortType == 'price [high - low]':
                query = query.order(-Item.price)
            elif sortType == 'date [new - old]':
                query = query.order(-Item.date)
            elif sortType == 'date [old - new]':
                query = query.order(Item.date)
            else:
                logging.info('invalid sort: ')
                logging.info(sortType)

        else:
            # Default sort.
            query = query.order(Item.name)

        return query

    def applyCheckboxes(self, query, filters, argDict):
        # TODO: verify this works for repeated properties as well? (e.g. colors, industries, etc.)
        for f in filters:
            if f['property_name'] in argDict:
                fValues = argDict[f['property_name']]

                query = query.filter(getattr(Item, f['property_name']).IN(fValues))

                """
                for i in fValues:
                    query = query.filter(getattr(Item, f['name']) == i)
                """

        return query

    def filterByPrice(self, results, priceMin, priceMax):
        filtered_results = []

        for r in results:
            if r.price >= priceMin and r.price <= priceMax:
                filtered_results.append(r)

        return filtered_results

class WhoWoreWhatHandler(BaseHandler):
    def get(self):
        """
        coverflow_data = Coverflow.query().order(Coverflow.order_id).fetch()
        logging.info(coverflow_data)

        template_vars = {
                'coverflow_data': coverflow_data
        }

        logging.info('in who wore what handler logging')
        self.render_template('templates/who_wore_what.html', template_vars)
        """

        #look_data = Look.query().order(Look.id).fetch()
        #logging.info(look_data)

        posting_data = Posting.query().order(-Posting.date).fetch()
        logging.info(posting_data)

        template_vars = {
                'posting_data': posting_data 
        }

        logging.info('in who wore what handler logging')
        self.render_template('templates/who_wore_what.html', template_vars)

class WhoWoreWhatLookHandler(BaseHandler):
    def get(self):
        try: 
            id_arg= self.request.get('id') 

            query = Look.query(getattr(Look, 'id') == int(id_arg))
            result = query.fetch()[0]
            logging.info('result')
            logging.info(result)

            similar_styles = []
            for key in result.similar_style_keys:
                similar_styles.append(key.get())

            template_vars = {
                    'look': result, 
                    'similar_styles': similar_styles
            }

            # Check if it's a valid person.
            if self.request.get('id') == '':
                print "didn't get a valid look id value in get request."

            else:
                # Display normal style guides page.
                logging.info('in look handler logging')
                self.render_template('templates/look.html', template_vars)

        except(TypeError, ValueError):
            template_vars['message'] = "Invalid look."
            self.render_template('templates/danger_message.html', template_vars)

class WhoWoreWhatPersonHandler(BaseHandler):
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
                    'posting_to_similar_styles_dict': posting_to_similar_style_dict
            }

            # Check if it's a valid person.
            if self.request.get('person') == '':
                print "didn't get a valid person value in get request."

            else:
                # Display normal style guides page.
                logging.info('in person handler logging')
                self.render_template('templates/person.html', template_vars)

        except(TypeError, ValueError):
            template_vars['message'] = "Invalid person."
            self.render_template('templates/danger_message.html', template_vars)

class StyleGuidesIndustryHandler(BaseHandler):
    def get(self):
        try: 
            industry_arg = self.request.get('industry')

            industry_results = IndustryStyle.query(getattr(IndustryStyle, 'industry') == industry_arg).fetch()

            logging.info(industry_results)

            industry_dict = {}

            for r in industry_results:
                industry_dict[r.relevance] = r

            logging.info(industry_dict)

            industry_data = [
                    industry_dict['high'], 
                    industry_dict['medium'], 
                    industry_dict['low']
            ]

            logging.info(industry_data)

            template_vars = {
                    'industry_names': INDUSTRIES, 
                    'industry_data': industry_data, 
                    'industry': industry_arg
            }

            # Check if it's a valid industry.
            if self.request.get('industry') == '':
                print "didn't get a valid industry value in get request."

            else:
                # Display normal style guides page.
                logging.info('in industry handler logging')
                self.render_template('templates/industry.html', template_vars)

        except(TypeError, ValueError):
            template_vars['message'] = "Invalid industry."
            self.render_template('templates/danger_message.html', template_vars)

class StyleGuidesStyleHandler(BaseHandler):
    def get(self):
        #try: 
        dress_code_arg = self.request.get('dress_code')

        #dress_code_data = LookOccasion.query(getattr(LookOccasion, 'dress_code') == dress_code_arg).order(LookOccasion.order_id).fetch()
        dress_code_data = StyleInfo.query(getattr(StyleInfo, 'name') == dress_code_arg).get()
        data = dress_code_data
        logging.info(data)

        template_vars = {
                'industry_names': INDUSTRIES, 
                'dress_code_data': data, 
                'dress_code': dress_code_arg
        }

        # Check if it's a valid industry.
        if dress_code_arg == '':
            print "didn't get a valid style value in get request."

        else:
            # Display normal industry page.
            logging.info('in style handler logging')
            self.render_template('templates/style.html', template_vars)

        """
        except(TypeError, ValueError):
            logging.info(TypeError)
            logging.info(ValueError)
            template_vars['message'] = "Invalid style."
            self.render_template('templates/danger_message.html', template_vars)
        """


class StyleGuidesHandler(BaseHandler):
    def get(self):

        dress_code_data = [
                {'name': 'biz formal', 'img_src': '/images/businessformal.jpg'},
                {'name': 'biz casual', 'img_src': '/images/businesscasual.jpg'},
                {'name': 'smart casual', 'img_src': '/images/smartcasual.jpg'},
                {'name': 'tech casual', 'img_src': '/images/techcasual.jpg'}]


        template_vars = {
                'industry_names': INDUSTRIES, 
                'dress_code_data': dress_code_data
        }

        logging.info('in style guides handler logging')
        self.render_template('templates/style_guides.html', template_vars)

class SignUpHandler(BaseHandler):
    def get(self):
            self.render_template('templates/sign_up.html')

class BlogHandler(BaseHandler):
    def get(self):
            self.render_template('templates/blog.html')

class PageNotFoundHandler(BaseHandler):
    def get(self):
            template_vars = {
                'message': 'Error 404. Page not found.'
            }
            self.render_template('templates/danger_message.html', template_vars)


app = webapp2.WSGIApplication(routes=[
    ('/shop', ShopHandler),
    ('/whoworewhat/look', PageNotFoundHandler), #WhoWoreWhatLookHandler),
    ('/whoworewhat/person', PageNotFoundHandler), #WhoWoreWhatPersonHandler),
    ('/whoworewhat', PageNotFoundHandler), #WhoWoreWhatHandler),
    ('/styleguides/industry', StyleGuidesIndustryHandler),
    ('/styleguides/style', StyleGuidesStyleHandler),
    ('/styleguides', StyleGuidesHandler),
    ('/populatedatastore', DatastoreHandler),
    ('/signup', SignUpHandler),
    ('/blog', PageNotFoundHandler),#BlogHandler),
    ('/', HomeHandler),
    ('/home', HomeHandler),
    ('/.*', PageNotFoundHandler)
], debug=True, config={
    'webapp2_extras.auth': {
        'user_model': 'models.User',
        'user_attributes': ['name']
    },
    'webapp2_extras.sessions': {
        'secret_key': 'YOUR_SECRET_KEY'
    }
})
