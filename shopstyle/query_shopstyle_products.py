import urllib2
import csv
import json

VERSION = "v2"
METHOD_NAME = "products"
API_KEY = "uid849-34126543-19"
CATEGORY = "dresses"
OFFSET = 0
OFFSET_MAX = 100 # max that shopstyle sets
LIMIT = 50 # max that shopstyle sets

URL = "http://api.shopstyle.com/api/" + VERSION + "/" + METHOD_NAME + "/?pid=" + API_KEY +"&cat=" + CATEGORY + "&offset=" + str(OFFSET) + "&limit=" + str(LIMIT)

with open('shopstyle_products.csv', 'wb') as writefile:
    writer = csv.writer(writefile)
    writer.writerow(['sku_id', 'brand', 'name', 'image_1', 'image_2', 'price', 'apparel', 'occasion', 'dress_code', 'url', 'discount', 'weather', 'geography', 'colors', 'accessory'])

    with open('selected_categories.csv', 'rb') as readfile:
        reader = csv.reader(readfile)
        for row in reader:
            values = row[1: len(row)]
            values = [v for v in values if v] # Remove empty strings from list.

            CATEGORY = row[1] # second column is the id of the category we want to query for
            OFFSET = 0

            # Continue if we haven't reached the max / "last page" of the results
            while OFFSET <= OFFSET_MAX:

                # Get the response from the api call
                response = urllib2.urlopen(URL)
                json_string = response.read()
                json_obj = json.loads(json_string)


                for p in json_obj['products']:

                    # In case a product falls under multiple categories, need to add all of them
                    combined_categories = ""
                    if len(p['categories']) > 0:
                        combined_categories += p['categories'][0]['name']

                        for c in p['categories'][1:]:  # Iterate over everything except the last item
                            combined_categories += ", " + c['name']

                    # In case a product has multiple colors
                    combined_colors = ""
                    if len(p['colors']) > 0:
                        combined_colors += p['colors'][0]['name']

                        for c in p['colors'][1:]:  # Iterate over everything except the last item
                            combined_colors += ", " + c['name']


                    result = [""]

                    if 'brand' in p:
                        result.append(p['brand']['name'].encode('utf-8'))
                    else:
                        result.append("")

                    #result.extend([p['name'].encode('utf-8'), p['image']['sizes']['Best']['url'].encode('utf-8'), "", p['price'].encode('utf-8'), combined_categories.encode('utf-8'), "", "", p['clickUrl'].encode('utf-8'), "", "", "", combined_colors.encode('utf-8'), ""])
                    #result.extend([p['name'].encode('utf-8'), p['image']['sizes']['Best']['url'].encode('utf-8'), "", p['price'].encode('utf-8'), combined_categories.encode('utf-8'), "", "", p['clickUrl'].encode('utf-8'), "", "", "", combined_colors.encode('utf-8'), ""])

                    writer.writerow(result)

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