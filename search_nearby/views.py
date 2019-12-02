import pprint
from enum import Enum

from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from pymongo import MongoClient, GEO2D, GEOSPHERE


def index(request):
    return render(request, 'search_nearby/home.html')

# Connect with mongoDB
collection_accident = settings.DB.accident
collection_accident.create_index([("Location", GEO2D)])

def nearby_accidents(request):
    lon = request.GET.get('lon', None)
    lat = request.GET.get('lat', None)

    if request.method != 'GET' or not lat or not lon:
        return JsonResponse({})

    try:
        lon = float(lon)
        lat = float(lat)
        radius = request.GET.get('radius', 500)
        limit = request.GET.get('limit', 0)

        filter_type = int(request.GET.get('filter_type', FilterType.LIGHT_CONDITIONS))
    except:
        return JsonResponse({})

    accidents = get_nearby_accidents(lat, lon, radius, limit)
    frequencies = transform_to_filter(accidents, filter_type)

    return JsonResponse({frequencies})

class FilterType(Enum):
    LIGHT_CONDITIONS = 0,
    ROAD_SURFACE_CONDITIONS = 1,
    ROAD_TYPE = 2,
    WEATHER_CONDITIONS = 3,
    YEAR = 4,

def transform_to_filter(accidents, filter_type):
    frequencies = {}

    for accident in accidents:
        if filter_type == FilterType.LIGHT_CONDITIONS:
            val = accident['Light_Conditions']
        elif filter_type == FilterType.ROAD_SURFACE_CONDITIONS:
            val = accident['Road_Surface_Conditions']
        elif filter_type == FilterType.ROAD_TYPE:
            val = accident['Road_Type']
        elif filter_type == FilterType.WEATHER_CONDITIONS:
            val = accident['Weather_Conditions']
        elif filter_type == FilterType.YEAR:
            val = accident['Year']

        if val not in frequencies:
            frequencies[val] = 1
        else:
            frequencies[val] += 1

    return frequencies

# Query
def get_nearby_accidents(lon, lat, radius=500, lim=0):
    query = {"Location": {"$geoWithin": {"$centerSphere": [[lon, lat], radius/6378100]}}}
    accident = collection_accident.find(query).limit(lim)
    return accident.toArray()
