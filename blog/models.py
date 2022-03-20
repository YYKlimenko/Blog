from django.db import models
from django.urls import reverse
from user.models import User


class Category(models.Model):
    name = models.CharField('Наименование категории', max_length=50)
    slug = models.SlugField('Слаг', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(models.Model):
    name = models.CharField('Тэг', max_length=50)
    slug = models.SlugField('Слаг', max_length=50)

    def __str__(self):
        return f'#{self.name}'

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    text = models.TextField('Комментарий', max_length=300)
    date_pub = models.DateTimeField('Дата публикации', auto_now_add=True)
    post = models.ForeignKey('Post',
                             on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name='Комментируемое сообщение')
    parent = models.ForeignKey('Comment',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name='children',
                               verbose_name='Родительский комментарий')
    likes = models.ManyToManyField(User, blank=True, related_name='comments', verbose_name='Лайки')

    def __str__(self):
        return f'{str(self.text)}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-date_pub',)


class Post(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True,
                               verbose_name='Автор')
    title = models.CharField('Заголовок', max_length=100, unique=True)
    slug = models.SlugField('Слаг', max_length=100, unique=True)
    image = models.ImageField('Изображение', upload_to='images/%Y/%m/%d/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts', verbose_name='Теги')
    preview_text = models.TextField('Превью', max_length=500)
    text = models.TextField('Текст', max_length=5000)
    date_pub = models.DateTimeField('Дата публикации', auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='posts', verbose_name='Лайки')
    is_published = models.BooleanField("Опубликовано", blank=True, default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'category_slug': self.category.slug, 'post_slug': self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-date_pub',)
