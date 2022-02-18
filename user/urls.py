from django.urls import path
from .views import RegisterUser, LoginUser, logout_user


urlpatterns = [
    path('auth/register', RegisterUser.as_view(), name='register'),
    path('auth/login', LoginUser.as_view(), name='login'),
    path('auth/logout', logout_user, name='logout'),
]

