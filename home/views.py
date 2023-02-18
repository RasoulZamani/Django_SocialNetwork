from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home/index.html')#HttpResponse("This is Home Page!")    