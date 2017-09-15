import csv
file=open('dbInit/CountryCodes.csv')
reader=csv.reader(file)

from www.models import Country
first=True
n=1
for p in reader:
    if first:
        first=False
    else:
        c=Country(name=p[0],codeA2=p[1],codeA3=p[2])
        print(c)
        c.save()
