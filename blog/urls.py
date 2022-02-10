from django.urls import path
from blog.views import PostView, ShowPost, Post_Cat_View, Post_Tag_View, RegisterUser, LoginUser, logout_user



urlpatterns = [
    path('', PostView.as_view(), name='index'),
    path('auth/register', RegisterUser.as_view(), name='register'),
    path('auth/login', LoginUser.as_view(), name='login'),
     path('auth/logout', logout_user, name='logout'),
    path('<slug:category_slug>', Post_Cat_View.as_view(), name='category'),
    path('tags/<slug:tag_slug>', Post_Tag_View.as_view(), name='tag'),
    path('<slug:category_slug>/<slug:post_slug>', ShowPost.as_view(), name='post'),



]

