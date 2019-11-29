from django.urls import url

from .views import *

urlpatterns = [
    url(r'^$', index),
]