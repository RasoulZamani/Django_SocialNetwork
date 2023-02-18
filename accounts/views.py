from django.shortcuts import render
from django.views import View 
from .forms import UserRegisterForm

# Create your views here.
class RegisterView(View):
    """CBV for Register"""
    def get(self, request):
        user_form = UserRegisterForm()
        
        return render(request, 'accounts/register.html', {'user_form':user_form}) 
    
    def post(self, request):
        return render(request, 'accounts/register.html')    