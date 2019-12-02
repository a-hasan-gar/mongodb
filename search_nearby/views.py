import pprint
from enum import IntEnum

from django.http import JsonResponse
from django.shortcuts import render

from .form import *

from django.conf import settings
from pymongo import MongoClient, GEO2D, GEOSPHERE

def index(request):

    opsi = opsi_filter()
    return render(request, 'search_nearby/home.html', {'opsi' : opsi})


# Connect with mongoDB
collection_accident = settings.DB.accident

EARTH_RADIUS = 6378100 # in meter
MAX_BATCH_SIZE = 100000

def nearby_accidents(request):
    if request.method != 'GET' or 'lon' not in request.GET or 'lat' not in request.GET:
        return JsonResponse({})

    try:
        lon = float(request.GET['lon'])
        lat = float(request.GET['lat'])
        radius = float(request.GET.get('radius', 500))
        limit = int(request.GET.get('limit', 0))
        filter_type = int(request.GET.get('filter_type', FilterType.LIGHT_CONDITIONS))

    except:
        return JsonResponse({})


    accidents = get_nearby_accidents(lon, lat, radius, limit)
    frequencies = transform_to_filter(accidents, filter_type)

    return JsonResponse(frequencies)

class FilterType(IntEnum):
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
        else:
            continue

        if val not in frequencies:
            frequencies[val] = 1
        else:
            frequencies[val] += 1

    return frequencies

# Query
def get_nearby_accidents(lon, lat, radius=500, lim=0):
    lim = min(lim, MAX_BATCH_SIZE)
    query = {"Location": {"$geoWithin": {"$centerSphere": [[lon, lat], radius / EARTH_RADIUS]}}}
    accident = collection_accident.find(query, batch_size=lim).limit(lim)
    return list(accident)
