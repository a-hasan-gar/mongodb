import pprint
import googlemaps
from enum import IntEnum

from django.http import JsonResponse
from django.shortcuts import render
import requests
from .form import *

from django.conf import settings
from pymongo import MongoClient, GEO2D, GEOSPHERE

gmaps = googlemaps.Client(key="AIzaSyCRmg-YeF4L81AF0gAenxovhsepQl2-K1U") 


def index(request):
    json_res = {}
    longs= -0.1278
    lat = 51.5074
    opsi = opsi_filter(initial={'lat_lon':"51.5074,-0.1278"})
    if request.method == 'POST':
       # res = opsi_filter(request.POST)
        print("ini request.POST")
        print(request.POST )
    
        radius = request.POST['radius']
        limit = request.POST['limit']
        filter_type = request.POST['filter_type']
        # cities_opt = request.POST.get('cities', False)
        lonlan = request.POST.get('lat_lon', False)
        lon = int(lonlan.split(", ")[1])
        lat = int(lonlan.split(", ")[0])
        #tp bingung gmn masukin value pinnya ke post
        print("ini cities_opt")
        print(cities_opt)
        # lon = request.POST['lon']
        # lat = request.POST.get('lat', False)
        #url = 'http://167.71.204.99/accidents/nearby?'+cities_opt+'&radius='+radius+"&limit="+limit+"&filter_type="+filter_type
        url = 'http://167.71.204.99/accidents/nearby?'+"lon="+lon+"&lat="+lat+'&radius='+radius+"&limit="+limit+"&filter_type="+filter_type
        print(url)
        req = requests.get(url)
        json_res = req.json()
        print(json_res)

    return render(request, 'search_nearby/home.html', {'opsi' : opsi, 'json_res' : json_res, 'lat':lat,'longs':longs})


# Connect with mongoDB
collection_accident = settings.DB.accident

EARTH_RADIUS = 6378100 # in meter

def page_coordinate(request):
    
    places = place()
    lat_long = get_location(str(request.GET['place']))
    lat= lat_long['lat']
    longs=lat_long['lng']
    str_lat = str(lat)
    str_long = str(longs)
    opsi = opsi_filter(initial={'lat_lon':str_lat+','+str_long})
    return render(request, 'search_nearby/home.html', {'opsi' : opsi,'lat':lat,'longs':longs,'places':places})

def map_coordinate(request):
    
    places = place()
    opsi = opsi_filter()
    lat_long = get_location(str(request.GET['lat_lon']))
    lat= lat_long['lat']
    longs=lat_long['lng']
    return render(request, 'search_nearby/home.html', {'opsi' : opsi,'lat':lat,'longs':longs,'places':places})

def get_location(name):
    geocode_result = gmaps.geocode(name)
    lat_long= geocode_result[0]['geometry']['location']
    return lat_long


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
    query = {"Location": {"$geoWithin": {"$centerSphere": [[lon, lat], radius / EARTH_RADIUS]}}}
    accident = collection_accident.find(query, batch_size=lim).limit(lim)
    return list(accident)


