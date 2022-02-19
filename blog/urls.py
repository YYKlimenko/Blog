from django.urls import path
from blog.views import PostListView, ShowPost, PostCatListView, PostTagListView, SearchPostListView

app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('search/result', SearchPostListView.as_view(), name='search'),
    path('<slug:category_slug>', PostCatListView.as_view(), name='category'),
    path('tags/<slug:tag_slug>', PostTagListView.as_view(), name='tag'),
    path('<slug:category_slug>/<slug:post_slug>', ShowPost.as_view(), name='post'),

]

