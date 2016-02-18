import csv
"""
with open('test_data.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    first = True
    keys = []
    items = []
    for row in reader:
        if (first):
            keys = row
            first = False
        else:
            print row
            d = {}
            for r in range(len(row)):
                if keys[r] == 'occasion':
                    d[keys[r]] = row[r].split(', ')
                else:
                    d[keys[r]] = row[r]

            print d
            print
"""
a = [1, 2, 3]
b = a[1:len(a)]
print b