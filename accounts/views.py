from django.shortcuts import render, redirect
from django.views import View 
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import authenticate, login


class UserRegisterView(View):
    """CBV for registering user"""
    
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
    
    
class UserLoginView(View):
    """CBV for Login user"""
        
    form_class     = UserLoginForm
    template_class = 'accounts/login.html'
        
    def get(self, request):
        user_form = self.form_class()
        
        return render(request, self.template_class, {'user_form':user_form}) 
    
    def post(self, request):
        user_form = self.form_class(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            user = authenticate(request, username=cd['username'],password= cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, f"Hi Dear {cd['username']} ! You have logged in successfuly!",'success')
        
                return redirect('home:home')
                
            messages.error(request, "Wrong username or password!",'error')

        return render(request, self.template_class, {'user_form':user_form})
    
    