from django.shortcuts import render
from .form import *

# Create your views here.
def index(request):
    opsi = opsi_filter()
    return render(request, 'search_nearby/home.html', {'opsi' : opsi})

