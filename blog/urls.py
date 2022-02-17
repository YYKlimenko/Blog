from django.urls import path
from blog.views import PostListView, ShowPost, PostCatListView, PostTagListView,  LoginUser, logout_user, RegisterUser



urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('auth/register', RegisterUser.as_view(), name='register'),
    path('auth/login', LoginUser.as_view(), name='login'),
    path('auth/logout', logout_user, name='logout'),
    path('<slug:category_slug>', PostCatListView.as_view(), name='category'),
    path('tags/<slug:tag_slug>', PostTagListView.as_view(), name='tag'),
    path('<slug:category_slug>/<slug:post_slug>', ShowPost.as_view(), name='post'),



]

