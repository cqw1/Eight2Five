import urllib2
import csv
import json

VERSION = "v2"
METHOD_NAME = "categories"
API_KEY = "uid849-34126543-19"
FORMAT = "json"
url = "http://api.shopstyle.com/api/" + VERSION + "/" + METHOD_NAME + "/?pid=" + API_KEY +"&format=" + FORMAT

with open('selected_categories.csv', 'rb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['name', 'id'])

    for d in data:
        writer.writerow([d['name'].encode('utf-8'), d['id'].encode('utf-8')])

with open('categories', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['name', 'id'])

    for d in data:
        writer.writerow([d['name'].encode('utf-8'), d['id'].encode('utf-8')])



with open('selected_categories.csv', 'rb') as readfile:
    reader = csv.reader(readfile)
    for row in reader:
        values = row[0: len(row)]
        values = [v for v in values if v] # Remove empty strings from list.

        NAME = row[0] # second column is the id of the category we want to query for
        if NAME == "name":
            # Skip the first row
            continue

        url = "http://api.shopstyle.com/api/" + VERSION + "/" + METHOD_NAME + "/?pid=" + API_KEY +"&format=" + FORMAT

        response = urllib2.urlopen(url)
        json_string = response.read()

        json_obj = json.loads(json_string)
        data = json_obj[METHOD_NAME]




