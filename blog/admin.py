from django.contrib import admin
from .models import Post, Category, Comment, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_pub')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'text')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_pub')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'text')




admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Tag)
# Register your models here.
