from django.test import TestCase
from blog import services
from blog.models import Post, Category, Tag


class ServicesTestClass(TestCase):
    category_name = 'test_cat'
    category_slug = 'testcatslug'
    post_title = 'Тестовый пост'
    post_slug = 'testpostslug'
    post_preview_text = 'Тестовый превью текст'
    post_text = 'Основной тестовый текст'

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name=cls.category_name, slug=cls.category_slug)
        cls.tag = Tag.objects.create(name='тестовый тег', slug='testtag')
        cls.post = Post.objects.create(title=cls.post_title,
                                       slug=cls.post_slug,
                                       category=cls.category,
                                       preview_text=cls.post_preview_text,
                                       text=cls.post_text,
                                       is_published=True)
        cls.post.tags.set([cls.tag])
        cls.post_queryset = Post.objects.filter(slug=cls.post_slug)

    def test_get_post(self):
        self.assertEqual(services.get_post(self.post_slug), self.post, 'Возвращает неверный пост')
        self.assertEqual(services.get_post('slug_then_not_exists'), None, 'Возвращает неверный пост')

    def test_get_filtered_posts(self):
        self.assertEqual(list(services.get_filtered_posts(slug=self.post_slug)),
                         list(self.post_queryset),
                         'Возвращает неверный Queryset')

    def test_get_searched_posts(self):
        self.assertEqual(list(services.get_searched_posts('Основной')),
                         list(self.post_queryset),
                         'Возвращает неверный Queryset')
        self.assertEqual(list(services.get_searched_posts('превью')),
                         list(self.post_queryset),
                         'Возвращает неверный Queryset')

    def test_get_tagged_posts(self):
        self.assertEqual(list(services.get_tagged_posts(self.tag)),
                         list(self.post_queryset),
                         'Возвращает неверный Queryset')
