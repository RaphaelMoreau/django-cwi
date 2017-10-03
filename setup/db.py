import csv
from www.models import Country, AdType, AdPlace, Platform
import sys,os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def all():
    countries()
    types()
    places()
    platforms()

def countries():
    print("Importing country codes")
    file=open(os.path.join(BASE_DIR,'CountryCodes.csv'))
    reader=csv.reader(file)
    first=True
    for p in reader:
        if first:
            first=False
        else:
            c=Country(name=p[0], codeA2=p[1], codeA3=p[2], display=p[4])
            c.save()

def types():
    print("Importing ad types")
    file=open(os.path.join(BASE_DIR,'AdTypes.csv'))
    reader=csv.reader(file)
    first=True
    for p in reader:
        if first:
            first=False
        else:
            c=AdType(id=p[0], name=p[1])
            c.save()

def places():
    print("Importing ad places")
    file=open(os.path.join(BASE_DIR,'AdPlaces.csv'))
    reader=csv.reader(file)
    first=True
    for p in reader:
        if first:
            first=False
        else:
            c=AdPlace(id=p[0], name=p[1])
            c.save()

def platforms():
    print("Importing platforms")
    file=open(os.path.join(BASE_DIR,'Platforms.csv'))
    reader=csv.reader(file)
    first=True
    for p in reader:
        if first:
            first=False
        else:
            c=Platform(id=p[0], name=p[1])
            c.save()
