from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
#from django.contrib.auth.models import User  
from .models import Post, Comment, Like
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostCreateUpdateForm, CommentCreateForm, CommentReplyForm, SearchForm
from django.utils.text import slugify


#def home(request):
#    return render(request, 'home/index.html')#HttpResponse("This is Home Page!")
class HomeView(View):
    """CBV for home page"""
    
    class_form = SearchForm
    
    def get(self, request):
        posts = Post.objects.all()
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
        return render(request, 'home/index.html', {'posts':posts, 'search_form':self.class_form}) 
              
    
class PostDetailView(View):
    """CBV for post details"""
    class_form = CommentCreateForm
    class_reply_form = CommentReplyForm
    def setup(self, request, *args, **kwargs):
        self.post_inst = Post.objects.get(pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        post = self.post_inst
        comments = post.post_comment.filter(is_reply=False)
        user_liked=False
        if request.user.is_authenticated and post.user_like(request.user):
            user_liked=True    
        return render(request, 'home/details.html',
                      {'post':post, 'comments':comments, 'comment_form':self.class_form, 'reply_form':self.class_reply_form, 'user_liked':user_liked})
    
    def post(self, request, *args, **kwargs):
        comment_form = self.class_form(request.POST)
        if comment_form.is_valid():
            new_commetn = comment_form.save(commit=False)
            new_commetn.user = request.user
            new_commetn.post = self.post_inst
            new_commetn.save()
            messages.success(request, 'Your comment was sent seccessfuly!', 'seccess')
            return redirect('home:post_details', self.post_inst.id, self.post_inst.slug)
   
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
    class_form = PostCreateUpdateForm
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
            new_post=form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:40])
            new_post.save()
            messages.success(request, 'Your post was updated seccessfuly!', 'seccess')
            return redirect('home:post_details', new_post.id, new_post.slug )
        

class PostCreateView(LoginRequiredMixin, View):
    """CBV for creating post """
    class_form = PostCreateUpdateForm
 
    def get(self, request):
        form = self.class_form()
        return render(request, 'home/create.html', {'form':form})
        
    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid:
            new_post=form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:10])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'Your new post is created seccessfuly!', 'seccess')
            return redirect('home:post_details', new_post.id, new_post.slug )
             
class PostAddReplyView(LoginRequiredMixin, View):
    """CBV for adding reply """
    class_form = CommentReplyForm
    
    def post(self, request, post_id, comment_id):
        post    = get_object_or_404(Post, id=post_id )
        comment = get_object_or_404(Comment, id=comment_id)
        
        reply_form = self.class_form(request.POST)
        if reply_form.is_valid():
            new_reply          = reply_form.save(commit=False)
            new_reply.user     = request.user
            new_reply.post     = post
            new_reply.reply    = comment 
            new_reply.is_reply = True
            
            new_reply.save()
            messages.success(request, 'Your reply was sent seccessfuly!', 'seccess')
            return redirect('home:post_details', post.id, post.slug)
        
class PostLikeView(LoginRequiredMixin, View):
    """CBV for like """
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like = Like.objects.filter(user=request.user, post=post)
        if like.exists():
            messages.error(request, 'only one like you can give to one post!', 'error')
        else:
            Like.objects.create(user=request.user, post=post)
            messages.success(request, 'You liked this post seccessfully!', 'seccess')
        return redirect('home:post_details', post.id, post.slug)
            