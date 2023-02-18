from django.shortcuts import render
from django.views import View 

# Create your views here.
class RegisterView(View):
    """CBV for Register"""
    def get(self, request):
        return render(request, 'accounts/register.html') 
    
    def post(self, request):
        return render(request, 'accounts/register.html')    