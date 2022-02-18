from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/avatar/%Y/%m/%d/', blank=True, verbose_name='Аватар', default='images/avatar/default.bmp')
    email = models.EmailField('E-mail', unique=True)