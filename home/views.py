from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
#from django.contrib.auth.models import User  
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostUpdateForm
from django.utils.text import slugify
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
    

class PostUpdateView(LoginRequiredMixin, View):
    """CBV for updating post """
    class_form = PostUpdateForm
    def setup(self, request, *args, **kwargs):
        self.post_inst = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)
  
    def dispatch(self, request, *args, **kwargs):
        post = self.post_inst
        if not post.user.id == request.user.id :
            messages.error(request, 'You can not update other posts!!', 'error')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, post_id):
        post = self.post_inst
        form = self.class_form(instance=post)
        return render(request, 'home/update.html', {'form':form})
        
    def post(self, request, post_id):
        post = self.post_inst
        form = self.class_form(request.POST, instance=post)
        if form.is_valid:
            new_data=form.save(commit=False)
            new_data.slug = slugify(form.cleaned_data['body'][:40])
            new_data.save()
            messages.success(request, 'Your post was updated seccessfuly!', 'seccess')
            return redirect(request, 'home:post_details', post.id, post.slug )
            
        