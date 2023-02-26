from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    body    = models.TextField()
    slug    = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created','-body')       
        
         
    def __str__(self) -> str:
        return f"{self.slug} - last update:{self.updated}"
    
    def get_absolute_url(self):
        return reverse("home:post_details", args=(self.id, self.slug))
    
    def like_count(self):
        """counting likes"""
        return self.post_like.count()
    
    def user_like(self, user):
        """user has liked or no"""
        user_like = user.user_like.filter(post=self)
        if user_like.exists():
            return True
        return False
    
            
class Comment(models.Model):
    """model for comments"""
    user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    post  = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply_comment',
                blank=True, null=True)
    is_reply= models.BooleanField(default=False)
    body    = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f" {self.user}: {self.body[:40]}"
    
    
    
class Like(models.Model):
    """model for likes"""
    user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post  = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')
    
    def __str__(self):
        return f" {self.user} likes {self.post.body[:40]}"
    
    