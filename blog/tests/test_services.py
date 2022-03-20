from django.test import TestCase
from blog import services
from blog.models import Post, Category

class ServicesTestClass(TestCase):
    category_name = 'test_cat'
    category_slug ='testcatslug'
    post_title = 'Тестовый пост'
    post_slug = 'testpostslug'
    post_preview_text = 'Тестовый превью текст'
    post_text = 'Основной тестовый текст'

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name=cls.category_name, slug=cls.category_slug)
        Post.objects.create(title=cls.post_title,
                            slug=cls.post_slug,
                            category=cls.category,
                            preview_text=cls.post_preview_text,
                            text=cls.post_text,
                            is_published=True)

    def test_get_post(self):
        post = services.get_post(self.post_slug).get()
        self.assertEqual(post.slug, self.post_slug, 'Слаг неверный')
        self.assertEqual(post.category, self.category, 'Категория не верна')
        self.assertEqual(post.preview_text, self.post_preview_text, 'Превью текст неверен')
        self.assertEqual(post.text, self.post_text, 'Текст неправильный')





