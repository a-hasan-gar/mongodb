from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'search_nearby/home.html')