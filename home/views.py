from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
#from django.contrib.auth.models import User  
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


#def home(request):
#    return render(request, 'home/index.html')#HttpResponse("This is Home Page!")
class HomeView(View):
    """CBV for home page"""
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts':posts}) 
              
    
class PostDetailView(View):
    """CBV for post details"""
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        return render(request, 'home/details.html', {'post':post})
    
   
class PostDeleteView(LoginRequiredMixin, View):
    """CBV for deleting post """
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id :
            post.delete()
            messages.success(request, 'Your post was deleted seccessfuly!', 'seccess')
        else:
            messages.error(request, 'You can not delete other posts!!', 'error')
            
        return redirect('home:home')