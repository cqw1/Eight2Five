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

GENDERS = [
    'men', 
    'women'
]

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
    gender = ndb.StringProperty(required=True, choices=GENDERS)
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

        men_shop_filters = DropdownSection(
                heading='men', 
                items=['tops', 'bottoms', 'suits', 'outerwear'], 
                dropdown='shop',
                order_id=0)
        men_shop_filters.put()

        women_shop_filters = DropdownSection(
                heading='women', 
                items=['tops', 'bottoms', 'dresses', 'suits', 'outerwear'], 
                dropdown='shop',
                order_id=1)
        women_shop_filters.put()

        #=============================================================== LOOKOCCASION === 
        
        smartcasual_one = LookOccasion(
                style='smart casual',
                look_img_src='/images/smartcasual.png',
                look_descriptions=['White jeans and top', 'Beige blazer'],
                occasion_img_src='/images/smartcasual.png',
                occasion_descriptions=['Casual Fridays'],
                order_id=0,
                shop_page='TODO')
        smartcasual_one.put()

        smartcasual_two = LookOccasion(
                style='smart casual',
                look_img_src='/images/smartcasual.png',
                look_descriptions=['Something', 'Or another'],
                occasion_img_src='/images/smartcasual.png',
                occasion_descriptions=['The Happy Hour'],
                order_id=1,
                shop_page='TODO')
        smartcasual_two.put()

        businesscasual_one = LookOccasion(
                style='business casual',
                look_img_src='/images/businesscasual.png',
                look_descriptions=['White jeans and top', 'Beige blazer'],
                occasion_img_src='/images/businesscasual.png',
                occasion_descriptions=['Casual Fridays'],
                order_id=0,
                shop_page='TODO')
        businesscasual_one.put()

        businesscasual_two = LookOccasion(
                style='business casual',
                look_img_src='/images/businesscasual.png',
                look_descriptions=['Something', 'Or another'],
                occasion_img_src='/images/businesscasual.png',
                occasion_descriptions=['The Happy Hour'],
                order_id=1,
                shop_page='TODO')
        businesscasual_two.put()

        businessformal_one = LookOccasion(
                style='business formal',
                look_img_src='/images/businessformal.png',
                look_descriptions=['White jeans and top', 'Beige blazer'],
                occasion_img_src='/images/businessformal.png',
                occasion_descriptions=['Casual Fridays'],
                order_id=0,
                shop_page='TODO')
        businessformal_one.put()

        businessformal_two= LookOccasion(
                style='business formal',
                look_img_src='/images/businessformal.png',
                look_descriptions=['Something', 'Or another'],
                occasion_img_src='/images/businessformal.png',
                occasion_descriptions=['The Happy Hour'],
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
                name="Default Name",
                brand="JCrew",
                gender='women',
                article='tops',
                price=49.99,
                colors=['black', 'white', 'gray'],
                sizes=['xs', 's', 'm', 'l', 'xl'],
                industries=['consulting'],
                styles=['smart casual', 'business casual'],
                description='Something I made up.',
                img_src='/images/charmanderllama.png',
                external_src='TODO',
                smaller_imgs=['/images/charmanderllama.png', '/images/charmeleonllama.png', '/images/charizardllama.png'],
                date=datetime.date(2016, 1, 7))
        one.put()

        two = Item(
                sku_id=0,
                name="A",
                brand="JCrew",
                gender='women',
                article='tops',
                price=49.99,
                colors=['black', 'white', 'gray'],
                sizes=['xs', 's', 'm', 'l', 'xl'],
                industries=['consulting'],
                styles=['smart casual', 'business casual'],
                description='Something I made up.',
                img_src='/images/charmanderllama.png',
                external_src='TODO',
                smaller_imgs=['/images/charmanderllama.png', '/images/charmeleonllama.png', '/images/charizardllama.png'],
                date=datetime.date(2016, 1, 7))
        two.put()

        three = Item(
                sku_id=0,
                name="B",
                brand="JCrew",
                gender='men',
                article='bottoms',
                price=39.99,
                colors=['black', 'white', 'gray'],
                sizes=['xs', 's', 'm', 'l', 'xl'],
                industries=['consulting'],
                styles=['smart casual', 'business casual'],
                description='Something I made up.',
                img_src='/images/charmanderllama.png',
                external_src='TODO',
                smaller_imgs=['/images/charmanderllama.png', '/images/charmeleonllama.png', '/images/charizardllama.png'],
                date=datetime.date(2016, 1, 10))
        three.put()

        for i in range(40):
            four = Item(
                    sku_id=0,
                    name="C",
                    brand="JCrew",
                    gender='men',
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
            four.put()
        ############################################################### END DATASTORE ####


class HomeHandler(webapp2.RequestHandler):
    def get(self):
        template_vars = {
                'styleguide_sections': self.app.config.get('styleguide_sections')}
        logging.info(self.app.config.get('styleguide_sections'))

        home_template = jinja_environment.get_template('templates/home.html')
        logging.info('in main handler logging')
        self.response.write(home_template.render(template_vars))

class ShopHandler(webapp2.RequestHandler):
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
                'name': 'gender',
                'selections': GENDERS
            },
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
    
        logging.info('================= RESULTS =====================')
        for r in results:
            logging.info(r)
            logging.info('----------------------')

        logging.info('======================================')

        template_vars = {
                'styleguide_sections': self.app.config.get('styleguide_sections'),
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
                'results': results
        }

        shop_template = jinja_environment.get_template('templates/shop.html')
        logging.info('in shop handler logging')
        self.response.write(shop_template.render(template_vars))

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

class WhoWoreWhatHandler(webapp2.RequestHandler):
    def get(self):
        coverflow_data = Coverflow.query().order(Coverflow.order_id).fetch()
        logging.info(coverflow_data)

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

            logging.info(self.app.config.get('styleguide_sections'))

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
                    industry_dict['high'], 
                    industry_dict['medium'], 
                    industry_dict['low']
            ]

            logging.info(industry_data)

            template_vars = {
                    'industry_names': INDUSTRIES, 
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
                    'industry_names': INDUSTRIES, 
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
                {'name': 'smart casual', 'img_src': '/images/smartcasual.png'},
                {'name': 'business casual', 'img_src': '/images/businesscasual.png'},
                {'name': 'business formal', 'img_src': '/images/businessformal.png'}]

        logging.info(self.app.config.get('styleguide_sections'))

        template_vars = {
                'industry_names': INDUSTRIES, 
                'style_data': style_data, 
                'styleguide_sections': self.app.config.get('styleguide_sections')}

        style_guides_template = jinja_environment.get_template('templates/style_guides.html')
        logging.info('in style guides handler logging')
        self.response.write(style_guides_template.render(template_vars))

class PageNotFoundHandler(webapp2.RequestHandler):
    def get(self):
            self.response.write('<html><body><p>Error 404. Page not found.</p></body></html>')



app = webapp2.WSGIApplication(routes=[
    ('/shop', ShopHandler),
    ('/whoworewhat/person', WhoWoreWhatPersonHandler),
    ('/whoworewhat', WhoWoreWhatHandler),
    ('/styleguides/industry', StyleGuidesIndustryHandler),
    ('/styleguides/style', StyleGuidesStyleHandler),
    ('/styleguides', StyleGuidesHandler),
    ('/populatedatastore', DatastoreHandler),
    ('/', HomeHandler),
    ('/home', HomeHandler),
    ('/.*', PageNotFoundHandler)
], debug=True, config={
    'styleguide_sections': DropdownSection.query(getattr(DropdownSection, 'dropdown') == 'style guides').order(DropdownSection.order_id).fetch() 
})
