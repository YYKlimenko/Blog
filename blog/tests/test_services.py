from django.test import TestCase
from blog import services
from blog.models import Post, Category
from user.models import User


class ServicesTestClass(TestCase):
    def setUpTestData(cls):
        User.objects.create
        Category.objects.create(name='test_cat', slug='testcat')
        Post.objects.create(author=0,
                            title='Тестовый пост',
                            slug='testpost',
                            category='0',
                            preview_text='Тестовый превью текст',
                            text='Основной тестовый текст',
                            is_published=True)


    def test_get_post(self):
        pass
