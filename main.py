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

ARTICLES = [
    'tops', 
    'bottoms', 
    'dresses', 
    'suits', 
    'outerwear'
]

BRANDS = [
    'JCrew', 
    'Ann Taylor',
    'Zara'
]

SIZES = [
    'xs', 
    's', 
    'm', 
    'l', 
    'xl', 
    'xxl'
]

STYLES = [
    'smart casual', 
    'business casual', 
    'business formal'
]

# Alpha sorted.
COLORS = [
    'black', 
    'blue', 
    'navy',
    'brown', 
    'gray', 
    'green', 
    'orange', 
    'pink', 
    'purple',
    'red', 
    'white', 
    'yellow', 
]

# Alpha sorted.
INDUSTRIES = [
    'consulting', 
    'industry 2'
]

SHOP_SORTS = [
    'name [a - z]', 
    'name [z - a]', 
    'price [low - high]', 
    'price [high - low]', 
    'date [new - old]', 
    'date [old - new]'
]

SHOP_SORT_DEFAULT = SHOP_SORTS[0]

ITEMS_PER_PAGE = [
        15, 
        30, 
        90, 
        'all'
]

ITEMS_PER_PAGE_DEFAULT = ITEMS_PER_PAGE[0]

PAGE_DEFAULT = 1

RELEVANCE = [
    'high',
    'medium',
    'low'
]

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

class Posting(ndb.Model):
    img_src = ndb.TextProperty(required=True)
    description = ndb.TextProperty(required=True)
    date = ndb.DateProperty(required=True)
    similar_style_keys = ndb.KeyProperty(kind='SimilarStyle', repeated=True)

class Person(ndb.Model):
    # Name must match coverflow name.
    name = ndb.StringProperty(required=True)
    bio = ndb.TextProperty(required=True)
    postings = ndb.LocalStructuredProperty(Posting, repeated=True)

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

class LookOccasion(ndb.Model):
    style = ndb.StringProperty(required=True, choices=STYLES)
    look_img_src = ndb.TextProperty(required=True)
    look_descriptions = ndb.TextProperty(repeated=True)
    occasion_img_src = ndb.TextProperty(required=True)
    occasion_descriptions = ndb.TextProperty(repeated=True)
    order_id = ndb.IntegerProperty(required=False, default=0)
    shop_page = ndb.TextProperty(required=True)

class IndustryStyle(ndb.Model):
    industry = ndb.StringProperty(required=True, choices=INDUSTRIES)
    style = ndb.StringProperty(required=True, choices=STYLES)
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
    article = ndb.StringProperty(required=True, choices=ARTICLES)
    price = ndb.FloatProperty(required=True)
    colors = ndb.StringProperty(repeated=True, choices=COLORS)
    industries = ndb.StringProperty(repeated=True, choices=INDUSTRIES)
    styles = ndb.StringProperty(repeated=True, choices=STYLES)
    sizes = ndb.StringProperty(repeated=True, choices=SIZES)

    # Description (product info) on item page.
    description = ndb.TextProperty(required=False, default='Description currently unavailable.')

    # Main image on shopping grid page.
    img_src = ndb.TextProperty(required=True)

    # Link to outside website.
    external_src = ndb.TextProperty(required=True)

    # Smaller images shown on item page of different perspectives.
    smaller_imgs = ndb.TextProperty(repeated=True)

    # Date added to database
    date = ndb.DateProperty(required=True)

