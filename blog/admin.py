from django.contrib import admin
from .models import Post, Category, Comment, Tag, User


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_pub', 'author', 'category', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'text', 'author')
    list_editable = ('is_published',)
    list_filter = ('category', 'author')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_pub', 'author', 'post')
    list_display_links = ('id',)
    search_fields = ('text', 'author')
    list_filter = ('post', 'author')


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag)
admin.site.register(User)
