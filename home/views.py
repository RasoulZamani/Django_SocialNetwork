from django.shortcuts import render
from django.http import HttpResponse
from django.views import View 
# Create your views here.

#def home(request):
#    return render(request, 'home/index.html')#HttpResponse("This is Home Page!")
class HomeView(View):
    """CBV for home page"""
    def get(self, request):
        return render(request, 'home/index.html') 
    
    def post(self, request):
        return render(request, 'home/index.html')           