import urllib2
import csv
import json

VERSION = "v2"
METHOD_NAME = "products"
API_KEY = "uid849-34126543-19"
CATEGORY = "dresses"
#url = "http://api.shopstyle.com/api/" + VERSION + "/" + METHOD_NAME + "/?pid=" + API_KEY +"&cat=" + CATEGORY

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
data = json_obj[METHOD_NAME]

with open('products.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['name', 'id'])

    for d in data:
        writer.writerow([d['name'].encode('utf-8') + str(d['id'])])

"""