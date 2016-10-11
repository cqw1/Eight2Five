import urllib2
import csv
import json

VERSION = "v2"
METHOD_NAME = "products"
API_KEY = "uid849-34126543-19"
CATEGORY = "dresses"
RETAILER = ""
OFFSET = 0
OFFSET_MAX = 29 # max that shopstyle sets, normally 100
LIMIT = 30 # max that shopstyle sets, normally 50

sku_set = set()

#Strips whitespace and turns all letters to lowercase.
def unformat(s):
    return ''.join(s.split()).lower()


with open('shopstyle_products.csv', 'wb') as writefile:
    writer = csv.writer(writefile)
    writer.writerow(['sku_id', 'brand', 'name', 'image_1', 'image_2', 'price', 'apparel', 'occasion', 'dress_code', 'url', 'discount', 'weather', 'geography', 'colors', 'accessory'])

    with open('selected_retailers.csv', 'rb') as retailers_file:
        retailers_reader = csv.reader(retailers_file)
        for retailers_row in retailers_reader:
            retailers_values = retailers_row[1: len(retailers_row)]
            retailers_values = [rv for rv in retailers_values if rv] # Remove empty strings from list.

            RETAILER = retailers_row[1] # second column is the id of the retailer we want to query for

            if RETAILER == 'id':
                continue;

            print "reading retailer: " + RETAILER

            with open('selected_categories.csv', 'rb') as categories_file:
                categories_reader = csv.reader(categories_file)
                for categories_row in categories_reader:
                    categories_values = categories_row[1: len(categories_row)]
                    categories_values = [cv for cv in categories_values if cv] # Remove empty strings from list.

                    CATEGORY = categories_row[1] # second column is the id of the category we want to query for

                    if CATEGORY == 'id':
                        continue;

                    print "reading category: " + CATEGORY
                    OFFSET = 0

                    # Continue if we haven't reached the max / "last page" of the results
                    while OFFSET <= OFFSET_MAX:
                        print "offset: " + str(OFFSET)

                        URL = "http://api.shopstyle.com/api/" + VERSION + "/" + METHOD_NAME + "/?pid=" + API_KEY +"&cat=" + CATEGORY + "&offset=" + str(OFFSET) + "&limit=" + str(LIMIT) + "&fl=r" + RETAILER
                        print "URL: " + URL

                        # Get the response from the api call
                        response = urllib2.urlopen(URL)
                        json_string = response.read()
                        json_obj = json.loads(json_string)


                        for p in json_obj['products']:

                            """
                            # In case a product has multiple colors
                            combined_colors = ""
                            if len(p['colors']) > 0:
                                combined_colors += p['colors'][0]['name']

                                for c in p['colors'][1:]:  # Iterate over everything except the last item
                                    combined_colors += ", " + c['name']
                            """


                            #if p['name'] in sku_set, keeps track of duplicates:
                            if unformat(p['name']) in sku_set:
                                continue

                            else:
                                #sku_set.add(p['id'])
                                sku_set.add(unformat(p['name']))


                            result = [p['id']]

                            # Adds brand
                            if 'brand' in p:
                                result.append(p['brand']['name'].encode('utf-8'))
                            else:
                                continue

                            """
                            if 'retailer' in p:
                                result.append(p['retailer']['name'].encode('utf-8'))
                            else:
                                result.append("")
                            """

                            # Adds name.
                            if 'name' in p:
                                result.append(p['name'].encode('utf-8'))
                            else:
                                continue

                            # Adds image_1 and image_2
                            if 'image' in p:
                                if 'Original' in p['image']['sizes']:
                                    result.append(p['image']['sizes']['Original']['url'])
                                    result.append(p['image']['sizes']['Original']['url'])
                                elif 'Best' in p['image']['sizes']:
                                    result.append(p['image']['sizes']['Best']['url'])
                                    result.append(p['image']['sizes']['Best']['url'])
                                else:
                                    result.append('no Best or Original image')
                                    result.append('no Best or Original image')
                            else:
                                continue

                            # Adds price
                            if 'price' in p:
                                result.append(p['price'])
                            else:
                                continue

                            """
                            # In case a product falls under multiple categories, need to add all of them
                            combined_categories = ""
                            if len(p['categories']) > 0:
                                combined_categories += p['categories'][0]['name']

                                for c in p['categories'][1:]:  # Iterate over everything except the last item
                                    combined_categories += ", " + c['name']

                                result.append(combined_categories)
                            else:
                                result.append(CATEGORY)
                            """

                            # TODO. implement category mappings.
                            result.append("dress")

                            # Skip occasion
                            result.append("")

                            # Skip dress_code 
                            result.append("")

                            # Add url
                            if 'pageUrl' in p:
                                result.append(p['pageUrl'])
                            else:
                                continue

                            # Skip discount 
                            result.append("")

                            # Skip weather 
                            result.append("")

                            # Skip geography 
                            result.append("")

                            # Skip colors 
                            result.append("")

                            # Skip accessory 
                            result.append("")



                            #result.extend([p['name'].encode('utf-8'), p['image']['sizes']['Best']['url'].encode('utf-8'), "", p['price'].encode('utf-8'), combined_categories.encode('utf-8'), "", "", p['clickUrl'].encode('utf-8'), "", "", "", combined_colors.encode('utf-8'), ""])
                            #result.extend([p['name'].encode('utf-8'), p['image']['sizes']['Best']['url'].encode('utf-8'), "", p['price'].encode('utf-8'), combined_categories.encode('utf-8'), "", "", p['clickUrl'].encode('utf-8'), "", "", "", combined_colors.encode('utf-8'), ""])

                            writer.writerow(result)
                            #print "writing " + str(p['id'])

                        OFFSET += LIMIT






"""
# get by product id
PRODUCT_ID = 517944558
url = "http://api.shopstyle.com/api/" + VERSION + "/" + METHOD_NAME + "/" + str(PRODUCT_ID) + "?pid=" + API_KEY 

response = urllib2.urlopen(url)
json_string = response.read()

json_obj = json.loads(json_string)
one = json_obj

response = urllib2.urlopen(url)
json_string = response.read()

json_obj = json.loads(json_string)
two = json_obj 

print one['id']
print two['id']
print one['id'] == two['id']

"""



"""
data = json_obj[METHOD_NAME]

with open('products.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['name', 'id'])

    for d in data:
        writer.writerow([d['name'].encode('utf-8') + str(d['id'])])

"""