class DatastoreHandler(webapp2.RequestHandler):
    def get(self):
        ############################################################# BEGIN DATASTORE ####
        logging.info('hello from datastore')

        
        #===================================================================== PERSON === 
        """
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
        """

        one_a_marissa_mayer = SimilarStyle(
                img_src='/images/who_wore_what/marissa_mayer/Marissa_1_a.jpg', 
                item_page='https://www.jcrew.com/womens_category/dresses/weartowork/PRDOVR~E4684/E4684.jsp?color_name=black', 
                description='Insert description.',
                brand='JCrew',
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
            description='Insert description.',
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
            description='Insert description.',
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
            description='Insert description.',
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
                brand='JCrew',
                price=350)
        one_a_key_indra_nooyi = one_a_indra_nooyi.put()

        posting_one_indra_nooyi = Posting(
            img_src='/images/who_wore_what/indra_nooyi/Indra_1.jpg',
            description='Insert description.',
            date=datetime.date(2016, 1, 18))
        posting_one_indra_nooyi.similar_style_keys.append(one_a_key_indra_nooyi)

        two_a_indra_nooyi = SimilarStyle(
                img_src='/images/who_wore_what/indra_nooyi/Indra_2_a.jpg', 
                item_page='https://www.jcrew.com/womens_category/blazers/regent/PRDOVR~B0323/B0323.jsp?color_name=BOHEMIAN%20RED&styles=B0323-RD6013', 
                description='Insert description.',
                brand='JCrew',
                price=198)
        two_a_key_indra_nooyi = two_a_indra_nooyi.put()

        posting_two_indra_nooyi = Posting(
            img_src='/images/who_wore_what/indra_nooyi/Indra_2.jpg',
            description='Insert description.',
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
                brand='JCrew',
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

        #================================================================ COVERFLOW === 
        """

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
        """

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
                items=['smart casual', 'business casual', 'business formal'], 
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
                items=['tops', 'bottoms', 'dresses', 'suits', 'outerwear'], 
                dropdown='shop',
                order_id=1)
        shop_filters.put()

        #=============================================================== LOOKOCCASION === 
        
        smartcasual_one = LookOccasion(
                style='smart casual',
                look_img_src='/images/smartcasual.png',
                look_descriptions=['White and blue stripe fit and flare dress'],
                occasion_img_src='/images/smartcasual.png',
                occasion_descriptions=['This dress is perfect for casual Fridays, a summer happy hour, or an outdoor work BBQ!'],
                order_id=0,
                shop_page='TODO')
        smartcasual_one.put()

        smartcasual_two = LookOccasion(
                style='smart casual',
                look_img_src='/images/Casual Friday.jpg',
                look_descriptions=['Dark wash jeans with striped tank top and black cotton blazer'],
                occasion_img_src='/images/Casual Friday.jpg',
                occasion_descriptions=['Go from casual Friday in the office to after work drinks.  This outfit does it all!'],
                order_id=1,
                shop_page='TODO')
        smartcasual_two.put()

        businesscasual_one = LookOccasion(
                style='business casual',
                look_img_src='/images/businesscasual.png',
                look_descriptions=['Tan slacks with silk white top and a decorative neck tie'],
                occasion_img_src='/images/businesscasual.png',
                occasion_descriptions=['Wear this outfit for everyday meetings or traveling to and from client site.'],
                order_id=0,
                shop_page='TODO')
        businesscasual_one.put()

        businesscasual_two = LookOccasion(
                style='business casual',
                look_img_src='/images/Biz Casual skirt.jpg',
                look_descriptions=['Beige pencil skirt with navy long sleeve button down shirt'],
                occasion_img_src='/images/Biz Casual skirt.jpg',
                occasion_descriptions=['Great outfit for the office, presenting to the team, and going out for lunch meetings.'],
                order_id=1,
                shop_page='TODO')
        businesscasual_two.put()

        businessformal_one = LookOccasion(
                style='business formal',
                look_img_src='/images/businessformal.png',
                look_descriptions=['Black suit jacket with matching pant and a white silk top'],
                occasion_img_src='/images/businessformal.png',
                occasion_descriptions=['Wear this suit for big presentations, executive meetings, or any time you need to make a great impression!'],
                order_id=0,
                shop_page='TODO')
        businessformal_one.put()

        businessformal_two= LookOccasion(
                style='business formal',
                look_img_src='/images/Biz formal skirtsuit.jpg',
                look_descriptions=['Grey suit jacket with matching skirt and a navy top'],
                occasion_img_src='/images/Biz formal skirtsuit.jpg',
                occasion_descriptions=['This skirt suit is great for big meetings, first day on a important job, or sales presentations.],
                order_id=1,
                shop_page='TODO')
        businessformal_two.put()

        #======================================================= INDUSTRYSTYLE === 

        consulting_sc = IndustryStyle(
                industry='consulting',
                style='smart casual',
                img_src='/images/smartcasual.png',
                relevance='low',
                activities=['Happy hour', 'Social hangouts'],
                attire=['Jeans', 'Blazer'],
                shop_page='TODO')
        consulting_sc.put()

        consulting_bc = IndustryStyle(
                industry='consulting',
                style='business casual',
                img_src='/images/businesscasual.png',
                relevance='medium',
                activities=['Casual fridays in office'],
                attire=['Dress pant', 'Shirt'],
                shop_page='TODO')
        consulting_bc.put()

        consulting_bf = IndustryStyle(
                industry='consulting',
                style='business formal',
                img_src='/images/businessformal.png',
                relevance='high',
                activities=['Client site activities'],
                attire=['Dark suit', 'Top', 'etc.'],
                shop_page='TODO')
        consulting_bf.put()

        industry_sc = IndustryStyle(
                industry='industry 2',
                style='smart casual',
                img_src='/images/smartcasual.png',
                relevance='high',
                activities=['Happy hour', 'Social hangouts'],
                attire=['Jeans', 'Blazer'],
                shop_page='TODO')
        industry_sc.put()

        industry_bc = IndustryStyle(
                industry='industry 2',
                style='business casual',
                img_src='/images/businesscasual.png',
                relevance='low',
                activities=['Casual fridays in office'],
                attire=['Dress pant', 'Shirt'],
                shop_page='TODO')
        industry_bc.put()

        industry_bf = IndustryStyle(
                industry='industry 2',
                style='business formal',
                img_src='/images/businessformal.png',
                relevance='medium',
                activities=['Client site activities'],
                attire=['Dark suit', 'Top', 'etc.'],
                shop_page='TODO')
        industry_bf.put()


        #================================================================== ITEM === 
        one = Item(
                sku_id=0,
                name="denim shirtdress",
                brand="Ann Taylor",
                article='dresses',
                price=139,
                colors=['navy'],
                sizes=['xs', 's', 'm', 'l', 'xl'],
                industries=['consulting'],
                styles=['smart casual'],
                description='Demin Shirtdress',
                img_src='/images/items/AT01.jpg',
                external_src='TODO',
                smaller_imgs=['/images/charmanderllama.png', '/images/charmeleonllama.png', '/images/charizardllama.png'],
                date=datetime.date(2016, 1, 7))
        one.put()

        two = Item(
                sku_id=1,
                name="tropical whool sheath dress",
                brand="Ann Taylor",
                article='dresses',
                price=169,
                colors=['navy', 'black'],
                sizes=['xs', 's', 'm', 'l', 'xl'],
                industries=['consulting'],
                styles=['business formal', 'business casual'],
                description='tropical whool sheath dress',
                img_src='/images/items/AT02.jpg',
                external_src='TODO',
                smaller_imgs=['/images/charmanderllama.png', '/images/charmeleonllama.png', '/images/charizardllama.png'],
                date=datetime.date(2016, 1, 7))
        two.put()

        three = Item(
                sku_id=2,
                name="sleeveless shirtdress",
                brand="Ann Taylor",
                article='dresses',
                price=129,
                colors=['navy', 'red'],
                sizes=['xs', 's', 'm', 'l', 'xl'],
                industries=['consulting'],
                styles=['smart casual', 'business casual'],
                description='Classy shirtdress',
                img_src='/images/items/AT04.jpg',
                external_src='TODO',
                smaller_imgs=['/images/charmanderllama.png', '/images/charmeleonllama.png', '/images/charizardllama.png'],
                date=datetime.date(2016, 1, 10))
        three.put()
      four = Item(
                sku_id=3,
                name="stripe double v sheath dress",
                brand="Ann Taylor",
                article='dresses',
                price=129,
                colors=['black'],
                sizes=['xs', 's', 'm', 'l', 'xl'],
                industries=['consulting'],
                styles=['smart casual', 'business casual'],
                description='Classy v-neck dress',
                img_src='/images/items/AT03.jpg',
                external_src='TODO',
                smaller_imgs=['/images/charmanderllama.png', '/images/charmeleonllama.png', '/images/charizardllama.png'],
                date=datetime.date(2016, 1, 10))
        four.put()
        
        five = Item(
                sku_id=3,
                name="wrap flare dress",
                brand="Ann Taylor",
                article='dresses',
                price=129,
                colors=['navy'],
                sizes=['xs', 's', 'm', 'l', 'xl'],
                industries=['consulting'],
                styles=['smart casual', 'business casual'],
                description='Classy wrap dress',
                img_src='/images/items/AT05.jpg',
                external_src='TODO',
                smaller_imgs=['/images/charmanderllama.png', '/images/charmeleonllama.png', '/images/charizardllama.png'],
                date=datetime.date(2016, 1, 10))
        five.put()
     
       six = Item(
                sku_id=3,
                name="mesh stitch sweter dress",
                brand="Ann Taylor",
                article='dresses',
                price=139,
                colors=['black'],
                sizes=['xs', 's', 'm', 'l', 'xl'],
                industries=['consulting'],
                styles=['smart casual', 'business casual'],
                description='Classy sweater dress',
                img_src='/images/items/AT06.jpg',
                external_src='TODO',
                smaller_imgs=['/images/charmanderllama.png', '/images/charmeleonllama.png', '/images/charizardllama.png'],
                date=datetime.date(2016, 1, 10))
        six.put()   
       seven = Item(
                sku_id=3,
                name="cotton sateen sheath dress",
                brand="Ann Taylor",
                article='dresses',
                price=129,
                colors=['black'],
                sizes=['xs', 's', 'm', 'l', 'xl'],
                industries=['consulting'],
                styles=['smart casual', 'business casual'],
                description='Classy sweater dress',
                img_src='/images/items/AT07.jpg',
                external_src='TODO',
                smaller_imgs=['/images/charmanderllama.png', '/images/charmeleonllama.png', '/images/charizardllama.png'],
                date=datetime.date(2016, 1, 10))
        seven.put()   
        
        eight = Item(
                sku_id=3,
                name="structured peplum short sleeve top",
                brand="Ann Taylor",
                article='tops',
                price=59.50,
                colors=['black'],
                sizes=['xs', 's', 'm', 'l', 'xl'],
                industries=['consulting'],
                styles=['smart casual', 'business casual'],
                description='Peplum top',
                img_src='/images/items/AT09.jpg',
                external_src='TODO',
                smaller_imgs=['/images/charmanderllama.png', '/images/charmeleonllama.png', '/images/charizardllama.png'],
                date=datetime.date(2016, 1, 10))
        eight.put()   
        
        night = Item(
                sku_id=3,
                name="shadow floral pencil skirt",
                brand="Ann Taylor",
                article='bottoms',
                price=89,
                colors=['navy'],
                sizes=['xs', 's', 'm', 'l', 'xl'],
                industries=['consulting'],
                styles=['smart casual', 'business casual'],
                description='Floral pencil skirt',
                img_src='/images/items/AT10.jpg',
                external_src='TODO',
                smaller_imgs=['/images/charmanderllama.png', '/images/charmeleonllama.png', '/images/charizardllama.png'],
                date=datetime.date(2016, 1, 10))
        night.put() 
        
        for i in range(30):
            ten = Item(
                    sku_id=0,
                    name="c",
                    brand="JCrew",
                    article='suits',
                    price=45.99,
                    colors=['black', 'white', 'gray'],
                    sizes=['xs', 's', 'm', 'l', 'xl'],
                    industries=['consulting'],
                    styles=['smart casual', 'business casual'],
                    description='Something I made up.',
                    img_src='/images/charmanderllama.png',
                    external_src='TODO',
                    smaller_imgs=['/images/charmanderllama.png', '/images/charmeleonllama.png', '/images/charizardllama.png'],
                    date=datetime.date(2015, 1, 9))
            ten.put()
        ############################################################### END DATASTORE ####


class HomeHandler(BaseHandler):
    def get(self):
        logging.info('in main handler logging')
        #self.render_template('templates/home.html')
        self.render_template('templates/leka/index7.html')

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


        filters = [
            {
                'name': 'article',
                'selections': ARTICLES
            },
            {
                'name': 'colors',
                'selections': COLORS 
            },
            {
                'name': 'sizes',
                'selections': SIZES 
            },
            {
                'name': 'brand',
                'selections': BRANDS 
            },
            {
                'name': 'styles',
                'selections': STYLES 
            },
            {
                'name': 'industries',
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
            if f['name'] in argDict:
                fValues = argDict[f['name']]
                for i in fValues:
                    query = query.filter(getattr(Item, f['name']) == i)

        return query

class WhoWoreWhatHandler(BaseHandler):
    def get(self):
        coverflow_data = Coverflow.query().order(Coverflow.order_id).fetch()
        logging.info(coverflow_data)

        template_vars = {
                'coverflow_data': coverflow_data
        }

        logging.info('in who wore what handler logging')
        self.render_template('templates/who_wore_what.html', template_vars)

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

            industry_results= IndustryStyle.query(getattr(IndustryStyle, 'industry') == industry_arg).fetch()

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
        try: 
            style_arg = self.request.get('style')

            style_data = LookOccasion.query(getattr(LookOccasion, 'style') == style_arg).order(LookOccasion.order_id).fetch()

            template_vars = {
                    'industry_names': INDUSTRIES, 
                    'style_data': style_data, 
                    'style': style_arg
            }

            # Check if it's a valid industry.
            if style_arg == '':
                print "didn't get a valid style value in get request."

            else:
                # Display normal industry page.
                logging.info('in style handler logging')
                self.render_template('templates/style.html', template_vars)

        except(TypeError, ValueError):
            template_vars['message'] = "Invalid style."
            self.render_template('templates/danger_message.html', template_vars)


class StyleGuidesHandler(BaseHandler):
    def get(self):

        style_data = [
                {'name': 'smart casual', 'img_src': '/images/smartcasual.png'},
                {'name': 'business casual', 'img_src': '/images/businesscasual.png'},
                {'name': 'business formal', 'img_src': '/images/businessformal.png'}]


        template_vars = {
                'industry_names': INDUSTRIES, 
                'style_data': style_data
        }

        logging.info('in style guides handler logging')
        self.render_template('templates/style_guides.html', template_vars)

class PageNotFoundHandler(BaseHandler):
    def get(self):
            template_vars = {
                'message': 'Error 404. Page not found.'
            }
            self.render_template('templates/danger_message.html', template_vars)

class SignUpHandler(BaseHandler):
    def get(self):
            self.render_template('templates/sign_up.html')


app = webapp2.WSGIApplication(routes=[
    ('/shop', ShopHandler),
    ('/whoworewhat/person', WhoWoreWhatPersonHandler),
    ('/whoworewhat', WhoWoreWhatHandler),
    ('/styleguides/industry', StyleGuidesIndustryHandler),
    ('/styleguides/style', StyleGuidesStyleHandler),
    ('/styleguides', StyleGuidesHandler),
    ('/populatedatastore', DatastoreHandler),
    ('/signup', SignUpHandler),
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
