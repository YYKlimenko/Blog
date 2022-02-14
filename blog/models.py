# from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from project1 import settings
from mptt.models import MPTTModel, TreeForeignKey
from mptt import register


class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/avatar/%Y/%m/%d/', blank=True, verbose_name='Аватар', default='images/avatar/default.bmp')
    email = models.EmailField('E-mail', unique=True)



class Category(models.Model):
    name = models.CharField(max_length = 50, verbose_name='Наименование')
    slug = models.SlugField(max_length = 50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Tag(models.Model):
    name = models.CharField(max_length = 50, verbose_name='Тэг')
    slug = models.SlugField(max_length = 50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length = 300, verbose_name='Комментарий')
    date_pub = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    post = models.ForeignKey(
                             'Post',
                             on_delete=models.CASCADE,
                             verbose_name='Комментируемое сообщение',
                             related_name = 'comments',
    )
    parent = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    likes = models.ManyToManyField(User, blank = True, related_name='comments', verbose_name = 'Лайки')

    def __str__(self):
        return f'Комментарий {str(self.id)}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-date_pub',)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET('Неизвестный автор'))
    title = models.CharField(max_length = 100, unique = True, verbose_name='Заголовок')
    slug = models.SlugField(max_length = 100, unique = True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True, verbose_name='Изображение')
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        verbose_name='Категория',
    )
    tags = models.ManyToManyField('Tag', blank = True, related_name='posts', verbose_name = 'Теги',)
    preview_text = models.TextField(max_length = 200, verbose_name='Превью')
    text = models.TextField(max_length = 5000, verbose_name='Текст')
    date_pub = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    likes = models.ManyToManyField(User, blank = True, related_name='posts', verbose_name = 'Лайки')
    is_published = models.BooleanField("Опубликовано", null=True, blank=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'category_slug': self.category.slug, 'post_slug': self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-date_pub',)



