from django.db.models import Count
from django.db.models.query import Prefetch, Q
from .models import Post, Comment, Tag, Category


""" Бизнес-логика """


def get_post(**filter_kwargs):
    defer_list = ('author__date_joined', 'author__is_active',
                  'author__is_staff', 'author__is_superuser',
                  'author__password', 'author__username',
                  'author__email','author__last_login')
    return Post.objects.filter(
        **filter_kwargs
        ).select_related('author', 'category'
        ).prefetch_related(
                Prefetch(
                    'comments',
                    Comment.objects.filter(
                        parent__isnull = True
                        ).annotate(likes_count=Count('likes')
                        ).select_related('author'
                        ).prefetch_related(
                            Prefetch(
                                     'children',
                                     Comment.objects.annotate(
                                         likes_count=Count('likes')
                                         ).select_related('author'
                                         ).defer(*defer_list))
                        ).order_by('-date_pub'
                        ).defer(*defer_list)))


def _get_posts(posts):
    return posts.prefetch_related('tags'
                                  ).select_related('category', 'author'
                                  ).order_by('-date_pub'
                                  ).defer('text', 'is_published', 'author__avatar', 'author__date_joined',
                                           'author__is_active', 'author__is_staff', 'author__is_superuser',
                                           'author__password', 'author__username', 'author__email',
                                            'author__last_login'
                                  ).annotate(comments_count=Count('comments'))


def get_filtered_posts(**filter_kwargs):
    return _get_posts(Post.objects.filter(**filter_kwargs))


def get_searched_posts(search_text):
    return _get_posts(
                      Post.objects.filter(
                                          Q(is_published = True
                                          )&Q(title__icontains=search_text)|
                                          Q(preview_text__icontains=search_text)|
                                          Q(text__icontains=search_text)))


def get_taged_posts(tag):
    return _get_posts(tag.posts.filter(is_published = True))


def get_category(slug):
    return Category.objects.get(slug=slug)


def get_tag(slug):
    tag = Tag.objects.get(slug=slug)
    return tag


def handle_like(liked_object, user_id):
    if liked_object.likes.filter(pk = user_id):
        liked_object.likes.remove(user_id)
    else:
        liked_object.likes.add(user_id)










