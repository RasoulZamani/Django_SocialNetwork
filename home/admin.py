from django.contrib import admin
from .models import Post, Comment, Like

# Register your models here.
#admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=('user', 'updated',)
    search_fields=('slug',)
    list_filter = ('updated',)
    prepopulated_fields={'slug':('body',)}
    raw_id_fields=('user',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('user', 'post','created','is_reply')
    list_filter = ('created',)
    raw_id_fields=('user', 'post', 'reply')


admin.site.register(Like)