from django.shortcuts import render
from django.conf import settings
import pprint
from pymongo import MongoClient, GEO2D, GEOSPHERE


# Create your views here.
def index(request):
    return render(request, 'search_nearby/home.html')

# Connect with mongoDB
collection_accident = settings.DB.accident
collection_accident.create_index([("Location", GEO2D)])

# Query
def get_nearby_accident(lon, lat, radius=500, lim=0):
    query = {"Location": {"$geoWithin": {"$centerSphere": [[lon, lat], radius/6378100]}}}
    accident = collection_accident.find(query).limit(lim)
    return accident.toArray()
