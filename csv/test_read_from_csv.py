import csv

with open('test_data.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print row

