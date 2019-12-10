from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('accidents/nearby', nearby_accidents, name='nearby-accidents'),
    path('accidents/nearbycoord', nearby_accidents_coord, name='nearby-accidents-coord'),
    # path('coordinate', page_coordinate, name='lot-lang'),
]
