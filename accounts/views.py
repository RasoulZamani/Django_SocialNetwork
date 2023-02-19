from django.shortcuts import render, redirect
from django.views import View 
from .forms import UserRegisterForm
from django.contrib.auth.models import User 
from django.contrib import messages


# Create your views here.
class RegisterView(View):
    """CBV for Register"""
    
    form_class     = UserRegisterForm
    template_class = 'accounts/register.html'
    
    def get(self, request):
        user_form = self.form_class()
        
        return render(request, self.template_class, {'user_form':user_form}) 
    
    def post(self, request):
        user_form = self.form_class(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password'])
            messages.success(request, f"Hi Dear {cd['username']} ! Your account was created successfuly!",'success')
        
            return redirect('home:home')
        
        return render(request, self.template_class, {'user_form':user_form})